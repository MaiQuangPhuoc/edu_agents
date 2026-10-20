(() => {
  "use strict";
  const key = "eduagent-theme";
  const root = document.documentElement;
  const read = () => {
    try { return localStorage.getItem(key) === "dark" ? "dark" : "light"; }
    catch { return "light"; }
  };
  const apply = (mode) => {
    root.dataset.theme = mode;
    const label = mode === "dark" ? "Chuyển sang giao diện sáng" : "Chuyển sang giao diện tối";
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      button.setAttribute("aria-label", label);
      button.setAttribute("title", label);
      button.setAttribute("aria-pressed", String(mode === "dark"));
    });
  };
  apply(read());
  document.addEventListener("DOMContentLoaded", () => {
    apply(read());
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      button.addEventListener("click", () => {
        const next = root.dataset.theme === "dark" ? "light" : "dark";
        try { localStorage.setItem(key, next); } catch { /* storage unavailable */ }
        apply(next);
      });
    });
  });
})();
