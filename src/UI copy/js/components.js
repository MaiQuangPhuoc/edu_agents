// Nạp file HTML (header/footer) vào phần tử theo id
export async function injectHTML(targetId, htmlPath) {
  const host = document.getElementById(targetId);
  if (!host) return;
  try {
    const res = await fetch(htmlPath, { cache: "no-store" });
    const html = await res.text();
    host.innerHTML = html;
  } catch (e) {
    host.innerHTML = `<div style="padding:12px;color:#ef4444;border:1px dashed #ef4444;border-radius:8px">
      Không tải được ${htmlPath}. Hãy chạy qua server tĩnh (vd: VSCode Live Server).
    </div>`;
  }
}
