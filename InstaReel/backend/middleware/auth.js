const jwt=require('jsonwebtoken');
const User=require('../model/userModel');

const auth=async(req, res, next)=>{
    const token = req.header('Authorization')?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).send({ error: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = await User.findById(decoded.id).select('-password'); // Exclude password from response
    if (!req.user) {
      throw new Error();
    }
    next();
  } catch (err) {
    res.status(401).send({ error: 'Unauthorized' });
  }
}
module.exports=auth;
