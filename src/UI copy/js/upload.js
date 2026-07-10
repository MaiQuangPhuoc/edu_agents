const fileInput = document.getElementById("fileInput");
const fileInfo = document.getElementById("fileInfo");
const uploadBox = document.getElementById("uploadBox");

// Khi chọn file
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) {
    fileInfo.classList.remove("hidden");
    fileInfo.textContent = `📂 Tệp đã chọn: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
  } else {
    fileInfo.classList.add("hidden");
  }
});

// Kéo & thả file
uploadBox.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadBox.style.borderColor = "#0056d6";
});
uploadBox.addEventListener("dragleave", () => {
  uploadBox.style.borderColor = "#5aa9ff";
});
uploadBox.addEventListener("drop", (e) => {
  e.preventDefault();
  const file = e.dataTransfer.files[0];
  if (file) {
    fileInput.files = e.dataTransfer.files;
    fileInfo.classList.remove("hidden");
    fileInfo.textContent = `📂 Tệp đã chọn: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
  }
});
