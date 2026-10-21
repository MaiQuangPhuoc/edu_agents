(() => {
  "use strict";

  const $ = (selector) => document.querySelector(selector);
  const state = { roadmaps: [], connected: false, selectedRoadmap: null };
  let toastTimer;

  const element = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = String(text);
    return node;
  };

  function show(view) {
    ["#overview-view", "#roadmap-view", "#lesson-view"].forEach((selector) => {
      $(selector).hidden = selector !== view;
    });
    window.scrollTo(0, 0);
  }

  function toast(message) {
    const notice = $("#toast");
    notice.textContent = message;
    notice.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      notice.hidden = true;
    }, 3500);
  }

  function showEmpty(message) {
    const grid = $("#roadmap-grid");
    const empty = element("div", "roadmap-empty");
    empty.append(
      element("strong", "", "Chưa có lộ trình"),
      element("p", "", message)
    );
    grid.replaceChildren(empty);
  }

  function renderStats() {
    const roadmaps = state.roadmaps;
    const sessions = roadmaps.flatMap((roadmap) =>
      (Array.isArray(roadmap.phases) ? roadmap.phases : []).flatMap((phase) =>
        Array.isArray(phase.sessions) ? phase.sessions : []
      )
    );
    const completed = sessions.filter(
      (session) => session.status === "completed"
    ).length;
    const percent = sessions.length
      ? Math.round((completed / sessions.length) * 100)
      : 0;

    $("#roadmap-count").textContent = String(roadmaps.length);
    $("#roadmap-count-mark").textContent = "Planning Agent";
    $("#roadmap-bar").style.width = roadmaps.length ? "100%" : "0%";
    $("#roadmap-caption").textContent = roadmaps.length
      ? "Lộ trình được tải từ dữ liệu đã kết nối."
      : "Chưa có dữ liệu lộ trình.";

    $("#completed-count").textContent = String(completed);
    $("#session-count-mark").textContent = `${completed} / ${sessions.length}`;
    $("#completed-bar").style.width = `${percent}%`;
    $("#session-caption").textContent = `${completed} / ${sessions.length} buổi học`;

    $("#progress-percent").replaceChildren(
      document.createTextNode(String(percent)),
      element("span", "percent", "%")
    );
    $("#progress-bar").style.width = `${percent}%`;
  }

  function renderGrid() {
    const grid = $("#roadmap-grid");
    const subject = $("#subject-filter").value;
    const roadmaps = state.roadmaps.filter(
      (roadmap) => !subject || roadmap.subject === subject
    );
    grid.replaceChildren();

    if (!roadmaps.length) {
      showEmpty(
        state.roadmaps.length
          ? "Không có lộ trình cho môn học đã chọn."
          : "Khi có dữ liệu Planning Agent, lộ trình sẽ xuất hiện tại đây."
      );
      return;
    }

    roadmaps.forEach((roadmap, index) => {
      const phases = Array.isArray(roadmap.phases) ? roadmap.phases : [];
      const sessionCount = phases.reduce(
        (total, phase) =>
          total + (Array.isArray(phase.sessions) ? phase.sessions.length : 0),
        0
      );
      const card = element("button", "roadmap-card");
      card.type = "button";
      card.setAttribute(
        "aria-label",
        `Xem lộ trình ${roadmap.title || roadmap.subject || `số ${index + 1}`}`
      );

      const cover = element("div", "roadmap-cover");
      cover.append(
        element(
          "span",
          "cover-subject",
          roadmap.subject || "LỘ TRÌNH HỌC"
        ),
        element("span", "cover-num", String(index + 1).padStart(2, "0"))
      );
      const body = element("div", "card-body");
      body.append(
        element("h3", "", roadmap.title || roadmap.subject || "Lộ trình học"),
        element(
          "p",
          "",
          roadmap.description || roadmap.target
            ? [roadmap.description, roadmap.target && `Mục tiêu: ${roadmap.target}`]
                .filter(Boolean)
                .join(" · ")
            : "Chọn để xem các giai đoạn và buổi học."
        )
      );
      const footer = element("div", "card-foot");
      footer.append(
        element(
          "span",
          "",
          `${phases.length} giai đoạn · ${sessionCount} buổi học`
        ),
        element("b", "", "Xem lộ trình →")
      );
      body.append(footer);
      card.append(cover, body);
      card.addEventListener("click", () => openRoadmap(roadmap));
      grid.append(card);
    });
  }

  function renderObjectives(container, objectives) {
    if (!Array.isArray(objectives) || !objectives.length) return;
    container.append(element("h4", "detail-subheading", "Mục tiêu"));
    const list = element("ul", "objective-list");
    objectives.forEach((objective) => list.append(element("li", "", objective)));
    container.append(list);
  }

  function openRoadmap(roadmap) {
    state.selectedRoadmap = roadmap;
    const container = $("#roadmap-detail");
    const phases = Array.isArray(roadmap.phases) ? roadmap.phases : [];
    container.replaceChildren();

    const hero = element("section", "detail-hero");
    hero.append(
      element(
        "div",
        "detail-meta",
        `${roadmap.subject || "Lộ trình học"} · DỮ LIỆU ĐÃ KẾT NỐI`
      ),
      element("h1", "", roadmap.title || roadmap.subject || "Lộ trình học"),
      element(
        "p",
        "",
        [roadmap.description, roadmap.target && `Mục tiêu: ${roadmap.target}`]
          .filter(Boolean)
          .join(" · ") || "Các giai đoạn và buổi học trong lộ trình."
      )
    );
    container.append(hero);

    const layout = element("div", "detail-main");
    const phasePanel = element("section", "panel");
    phasePanel.append(
      element("div", "overline", "LỘ TRÌNH"),
      element("h2", "", "Các giai đoạn")
    );

    if (!phases.length) {
      phasePanel.append(
        element("p", "empty-copy", "Lộ trình này chưa có giai đoạn.")
      );
    }

    phases.forEach((phase, phaseIndex) => {
      const phaseNode = element("section", "phase");
      const heading = element("div", "phase-title");
      heading.append(
        element(
          "span",
          "phase-index",
          String(phaseIndex + 1).padStart(2, "0")
        ),
        element("h3", "", phase.title || `Giai đoạn ${phaseIndex + 1}`)
      );
      phaseNode.append(heading);
      if (phase.description) {
        phaseNode.append(element("p", "phase-description", phase.description));
      }
      renderObjectives(phaseNode, phase.objectives);

      const sessions = Array.isArray(phase.sessions) ? phase.sessions : [];
      if (!sessions.length) {
        phaseNode.append(
          element("p", "empty-copy", "Chưa có buổi học trong giai đoạn này.")
        );
      }

      sessions.forEach((session, sessionIndex) => {
        const button = element("button", "lesson-row");
        button.type = "button";
        const number = element(
          "span",
          "lesson-number",
          String(sessionIndex + 1).padStart(2, "0")
        );
        const info = element("span", "lesson-info");
        info.append(
          element("strong", "", session.title || `Buổi ${sessionIndex + 1}`),
          element(
            "small",
            "",
            [
              session.duration_minutes &&
                `${session.duration_minutes} phút`,
              session.status === "completed"
                ? "Đã hoàn thành"
                : "Chưa hoàn thành"
            ]
              .filter(Boolean)
              .join(" · ")
          )
        );
        button.append(number, info, element("span", "lesson-arrow", "→"));
        button.addEventListener("click", () =>
          openLesson(roadmap, phase, session, phaseIndex, sessionIndex)
        );
        phaseNode.append(button);
      });
      phasePanel.append(phaseNode);
    });

    const summary = element("aside", "panel");
    summary.append(
      element("div", "overline", "TỔNG QUAN"),
      element("h2", "", "Thông tin lộ trình")
    );
    const summaryItems = [
      ["Môn học", roadmap.subject || "—"],
      ["Giai đoạn", phases.length],
      [
        "Buổi học",
        phases.reduce(
          (total, phase) =>
            total + (Array.isArray(phase.sessions) ? phase.sessions.length : 0),
          0
        )
      ],
      ["Mục tiêu", roadmap.target || "—"]
    ];
    summaryItems.forEach(([label, value]) => {
      const row = element("div", "summary-item");
      row.append(element("span", "", label), element("b", "", value));
      summary.append(row);
    });

    layout.append(phasePanel, summary);
    container.append(layout);
    show("#roadmap-view");
  }

  function openLesson(roadmap, phase, session, phaseIndex, sessionIndex) {
    const container = $("#lesson-detail");
    container.replaceChildren();

    const hero = element("section", "detail-hero");
    hero.append(
      element(
        "div",
        "detail-meta",
        `${roadmap.subject || "Lộ trình"} · ${
          phase.title || `Giai đoạn ${phaseIndex + 1}`
        } · BUỔI ${sessionIndex + 1}`
      ),
      element("h1", "", session.title || `Buổi ${sessionIndex + 1}`),
      element(
        "p",
        "",
        [
          session.duration_minutes &&
            `Thời lượng: ${session.duration_minutes} phút`,
          session.status === "completed" ? "Đã hoàn thành" : "Chưa hoàn thành"
        ]
          .filter(Boolean)
          .join(" · ")
      )
    );
    container.append(hero);

    const layout = element("div", "lesson-layout");
    const content = element("article", "panel lesson-content");
    content.append(
      element("div", "overline", "NỘI DUNG BUỔI HỌC"),
      element("h2", "", session.title || `Buổi ${sessionIndex + 1}`)
    );
    if (session.description) {
      content.append(element("p", "lead", session.description));
    } else {
      content.append(
        element(
          "p",
          "lead",
          "Dữ liệu lộ trình hiện chưa cung cấp nội dung chi tiết cho buổi học này."
        )
      );
    }
    renderObjectives(content, session.objectives || phase.objectives);
    if (session.content) {
      content.append(element("div", "session-content", session.content));
    }

    const aside = element("aside", "panel");
    aside.append(element("div", "overline", "TỔNG QUAN"), element("h2", "", "Buổi học"));
    [
      ["Môn học", roadmap.subject || "—"],
      ["Giai đoạn", phase.title || `Giai đoạn ${phaseIndex + 1}`],
      [
        "Thời lượng",
        session.duration_minutes ? `${session.duration_minutes} phút` : "—"
      ],
      [
        "Trạng thái",
        session.status === "completed" ? "Đã hoàn thành" : "Chưa hoàn thành"
      ]
    ].forEach(([label, value]) => {
      const row = element("div", "summary-item");
      row.append(element("span", "", label), element("b", "", value));
      aside.append(row);
    });
    layout.append(content, aside);
    container.append(layout);
    show("#lesson-view");
  }

  async function loadRoadmaps() {
    const refresh = $("#refresh");
    refresh.disabled = true;
    $("#data-status").textContent = "ĐANG TẢI DỮ LIỆU";

    try {
      const response = await fetch("/api/ui/roadmaps", {
        headers: { Accept: "application/json" }
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || `HTTP ${response.status}`);
      }

      state.roadmaps = Array.isArray(data.roadmaps) ? data.roadmaps : [];
      state.connected = Boolean(data.connected);
      $("#data-status").textContent = data.demo
        ? "DỮ LIỆU MINH HỌA"
        : state.connected
          ? "DỮ LIỆU ĐÃ NẠP"
          : "CHƯA KẾT NỐI";
      $("#data-status").dataset.state = data.demo
        ? "demo"
        : state.connected
          ? "connected"
          : "disconnected";

      const filter = $("#subject-filter");
      const previousSubject = filter.value;
      filter.replaceChildren(new Option("Tất cả môn học", ""));
      [...new Set(state.roadmaps.map((roadmap) => roadmap.subject).filter(Boolean))]
        .sort((a, b) => a.localeCompare(b, "vi"))
        .forEach((subject) => filter.add(new Option(subject, subject)));
      filter.value = [...filter.options].some(
        (option) => option.value === previousSubject
      )
        ? previousSubject
        : "";

      $("#roadmap-caption-detail").textContent = state.connected
        ? data.demo
          ? "Đang dùng dữ liệu demo để xem trước giao diện."
          : "Chọn một lộ trình để xem các giai đoạn và buổi học."
        : "Chưa cấu hình nguồn dữ liệu lộ trình Planning Agent.";
      renderStats();
      renderGrid();
      if (!state.connected) {
        toast("Chưa có nguồn dữ liệu roadmap. Hãy cấu hình EDU_UI_ROADMAPS_JSON.");
      }
    } catch (error) {
      state.roadmaps = [];
      state.connected = false;
      $("#data-status").textContent = "LỖI KẾT NỐI";
      $("#data-status").dataset.state = "error";
      $("#roadmap-caption-detail").textContent =
        "Không thể tải dữ liệu lộ trình.";
      renderStats();
      showEmpty("Hãy kiểm tra backend và cấu hình nguồn dữ liệu lộ trình.");
      toast(
        `Không thể tải lộ trình: ${
          error instanceof Error ? error.message : String(error)
        }`
      );
    } finally {
      refresh.disabled = false;
    }
  }

  $("#subject-filter").addEventListener("change", renderGrid);
  $("#refresh").addEventListener("click", loadRoadmaps);
  $("#back-to-overview").addEventListener("click", () => show("#overview-view"));
  $("#back-to-roadmap").addEventListener("click", () => {
    if (state.selectedRoadmap) openRoadmap(state.selectedRoadmap);
  });
  loadRoadmaps();
})();
