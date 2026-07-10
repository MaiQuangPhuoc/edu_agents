// Xử lý click vào Nộp bài
document.getElementById("saveBtn").addEventListener("click", () => {
//   alert("Bài kiểm tra đã được nộp!");
    window.location.href = "danh_gia.html";
});

// Chuyển sang trang tự đánh giá
document.getElementById("selfEvalBtn").addEventListener("click", () => {
  window.location.href = "danhgia.html";
});

// Tô màu khi chọn đáp án
document.querySelectorAll("input[type=radio]").forEach(radio => {
  radio.addEventListener("change", () => {
    // reset style các đáp án khác trong cùng câu
    const group = document.querySelectorAll(`input[name=${radio.name}]`);
    group.forEach(r => r.parentElement.style.background = "white");

    // tô màu đáp án được chọn
    if (radio.checked) {
      radio.parentElement.style.background = "#d0ebff"; // xanh nhạt
    }
  });
});
