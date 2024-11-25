# Amazon Clone with Data Pipelines

A fully functional Amazon clone with automated data extraction pipelines for products and reels.
## Deployed Link : https://amazon-clone-swart-six.vercel.app 
## 🌟 Features

- Full e-commerce functionality with user authentication
- Product browsing and search
- Shopping cart management
- Order history
- Payment integration with Razorpay
- Automated data pipelines for content extraction
- Real-time product updates from pipelines to MongoDB

## 🛠️ Technology Stack

- **Frontend**: React.js
- **Backend**: Express.js, Node.js
- **Database**: MongoDB
- **HTTP Client**: Axios
- **Data Extraction**: Python (pipelines)
- **Payment Gateway**: Razorpay

## 📋 Prerequisites

- Node.js (v14 or higher)
- Python 3.8+
- MongoDB
- pip (Python package manager)
- npm (Node package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Vi-shub/Amazon_Smbhav/
cd amazon-clone
```

### 2. Backend Setup

```bash
# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Configure environment variables
# Edit .env file with your credentials:
MONGO_URI=yoyour_mongodb_uri
SECRET_KEY=your_secret_key
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_SECRET=your_razorpay_secret
```

### 3. Frontend Setup

```bash
# Navigate to client directory
cd client

# Install dependencies
npm install

# Create .env file for frontend
cp .env.example .env

# Configure frontend environment variables
REACT_APP_API_URL=http://localhost:8000
```

### 4. Pipeline Setup

```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install pipeline dependencies
pip install -r requirements.txt

# Create .env file for pipelines
cp pipeline.env.example pipeline.env
```

Configure the pipeline.env file with:
```
MONGODB_URI=your_mongodb_uri
DB_NAME=your_db_name
COLLECTION_NAME=your_collection_name
GENAI_API_KEY=your_api_key
```

## 🏃‍♂️ Running the Application

### 1. Start MongoDB
Ensure your MongoDB instance is running

### 2. Start Backend Server
```bash
npm run dev
```

### 3. Start Frontend
```bash
cd client
npm start
```

### 4. Run Data Pipelines

For product data extraction:
```bash
python pipeline.py
```

For reels data extraction:
```bash
python pipeline3.py
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details
