userInput.disabled = true;
loading_screen.style.display = 'flex';
var messagesCheck, numberCheck, x;
checkFilePaths();
function checkFilePaths(){
    fetch('http://127.0.0.1:5000/check', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        x = data;
        if (!data.messages){
            createFile('messages');
        }
        else{
            messagesCheck = true;
        }
        if (!data.audio){
            createFile('audio');
        }
        if (!data.number){
            createFile('number')
        }
        else{
            numberCheck = true;
        }
    })
    .then(() => {
        if (messagesCheck && numberCheck){
            getValue();
        }
    })
    .then(() => {

    })
    .catch((error) => {
        showErrorMessage('Error 504. Please try again later.');
    });
}
function createFile(type){
    fetch('http://127.0.0.1:5000/createFiles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'file': type })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.bool){
            showErrorMessage('Error 504. Please try again later.');
        }
        else{
            if (type === 'messages'){
                messagesCheck = true;
            }
            else if (type === 'number'){
                numberCheck = true;
            }
            if (messagesCheck && numberCheck){
                getValue();
            }
        }
    })
    .catch((error) => {
        showErrorMessage('Error 504. Please try again later.');
    });
}
function getValue(){
    fetch('http://127.0.0.1:5000/read', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.json==false){
            showErrorMessage('Error 504. Please try again later.');
        }
        else {
            chatHistory = JSON.parse(data.json);
            if (chatHistory.empty === true){
                chatHistory = [];
            }
        }
    })
    .then(() => {
        fetch('http://127.0.0.1:5000/rean', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.json==false){
                showErrorMessage('Error 504. Please try again later.');
            }
            else{
                numberOfMessages = JSON.parse(data.json).number_of_messages;
            }
        })
        .catch((error) => {
            showErrorMessage('Error 504. Please try again later.');
        });
    })
    .then(() => {
        loadOldMessages();
    })
    .catch((error) => {
        showErrorMessage('Error 504. Please try again later.');
    });
}

function checkEmpty(){
    if (chatHistory.length === 0){
        return true;
    }
    else{
        return false;
    }
}
function loadOldMessages(){
    if(checkEmpty()){
        const intro = `<h3> Welcome to KaabilBot™! </h3>
               <strong>KaabilBot</strong> is here to assist you with any query or task you have. True to its name, this bot is designed to handle a wide range of requests efficiently.`;
        addIntroMessage(intro);
        checkIncomplete();
        loading_screen.style.display = 'none';
        userInput.disabled = false;
    }
    else if(chatHistory.length === 1){
        const message = chatHistory[0].special;
        if (message){
            loadMsgs();
            return;
        }   
    }
    else{
        loadMsgs();
    }
}
function loadMsgs(){
    chatHistory.forEach(message => {
        if (message.id === undefined || message.id === null || message.bot === undefined || message.bot === null || message.content === undefined || message.content === null || message.user === undefined || message.user === null || message.time === undefined || message.time === null)   {
            return;
        }
        if (message.bot === true){
            addOldMessages(message.content);
        }
        else if (message.bot === false){
            addOldMessages(message.content, true);
        }
    });
    checkIncomplete();
    loading_screen.style.display = 'none';
    userInput.disabled = false;
}

function checkIncomplete(){
    const messages = document.getElementsByClassName('message');
    const lastMessage = messages[messages.length - 1];
    if (lastMessage.classList.contains('user-message')) {
        get_response(lastMessage.textContent);
    } 
}
