document.addEventListener("DOMContentLoaded", () => {
  const saveBtn = document.getElementById("saveBtn");

  // chỉ cho phép chọn 1 checkbox trong mỗi nhóm
  document.querySelectorAll(".options").forEach(group => {
    const checkboxes = group.querySelectorAll("input[type='checkbox']");
    checkboxes.forEach(cb => {
      cb.addEventListener("change", () => {
        if (cb.checked) {
          checkboxes.forEach(other => {
            if (other !== cb) other.checked = false;
          });
        }
      });
    });
  });

  saveBtn.addEventListener("click", () => {
    const data = [];

    document.querySelectorAll(".card").forEach(card => {
      const chapter = card.querySelector("h3").innerText;
      const exercises = [];

      card.querySelectorAll(".exercise").forEach(ex => {
        const title = ex.querySelector("label").innerText;
        const selected = [...ex.querySelectorAll("input[type='checkbox']")]
          .map((c, i) => c.checked ? i : null)
          .filter(v => v !== null)[0]; // chỉ lấy 1
        const note = ex.querySelector("input[type='text']").value;

        let status = null;
        if (selected === 0) status = "Chưa hiểu";
        if (selected === 1) status = "Hiểu một phần";
        if (selected === 2) status = "Hiểu rõ";

        exercises.push({ title, status, note });
      });

      data.push({ chapter, exercises });
    });

    console.log("Dữ liệu đã lưu:", data);
    alert("✅ Đã lưu dữ liệu thành công!");
  });
});

document.getElementById("testBtn").addEventListener("click", () => {
  window.location.href = "minitest.html";
});
