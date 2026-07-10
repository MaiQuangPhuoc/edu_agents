// Thêm tính năng tương tác nhỏ cho nút bài học
document.addEventListener("DOMContentLoaded", () => {
  const lessonButtons = document.querySelectorAll(".lessons button");

  lessonButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      alert(`Bạn đã chọn: ${btn.textContent}`);
    });
  });
});
