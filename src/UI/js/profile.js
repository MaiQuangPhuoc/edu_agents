const $ = sel => document.querySelector(sel);
const nameEl = $("#name");
const emailEl = $("#email");
const trackEl = $("#track");
const bioEl = $("#bio");
const avatarEl = $("#avatar");
const summaryEl = $("#summary");

function load(){
  const raw = localStorage.getItem("profile_demo");
  if (!raw) return;
  try {
    const p = JSON.parse(raw);
    nameEl.value = p.name || "";
    emailEl.value = p.email || "";
    trackEl.value = p.track || "";
    bioEl.value = p.bio || "";
    updateUI();
  } catch {}
}

function firstLetter(s){
  return (s || "").trim().charAt(0).toUpperCase() || "A";
}

function updateUI(){
  avatarEl.textContent = firstLetter(nameEl.value);
  const name = nameEl.value || "—";
  const email = emailEl.value || "—";
  const track = trackEl.value || "—";
  const bio = bioEl.value || "—";
  summaryEl.innerHTML = `
    <strong>${name}</strong><br/>
    <span style="color:var(--muted)">${email}</span><br/>
    Quan tâm: <span class="tag">${track}</span><br/><br/>
    ${bio}
  `;
}

$("#save").addEventListener("click", ()=>{
  const data = {
    name: nameEl.value.trim(),
    email: emailEl.value.trim(),
    track: trackEl.value,
    bio: bioEl.value.trim()
  };
  localStorage.setItem("profile_demo", JSON.stringify(data));
  updateUI();
  alert("Đã lưu hồ sơ (LocalStorage).");
});

$("#reset").addEventListener("click", ()=>{
  localStorage.removeItem("profile_demo");
  nameEl.value = emailEl.value = bioEl.value = "";
  trackEl.value = "";
  updateUI();
});

[nameEl, emailEl, trackEl, bioEl].forEach(el=>{
  el.addEventListener("input", updateUI);
});

document.addEventListener("DOMContentLoaded", ()=>{
  load();
  updateUI();
});
