import { injectHTML } from "./components.js";

async function boot() {
  // Nạp header & footer
  await injectHTML("app-header", "./header.html");
  await injectHTML("app-footer", "./footer.html");

  // Đánh dấu menu đang active theo tên file
  const path = location.pathname.split("/").pop() || "index.html";
  const nav = document.querySelector(".nav");
  if (nav) {
    nav.querySelectorAll("a").forEach(a => {
      const href = a.getAttribute("href");
      if (href && href.endsWith(path)) a.classList.add("active");
    });
  }

  // Hiệu ứng nhỏ cho nút
  document.querySelectorAll(".btn").forEach(btn => {
    btn.addEventListener("click", () => {
      btn.animate([{ transform:"scale(1)"},{ transform:"scale(0.98)"},{ transform:"scale(1)"}], { duration:160 });
    });
  });
}

document.addEventListener("DOMContentLoaded", boot);
