from flask import Flask, request, jsonify
import pickle
import pandas as pd
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

# Load environment variables
load_dotenv()

# Load the trained NMF model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'nmf_model.pkl')

def load_model():
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

# MongoDB URI
MONGO_URI = os.getenv('MONGO_URI')

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.get_database('short-videos-app')  # Replace 'short-videos-app' with your database name

@app.route('/')
def home():
    return "Welcome to the Recommendation System API"

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        user_name = data.get('userName')

        # Fetch interaction data from MongoDB
        collection = db.get_collection('interactions')  # Replace 'interactions' with your collection name
        interaction_data = pd.DataFrame(list(collection.find()))

        if interaction_data.empty:
            return jsonify({'error': f'No interaction data found for user {user_name}'}), 404

        # Transform interaction types into numerical values
        interaction_mapping = {'view': 1, 'like': 2}
        interaction_data['interactionType'] = interaction_data['interactionType'].map(interaction_mapping)

        # Create the interaction matrix
        interaction_matrix = interaction_data.pivot_table(index='userName', columns='videoId', values='interactionType', fill_value=0)

        # Ensure the user has interaction data
        if user_name not in interaction_matrix.index:
            return jsonify({'error': f'No interaction data found for user {user_name}'}), 404

        # Fill missing columns to match the training set
        all_video_ids = interaction_matrix.columns
        user_vector = interaction_matrix.loc[user_name]
        user_vector = user_vector.reindex(all_video_ids, fill_value=0).values.reshape(1, -1)

        # Get recommendations for the user
        user_prediction = model.inverse_transform(model.transform(user_vector))
        user_recommendations = pd.Series(user_prediction.flatten(), index=all_video_ids)

        # Return up to 25 recommendations
        top_recommendations = user_recommendations.sort_values(ascending=False).head(25).index.tolist()
        return jsonify({'recommendations': top_recommendations})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to port 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)




