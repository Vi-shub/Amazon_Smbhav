const  {model, Schema}=require('mongoose');
const bcrypt=require('bcrypt');
const jwt=require('jsonwebtoken');
const userSchema = new Schema({
    userName: {
		type: String,
		required: true,
	},
	email: {
		type: String,
		unique: true,
		required: true,
	},
	password: {
		type: String,
		required: true,
	},
	
});
userSchema.pre('save', async function(next){
	if(!this.isModified('password')) return next();
	this.password=await bcrypt.hash(this.password, 10);
	next();
});
userSchema.methods.comparePassword=async function(password){
	return await bcrypt.compare(password, this.password);
};
userSchema.methods.generateJWT=function(){
	return jwt.sign(
		{id:this._id, userName:this.userName, email:this.email},
		 process.env.JWT_SECRET,
		{expiresIn:'1d'});
};
module.exports=model("user", userSchema);