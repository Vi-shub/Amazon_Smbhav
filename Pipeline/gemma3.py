import google.generativeai as genai
import re
import json
import logging
from pymongo import MongoClient
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MongoDB Configuration
MONGO_URI = "mongodb+srv://rameshgudpawar:Ramesh@cluster0.a74wx6z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "test"
COLLECTION_NAME = "products"

# Configure the Gemini API
genai.configure(api_key="AIzaSyC0oKVxPwznpzXCjtezB0iAyOA6mqfm9bU")
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

def generate_product_json(context, scraped_data=None):
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
        "id": "number",
        "url": "string",
        "resUrl": "string",
        "price": "string with ₹",
        "value": "string number",
        "accValue": "number",
        "discount": "string with %",
        "mrp": "string with ₹",
        "name": "string",
        "points": ["array of feature strings"]
    }}

    Use this information to generate the product:
    {context}
    
    Ensure:
    - All prices include ₹ symbol
    - Discount includes % symbol
    - Points are detailed feature descriptions
    - URLs follow the pattern 'images/products/X.jpg' and '../images/products/Xres.jpg'
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

def main():
    # Example inputs
    scraped_content = """
    Lenovo ThinkBook 14 Intel Core i5 11th Gen
    Price: ₹61,990.00 MRP: ₹1,15,668.00 (46% OFF)
    • ThinkBook 14 Reliability tested on 12 MIL-STD-810H Methods
    • Processor: 11th Gen Intel Core i5-1135G7
    • 16GB RAM/512GB SSD
    • Windows 11 Home with MS Office 2021
    """
    
    ocr_content = """
    LENOVO THINKBOOK 14
    Intel Core i5 11th Gen
    16GB RAM
    512GB SSD
    Windows 11
    MRP: ₹1,15,668.00
    Our Price: ₹61,990.00
    """

    try:
        # Initialize MongoDB connection
        mongo_handler = MongoDBHandler()
        
        # Preprocess input data
        clean_scraped = preprocess_text(scraped_content)
        clean_ocr = preprocess_text(ocr_content)
        
        logging.info("Starting product information processing")
        
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
        
        product_data = generate_product_json(context, initial_data)
        print("\nGenerated Product Data:")
        print(json.dumps(product_data, indent=2))
        
        # Insert into MongoDB
        inserted_id = mongo_handler.insert_product(product_data)
        logging.info(f"Product successfully inserted with ID: {inserted_id}")
        
        # Close MongoDB connection
        mongo_handler.close_connection()
        
        return product_data
        
    except Exception as e:
        logging.error(f"Error processing product: {str(e)}")
        return None

if __name__ == "__main__":
    main()