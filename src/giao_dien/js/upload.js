const uploadBox = document.getElementById("uploadBox");

uploadBox.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadBox.style.background = "#e0f0ff";
});

uploadBox.addEventListener("dragleave", () => {
  uploadBox.style.background = "linear-gradient(to bottom right, #f0f7ff, #ffffff)";
});

uploadBox.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadBox.style.background = "#d6ebff";
  alert("📂 Bạn vừa thả " + e.dataTransfer.files.length + " tệp!");
});
