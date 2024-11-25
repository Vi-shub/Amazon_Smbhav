const express=require('express');
const {userSignUp, userLogin}=require('../controllers/userController');
const router=express.Router();
router.post('/login', userLogin );
//router.put('/post', updateUser);
router.post('/signup',userSignUp
);
module.exports=router;