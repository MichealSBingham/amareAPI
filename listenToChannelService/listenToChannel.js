const StreamChat = require('stream-chat').StreamChat;
const io = require('socket.io-client');

// Set up Stream Chat client
const apiKey = '92jyyxebed2m';
const apiSecret = 'zh8xege9catts7pfdageqsfc6vhgwttqedrsa9kvfyxjmucqst4wn97ycgn765wc';
const chatClient = new StreamChat(apiKey, apiSecret, { allowServerSideConnect: true });

// Function to create a channel, watch it, and listen for new messages
async function listenToChannel(user1id, user2id) {
  // Generate the channel ID
  const userList = [user1id, user2id];

  const adminUserId = 'dasha';
  const adminToken = await chatClient.createToken(adminUserId);
  await chatClient.upsertUser({
    id: adminUserId,
    role: 'admin', // Specify the admin role during user creation or update
  });
  
  await chatClient.connectUser({ id: adminUserId }, adminToken);
  

  // Set up the channel
  const channel = chatClient.channel('messaging', { members: userList });
  await channel.create();
  const state = await channel.watch();

  // Listen for new messages
  channel.on('message.new', (event) => {
   

    const userSendingMessage = event.user.id;
    const messageText = event.message.text;
    //console.log('Received message event:', event);

    // Process the message (add your processing logic here)
    console.log(`Received message from user ${userSendingMessage}: ${messageText}`);
  });

  console.log(`listening to channel id ${channel.id} `)

}

// Example: Listen for messages for users 'user1' and 'user2'
listenToChannel('2V2mJdDLt7Q5fVUl8O8PtQv3tQN2', 'ZH17wkDgkIVFqQ2F9wtwcRPi5oo1');

setInterval(() => {}, 1000);


// Example: Listen for messages for users 'user1' and 'user2'
//listenToChannel("!members-bdRFBY75-BL-SIErP2Ekytk5XT2EPpxDkEJgTCr0-Wk");
