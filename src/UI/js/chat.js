const chatBody = document.getElementById("chatBody");
const form = document.getElementById("chatForm");
const input = document.getElementById("chatText");
const themeToggle = document.getElementById("themeToggle");
const plusBtn = document.getElementById("plusBtn");
const menu = document.getElementById("optionMenu");
const selected = document.getElementById("selectedOptions");

plusBtn.addEventListener("click", () => {
  menu.classList.toggle("hidden");
});

// Chỉ giữ 1 option hiển thị gần nhất
document.querySelectorAll(".option").forEach(opt => {
  opt.addEventListener("click", () => {
    const val = opt.getAttribute("data-value");
    const text = opt.innerText.trim();

    // Xóa option trước đó (chỉ hiện 1)
    selected.innerHTML = "";

    // Tạo phần hiển thị cho option vừa chọn
    const div = document.createElement("div");
    div.className = "selected";
    div.innerHTML = `<span class="selected-text">${text} (${val})</span> <button type="button" class="remove" aria-label="Hủy lựa chọn">X</button>`;

    // Gắn sự kiện xóa
    const btnRemove = div.querySelector(".remove");
    btnRemove.addEventListener("click", () => {
      div.remove();
    });

    //  alert(`Đã chọn: ${text} (giá trị: ${val})`);

    selected.appendChild(div);

    // Ẩn menu sau khi chọn
    menu.classList.add("hidden");
  });
});

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
