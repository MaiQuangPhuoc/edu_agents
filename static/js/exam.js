let examQuestions = [];

async function beginExam() {
  const res = await fetch(`/api/exam/${EXAM_ID}`);
  const data = await res.json();
  if (data.error) { alert(data.error); return; }
  examQuestions = data.questions;

  document.getElementById("intro-view").style.display = "none";
  document.getElementById("submit-bar").style.display = "block";
  renderQuestions("take");
}

function renderQuestions(mode, detailById = {}) {
  const wrap = document.getElementById("question-list");
  wrap.style.display = "block";
  wrap.innerHTML = examQuestions.map((q, i) => {
    const d = detailById[q.id];
    const optionsHtml = Object.entries(q.options).map(([key, text]) => {
      let cls = "option";
      if (mode === "review") {
        if (key === d.correct_answer) cls += " correct";
        else if (key === d.your_answer && !d.is_correct) cls += " wrong";
      }
      const disabled = mode === "review" ? "disabled" : "";
      const checked = d && d.your_answer === key ? "checked" : "";
      return `<label class="${cls}"><input type="radio" name="q-${q.id}" value="${key}" ${disabled} ${checked}> ${key}. ${text}</label>`;
    }).join("");

    const giaiThich = mode === "review"
      ? `<div class="giai-thich">${d.giai_thich}</div>` : "";

    return `<div class="q-card">
      <div class="q-title">Câu ${i + 1}: ${q.question}</div>
      ${optionsHtml}
      ${giaiThich}
    </div>`;
  }).join("");
}

async function submitExam() {
  const answers = {};
  examQuestions.forEach(q => {
    const picked = document.querySelector(`input[name="q-${q.id}"]:checked`);
    answers[q.id] = picked ? picked.value : "";
  });

  const res = await fetch(`/api/exam/${EXAM_ID}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answers }),
  });
  const data = await res.json();

  const detailById = {};
  data.detail.forEach(d => detailById[d.id] = d);

  document.getElementById("submit-bar").style.display = "none";
  const badge = document.getElementById("score-badge");
  badge.style.display = "inline-block";
  badge.innerText = `${data.score}/${data.total} điểm`;

  renderQuestions("review", detailById);
}