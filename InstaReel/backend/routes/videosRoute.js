const express = require('express');
const router = express.Router();
const multer = require('multer');
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });
const auth = require('../middleware/auth');
const { editStats, postShortVideos, getAllshortVideos, getUserVideos } = require('../controllers/shortVideosController');

router.get('/getAllVideos', getAllshortVideos);
router.post('/upload', upload.single('video'), postShortVideos);
router.put('/editStats/:id', editStats);
router.post('/getUserVideos', auth, getUserVideos);

module.exports = router;
