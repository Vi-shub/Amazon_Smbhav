const mongoose = require('mongoose');

const InteractionSchema = new mongoose.Schema({
  userName: String,
  videoId: String,
  interactionType: String,  // 'view' or 'like'
});

const Interaction = mongoose.model('Interaction', InteractionSchema);

module.exports=Interaction;