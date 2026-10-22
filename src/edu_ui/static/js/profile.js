(() => {
  "use strict";

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const form = $("#profile-form");
  const state = { profile: null, saving: false, loading: false };

  function status(text, kind = "") {
    const node = $("#profile-status");
    node.textContent = text;
    node.className = kind ? `is-${kind}` : "";
  }

  function localDateTime(value) {
    if (!value) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
    return date.toISOString().slice(0, 16);
  }

  function isoDateTime(value) {
    return value ? new Date(value).toISOString() : null;
  }

  function setValue(selector, value) {
    const input = $(selector);
    if (!input) return;
    if (input.type === "checkbox") {
      input.checked = Boolean(value);
    } else if (input.type === "datetime-local") {
      input.value = localDateTime(value);
    } else {
      input.value = value ?? "";
    }
  }

  function numberValue(input, fallback = null) {
    if (!input || input.value.trim() === "") return fallback;
    const value = Number(input.value);
    return Number.isFinite(value) ? value : fallback;
  }

  function lines(value) {
    return String(value || "")
      .split(/\r?\n/)
      .map((item) => item.trim())
      .filter(Boolean);
  }

  function setLines(input, values) {
    input.value = Array.isArray(values) ? values.join("\n") : "";
  }

  function cloneTemplate(id) {
    const template = document.getElementById(id);
    return template.content.firstElementChild.cloneNode(true);
  }

  function attachRemove(item) {
    $("[data-remove-item]", item).addEventListener("click", () => item.remove());
  }

  function addTopic(container, topic = {}) {
    const item = cloneTemplate("topic-template");
    for (const [key, value] of Object.entries(topic)) {
      const input = $(`[data-field="${key}"]`, item);
      if (input) {
        input.value = input.type === "datetime-local"
          ? localDateTime(value)
          : value ?? "";
      }
    }
    attachRemove(item);
    container.append(item);
  }

  function addAbility(ability = {}) {
    const item = cloneTemplate("ability-template");
    const subjectInput = $('[data-field="mon_hoc"]', item);
    const title = $("h3", item);
    const updateTitle = () => {
      title.textContent = subjectInput.value.trim() || "Năng lực môn học";
    };
    subjectInput.value = ability.mon_hoc || "";
    subjectInput.addEventListener("input", updateTitle);
    updateTitle();
    const score = $('[data-field="diem_hien_tai"]', item);
    score.value = ability.diem_hien_tai ?? "";
    $('[data-field="da_test_dau_vao"]', item).checked = Boolean(ability.da_test_dau_vao);
    setLines($('[data-list-field="diem_manh"]', item), ability.diem_manh);
    setLines($('[data-list-field="diem_yeu"]', item), ability.diem_yeu);
    const topics = $("[data-topic-list]", item);
    (ability.chu_de || []).forEach((topic) => addTopic(topics, topic));
    $("[data-add-topic]", item).addEventListener("click", () => addTopic(topics));
    attachRemove(item);
    $("#abilities-list").append(item);
  }

  function addGoal(goal = {}) {
    const item = cloneTemplate("goal-template");
    for (const [key, value] of Object.entries(goal)) {
      const input = $(`[data-field="${key}"]`, item);
      if (input) input.value = value ?? "";
    }
    setLines($('[data-list-field="dang_bai_can_giu"]', item), goal.dang_bai_can_giu);
    attachRemove(item);
    $("#goals-list").append(item);
  }

  function addAvailability(day = "", times = []) {
    const item = cloneTemplate("availability-template");
    $('[data-field="day"]', item).value = day;
    $('[data-field="times"]', item).value = Array.isArray(times) ? times.join("\n") : "";
    attachRemove(item);
    $("#availability-list").append(item);
  }

  function setOptionalBoolean(selector, value) {
    $(selector).value = value === null || value === undefined ? "" : String(value);
  }

  function populate(profile) {
    state.profile = profile;
    $("#student-id").value = profile.student_id;
    setValue("#full-name", profile.ca_nhan.ho_ten);
    setValue("#grade", profile.ca_nhan.khoi_lop);
    setLines($("#interests"), profile.ca_nhan.so_thich);
    setLines($("#activities"), profile.ca_nhan.hoat_dong_ngoai_khoa);

    $("#abilities-list").replaceChildren();
    (profile.nang_luc || []).forEach(addAbility);
    $("#goals-list").replaceChildren();
    (profile.muc_tieu || []).forEach(addGoal);

    setOptionalBoolean("#pref-documents", profile.so_thich_hoc.dung_tai_lieu);
    setOptionalBoolean("#pref-videos", profile.so_thich_hoc.dung_video);
    setOptionalBoolean("#pref-exercises", profile.so_thich_hoc.bai_tap_sau_buoi);
    setOptionalBoolean("#pref-summary", profile.so_thich_hoc.tom_tat_cuoi_buoi);
    setValue("#session-minutes", profile.so_thich_hoc.thoi_luong_buoi_phut);

    setValue("#sessions-per-week", profile.lich_hoc.so_buoi_tuan);
    $("#availability-list").replaceChildren();
    Object.entries(profile.lich_hoc.khung_gio_ranh || {})
      .forEach(([day, times]) => addAvailability(day, times));
    setLines($("#busy-schedule"), profile.lich_hoc.lich_ban);

    setValue("#completion-rate", profile.tien_do.ti_le_hoan_thanh);
    setValue("#streak-days", profile.tien_do.so_ngay_lien_tiep);
    setValue("#last-active", profile.tien_do.lan_hoat_dong_cuoi);
    setValue("#motivation-signal", profile.tien_do.tin_hieu_dong_luc);
    setValue("#profile-version", profile.version);
    setValue("#profile-updated", profile.updated_at
      ? new Date(profile.updated_at).toLocaleString("vi-VN")
      : "Chưa cập nhật");
  }

  async function api(url, options) {
    const response = await fetch(url, options);
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(typeof data.detail === "string" ? data.detail : `HTTP ${response.status}`);
    }
    return data;
  }

  function profileUrl(studentId) {
    return `/api/ui/students/${encodeURIComponent(studentId)}/profile`;
  }

  async function loadProfile() {
    if (state.loading || state.saving) return;
    const studentId = $("#student-id").value.trim();
    if (!/^[A-Za-z0-9_-]{1,80}$/.test(studentId)) {
      status("Mã học sinh chỉ được gồm chữ, số, dấu gạch ngang và gạch dưới.", "error");
      $("#student-id").focus();
      return;
    }
    state.loading = true;
    $("#load-profile").disabled = true;
    status("Đang tải hồ sơ…");
    try {
      const profile = await api(profileUrl(studentId));
      populate(profile);
      status("Đã tải hồ sơ học sinh.");
    } catch (error) {
      status(error instanceof Error ? error.message : String(error), "error");
    } finally {
      state.loading = false;
      $("#load-profile").disabled = false;
    }
  }

  function collectProfile() {
    const studentId = $("#student-id").value.trim();
    const khungGioRanh = {};
    $$("[data-availability-item]").forEach((item) => {
      const day = $('[data-field="day"]', item).value.trim();
      const times = lines($('[data-field="times"]', item).value);
      if (day && times.length) {
        khungGioRanh[day] = [...new Set([...(khungGioRanh[day] || []), ...times])];
      }
    });

    return {
      student_id: studentId,
      ca_nhan: {
        ho_ten: $("#full-name").value.trim(),
        khoi_lop: numberValue($("#grade"), 10),
        so_thich: lines($("#interests").value),
        hoat_dong_ngoai_khoa: lines($("#activities").value),
      },
      nang_luc: $$("[data-ability-item]").map((item) => ({
        mon_hoc: $('[data-field="mon_hoc"]', item).value.trim(),
        diem_hien_tai: numberValue($('[data-field="diem_hien_tai"]', item)),
        diem_manh: lines($('[data-list-field="diem_manh"]', item).value),
        diem_yeu: lines($('[data-list-field="diem_yeu"]', item).value),
        da_test_dau_vao: $('[data-field="da_test_dau_vao"]', item).checked,
        chu_de: $$("[data-topic-item]", item).map((topic) => ({
          chapter_id: $('[data-field="chapter_id"]', topic).value.trim(),
          lesson: $('[data-field="lesson"]', topic).value.trim(),
          muc_nam: numberValue($('[data-field="muc_nam"]', topic)),
          do_tin_cay: numberValue($('[data-field="do_tin_cay"]', topic), 0),
          nguon: $('[data-field="nguon"]', topic).value,
          cap_nhat: isoDateTime($('[data-field="cap_nhat"]', topic).value),
        })),
      })),
      muc_tieu: $$("[data-goal-item]").map((item) => ({
        mon_hoc: $('[data-field="mon_hoc"]', item).value.trim(),
        muc_tieu_diem: numberValue($('[data-field="muc_tieu_diem"]', item)),
        han_chot: $('[data-field="han_chot"]', item).value.trim() || null,
        ngay_ket_thuc: $('[data-field="ngay_ket_thuc"]', item).value || null,
        so_tuan_con_lai: numberValue($('[data-field="so_tuan_con_lai"]', item)),
        uu_tien: $('[data-field="uu_tien"]', item).value || null,
        dang_bai_can_giu: lines($('[data-list-field="dang_bai_can_giu"]', item).value),
      })),
      so_thich_hoc: {
        dung_tai_lieu: $("#pref-documents").value === "" ? null : $("#pref-documents").value === "true",
        dung_video: $("#pref-videos").value === "" ? null : $("#pref-videos").value === "true",
        bai_tap_sau_buoi: $("#pref-exercises").value === "" ? null : $("#pref-exercises").value === "true",
        tom_tat_cuoi_buoi: $("#pref-summary").value === "" ? null : $("#pref-summary").value === "true",
        thoi_luong_buoi_phut: numberValue($("#session-minutes")),
      },
      lich_hoc: {
        so_buoi_tuan: numberValue($("#sessions-per-week")),
        khung_gio_ranh: khungGioRanh,
        lich_ban: lines($("#busy-schedule").value),
      },
      tien_do: {
        ti_le_hoan_thanh: numberValue($("#completion-rate")),
        so_ngay_lien_tiep: numberValue($("#streak-days"), 0),
        lan_hoat_dong_cuoi: isoDateTime($("#last-active").value),
        tin_hieu_dong_luc: $("#motivation-signal").value.trim() || null,
      },
      version: state.profile?.version || 1,
      updated_at: state.profile?.updated_at || null,
    };
  }

  async function saveProfile(event) {
    event.preventDefault();
    if (state.saving || state.loading) return;
    if (!form.reportValidity()) return;
    const studentId = $("#student-id").value.trim();
    if (!/^[A-Za-z0-9_-]{1,80}$/.test(studentId)) {
      status("Mã học sinh chỉ được gồm chữ, số, dấu gạch ngang và gạch dưới.", "error");
      $("#student-id").focus();
      return;
    }
    const saveButtons = $$(".save-button");
    state.saving = true;
    saveButtons.forEach((button) => {
      button.disabled = true;
      button.dataset.previousText = button.textContent;
      button.textContent = "Đang lưu…";
    });
    status("Đang lưu hồ sơ…");
    try {
      const profile = await api(profileUrl(studentId), {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(collectProfile()),
      });
      populate(profile);
      status("Đã lưu đầy đủ hồ sơ học sinh.", "success");
    } catch (error) {
      status(error instanceof Error ? error.message : String(error), "error");
    } finally {
      state.saving = false;
      saveButtons.forEach((button) => {
        button.disabled = false;
        button.textContent = button.dataset.previousText || "Lưu hồ sơ";
        delete button.dataset.previousText;
      });
    }
  }

  $("#add-ability").addEventListener("click", () => addAbility());
  $("#add-goal").addEventListener("click", () => addGoal());
  $("#add-availability").addEventListener("click", () => addAvailability());
  $("#load-profile").addEventListener("click", loadProfile);
  form.addEventListener("submit", saveProfile);

  loadProfile();
})();
