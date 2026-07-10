const dropArea = document.getElementById("drop-area");
const fileElem = document.getElementById("fileElem");
const fileNameDisplay = document.getElementById("file-name");
const sendLinkBtn = document.getElementById("send-link-btn");

// Drag over
dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropArea.classList.add("dragover");
});

// Drag leave
dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("dragover");
});

// Drop
dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  dropArea.classList.remove("dragover");
  const file = e.dataTransfer.files[0];
  handleFile(file);
});

// File selected from input
fileElem.addEventListener("change", (e) => {
  const file = e.target.files[0];
  handleFile(file);
});

// function handleFile(file) {
//   if (file && /\.(doc|docx)$/i.test(file.name)) {
//     fileNameDisplay.textContent = ` Đã chọn: ${file.name}`;
//     // TODO: gửi file lên server tại đây
//   } else {
//     fileNameDisplay.textContent = "❌ Vui lòng chọn file Word (.doc hoặc .docx)";
//   }
// }

let selectedFile = null;

fileElem.addEventListener("change", () => {
  selectedFile = fileElem.files[0];
  handleFile(selectedFile);
});

function handleFile(file) {
  if (file && /\.(doc|docx)$/i.test(file.name)) {
    fileNameDisplay.textContent = ` Đã chọn: ${file.name}`;
    sendLinkBtn.style.display = "inline-block";

    sendLinkBtn.onclick = async () => {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const res = await fetch("http://localhost:8000/upload", {
          method: "POST",
          body: formData
        });

        const result = await res.text();
        alert("📥 Phản hồi từ server:\n" + result);
      } catch (err) {
        alert("❌ Lỗi khi gửi file!");
        console.error(err);
      }
    };
  } else {
    fileNameDisplay.textContent = "❌ Vui lòng chọn file Word (.doc hoặc .docx)";
    sendLinkBtn.style.display = "none";
  }
}