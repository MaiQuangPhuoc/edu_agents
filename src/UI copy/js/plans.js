const rowsEl = document.getElementById("planRows");
const emptyEl = document.getElementById("empty");
const qEl = document.getElementById("q");
const statusEl = document.getElementById("status");
const newBtn = document.getElementById("newPlanBtn");

let PLANS = []; // danh sách kế hoạch toàn cục

function parseTime(str) {
  return new Date(str.replace(/\//g, "-"));
}



function render(list){
  rowsEl.innerHTML = "";
  if (!list.length){
    emptyEl.style.display = "block";
    return;
  }
  emptyEl.style.display = "none";

  list.sort((a, b) => parseTime(b.time) - parseTime(a.time));

  let id  = null;
  let newValue = null;
  let planId = null;
  let newStatus = null;


  list.forEach(p=>{
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="btnn" data-actt="openn" data-id="${p.plan_id}">${p.plan_id || "N/A"}</td>
      <td class="editable" data-field="plan_name"><strong>${p.plan_name || "k có"}</strong></td>
      <td>${p.time || "N/A"}</td>
      <td>${p.sessions_done}/${p.total_number_sessions}</td>
      <td class="editable" data-field="status"><strong>${p.status || "Chưa có"}</strong></td>
      <td>
        <button class="btn" data-act="open" data-id="${p.plan_id}">Mở</button>
      </td>
    `;

    // Khi click vào "learning_goals", thay nó thành input
    tr.querySelector("[data-field='plan_name']").addEventListener("click", function () {
      planId = p.plan_id;
      const currentValue = p.plan_name || "ko có";
      const input = document.createElement("input");
      input.value = currentValue;

      this.innerHTML = "";
      this.appendChild(input);

      // bắt sự kiện nhập để lưu lại giá trị mới
      input.addEventListener("input", function () {
        newValue = this.value;
      });

      // nếu thoát input (blur) mà không bấm lưu thì vẫn hiển thị lại
      input.addEventListener("blur", function () {
        if (!newValue) newValue = currentValue;
        // hiển thị text thay vì input
        tr.querySelector("[data-field='plan_name']").innerHTML = "<strong>" + newValue + "</strong>";
      });



      input.focus();
    });

    tr.querySelector("[data-field='status']").addEventListener("click", function () {
      planId = p.plan_id;
      const currentValue = p.status || "Chưa có";
      const input = document.createElement("input");
      input.value = currentValue;
      this.innerHTML = "";
      this.appendChild(input);

      input.addEventListener("input", function () {
        newStatus = this.value;
      });
      input.addEventListener("blur", function () {
        if (!newStatus) newStatus = currentValue;
        tr.querySelector("[data-field='status']").innerHTML = "<strong>" + newStatus + "</strong>";
      });

      input.focus();
    });


    // let id = '';
    tr.querySelector("[data-actt='openn']").addEventListener("click", () => {
      id = tr.querySelector("[data-actt='openn']").dataset.id;
      // alert(id);
    });

    rowsEl.appendChild(tr);
  });

    // Khi click nút Lưu
  document.getElementById("btnSave").addEventListener("click", function () {
    fetch("http://127.0.0.1:5000/update_plan", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        plan_id: planId,
        plan_name: newValue,
        status: newStatus
      })
    })
    .then(res => res.json())
    .then(data => {
      console.log("Server trả về:", data);
      alert("Đã gửi thành công!");
    });
  });


    // Khi click nút Xóa
  document.getElementById("btnDelete").addEventListener("click", function () {
    // alert("⚠️ Bạn có chắc muốn XÓA kế hoạch này không?" + id);
    fetch(`http://127.0.0.1:5000/delete_plan/${id}`, { method: "DELETE" })
      .then(res => res.json())
      .then(data => {
        // alert("Đã xóa kế hoạch");
        location.reload();
      });
  });


  // gắn sự kiện cho nút
  rowsEl.querySelectorAll("[data-act='open']").forEach(btn=>{
    btn.addEventListener("click", ()=>{
      const id = btn.dataset.id;
      location.href = `./overview.html?id=${id}`;
    });
  });
}

function applyFilter(){
  const q = qEl.value.trim().toLowerCase();
  const st = statusEl.value;
  const list = PLANS.filter(p=>{
    const okQ = !q || (p.plan_id.toLowerCase().includes(q)) ;
    const okS = !st || p.status === st;
    return okQ && okS;
  });
  render(list);
}

qEl.addEventListener("input", applyFilter);
statusEl.addEventListener("change", applyFilter);

newBtn.addEventListener("click", ()=>{
  location.href = "./chat.html";
});

async function loadPlans() {
  try {
    const res = await fetch("http://127.0.0.1:5000/get_all_plans");
    PLANS = await res.json();
    render(PLANS);
  } catch (err) {
    console.error("Lỗi load kế hoạch:", err);
  }
}


window.onload = loadPlans;
