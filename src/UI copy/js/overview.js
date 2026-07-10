// const MODULES = [
//   {
//     name:"Chương 1: Mệnh đề và tập hợp",
//     desc:"Chương này học về mệnh đề, tập hợp và các phép toán trên tập hợp.",
//     content:"Mệnh đề logic, tập hợp, giao – hợp – hiệu.",
//     lessons:["Mệnh đề","Tập hợp","Các phép toán trên tập hợp"],
//     priority:"Cao / 3 tuần",
//     progress:0.6
//   },
//   {
//     name:"Chương 2: Hàm số bậc nhất và bậc hai",
//     desc:"Giới thiệu về hàm số bậc nhất và bậc hai, đồ thị và ứng dụng.",
//     content:"Hàm số, đồ thị, nghiệm của phương trình bậc hai.",
//     lessons:["Hàm số bậc nhất","Hàm số bậc hai","Đồ thị và ứng dụng"],
//     priority:"Trung bình / 4 tuần",
//     progress:0.3
//   }
// ];

// function renderModule(m){
//   const wrap = document.createElement("div");
//   wrap.className="module-card";
//   wrap.innerHTML=`
//     <div class="module-header">
//       <h3>${m.name}</h3>
//       <span class="priority">Ưu tiên: ${m.priority}</span>
//     </div>
//     <p><strong>Mô tả:</strong> ${m.desc}</p>
//     <p><strong>Nội dung cần nắm:</strong> ${m.content}</p>
//     <div class="lessons">
//       ${m.lessons.map((l,i)=>`<div class="lesson" data-lesson="${l}" data-index="${i+1}">${l}</div>`).join("")}
//     </div>
//     <div class="resources">
//       <span>📺 Video</span><span>📄 Tài liệu</span><span>📝 Quiz</span>
//     </div>
//     <div class="progress-wrap">
//       <div class="progress" style="width:${Math.round(m.progress*100)}%"></div>
//     </div>
//   `;
  
//   // gắn sự kiện click
//   wrap.querySelectorAll(".lesson").forEach(el=>{
//     el.addEventListener("click", ()=>{
//       const lessonName = el.dataset.lesson;
//       location.href = `./lesson.html?title=${encodeURIComponent(lessonName)}`;
//     });
//   });

//   return wrap;
// }


// const modulesEl = document.getElementById("modules");
// MODULES.forEach(m=>modulesEl.appendChild(renderModule(m)));


// // -----------------------------------------------------------------------------
// async function loadPlan() {
//   const params = new URLSearchParams(location.search);
//   const planId = params.get("id");

//   if (!planId) {
//     console.error("Không có planId trong URL");
//     return;
//   }

//   try {
//     const res = await fetch(`http://127.0.0.1:5000/overview/${planId}`);
//     if (!res.ok) throw new Error("Lỗi lấy dữ liệu");
//     const data = await res.json();

//     console.log("Dữ liệu kế hoạch:", data);
//     // render data ra HTML
//   } catch (err) {
//     console.error(err);
//   }
// }

// loadPlan();









// function renderModule(m){
//   const wrap = document.createElement("div");
//   wrap.className="module-card";
//   wrap.innerHTML=`
//     <div class="module-header">
//       <h3>${m.overview_result.learner_profile.learning_goals}</h3>
//       <span class="priority">Ưu tiên: ${m.overview_result.study_modules.priority}</span>
//     </div>
//     <p><strong>Mô tả:</strong> ${m.overview_result.study_modules.description || ""}</p>
//     <div class="lessons">
//       ${m.overview_result.study_modules.lesson_titles.map((l,i)=>`<div class="lesson" data-lesson="${l}" data-index="${i+1}">${l}</div>`).join("")}
//     </div>
//     <div class="progress-wrap">
//       <div class="progress" style="width:${Math.round((m.study_details_result.sessions_done/m.study_details_result.total_number_sessions || 0)*100)}%"></div>
//     </div>
//   `;

//   wrap.querySelectorAll(".lesson").forEach(el=>{
//     el.addEventListener("click", ()=>{
//       const lessonName = el.dataset.lesson;
//       location.href = `./lesson.html?title=${encodeURIComponent(lessonName)}`;
//     });
//   });

//   return wrap;
// }


// async function loadPlan() {
//   const params = new URLSearchParams(location.search);
//   const planId = params.get("id");

//   if (!planId) {
//     console.error("Không có planId trong URL");
//     return;
//   }

//   try {
//     const res = await fetch(`http://127.0.0.1:5000/overview/${planId}`);
//     if (!res.ok) throw new Error("Lỗi lấy dữ liệu");
//     const data = await res.json();

//     const overview = data.overview_result;

//     // --- Constraints ---
//     document.querySelector(".constraints").innerHTML = `
//       <div class="constraint-item">⏱️ ${overview.constraints.available_hours_per_day}/ngày</div>
//       <div class="constraint-item">📅 ${overview.constraints.available_days_per_week}</div>
//       <div class="constraint-item">🎯 Hạn chót: ${overview.constraints.deadline}</div>
//       <div class="constraint-item">⚡ Tối đa ${overview.constraints.max_modules_per_week}/tuần</div>
//     `;

//     // --- Learner Profile ---
//     document.querySelector(".learner ul").innerHTML = `
//       <li>Trình độ: ${overview.learner_profile.level}</li>
//       <li>Phong cách học: ${overview.learner_profile.preferred_study_style}</li>
//       <li>Mục tiêu: ${overview.learner_profile.learning_goals}</li>
//       <li>Phạm vi: ${overview.learner_profile.plan_scope}</li>
//     `;

