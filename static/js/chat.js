let currentSessionId = null;
let currentMode = "qa";

function loadHistoryList() {
  const list = JSON.parse(localStorage.getItem("eduagent_sessions") || "[]");
  const el = document.getElementById("history-list");
  el.innerHTML = list.map(s =>
    `<div class="history-item" onclick="openSession('${s.id}','${s.mode}')">${s.label}</div>`
  ).join("");
}

function saveSessionMeta(id, mode, label) {
  const list = JSON.parse(localStorage.getItem("eduagent_sessions") || "[]");
  list.unshift({ id, mode, label });
  localStorage.setItem("eduagent_sessions", JSON.stringify(list.slice(0, 30)));
  loadHistoryList();
}

async function startNewSession() {
  currentMode = document.getElementById("mode-select").value;
  document.getElementById("messages").innerHTML = "";

  if (currentMode === "plan") {
    addBubble("system", "Chức năng tạo lộ trình học chưa khả dụng, đang được phát triển.");
    currentSessionId = null;
    return;
  }

  const endpoint = currentMode === "qa" ? "/api/chat/session" : "/api/exam/session";
  const res = await fetch(endpoint, { method: "POST" });
  const data = await res.json();
  currentSessionId = data.session_id;
}

function openSession(id, mode) {
  // Bản đơn giản: chỉ khôi phục session_id + mode, lịch sử tin nhắn không lưu lại (chưa có DB)
  currentSessionId = id;
  currentMode = mode;
  document.getElementById("mode-select").value = mode;
  document.getElementById("messages").innerHTML = "";
  addBubble("system", "Đã khôi phục phiên trước — gõ tiếp để tiếp tục.");
}

function addBubble(role, text) {
  const el = document.createElement("div");
  el.className = `bubble ${role === "user" ? "user" : "system"}`;
  el.innerText = text;
  document.getElementById("messages").appendChild(el);
  el.scrollIntoView({ behavior: "smooth" });
  return el;
}

function addSuggestions(suggestions) {
  if (!suggestions || !suggestions.length) return;
  const wrap = document.createElement("div");
  wrap.className = "suggestions";
  wrap.innerHTML = suggestions.map(s => `<span class="chip" onclick="quickSend('${s.replace(/'/g, "\\'")}')">${s}</span>`).join("");
  document.getElementById("messages").appendChild(wrap);
}

function addExamCard(examId) {
  const wrap = document.createElement("div");
  wrap.className = "exam-card";
  wrap.innerHTML = `<p>Đề kiểm tra đã sẵn sàng.</p><button class="btn-primary" onclick="window.location.href='/exam/${examId}/take'">Vào làm bài</button>`;
  document.getElementById("messages").appendChild(wrap);
}

function quickSend(text) {
  document.getElementById("input-box").value = text;
  sendMessage();
}

async function sendMessage() {
  const box = document.getElementById("input-box");
  const text = box.value.trim();
  if (!text) return;

  if (currentMode === "plan") {
    addBubble("user", text);
    addBubble("system", "Chức năng tạo lộ trình học chưa khả dụng.");
    box.value = "";
    return;
  }

  if (!currentSessionId) await startNewSession();
  addBubble("user", text);
  box.value = "";

  const endpoint = currentMode === "qa"
    ? `/api/chat/session/${currentSessionId}/message`
    : `/api/exam/session/${currentSessionId}/message`;

  const res = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text }),
  });
  const data = await res.json();

  if (currentMode === "qa") {
    addBubble("system", data.final_answer || "");
    addSuggestions(data.suggestions);
    saveSessionMeta(currentSessionId, "qa", text.slice(0, 30));
  } else {
    addBubble("system", data.ai_message || "");
    if (data.flags && data.flags.evaluate_done && data.exam_id) {
      addExamCard(data.exam_id);
    }
    saveSessionMeta(currentSessionId, "exam", text.slice(0, 30));
  }
}

window.onload = () => { loadHistoryList(); startNewSession(); };