document.getElementById("sendBtn").addEventListener("click", sendMessage);

function sendMessage() {
  const input = document.getElementById("userInput");
  const text = input.value.trim();
  if (text === "") return;

  addMessage("user", text);
  input.value = "";

  setTimeout(() => {
    addMessage("bot", "Cảm ơn bạn đã chia sẻ, tôi sẽ lưu thông tin này để cá nhân hoá lộ trình học 📘.");
  }, 1000);
}

function addMessage(sender, text) {
  const chatBody = document.getElementById("chatBody");
  const msg = document.createElement("div");
  msg.classList.add("message", sender);

  const avatar = document.createElement("div");
  avatar.classList.add("avatar");
  avatar.textContent = sender === "bot" ? "🤖" : "🧑";

  const msgText = document.createElement("div");
  msgText.classList.add("text");
  msgText.textContent = text;

  msg.appendChild(avatar);
  msg.appendChild(msgText);
  chatBody.appendChild(msg);

  chatBody.scrollTop = chatBody.scrollHeight;
}
