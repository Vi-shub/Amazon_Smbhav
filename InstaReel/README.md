# InstaReel

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Getting Started](#getting-started)
5. [Installation](#installation)
6. [Usage](#usage)
7. [API Endpoints](#api-endpoints)
8. [Contributing](#contributing)
9. [Contact](#contact)

## Introduction

ALPSHOT is a web application that allows users to create, share, and view short video clips, similar to popular social media platforms like TikTok and Instagram Reels. This project is built using the MERN stack (MongoDB, Express, React, Node.js).

## Features

- User authentication and authorization
- Upload and playback of short video clips
- Like, comment, and share functionality
- User profiles with video collections
- Responsive design for mobile and desktop

## Technologies Used

- **Frontend**: React, Tailwind CSS
- **Backend**: Node.js, Express
- **Database**: MongoDB
- **Cloud Storage**: Cloudinary (for storing video files)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Node.js
- MongoDB
- cloudinary account (or another cloud storage service)

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/Rajukumarsaw/shorts_videos_apps.git
   cd shorts_videos_apps
   ```
2. Install backend dependencies
   ```sh
   cd backend
   npm install

   ```
3. Install frontend dependencies
   ```sh
   cd ../frontend
   npm install

   ```

## Configuration

### Backend:

- Create a `.env` file in the backend directory and add the following variables:

  ```
  MONGO_URI=your_mongodb_uri
  CLOUDINARY_API_KEY=your_cloudinary_api_key
  CLOUDINARY_API_SECRET=your_cloudinary_api_secret_key
  PORT=8000
  ```

### Frontend:

- Create a `.env` file in the frontend directory and add the following variable:
  ```
  VITE_SERVER_URL=http://localhost:8000
  ```

## Running the Application

### Start the backend server:

    cd backend
      npm run dev

### Start the frontend server:

- open new terminal

  ```sh
   cd frontend
   npm run dev
  ```

 The application should now be running on [http://localhost:5173](http://localhost:5173).

## Usage

- Register or log in to your account.
- Upload videos, view users' videos, like, comment, and share.
- Customize your profile.

## API Endpoints

### Here are some key API endpoints available in the application:

#### Auth Routes

- POST `/user/login` - Login a new user
- POST `/user/signup` - Register a user

#### Video Routes

- GET `/shortVideos/getAllVideos` - Get all videos
- POST `/shortVideos/upload` - Upload a new video
- POST `/shortVideos/getUserVideos` - Get a specific user videos
- PUT `/shortVideos/editStats/:id` - update likes and comment of the video

## Contributing

- Contributions are welcome! Please follow these steps:
  1. Fork the repository
  2. Create a new branch (`git checkout -b feature/your-feature`)
  3. Commit your changes (`git commit -m 'Add some feature'`)
  4. Push to the branch (`git push origin feature/your-feature`)
  5. Open a pull request
