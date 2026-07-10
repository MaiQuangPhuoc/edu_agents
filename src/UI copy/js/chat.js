const chatBody = document.getElementById("chatBody");
const form = document.getElementById("chatForm");
const input = document.getElementById("chatText");
const themeToggle = document.getElementById("themeToggle");

function addMsg({ text, who }) {
  const row = document.createElement("div");
  row.className = `row ${who}`;
  const bubble = document.createElement("div");
  bubble.className = "msg";
  bubble.innerHTML = `<p>${escapeHTML(text)}</p>`;
  row.appendChild(bubble);
  chatBody.appendChild(row);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function escapeHTML(s){
  return (s||"").replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
}

function addTyping(){
  const row = document.createElement("div");
  row.className = "row bot";
  row.id = "typing";
  row.innerHTML = `<div class="msg"><span class="typing"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>`;
  chatBody.appendChild(row);
  chatBody.scrollTop = chatBody.scrollHeight;
}
function removeTyping(){
  const t = document.getElementById("typing");
  if (t) t.remove();
}



form.addEventListener("submit", (e)=>{
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  addMsg({ text, who:"user" });
  input.value = "";
  addTyping();

  fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  })
  .then(res => res.json())
  .then(data => {
    removeTyping();
    addMsg({ text: data.reply, who:"bot" });
  })
  .catch(err => {
    removeTyping();
    addMsg({ text: "❌ Lỗi server", who:"bot" });
    console.error(err);
  });
});


// lời chào ban đầu
addMsg({ who:"bot", text:"Xin chào! Mình là Trợ lý học tập. Bạn muốn tạo kế hoạch học mới hay xem gợi ý?" });

// document.addEventListener("DOMContentLoaded", () => {
//   const themeToggle = document.getElementById("themeToggle");

//   themeToggle.addEventListener("click", () => {
//     document.body.classList.toggle("dark");
//     if (document.body.classList.contains("dark")) {
//       themeToggle.textContent = "☀️"; // nếu đang dark thì hiện nút mặt trời
//     } else {
//       themeToggle.textContent = "🌙"; // nếu đang light thì hiện nút mặt trăng
//     }
//   });
// });
