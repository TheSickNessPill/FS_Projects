let createDialogButton, deleteDialogButton, createChatButton, editChatButton,
deleteChatButton, sendTextButton;

createDialogButton = document.getElementsByClassName("create-dialog-button")[0];
deleteDialogButton = document.getElementsByClassName("delete-dialog-button")[0];
createChatButton = document.getElementsByClassName("create-chat-button")[0];
editChatButton = document.getElementsByClassName("edit-chat-button")[0];
deleteChatButton = document.getElementsByClassName("delete-chat-button")[0];
sendTextButton = document.getElementsByClassName("send_text_button")[0];


createDialogButton.addEventListener(
    "click",
    async function(){
        let another_username = prompt("Enter name of user to create dialog: ").trim();

        let createDialogResult = async () => {
            return fetch(`/messenger/createdialog/?another_username=${another_username}`)
                .then((response) => { return response.json(); })
                .then((json) => { return json; })
                .catch(() => { console.log("error"); })
        };

        let response = await createDialogResult();
        console.log("createdialog", response);

        if (response.status === "ok"){
            let dialogsBody = document.getElementsByClassName("dialogs-aside-body")[0];
            dialogsBody.innerHTML +=`
                <div class="dialogs-aside-dialog-name">
                    <a style="font-size:20px;" href="?dialog_name=${response.dialogname}"> ${response.dialogname} </a>
                </div>
            `;
            alert(`Created dialog ${response.dialogname}`)
        }
        else if (response.status === "error"){
            alert(response.errortext);
        }
    }
);


deleteDialogButton.addEventListener(
    "click",
    async function(){
        let another_username = prompt("Enter username to delete dialog with this user:")

        let deleteDialogResult = async () => {
            return fetch(`deletedialog/?username=${another_username}`)
                .then((response) => { return response.json(); })
                .then((json) => { return json; })
                .catch(() => { console.log("error"); })
        }

        let response = await deleteDialogResult();
        console.log("deleteDialog", response)
        if (response.status === "ok"){
            console.log("deleteDialog", response.dialogname);
            let dialogsBody = document.getElementsByClassName("dialogs-aside-body")[0];
            for (let elem of dialogsBody.children){
                if (elem.getElementsByTagName("a")[0].text.trim() === response.dialogname){
                    dialogsBody.removeChild(elem);
                    alert(`Dialog deleted ${response.dialogname}`)
                    break;
                }
            }
        }
        else if (response.status === "error"){
            alert(response.errortext);
        }
    }
)


createChatButton.addEventListener(
    "click",
    async function(){
        let chatname = prompt("Enter chatname to create chat: ").trim();
        let usernames = prompt("Enter space spareted usernamnes to invite they to chat").trim();

        let createDialogResult = async () => {
            return fetch(`createchat/?chatname=${chatname}&usernames=${usernames}`)
                .then((response) => { return response.json(); })
                .then((json) => { return json; })
                .catch(() => { console.log("error"); })
        };

        let response = await createDialogResult();
        console.log("createchat", response);

        if (response["status"] === "ok"){
            let chatsBody = document.getElementsByClassName("chat-aside-body")[0];
            chatsBody.innerHTML +=`
                <div class="chat-aside-chat-name">
                    <a style="font-size:20px;" href="?chat_name=${response.chatname}"> ${response.chatname} </a>
                </div>
            `;
        }
        else if (response.status === "error"){
            alert(response.errortext);
        }
    }
)


editChatButton.addEventListener(
    "click",
    async function(){
        let chatName = prompt("Enter chat name to set new new chat name:").trim();
        let newChatName = prompt("Enter new chat name for this chat:").trim();

        let createDialogResult = async () => {
            return fetch(`editchat/?chatname=${chatName}&newchatname=${newChatName}`)
                .then((response) => { return response.json(); })
                .then((json) => { return json; })
                .catch(() => { console.log("error"); })
        };

        let response = await createDialogResult();
        console.log("editchat", response);

        if (response["status"] === "ok"){
            let chatsBody = document.getElementsByClassName("chat-aside-body")[0];
            for (let elem of chatsBody.children){
                console.log(elem)
                let tag_a = elem.getElementsByTagName("a")[0];
                console.log(tag_a)
                if (tag_a.text.trim() === chatName){
                    console.log(tag_a.text.trim())
                    tag_a.text = newChatName;
                    break;
                }
            }
        }
        else if (response.status === "error"){
            alert(response.errortext);
        }
    }
)

deleteChatButton.addEventListener(
    "click",
    async function(){
        let chatName = prompt("Enter chat name to delete:").trim();

        let createDialogResult = async () => {
            return fetch(`deletechat/?chatname=${chatName}`)
                .then((response) => { return response.json(); })
                .then((json) => { return json; })
                .catch(() => { console.log("error"); })
        };

        let response = await createDialogResult();
        console.log("delete", response);

        if (response["status"] === "ok"){
            let chatsBody = document.getElementsByClassName("chat-aside-body")[0];
            for (let elem of chatsBody.children){
                tag_a = elem.getElementsByTagName("a")[0]
                if (tag_a.text.trim() === response.chatname){
                    chatsBody.removeChild(elem);
                    alert(`Chat deleted ${response.chatname}`)
                    break;
                }
            }
        }
        else if (response.status === "error"){
            alert(response.errortext);
        }
    }
)


sendTextButton.addEventListener(
    "click",
    async function(){
        let textAreaText = document.getElementsByClassName("send-text-field")[0].value.trim();
        let tagPText = document.getElementsByClassName("chat-main-head")[0].getElementsByTagName("p")[0].textContent.trim();
        let method = tagPText.includes("Chat")? "sendchattext" : "senddialogtext";

        let chatDialogName = tagPText.split(" ")[1];

        if (textAreaText){
            let url = `${method}/?name=${chatDialogName}&text=${textAreaText}`;
            console.log("URL:", url);
            let createMessageAndSave = async () => {
                return fetch(url)
                    .then((response) => { return response.json(); })
                    .then((json) => { return json; })
                    .catch(() => { console.log("error"); })
            };
            let response = await createMessageAndSave();
            console.log("createMessageAndSave", response);

            if (response["status"] === "ok"){
                let text = response.text;
                let chat = response.chat;
                let username = response.user;
                let time = response.time;

                console.log(text);
                console.log(chat);
                console.log(username);
                console.log(time);

                let messagesContainer = document.getElementsByClassName("messages-container")[0];
                messagesContainer.innerHTML += `
                    <div class="message-container">
                        <p> ${username} </p>
                        <p> ${text} </p>
                        <p> ${time} </p>
                    <div>
                `;
            }
            else if (response.status === "error"){
                alert(response.errortext);
            }
        }

    }
)

