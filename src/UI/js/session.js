// session.js - handle interactive behaviors on session.html

// document.addEventListener("DOMContentLoaded", () => {
//   // Highlight today's session
//   const sessionInfo = document.querySelector(".session-info");
//   if (sessionInfo) {
//     sessionInfo.style.animation = "fadeIn 0.8s ease-in-out";
//   }

//   // Click on resource links -> show alert or future modal
//   document.querySelectorAll(".resources a").forEach(link => {
//     link.addEventListener("click", (e) => {
//       e.preventDefault();
//       const type = link.textContent.trim();
//       alert(`📂 Mở tài nguyên: ${type}`);
//       // sau này thay bằng modal hoặc open resource viewer
//     });
//   });
// });

// // Simple animation keyframe inject
// const style = document.createElement("style");
// style.innerHTML = `
// @keyframes fadeIn {
//   from { opacity: 0; transform: translateY(10px); }
//   to   { opacity: 1; transform: translateY(0); }
// }`;
// document.head.appendChild(style);


// document.addEventListener("DOMContentLoaded", async () => {
//   const params = new URLSearchParams(window.location.search);
//   const lessonId = params.get("lesson_id");
//   const sessionId = params.get("session_id");
//   const planId   = params.get("plan_id"); // có thể null

//   if (!lessonId || !sessionId) {
//     console.warn("Thiếu lesson_id hoặc session_id");
//     return;
//   }

//   await fetch("http://127.0.0.1:5000/debug", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ lesson_id: lessonId, session_id: sessionId, plan_id: planId })
//   });
// });


// document.addEventListener("DOMContentLoaded", async () => {
//   const params = new URLSearchParams(window.location.search);
//   const lessonId = params.get("lesson_id");
//   const sessionId = params.get("session_id");
//   const planId   = params.get("plan_id");

//   if (!lessonId || !sessionId) {
//     console.warn("Thiếu lesson_id hoặc session_id");
//     return;
//   }

//   const res = await fetch("http://127.0.0.1:5000/debug", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ lesson_id: lessonId, session_id: sessionId, plan_id: planId })
//   });

//   const data = await res.json(); // ✅ nhận object session
//   alert("data: " + data)
//   renderSession(data);
// });

// function renderSession(session) {
//   // Cập nhật tiêu đề bài học
//   document.querySelector(".lesson-detail h2").innerHTML = 
//     `📌 Bài học: ${session.session_name} <span class="badge">Buổi ${session.session_number}</span>`;

//   // Thông tin chung
//   document.querySelector(".session-info").innerHTML = `
//     <div class="info-item">📅 Ngày: ${session.daily.session_date}</div>
//     <div class="info-item">⏰ Thời gian: ${session.daily.duration_minutes} phút</div>
//     <div class="info-item">😎 Trạng thái: ${session.status}</div>
//   `;

//   // Nội dung
//   document.querySelector(".content .box ul").innerHTML = `
//     <li>${session.core_content}</li>
//   `;

//   // Mục tiêu
//   const objectivesHtml = session.objectives.map(o => `<li>${o}</li>`).join("");
//   document.querySelectorAll(".content .box ul")[0].innerHTML = objectivesHtml;

//   // Hoạt động
//   const activitiesHtml = session.activities.map(a => `<li>${a}</li>`).join("");
//   document.querySelectorAll(".content .box ul")[1].innerHTML = activitiesHtml;

//   // Bài tập
//   const assignmentsHtml = session.assignments.map(a => `<p>- ${a}</p>`).join("");
//   document.querySelector(".exercise").innerHTML = `
//     <h3>✍️ Dạng bài tập</h3>
//     ${assignmentsHtml}
//   `;

//   // Tài nguyên
//   const resourcesHtml = session.resources.map(r => 
//     `<a href="${r.url}" target="_blank">[${r.type}] ${r.title}</a>`
//   ).join("<br>");
//   document.querySelector(".resources").innerHTML = `
//     <h3>📂 Tài Nguyên</h3>
//     ${resourcesHtml}
//   `;
// }



document.addEventListener("DOMContentLoaded", async () => {
  const params = new URLSearchParams(window.location.search);
  const lessonId = params.get("lesson_id");
  const sessionId = params.get("session_id");
  const planId   = params.get("plan_id");

  const res = await fetch("http://127.0.0.1:5000/debug", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ lesson_id: lessonId, session_id: sessionId, plan_id: planId })
  });
  const data = await res.json();

  // header
  document.getElementById("session-date").textContent   = data.daily.session_date;
  document.getElementById("session-number").textContent = data.daily.duration_minutes + "phút";
  document.getElementById("session-time").textContent   = data.daily.hours + "giờ";

  // lesson detail
  document.getElementById("lesson-title").textContent = data.session_name;
  document.getElementById("lesson-plan").textContent  = "Buổi "+ data.session_number;

  // nội dung cần nắm
  const core = document.getElementById("core-content");
  core.innerHTML = "";
  (Array.isArray(data.objectives) ? data.objectives : [data.core_content])
    .forEach(item => {
      const li = document.createElement("li");
      li.textContent = item;
      core.appendChild(li);
    });

  // hoạt động
  const act = document.getElementById("activities");
  act.innerHTML = "";
  data.activities.forEach(a => {
    const li = document.createElement("li");
    li.textContent = a;
    act.appendChild(li);
  });

  // bài tập
  const ass = document.getElementById("assignments");
  ass.innerHTML = "";
  data.assignments.forEach(a => {
    const li = document.createElement("li");
    li.textContent = a;
    ass.appendChild(li);
  });

  // tài nguyên
  const resDiv = document.getElementById("resources");
  resDiv.innerHTML = "";
  data.resources.forEach(r => {
    const a = document.createElement("a");
    a.href = r.url;
    a.textContent = `[${r.type}]`;
    a.target = "_blank";
    resDiv.appendChild(a);
  });
});
