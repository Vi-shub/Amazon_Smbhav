const mongoose = require('mongoose');
const User = require('../model/userModel');
const bcrypt = require('bcrypt');

const userSignUp = async (req, res) => {
	try {
		const { email, userName, password } = req.body;

		// Check if email or username already exists
		const existingUser = await User.findOne({ $or: [{ email }, { userName }] });

		if (existingUser) {
			if (existingUser.email === email) {
				return res.send({ message: "Email id already registered.", alert: false });
			}
			if (existingUser.userName === userName) {
				return res.send({ message: "Username already exists, try another", alert: false });
			}
		}

		// Create new user
		const user = new User({ userName, email, password });
		await user.save();

		// Return success message
		res.status(201).send({ message: "Successfully Signed Up", alert: true });
	} catch (error) {
		res.status(400).send(error);
	}
};

const userLogin = async (req, res) => { 
	try {
		const { email, password } = req.body;
		const user = await User.findOne({ email });

		if (user) {
			// Compare the provided password with the stored hashed password
			const isPasswordValid = await bcrypt.compare(password, user.password);

			if (isPasswordValid) {
				const userData = {
					_id: user._id,
					userName: user.userName,
					email: user.email,
					token: user.generateJWT()
				};
                   console.log(userData.token);
				res.send({
					message: "Successfully Logged In",
					alert: true,
					data: userData,
				});
			} else {
				res.send({
					message: "Invalid email or password",
					alert: false,
				});
			}
		} else {
			res.send({
				message: "Email is not available, please sign up first",
				alert: false,
			});
		}
	} catch (error) {
		res.send({ message: error.message });
	}
};

module.exports = {
	userSignUp,
	userLogin,
};