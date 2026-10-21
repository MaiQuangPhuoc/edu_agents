(() => {
  "use strict";

  const $ = (selector) => document.querySelector(selector);
  const STUDENT_ID = "hs_002";
  let exams = [];

  const message = (text = "") => {
    $("#message").textContent = text;
  };

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = String(text);
    return node;
  }

  async function api(url, options) {
    const response = await fetch(url, options);
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.detail || `HTTP ${response.status}`);
    }
    return data;
  }

  function showDetail(visible) {
    $("#list-view").hidden = visible;
    $("#detail-view").hidden = !visible;
    window.scrollTo(0, 0);
  }

  async function load() {
    const refresh = $("#refresh");
    const list = $("#exam-list");
    refresh.disabled = true;
    message();

    try {
      const data = await api(
        `/api/ui/exams?student_id=${encodeURIComponent(STUDENT_ID)}`
      );
      exams = Array.isArray(data.exams) ? data.exams : [];
      $("#demo-banner").hidden = !data.demo;

      const subject = $("#subject");
      const previousSubject = subject.value;
      subject.replaceChildren(new Option("Tất cả môn", ""));
      [...new Set(exams.map((exam) => exam.subject).filter(Boolean))]
        .sort((a, b) => a.localeCompare(b, "vi"))
        .forEach((name) => subject.add(new Option(name, name)));
      subject.value = [...subject.options].some(
        (option) => option.value === previousSubject
      )
        ? previousSubject
        : "";

      render();
    } catch (error) {
      const detail = error instanceof Error ? error.message : String(error);
      message(detail);
      list.replaceChildren(
        element("div", "empty", `Không thể tải danh sách đề: ${detail}`)
      );
    } finally {
      refresh.disabled = false;
    }
  }

  function render() {
    const list = $("#exam-list");
    const subject = $("#subject").value;
    const status = $("#status-filter").value;
    const sort = $("#sort").value;
    const shown = exams.filter((exam) => {
      const matchesSubject = !subject || exam.subject === subject;
      const matchesStatus =
        !status ||
        (status === "done" ? exam.completed : !exam.completed);
      return matchesSubject && matchesStatus;
    });

    shown.sort((a, b) =>
      sort === "subject"
        ? a.subject.localeCompare(b.subject, "vi")
        : String(b.last_activity || b.created_at || "").localeCompare(
            String(a.last_activity || a.created_at || "")
          )
    );

    list.replaceChildren();
    if (!shown.length) {
      list.append(
        element(
          "div",
          "empty",
          "Chưa có bài kiểm tra phù hợp. Danh sách sẽ xuất hiện khi backend có đề kiểm tra được lưu."
        )
      );
      return;
    }

    shown.forEach((exam) => {
      const row = element("article", "exam-item");
      const body = element("div");
      body.append(
        element("div", "exam-name", exam.title),
        element(
          "div",
          "sub",
          `${exam.subject} · ${exam.question_count} câu · ${
            exam.completed ? "Đã làm" : "Chưa làm"
          }`
        )
      );

      const actions = element("div", "exam-actions");
      const badge = element(
        "span",
        `label ${exam.completed ? "done" : ""}`,
        exam.completed ? "Đã làm" : "Chưa làm"
      );
      const button = element(
        "button",
        "",
        exam.completed ? "Xem kết quả" : "Làm bài"
      );
      button.type = "button";
      button.addEventListener("click", () => openExam(exam.exam_id));
      actions.append(badge, button);
      row.append(body, actions);
      list.append(row);
    });
  }

  async function openExam(examId) {
    message();

    try {
      const data = await api(
        `/api/ui/exams/${encodeURIComponent(
          examId
        )}?student_id=${encodeURIComponent(STUDENT_ID)}`
      );
      const content = $("#exam-detail");
      content.replaceChildren(
        element("h2", "", data.title),
        element(
          "p",
          "sub",
          `${data.subject} · ${data.questions.length} câu hỏi`
        )
      );

      if (data.completed) {
        content.append(
          element(
            "div",
            "summary",
            `Điểm: ${data.result.correct}/${data.result.total} (${data.result.percent}%)`
          )
        );
        data.questions.forEach((question, index) => {
          const result = element("div", "question");
          result.append(
            element("strong", "", `Câu ${index + 1}: ${question.text}`),
            element(
              "div",
              "",
              `Bạn chọn: ${data.result.answers[question.id] || "Chưa chọn"}`
            ),
            element(
              "div",
              "",
              `Đáp án đúng: ${data.result.correct_answers[question.id]}`
            )
          );
          content.append(result);
        });
      } else {
        const form = element("form");
        form.id = "take-exam";
        data.questions.forEach((question, index) => {
          const field = element("fieldset", "question");
          field.append(
            element("strong", "", `Câu ${index + 1}: ${question.text}`)
          );

          Object.entries(question.options).forEach(([key, value]) => {
            const label = element("label", "answer");
            const radio = element("input");
            radio.type = "radio";
            radio.name = `q_${question.id}`;
            radio.value = key;
            label.append(radio, element("span", "", `${key}. ${value}`));
            field.append(label);
          });
          form.append(field);
        });

        const submit = element("button", "submit", "Nộp bài");
        submit.type = "submit";
        form.append(submit);
        form.addEventListener("submit", async (event) => {
          event.preventDefault();
          const answers = {};
          data.questions.forEach((question) => {
            const checked = form.querySelector(
              `input[name="q_${CSS.escape(question.id)}"]:checked`
            );
            if (checked) answers[question.id] = checked.value;
          });

          if (
            Object.keys(answers).length !== data.questions.length &&
            !confirm("Bạn chưa trả lời hết câu hỏi. Vẫn nộp bài?")
          ) {
            return;
          }

          submit.disabled = true;
          try {
            await api(
              `/api/ui/exams/${encodeURIComponent(
                examId
              )}/submit?student_id=${encodeURIComponent(STUDENT_ID)}`,
              {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ answers })
              }
            );
            await load();
            await openExam(examId);
          } catch (error) {
            message(error instanceof Error ? error.message : String(error));
            submit.disabled = false;
          }
        });
        content.append(form);
      }

      showDetail(true);
    } catch (error) {
      message(error instanceof Error ? error.message : String(error));
    }
  }

  $("#back").addEventListener("click", () => showDetail(false));
  $("#refresh").addEventListener("click", load);
  ["#subject", "#status-filter", "#sort"].forEach((selector) => {
    $(selector).addEventListener("change", render);
  });
  document.querySelectorAll(".soon").forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      message("Trang này đang phát triển.");
    });
  });

  load();
})();
