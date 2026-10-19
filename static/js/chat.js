const modeTitles = {
  qa: "Hỏi đáp kiến thức",
  exam: "Tạo đề kiểm tra",
  plan: "Lộ trình học tập",
};

let currentSessionId = null;
let currentMode = "qa";
let isSending = false;

const elements = {
  form: document.getElementById("chat-form"),
  input: document.getElementById("input-box"),
  messages: document.getElementById("messages"),
  welcome: document.getElementById("welcome"),
  sendButton: document.getElementById("send-button"),
  modeSelect: document.getElementById("mode-select"),
  modeTitle: document.getElementById("mode-title"),
};

function readSessions() {
  try {
    const sessions = JSON.parse(localStorage.getItem("eduagent_sessions") || "[]");
    return Array.isArray(sessions) ? sessions : [];
  } catch {
    return [];
  }
}

function loadHistoryList() {
  const sessions = readSessions();
  const list = document.getElementById("history-list");
  const empty = document.getElementById("history-empty");
  document.getElementById("history-count").textContent = String(sessions.length);
  empty.hidden = sessions.length > 0;
  list.replaceChildren();

  for (const session of sessions) {
    const item = document.createElement("button");
    item.type = "button";
    item.className = `history-item${session.id === currentSessionId ? " active" : ""}`;
    item.textContent = session.label;
    item.title = session.label;
    item.addEventListener("click", () => openSession(session.id, session.mode));
    list.appendChild(item);
  }
}

function saveSessionMeta(id, mode, label) {
  const sessions = readSessions().filter((session) => session.id !== id);
  sessions.unshift({ id, mode, label: label.slice(0, 48) });
  try {
    localStorage.setItem("eduagent_sessions", JSON.stringify(sessions.slice(0, 30)));
  } catch (error) {
    console.warn("Không thể lưu lịch sử trò chuyện trên trình duyệt.", error);
  }
  loadHistoryList();
}

async function startNewSession() {
  currentMode = elements.modeSelect.value;
  currentSessionId = null;
  elements.messages.replaceChildren(elements.welcome);
  elements.welcome.hidden = currentMode !== "qa";
  elements.modeTitle.textContent = modeTitles[currentMode];
  loadHistoryList();

  if (currentMode === "plan") {
    addMessage("assistant", "Chức năng tạo lộ trình học đang được phát triển.");
    return;
  }

  const endpoint = currentMode === "qa" ? "/api/chat/session" : "/api/exam/session";
  const response = await fetch(endpoint, { method: "POST" });
  if (!response.ok) throw new Error(`Không thể tạo cuộc trò chuyện (HTTP ${response.status}).`);
  const data = await response.json();
  if (!data.session_id) throw new Error("Máy chủ không trả về mã phiên trò chuyện.");
  currentSessionId = data.session_id;
  loadHistoryList();
}

function openSession(id, mode) {
  currentSessionId = id;
  currentMode = mode;
  elements.modeSelect.value = mode;
  elements.modeTitle.textContent = modeTitles[mode] || modeTitles.qa;
  elements.messages.replaceChildren();
  elements.welcome.hidden = true;
  addMessage("assistant", "Đã chọn cuộc trò chuyện này. Bạn có thể tiếp tục đặt câu hỏi.");
  loadHistoryList();
}

