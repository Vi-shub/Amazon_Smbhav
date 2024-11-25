import google.generativeai as genai
import re
import json
import logging
from pymongo import MongoClient
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os
import cv2
import pytesseract
import speech_recognition as sr
from pydub import AudioSegment
import cloudinary
import cloudinary.uploader
import cloudinary.api
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configurations
USERNAME = "adv@gmail.com"
PASSWORD = "adv"
MONGO_URI = "mongodb+srv://rameshgudpawar:Ramesh@cluster0.a74wx6z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "test"
COLLECTION_NAME = "products"

# Configure APIs
genai.configure(api_key="AIzaSyC0oKVxPwznpzXCjtezB0iAyOA6mqfm9bU")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

cloudinary.config(
    cloud_name="dtwt3cwfo",
    api_key="471234751737446",
    api_secret="q-8F-XSvVNRISodMtolGxgCz0AM"
)

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class MongoDBHandler:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[DB_NAME]
            self.collection = self.db[COLLECTION_NAME]
            logging.info("Successfully connected to MongoDB")
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {str(e)}")
            raise

    def insert_product(self, product_data):
        try:
            # Ensure required fields exist with default values if missing
            default_product = {
                "id": 0,
                "url": "",
                "resUrl": "",
                "price": "₹0",
                "value": "0",
                "accValue": "0",
                "discount": "0%",
                "mrp": "₹0",
                "name": "Unknown Product",
                "points": [],
                "likes": "0"
            }
            product_data = {**default_product, **product_data}
            
            # Ensure proper data types
            product_data['id'] = int(product_data['id'])
            if isinstance(product_data['accValue'], str):
                product_data['accValue'] = re.sub(r'[^\d]', '', product_data['accValue'])
            
            if isinstance(product_data['points'], str):
                product_data['points'] = [product_data['points']]
            
            result = self.collection.insert_one(product_data)
            logging.info(f"Successfully inserted product with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logging.error(f"Error inserting product: {str(e)}")
            raise

    def close_connection(self):
        self.client.close()
        logging.info("MongoDB connection closed")

def extract_audio_from_video(video_path):
    """
    Extracts and transcribes audio from video file using pydub directly
    """
    try:
        # Convert video to audio using pydub
        audio_path = video_path.replace('.mp4', '.wav')
        video = AudioSegment.from_file(video_path, format="mp4")
        video.export(audio_path, format="wav")

        # Transcribe audio
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data)

        # Clean up audio file
        os.remove(audio_path)
        return transcription

    except Exception as e:
        logging.error(f"Error in audio transcription: {str(e)}")
        return "No audio transcription available"

def generate_default_product_json(id_temp=0, image_url=None):
    """Generate a default product JSON when context generation fails"""
    return {
        "id": id_temp,
        "url": image_url or "",
        "resUrl": image_url or "",
        "price": "₹0",
        "value": "0",
        "accValue": "0",
        "discount": "0%",
        "mrp": "₹0",
        "name": "Product Information Unavailable",
        "points": ["Product details could not be extracted"],
        "likes": "0"
    }

def scrape_and_process_videos():
    driver = None
    mongo_handler = None
    temp_dir = "temp_files"
    
    try:
        # Create temporary directory for files
        os.makedirs(temp_dir, exist_ok=True)
        
        driver = webdriver.Chrome()
        mongo_handler = MongoDBHandler()
        
        # Login process
        driver.get("https://shorts-videos-apps.vercel.app/login")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        # Navigate to profile
        driver.get("https://shorts-videos-apps.vercel.app/profile")
        video_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".bg-gray-800.p-4.rounded-lg"))
        )

        id_counter = 0

        for idx, video_element in enumerate(video_elements, start=1):
            video_path = os.path.join(temp_dir, f"video_{idx}.mp4")
            
            try:
                # Extract video and description
                video_url = video_element.find_element(By.TAG_NAME, "video").get_attribute("src")
                description = video_element.find_element(By.TAG_NAME, "p").text

                # Download video
                video_response = requests.get(video_url)
                with open(video_path, "wb") as video_file:
                    video_file.write(video_response.content)

                # Extract frame and upload to Cloudinary
                cap = cv2.VideoCapture(video_path)
                ret, frame = cap.read()
                image_url = None
                
                if ret:
                    frame_path = os.path.join(temp_dir, f"frame_{idx}.jpg")
                    cv2.imwrite(frame_path, frame)
                    try:
                        cloudinary_response = cloudinary.uploader.upload(frame_path)
                        image_url = cloudinary_response['url']
                    except Exception as e:
                        logging.error(f"Error uploading to Cloudinary: {str(e)}")
                    finally:
                        os.remove(frame_path)
                cap.release()

                # Extract text using OCR
                ocr_text = pytesseract.image_to_string(frame) if ret else ""

                # Transcribe audio
                audio_transcription = extract_audio_from_video(video_path)

                # Generate product data
                try:
                    combined_context = f"""
                    Description: {description}
                    OCR Text: {ocr_text}
                    Audio: {audio_transcription}
                    """
                    
                    product_data = generate_product_json(combined_context, None, id_counter, image_url)
                    if not product_data:
                        raise ValueError("Failed to generate product data")
                except Exception as e:
                    logging.error(f"Error generating product data: {str(e)}")
                    product_data = generate_default_product_json(id_counter, image_url)

                # Insert into MongoDB
                mongo_handler.insert_product(product_data)
                id_counter += 1

                logging.info(f"Successfully processed video {idx}")

            except Exception as e:
                logging.error(f"Error processing video {idx}: {str(e)}")
                continue
            finally:
                # Clean up video file
                if os.path.exists(video_path):
                    os.remove(video_path)

    except Exception as e:
        logging.error(f"Error in scraping process: {str(e)}")
    finally:
        # Clean up
        if driver:
            driver.quit()
        if mongo_handler:
            mongo_handler.close_connection()
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def generate_product_json(context, scraped_data=None, id_temp=0, image_url=None):
    """
    Generate product JSON with better error handling and validation
    """
    try:
        prompt = f"""
        Generate a product listing JSON with this structure:
        {{
            "id": {id_temp},
            "url": "{image_url or ''}",
            "resUrl": "{image_url or ''}",
            "price": "string with ₹",
            "value": "string number",
            "accValue": "number",
            "discount": "string with %",
            "mrp": "string with ₹",
            "name": "string",
            "points": ["array of feature strings"],
            "likes": "string"
        }}

        Context information:
        {context}
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extract JSON from response (in case there's additional text)
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found in response")
            
        product_data = json.loads(json_match.group())
        
        # Validate and clean data
        if not isinstance(product_data.get('points', []), list):
            product_data['points'] = [str(product_data.get('points', ''))]
            
        return product_data
        
    except Exception as e:
        logging.error(f"Error in JSON generation: {str(e)}")
        return generate_default_product_json(id_temp, image_url)

if __name__ == "__main__":
    scrape_and_process_videos()