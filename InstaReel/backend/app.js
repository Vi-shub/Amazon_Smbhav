const express=require('express');
require('dotenv').config();
const cors=require('cors');
const {urlencoded}=require('body-parser');

const connectToDb=require("./db");
const videoRoute=require('./routes/videosRoute');
const userRoute=require("./routes/userRoute");
const interactionRoute=require("./routes/interactionRoute");
const cloudinary = require('cloudinary').v2;


cloudinary.config({
  cloud_name: 'doin2x6n5',
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET
});

const app=express();
connectToDb();


//middleware
app.use(cors());
app.use(express.json());
app.use(urlencoded({ extended: true }));

app.use('/shortVideos',videoRoute);
app.use('/user',userRoute);
app.use('/interaction',interactionRoute);

module.exports=app;