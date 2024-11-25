###SCRAPE
###########################################################################################################################################################################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
import pytesseract
from PIL import Image
import google.generativeai as genai
import re
import json
import logging
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Set up Selenium WebDriver (Chrome)
driver = webdriver.Chrome()

# Open the Insta Clone login page
url = "https://instaclonexyz.vercel.app/login"
driver.get(url)
time.sleep(2)  # Allow the page to load

# Locate the username and password fields
username_field = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Username or email  address']")
password_field = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")

# Input test credentials
username = "shubu"
password = "shubu"
username_field.send_keys(username)
password_field.send_keys(password)

# Locate and click the login button
login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
login_button.click()

# Wait for redirection after login
time.sleep(5)

# Scrape data after login (e.g., posts, user profile, etc.)
# Example: Scrape all posts
posts = driver.find_elements(By.CSS_SELECTOR, ".card")  # Replace 'post-class' with the actual post class
# Create directories for storing text files and images
os.makedirs("texts", exist_ok=True)
os.makedirs("images", exist_ok=True)
for i, post in enumerate(posts, start=1):
    try:
        # Extract post details
        username = post.find_element(By.CSS_SELECTOR, ".user-details .left-details .username").text
        image_url = post.find_element(By.CSS_SELECTOR, ".post img").get_attribute("src")
        caption = post.find_element(By.CSS_SELECTOR, ".caption p").text
        likes = post.find_element(By.CSS_SELECTOR, "div.likes-count p").text

        # Save text details to a file
        text_file_path = os.path.join("texts", f"post{i}.txt")
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(f"Username: {username}\n")
            text_file.write(f"Image URL: {image_url}\n")
            text_file.write(f"Caption: {caption}\n")
            text_file.write(f"Likes: {likes}\n")

        print(f"Details saved in {text_file_path}")

        # Download and save the image
        image_file_path = os.path.join("images", f"img{i}.jpg")
        response = requests.get(image_url)
        with open(image_file_path, "wb") as image_file:
            image_file.write(response.content)

        print(f"Image saved as {image_file_path}")

    except Exception as e:
        print(f"An error occurred for post {i}: {e}")

# Close the browser
driver.quit()

##OCR
####################################################################################################################################################################
# Path to Tesseract executable (adjust this path for your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Paths
image_folder = './images'  # Folder where your images are stored
output_folder = './extracted_texts'

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each image
for image_file in os.listdir(image_folder):
    if image_file.lower().endswith(('png', 'jpg', 'jpeg')):
        image_path = os.path.join(image_folder, image_file)
        print(f"Processing: {image_file}")

        # Open image and perform OCR
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        # Save extracted text to a file
        output_file = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Text extracted to: {output_file}")

##GEMMA JSON GENERATION
#############################################################################################################################################################

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Configure the Gemini API
genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


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
            # Convert string values to appropriate types
            product_data['id'] = int(product_data['id'])
            product_data['accValue'] = int(re.sub(r'[^\d]', '', product_data['value']))
        
            # Ensure `accValue` matches MongoDB schema (convert to string if necessary)
            product_data['accValue'] = str(product_data['accValue'])
        
            # Ensure points is a list
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

def preprocess_text(text):
    """
    Cleans and preprocesses the input text.
    """
    if not text:
        return ""
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove emojis and special characters but keep currency symbols and percentages
    text = re.sub(r'[^\w\s.,₹%+-]', '', text, flags=re.UNICODE)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_price_info(text):
    """
    Extracts price related information from text.
    Returns a dict with price, mrp, and discount if found.
    """
    price_info = {
        'price': None,
        'mrp': None,
        'discount': None
    }
    
    # Look for price patterns (₹XX,XXX.XX)
    price_pattern = r'₹[\d,]+\.?\d*'
    prices = re.findall(price_pattern, text)
    
    if prices:
        price_info['price'] = prices[0]
        if len(prices) > 1:
            price_info['mrp'] = prices[1]
    
    # Look for discount patterns (-XX%)
    discount_pattern = r'-\d+%'
    discount = re.search(discount_pattern, text)
    if discount:
        price_info['discount'] = discount.group()
    
    return price_info

def clarify_context(scraped_content, ocr_content):
    """
    Combines scraped content and OCR content to generate a clarified context.
    Structures the information according to the product schema.
    """
    prompt = f"""
    Generate a structured product listing from this information.
    Include accurate price, specifications, and features.

    Scraped Content: {scraped_content}
    OCR Content: {ocr_content}

    Format the response with:
    1. Product name
    2. Price information (including MRP and discount if available)
    3. Key features and specifications (as bullet points)
    4. Image URLs if mentioned
    """
    
    try:
        response = model.generate_content(prompt)
        logging.info("Successfully generated context")
        return response.text.strip()
    except Exception as e:
        logging.error(f"Error in context generation: {str(e)}")
        raise RuntimeError(f"Error generating context: {e}")

