// // lấy title từ query string
// const params = new URLSearchParams(location.search);
// const title = params.get("title");
// if (title) {
//   document.getElementById("lesson-title").textContent = title;
// }
// document.querySelectorAll(".status-btn").forEach(btn => {
//   btn.addEventListener("click", () => {
//     if (btn.classList.contains("done")) {
//       btn.classList.remove("done");
//       btn.classList.add("not-done");
//       btn.textContent = "Chưa hoàn thành";
//     } else {
//       btn.classList.remove("not-done");
//       btn.classList.add("done");
//       btn.textContent = "Hoàn thành";
//     }
//   });
// });


// document.addEventListener("DOMContentLoaded", () => {
//   const lessons = document.querySelectorAll(".title");

//   lessons.forEach(lesson => {
//     lesson.addEventListener("click", () => {
//       const lessonId = lesson.dataset.id;
//       // Điều hướng sang session.html, truyền id qua URL
//       window.location.href = `session.html?id=${lessonId}`;
//     });
//   });
// });


// const params = new URLSearchParams(window.location.search);
// const planId = params.get("plan_id");
// const lessonId = params.get("lesson_id");




// if (lessonId) {
//   const res = await fetch(`http://127.0.0.1:5000/lesson/${planId}/${lessonId}`);
//   if (!res.ok) throw new Error("Lỗi lấy dữ liệu");
//   const data = await res.json();


// }


// document.addEventListener("DOMContentLoaded", async () => {
//   const params = new URLSearchParams(window.location.search);
//   const planId = params.get("plan_id");
//   const lessonId = params.get("lesson_id");

//   if (!planId || !lessonId) {
//     alert("Thiếu plan_id hoặc lesson_id");
//     return;
//   }

//   try {
//     const res = await fetch(`http://127.0.0.1:5000/lesson/${planId}/${lessonId}`);
//     if (!res.ok) throw new Error("Không lấy được dữ liệu từ server");
//     const data = await res.json();

//     // Tiêu đề
//     document.getElementById("lesson-title").textContent = data.lesson_title;

//     // Meta
//     document.getElementById("lesson-plan").textContent = data.lesson_plan;
//     document.getElementById("lesson-dif").textContent = `Độ khó: ${data.lesson_dif}`;
//     document.getElementById("lesson-duration").textContent = `Thời lượng: ${data.total_number_sessions_in_lesson} buổi học`;

//     // Description (Nội dung cốt lõi)
//     document.getElementById("lesson-description").textContent = data.descriptions;

//     // Mục tiêu
//     const objList = document.getElementById("lesson-objectives");
//     objList.innerHTML = data.objectives.map(o => `<li>${o}</li>`).join("");

//     // Sessions
//     const sessionsWrap = document.getElementById("lesson-sessions");
//     sessionsWrap.innerHTML = data.sessions.map((s, idx) => `
//       <div class="lesson">
//         <span class="title">${s.session_name}</span>
//         <button class="status-btn not-done">${s.status}</button>
//       </div>
//     `).join("");

//   } catch (err) {
//     console.error(err);
//     alert("Lỗi tải dữ liệu bài học");
//   }
// });


document.addEventListener("DOMContentLoaded", async () => {

const params = new URLSearchParams(window.location.search);
const planId = params.get("plan_id");
const lessonId = params.get("lesson_id");
  if (!planId || !lessonId) {
    alert("Thiếu plan_id hoặc lesson_id");
    return;
  }

  try {
    const res = await fetch(`http://127.0.0.1:5000/lesson/${planId}/${lessonId}`);
    if (!res.ok) throw new Error("Không lấy được dữ liệu từ server");
    const data = await res.json();

    // Tiêu đề
    document.getElementById("lesson-title").textContent = data.lesson_title;

    // Meta
    document.getElementById("lesson-plan").textContent = data.lesson_plan;
    document.getElementById("lesson-dif").textContent = `Độ khó: ${data.lesson_dif}`;
    document.getElementById("lesson-duration").textContent = `Thời lượng: ${data.total_number_sessions_in_lesson} buổi học`;

    // Description
    document.getElementById("lesson-description").textContent = data.descriptions;

    // Mục tiêu
    const objList = document.getElementById("lesson-objectives");
    objList.innerHTML = data.objectives.map(o => `<li>${o}</li>`).join("");

    // Sessions
    const sessionsWrap = document.getElementById("lesson-sessions");
    sessionsWrap.innerHTML = data.sessions.map((s, idx) => `
      <div class="lesson" data-session-id="${s.session_id}">
        <span class="title">${s.session_name} - buổi ${s.session_number}</span>
        <button class="status-btn">${s.status}</button>
      </div>
    `).join("");

    sessionsWrap.addEventListener("click", (e) => {
      const title = e.target.closest(".title");
      const container = title.closest(".lesson");
      const sessionId = container?.dataset?.sessionId;
      if (!title) return;
      // alert("đã click plan_id: " + planId + "\nlesson_id: "+ lessonId +"\nsessionId: " + sessionId);
      window.location.href =
        `session.html?lesson_id=${encodeURIComponent(lessonId)}&session_id=${encodeURIComponent(sessionId)}&plan_id=${encodeURIComponent(planId)}`;

    });


    // Sự kiện click button
    sessionsWrap.addEventListener("click", async (e) => {
      const btn = e.target.closest(".status-btn");
      if (!btn) return;

      const container = btn.closest(".lesson");
      const sessionId = container?.dataset?.sessionId;
      const currentStatus = (btn.textContent || "").trim();

      if (!sessionId || !currentStatus) {
        console.warn("Thiếu session_id hoặc status");
        return;
      }

      // Toggle status
      const newStatus = currentStatus === "Đã hoàn thành" ? "Chưa hoàn thành" : "Đã hoàn thành";

      // Gửi về Python
      try {
        await fetch(`http://127.0.0.1:5000/lesson/${planId}/${lessonId}/session/status`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId, status: newStatus })
        });

        // cập nhật lại nút
        btn.textContent = newStatus;
      } catch (err) {
        // console.error("Lỗi gửi dữ liệu:", err);
        console.log("Lỗi gửi dữ liệu");

      }
    });
  } catch (err) {
    console.error(err);
    alert("Lỗi tải dữ liệu bài học");
  }
});