function addMessage(role, text, options = {}) {
  elements.welcome.hidden = true;
  const row = document.createElement("div");
  row.className = `message-row ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.setAttribute("aria-hidden", "true");
  avatar.textContent = role === "user" ? "H" : "e";

  const content = document.createElement("div");
  content.className = "message-content";
  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  if (options.error) bubble.classList.add("message-error");
  bubble.textContent = text;
  content.appendChild(bubble);

  if (role === "assistant" && options.generationTime !== undefined) {
    const meta = document.createElement("div");
    meta.className = "message-meta";
    const sparkle = document.createElement("span");
    sparkle.className = "generation-icon";
    sparkle.textContent = "✦";
    const duration = document.createElement("span");
    duration.textContent = `Hoàn thành trong ${formatDuration(options.generationTime)}`;
    meta.append(sparkle, duration);
    content.appendChild(meta);
  }

  row.append(avatar, content);
  elements.messages.appendChild(row);
  scrollToBottom();
  return content;
}

function addSuggestions(suggestions, parent) {
  if (!Array.isArray(suggestions) || suggestions.length === 0) return;
  const wrap = document.createElement("div");
  wrap.className = "suggestions";
  for (const suggestion of suggestions) {
    if (typeof suggestion !== "string" || !suggestion.trim()) continue;
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "chip";
    chip.textContent = suggestion;
    chip.addEventListener("click", () => {
      elements.input.value = suggestion;
      updateComposer();
      elements.form.requestSubmit();
    });
    wrap.appendChild(chip);
  }
  if (wrap.childElementCount) parent.appendChild(wrap);
}

function addExamCard(parent, examId) {
  const card = document.createElement("div");
  card.className = "exam-card";
  const description = document.createElement("p");
  description.textContent = "Đề kiểm tra đã sẵn sàng.";
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = "Vào làm bài";
  button.addEventListener("click", () => {
    window.location.href = `/exam/${encodeURIComponent(examId)}/take`;
  });
  card.append(description, button);
  parent.appendChild(card);
}

function showTyping() {
  const row = document.createElement("div");
  row.className = "message-row assistant";
  row.id = "typing-indicator";
  row.setAttribute("aria-label", "Trợ lý đang tạo câu trả lời");
  row.innerHTML = '<div class="message-avatar" aria-hidden="true">e</div><div class="message-content"><div class="message-bubble typing-bubble"><span class="typing" aria-hidden="true"><span></span><span></span><span></span></span><span class="typing-label">Đang suy nghĩ...</span></div></div>';
  elements.messages.appendChild(row);
  scrollToBottom();
}

function hideTyping() {
  document.getElementById("typing-indicator")?.remove();
}

function formatDuration(seconds) {
  const duration = Number(seconds);
  if (!Number.isFinite(duration) || duration < 0) return "vài giây";
  return `${duration.toFixed(1)} giây`;
}

function cleanText(text) {
  if (!text) return "";
  return text.replace(/\\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
}

function jsonToReadable(value, depth = 0) {
  const pad = "  ".repeat(depth);
  if (Array.isArray(value)) {
    return value.map((item) => typeof item === "object" && item !== null
      ? `${pad}-\n${jsonToReadable(item, depth + 1)}`
      : `${pad}- ${item}`).join("\n");
  }
  if (value && typeof value === "object") {
    return Object.entries(value).map(([key, item]) => typeof item === "object" && item !== null
      ? `${pad}${key}:\n${jsonToReadable(item, depth + 1)}`
      : `${pad}${key}: ${item}`).join("\n");
  }
  return `${pad}${value}`;
}

function formatSystemText(raw) {
  let text = cleanText(raw);
  if (text.startsWith("✅ Kiểm tra hoàn tất.")) {
    return "Cảm ơn bạn đã kiên nhẫn, đề bài kiểm tra theo yêu cầu của bạn đã hoàn thành, chúc bạn làm tốt.";
  }
  text = text.replace(/```json\s*([\s\S]*?)```/g, (_match, jsonText) => {
    try {
      return `\n${jsonToReadable(JSON.parse(jsonText))}`;
    } catch {
      return jsonText;
    }
  });
  return cleanText(text);
}

function scrollToBottom() {
  elements.messages.scrollTop = elements.messages.scrollHeight;
}

function updateComposer() {
  elements.input.style.height = "auto";
  elements.input.style.height = `${Math.min(elements.input.scrollHeight, 140)}px`;
  document.getElementById("char-count").textContent = `${elements.input.value.length} / 4000`;
}

async function sendMessage() {
  if (isSending) return;
  const text = elements.input.value.trim();
  if (!text) return;
  if (currentMode === "plan") {
    addMessage("user", text);
    addMessage("assistant", "Chức năng tạo lộ trình học đang được phát triển.");
    elements.input.value = "";
    updateComposer();
    return;
  }

  isSending = true;
  elements.sendButton.disabled = true;

  try {
    if (!currentSessionId) await startNewSession();
    addMessage("user", text);
    elements.input.value = "";
    updateComposer();
    const startedAt = performance.now();
    showTyping();
    const endpoint = currentMode === "qa"
      ? `/api/chat/session/${encodeURIComponent(currentSessionId)}/message`
      : `/api/exam/session/${encodeURIComponent(currentSessionId)}/message`;
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || data.error || `Máy chủ phản hồi HTTP ${response.status}.`);
    if (data.error) throw new Error(data.error);
    hideTyping();

    const generationTime = typeof data.generation_time_seconds === "number"
      ? data.generation_time_seconds
      : (performance.now() - startedAt) / 1000;
    const answer = currentMode === "qa" ? data.final_answer : data.ai_message;
    const content = addMessage("assistant", formatSystemText(answer || "Mình chưa tạo được câu trả lời, bạn thử gửi lại nhé."), { generationTime });

    if (currentMode === "qa") {
      addSuggestions(data.suggestions, content);
    } else if (data.flags?.evaluate_done && data.exam_id) {
      addExamCard(content, data.exam_id);
    }
    saveSessionMeta(currentSessionId, currentMode, text);
  } catch (error) {
    hideTyping();
    addMessage("assistant", `Không thể nhận câu trả lời: ${error.message}`, { error: true });
  } finally {
    isSending = false;
    elements.sendButton.disabled = false;
    elements.input.focus();
  }
}

function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  const button = document.getElementById("theme-toggle");
  const nextTheme = theme === "dark" ? "light" : "dark";
  button.setAttribute("aria-label", `Chuyển sang giao diện ${nextTheme === "dark" ? "tối" : "sáng"}`);
  try {
    localStorage.setItem("eduagent_theme", theme);
  } catch (error) {
    console.warn("Không thể lưu giao diện đã chọn.", error);
  }
}

elements.form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage();
});

elements.input.addEventListener("input", updateComposer);
elements.input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    elements.form.requestSubmit();
  }
});

document.getElementById("new-chat-button").addEventListener("click", async () => {
  try {
    await startNewSession();
  } catch (error) {
    addMessage("assistant", `Không thể tạo cuộc trò chuyện: ${error.message}`, { error: true });
  }
});

elements.modeSelect.addEventListener("change", async () => {
  try {
    await startNewSession();
  } catch (error) {
    addMessage("assistant", `Không thể khởi tạo chế độ này: ${error.message}`, { error: true });
  }
});

document.getElementById("starter-prompts").addEventListener("click", (event) => {
  const button = event.target.closest("[data-prompt]");
  if (!button) return;
  elements.input.value = button.dataset.prompt;
  updateComposer();
  elements.form.requestSubmit();
});

document.getElementById("theme-toggle").addEventListener("click", () => {
  setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
});

window.addEventListener("load", async () => {
  loadHistoryList();
  let theme = "light";
  try {
    theme = localStorage.getItem("eduagent_theme") || "light";
  } catch (error) {
    console.warn("Không thể đọc giao diện đã lưu.", error);
  }
  setTheme(theme);
  try {
    await startNewSession();
  } catch (error) {
    addMessage("assistant", `Không thể kết nối máy chủ: ${error.message}`, { error: true });
  }
});
