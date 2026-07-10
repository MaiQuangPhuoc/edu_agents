const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

function appendMessage(text, sender = "user") {
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;
  msg.textContent = (sender === "bot" ? "🤖 " : "") + text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function handleSend() {
  const message = userInput.value.trim();
  if (!message) return;

  // Hiển thị tin nhắn người dùng
  appendMessage(message, "user");
  userInput.value = "";

  try {
    // Gửi đến API backend
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error("Phản hồi không hợp lệ từ server");
    }

    const data = await response.json();

    // Hiển thị phản hồi hệ thống
    appendMessage(data.reply, "bot");

  } catch (error) {
    // appendMessage("❌ Lỗi kết nối tới máy chủ.", "bot");
    console.error("Lỗi gửi yêu cầu:", error);
  }
}

// Gửi khi nhấn nút
sendBtn.onclick = handleSend;

// Gửi khi nhấn Enter
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") handleSend();
});