//     // --- Modules ---
//     const modulesEl = document.getElementById("modules");
//     modulesEl.innerHTML = "";
//     overview.study_modules.forEach(m => {
//       modulesEl.appendChild(renderModule(m));
//     });

//   } catch (err) {
//     console.error(err);
//   }
// }


const params = new URLSearchParams(location.search);
const planId = params.get("id");


function normalizeUrl(url) {
  const prefix = "http://localhost:5500/src/UI/html/";
  if (url.startsWith(prefix)) {
    return url.slice(prefix.length); // chỉ bỏ prefix đi
  }
  return url;
}




function renderModule(m, details, progress=0) {
  const wrap = document.createElement("div");
  wrap.className="module-card";

  // Tìm detail_plan ứng với module_name
  const detailPlan = details.detail_plans.find(dp => dp.module_name === m.module_name);

  wrap.innerHTML=`
    <div class="module-header">
      <h3>${m.module_name}</h3>
      <span class="priority">Ưu tiên: ${m.priority}</span>
    </div>
    <p><strong>Mô tả:</strong> ${m.description || ""}</p>
    <p><strong>Mục tiêu:</strong></p>
    <ul>
      ${m.objectives.map(o=>`<li>${o}</li>`).join("")}
    </ul>
    <div class="lessons">
      ${
        (detailPlan?.lessons || []).map(lesson => {
          return `
            <div class="lesson" 
                data-plan-id="${planId}" 
                data-lesson-id="${lesson.lesson_id}" 
                data-title="${lesson.lesson_title}">
                ${lesson.lesson_title}
            </div>`;
        }).join("")
      }
    </div>
    <div class="resources">
      ${m.resources.map(r => {
          const cleanUrl = normalizeUrl(r.url);
          return `<a href="https://${cleanUrl}" target="_blank">[ ${r.type} ]</a>`;
      }).join("<br>")}
    </div>
    <div class="progress-wrap">
      <div class="progress" style="width:${Math.round(progress*100)}%"></div>
    </div>
  `;

  // Gắn click cho từng lesson
  wrap.querySelectorAll(".lesson").forEach(el => {
    el.addEventListener("click", () => {
      const planId = el.dataset.planId;
      const lessonId = el.dataset.lessonId;
      location.href = `./lesson.html?plan_id=${encodeURIComponent(planId)}&lesson_id=${encodeURIComponent(lessonId)}`;
    });
  });

  return wrap;
}




function daysBetween(start, deadline) {
  if (!start || !deadline) return "";
  const startDate = new Date(start);
  const endDate = new Date(deadline);
  const diffTime = endDate - startDate;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays > 0 ? `(${diffDays} ngày)` : "Hết hạn";
}

// let lesson_id = 'ok';

 
async function loadPlan() {
  // const params = new URLSearchParams(location.search);
  // const planId = params.get("id");

  if (!planId) {
    alert("❌ Không tìm thấy ID kế hoạch.");

    return;
  }

  try {
    const res = await fetch(`http://127.0.0.1:5000/overview/${planId}`);
    if (!res.ok) throw new Error("Lỗi lấy dữ liệu");
    const data = await res.json();

    const overview = data.overview_result;
    const details = data.study_details_result;
    // lesson_id = details.detail_plans[0].lessons[0].lesson_id;  


    // if (lesson_id){
    //   alert("lesson_id ok");
    // }else{
    //   alert("lesson_id none")
    // }



    document.getElementById("plan-title").textContent = overview.learner_profile.learning_goals|| "KẾ HOẠCH HỌC TẬP";
    const deadline = overview.constraints?.deadline || "";
    const createdAt = data.time || "";
    document.getElementById("plan-scope").textContent = daysBetween(createdAt, deadline);


    // --- Constraints ---
    document.querySelector(".constraints").innerHTML = `
      <div class="constraint-item">⏱️ ${overview.constraints.available_hours_per_day}/ngày</div>
      <div class="constraint-item">📅 ${overview.constraints.available_days_per_week.join(", ")}</div>
      <div class="constraint-item">🎯 Hạn chót: ${overview.constraints.deadline}</div>
      <div class="constraint-item">⚡ Tối đa ${overview.constraints.max_modules_per_week}/tuần</div>
    `;

    // --- Learner Profile ---
    document.querySelector(".learner ul").innerHTML = `
      <li>Trình độ: ${overview.learner_profile.level}</li>
      <li>Phong cách học: ${overview.learner_profile.preferred_study_style}</li>
      <li>Mục tiêu: ${overview.learner_profile.learning_goals}</li>
      <li>Phạm vi: ${overview.learner_profile.plan_scope}</li>
    `;

    // --- Modules ---
    const modulesEl = document.getElementById("modules");
    modulesEl.innerHTML = "";
    // const overview = data.overview_result;
    // const details = data.study_details_result;

    overview.study_modules.forEach(m => {
      // tìm module tương ứng trong detail_plans
      const moduleDetail = details.detail_plans.find(dp => dp.module_name === m.module_name);

      let progress = 0;
      let total_done = 0;
      let total_sessions = 0;

      if (moduleDetail) {
        total_done = parseInt(moduleDetail.total_number_session_done_in_module);
        total_sessions = parseInt(moduleDetail.total_number_session_in_module);

        if (total_sessions > 0) {
          progress = total_done / total_sessions;
        }
      }

      console.log("Module:", m.module_name);
      console.log("Progress:", progress);
      console.log("Đã học:", total_done, "/", total_sessions);


      modulesEl.appendChild(renderModule(m, details,progress));
    });


  } catch (err) {
    console.error(err);
  }
}


document.addEventListener("DOMContentLoaded", loadPlan);


