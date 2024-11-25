const express=require('express');
const {getInteractionData, postInteractionData}=require("../controllers/interactionController");
const router=express.Router();

router.get("/getInteractionData", getInteractionData);
router.post("/postInteractionData", postInteractionData);

module.exports=router;