def generate_product_json(context, scraped_data=None, id_temp=0, image_url=None):
    """
    Generates a structured product JSON matching the required schema.
    Incorporates both generated context and any available scraped data.
    """
    # Combine context with scraped data if available
    if scraped_data:
        context = f"{context}\nAdditional Data: {json.dumps(scraped_data)}"
    
    prompt = f"""
    Generate a valid JSON product listing with this exact structure:
    {{
        "id": {id_temp},
        "url": "{image_url}",
        "resUrl": "same as url field",
        "price": "string with ₹",
        "value": "string number",
        "accValue": "number",
        "discount": "string with %",
        "mrp": "string with ₹",
        "name": "string",
        "points": ["array of feature strings"],
        "likes":"string"
    }}

    Use this information to generate the product:
    {context}
    
    Ensure:
    - Ensure id for each result is unique by incrementing it in every prompt
    - All prices include ₹ symbol
    - Discount includes % symbol
    - Points are detailed feature descriptions
    - Ensure that the valueof url and resUrl are same 
    """
    
    try:
        response = model.generate_content(prompt)
        generated_text = response.text.strip()
        
        # Extract JSON object
        json_match = re.search(r'\{[\s\S]*\}', generated_text)
        if not json_match:
            raise ValueError("No JSON object found in response")
            
        product_data = json.loads(json_match.group(0))
        
        # Process numerical values
        product_data['id'] = int(product_data['id'])
        product_data['accValue'] = int(re.sub(r'[^\d]', '', product_data['value']))
        product_data['url']=image_url.group(0)
        product_data['resUrl']=image_url.group(0)
        
        # Ensure points is a list
        if not isinstance(product_data['points'], list):
            product_data['points'] = [product_data['points']]
        
        logging.info("Successfully generated and validated product JSON")
        return product_data
        
    except Exception as e:
        logging.error(f"Error in JSON generation: {str(e)}")
        raise RuntimeError(f"Error generating JSON: {e}")

def extract_features_from_text(text):
    """
    Extracts features and specifications from text content.
    Returns a list of feature points.
    """
    # Split text into sentences
    sentences = re.split(r'[.•\n]+', text)
    
    # Filter and clean feature points
    features = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 10 and not re.match(r'^(price|₹|rs\.?|mrp)', sentence.lower()):
            features.append(sentence)
    
    return features

# Ensure MongoDBHandler, preprocess_text, clarify_context, extract_price_info,
# extract_features_from_text, and generate_product_json are defined elsewhere

# Define directories
extracted_text_folder = "extracted_texts"
texts_folder = "texts"
id_temp=0

try:
    # Initialize MongoDB connection
    mongo_handler = MongoDBHandler()

    # Process each pair of files
    for filename in os.listdir(texts_folder):
        id_temp+=1
        if filename.endswith(".txt"):
            # Determine corresponding files in both folders
            ocr_file_path = os.path.join(extracted_text_folder, filename.replace("post", "img"))
            scraped_file_path = os.path.join(texts_folder, filename)

                # Ensure both files exist
            if not os.path.exists(ocr_file_path):
                logging.warning(f"Missing OCR file: {ocr_file_path}")
                continue

            # Read content from both files
            with open(ocr_file_path, "r", encoding="utf-8") as ocr_file:
                ocr_content = ocr_file.read()

            with open(scraped_file_path, "r", encoding="utf-8") as scraped_file:
                scraped_content = scraped_file.read()

            # Regex to find the image URL
            image_url_regex = r"https://firebasestorage.googleapis.com[^\s]+"

            # Find the image URL using the regex
            image_url = re.search(image_url_regex, scraped_content)
            # Preprocess input data
            clean_scraped = preprocess_text(scraped_content)
            clean_ocr = preprocess_text(ocr_content)

            logging.info("Starting product information processing for %s", filename)

            # Generate context from both sources
            context = clarify_context(clean_scraped, clean_ocr)
            logging.info("\nClarified Context:\n%s", context)

            # Extract initial price information and features
            price_info = extract_price_info(clean_scraped + " " + clean_ocr)
            features = extract_features_from_text(clean_scraped + " " + clean_ocr)

            # Generate complete product JSON
            initial_data = {
                "price_info": price_info,
                "features": features
            }
            print("IMAGE URLRLRLRLRLLR: "+ str(image_url))

            product_data = generate_product_json(context, initial_data, id_temp, image_url)
            print(f"\nGenerated Product Data for {filename}:")
            print(json.dumps(product_data, indent=2))

            # Insert into MongoDB
            inserted_id = mongo_handler.insert_product(product_data)
            logging.info(f"Product successfully inserted with ID: {inserted_id}")

    # Close MongoDB connection
    mongo_handler.close_connection()

except Exception as e:
    logging.error(f"Error processing product: {str(e)}")




