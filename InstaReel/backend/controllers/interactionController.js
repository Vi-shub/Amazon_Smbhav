const Interaction=require("../model/interactionModel");

const getInteractionData = async (req, res) => {
    try {
      const { userName } = req.query;
  
      // Validate that userName is provided
      if (!userName) {
        return res.status(400).json({ error: "userName query parameter is required" });
      }
  
      // Find interaction data for the specified userName
      const interactionData = await Interaction.find({ userName });
  
      // Return the interaction data as JSON
      res.json(interactionData);
    } catch (error) {
      console.error("Error fetching interaction data:", error);
      res.status(500).send("Server error");
    }
  };
  
  
  

const postInteractionData=async(req, res)=>{

      try{
           await Interaction.create(req.body);
           res.send({ message: "user interaction data collected" });  
      } 
      catch(error){
         res.status(500).send({ message: error.message });
      }
};

module.exports={getInteractionData, postInteractionData};


