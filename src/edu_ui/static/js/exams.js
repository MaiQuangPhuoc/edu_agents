(() => {
  "use strict";

  const $ = (selector) => document.querySelector(selector);
  const STUDENT_ID = "hs_002";
  const state = {
    exams: [],
    active: null,
    questionIndex: 0,
    answers: {},
    submitting: false
  };
  const drafts = new Map();

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = String(text);
    return node;
  }

  function message(text = "", error = false) {
    const node = $("#message");
    node.textContent = text;
    node.classList.toggle("error-message", error);
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

  function renderStats() {
    const completed = state.exams.filter((exam) => exam.completed).length;
    $("#total-count").textContent = String(state.exams.length);
    $("#pending-count").textContent = String(state.exams.length - completed);
    $("#completed-count").textContent = String(completed);
    $("#library-caption").textContent = state.exams.length
      ? `${state.exams.length} bài luyện tập · Nội dung được lấy từ kho đề học tập`
      : "Các bài luyện tập sẽ xuất hiện tại đây khi có dữ liệu.";
  }

  function renderFilters() {
    const subject = $("#subject");
    const previous = subject.value;
    subject.replaceChildren(new Option("Tất cả môn", ""));
    [...new Set(state.exams.map((exam) => exam.subject).filter(Boolean))]
      .sort((first, second) => first.localeCompare(second, "vi"))
      .forEach((name) => subject.add(new Option(name, name)));
    subject.value = [...subject.options].some((option) => option.value === previous)
      ? previous
      : "";
  }

  function renderCards() {
    const list = $("#exam-list");
    const selectedSubject = $("#subject").value;
    const selectedStatus = $("#status-filter").value;
    const search = $("#search").value.trim().toLocaleLowerCase("vi");
    const sort = $("#sort").value;
    const visible = state.exams.filter((exam) => {
      const matchesSubject = !selectedSubject || exam.subject === selectedSubject;
      const matchesStatus = !selectedStatus ||
        (selectedStatus === "done" ? exam.completed : !exam.completed);
      const searchable = [
        exam.title,
        exam.subject,
        exam.chapter,
        ...(Array.isArray(exam.topics) ? exam.topics : [])
      ].filter(Boolean).join(" ").toLocaleLowerCase("vi");
      return matchesSubject && matchesStatus && searchable.includes(search);
    });

    visible.sort((first, second) => sort === "subject"
      ? String(first.subject || "").localeCompare(String(second.subject || ""), "vi")
      : String(second.last_activity || second.created_at || "")
        .localeCompare(String(first.last_activity || first.created_at || "")));

    list.replaceChildren();
    if (!visible.length) {
      const empty = element("div", "exam-empty");
      empty.append(
        element("span", "empty-mark", "—"),
        element("strong", "", state.exams.length
          ? "Không tìm thấy bài phù hợp"
          : "Chưa có bài luyện tập"),
        element("p", "", state.exams.length
          ? "Thử thay đổi từ khóa hoặc bộ lọc để xem thêm bài."
          : "Hãy kiểm tra dữ liệu đề trong thư viện bài tập.")
      );
      list.append(empty);
      return;
    }

    visible.forEach((exam) => {
      const index = state.exams.indexOf(exam);
      const row = element("article", "exam-row");
      row.append(element("span", "exam-row-index", String(index + 1).padStart(2, "0")));

      const copy = element("div", "exam-row-copy");
      copy.append(element("h3", "exam-row-title", exam.title || "Bài luyện tập"));
      const subtitle = element("p", "exam-row-subtitle");
      subtitle.append(
        element("span", "", exam.chapter || exam.subject || "Ôn tập tổng hợp"),
        element("span", "", `${Number(exam.question_count) || 0} câu hỏi`)
      );
      copy.append(subtitle);

      const status = element("span", `exam-status${exam.completed ? " is-complete" : ""}`,
        exam.completed ? "Đã hoàn thành" : "Chưa làm");
      const start = element("button", "start-exam-button",
        exam.completed ? "Xem kết quả" : "Bắt đầu");
      start.type = "button";
      start.addEventListener("click", () => openExam(exam.exam_id, start));

      row.append(copy, status, start);
      list.append(row);
    });
  }

  function renderReview(exam) {
    const content = $("#exam-detail");
    const result = exam.result || {};
    const answers = result.answers || {};
    const correctAnswers = result.correct_answers || {};
    const correct = Number(result.correct) || 0;
    const total = Number(result.total) || exam.questions.length;
    const percent = Number(result.percent) || 0;
    const intro = element("header", "result-heading");
    intro.append(
      element("p", "exam-eyebrow", `${exam.subject || "BÀI LUYỆN TẬP"} · KẾT QUẢ`),
      element("h1", "", exam.title),
      element("p", "", exam.chapter || "Xem lại từng câu và phần giải thích.")
    );

    const scoreCard = element("section", "result-score");
    scoreCard.append(element("div", "score-value", `${Math.round(percent)}%`));
    const scoreCopy = element("div");
    scoreCopy.append(
      element("strong", "", correct === total ? "Làm tốt lắm!" : "Bạn đã hoàn thành bài."),
      element("p", "", `Bạn trả lời đúng ${correct} trên ${total} câu. Xem lại lời giải để củng cố kiến thức.`)
    );
    scoreCard.append(scoreCopy);
    content.append(intro, scoreCard, element("h2", "review-heading", "Xem lại câu trả lời"));

    const reviewList = element("div", "review-list");
    exam.questions.forEach((question, index) => {
      const selected = answers[question.id];
      const answer = correctAnswers[question.id];
      const isCorrect = selected !== undefined && selected === answer;
      const questionCard = element("article", "review-card");
      const heading = element("div", "review-question-heading");
      const resultClass = selected === undefined
        ? ""
        : isCorrect ? "is-correct" : "is-wrong";
      heading.append(
        element("strong", "", `Câu ${index + 1} / ${exam.questions.length}`),
        element("span", `review-result ${resultClass}`,
          selected === undefined ? "Chưa trả lời" : isCorrect ? "Chính xác" : "Cần xem lại")
      );
      questionCard.append(heading, element("h3", "review-question", question.text));

      Object.entries(question.options || {}).forEach(([key, value]) => {
        const isAnswer = key === answer;
        const isSelected = key === selected;
        const option = element(
          "div",
          `review-option${isAnswer ? " is-correct" : ""}${isSelected && !isAnswer ? " is-wrong" : ""}`
        );
        option.append(element("span", "option-key", key), element("span", "option-copy", value));
        if (isAnswer) option.append(element("span", "option-state", "Đáp án đúng"));
        else if (isSelected) option.append(element("span", "option-state", "Bạn đã chọn"));
        questionCard.append(option);
      });

      if (question.explanation) {
        const explanation = element("div", "explanation");
        explanation.append(
          element("strong", "", "Giải thích"),
          element("p", "", question.explanation)
        );
        questionCard.append(explanation);
      }
      reviewList.append(questionCard);
    });
    content.append(reviewList);
  }

  function renderQuestionNavigation() {
    const navigation = $("#question-navigation");
    navigation.replaceChildren();
    state.active.questions.forEach((question, index) => {
      const button = element("button", "question-jump", String(index + 1));
      button.type = "button";
      button.setAttribute("aria-label", `Đến câu ${index + 1}`);
      if (index === state.questionIndex) button.setAttribute("aria-current", "step");
      if (Object.prototype.hasOwnProperty.call(state.answers, question.id)) {
        button.classList.add("is-answered");
      }
      button.addEventListener("click", () => {
        state.questionIndex = index;
        renderActiveQuestion();
      });
      navigation.append(button);
    });
  }

  function renderActiveQuestion() {
    const exam = state.active;
    const question = exam.questions[state.questionIndex];
    const total = exam.questions.length;
    const answered = exam.questions.filter((item) =>
      Object.prototype.hasOwnProperty.call(state.answers, item.id)).length;
    const index = state.questionIndex;
    const container = $("#current-question");
    container.replaceChildren();

    $("#question-progress-label").textContent = `Câu ${index + 1} / ${total}`;
    $("#question-progress-count").textContent = `${answered} / ${total} câu đã trả lời`;
    $("#question-progress-bar").style.width = `${total ? (answered / total) * 100 : 0}%`;
    $("#previous-question").disabled = index === 0;
    $("#next-question").hidden = index === total - 1;
    $("#submit-exam").hidden = index !== total - 1;

    const fieldset = element("fieldset", "active-question-card");
    fieldset.append(
      element("legend", "", `CÂU HỎI ${String(index + 1).padStart(2, "0")}`),
      element("h2", "active-question-text", question.text)
    );
    const options = element("div", "answer-options");
    Object.entries(question.options || {}).forEach(([key, value]) => {
      const isSelected = state.answers[question.id] === key;
      const label = element("label", `answer-option${isSelected ? " is-selected" : ""}`);
      const radio = element("input");
      radio.type = "radio";
      radio.name = "exam-answer";
      radio.value = key;
      radio.checked = isSelected;
      label.append(
        radio,
        element("span", "option-key", key),
        element("span", "option-copy", value)
      );
      radio.addEventListener("change", () => {
        state.answers[question.id] = key;
        drafts.set(exam.exam_id, { ...state.answers });
        options.querySelectorAll(".answer-option").forEach((option) => {
          const input = option.querySelector("input");
          option.classList.toggle("is-selected", input.checked);
        });
        const answeredCount = exam.questions.filter((item) =>
          Object.prototype.hasOwnProperty.call(state.answers, item.id)).length;
        $("#question-progress-count").textContent = `${answeredCount} / ${total} câu đã trả lời`;
        $("#question-progress-bar").style.width = `${(answeredCount / total) * 100}%`;
        $("#question-navigation").querySelectorAll(".question-jump")
          .forEach((jump, questionIndex) => {
            const currentQuestion = exam.questions[questionIndex];
            jump.classList.toggle(
              "is-answered",
              Object.prototype.hasOwnProperty.call(state.answers, currentQuestion.id)
            );
          });
      });
      options.append(label);
    });
    fieldset.append(options);
    container.append(fieldset);
    renderQuestionNavigation();
  }

  function renderTakeExam(exam) {
    const content = $("#exam-detail");
    const intro = element("header", "taking-heading");
    intro.append(
      element("p", "exam-eyebrow", `${exam.subject || "BÀI LUYỆN TẬP"} · ${exam.questions.length} CÂU HỎI`),
      element("h1", "", exam.title),
      element("p", "", exam.chapter || "Đọc kỹ từng câu hỏi và chọn phương án phù hợp nhất.")
    );

    const workspace = element("div", "exam-workspace");
    const main = element("section", "question-workspace");
    const progress = element("div", "question-progress");
    const progressTop = element("div", "progress-copy");
    const label = element("strong", "", "");
    label.id = "question-progress-label";
    const count = element("span", "", "");
    count.id = "question-progress-count";
    progressTop.append(label, count);
    const progressTrack = element("div", "progress-track");
    const progressBar = element("span");
    progressBar.id = "question-progress-bar";
    progressTrack.append(progressBar);
    progress.append(progressTop, progressTrack);

    const question = element("div");
    question.id = "current-question";
    main.append(progress, question);

    const controls = element("div", "question-controls");
    const previous = element("button", "previous-button", "← Câu trước");
    previous.id = "previous-question";
    previous.type = "button";
    previous.addEventListener("click", () => {
      state.questionIndex = Math.max(0, state.questionIndex - 1);
      renderActiveQuestion();
    });
    const actions = element("div");
    const next = element("button", "next-button", "Câu tiếp theo →");
    next.id = "next-question";
    next.type = "button";
    next.addEventListener("click", () => {
      state.questionIndex = Math.min(exam.questions.length - 1, state.questionIndex + 1);
      renderActiveQuestion();
    });
    const submit = element("button", "submit-button", "Nộp bài");
    submit.id = "submit-exam";
    submit.type = "button";
    submit.addEventListener("click", () => submitExam(exam.exam_id));
    actions.append(next, submit);
    controls.append(previous, actions);
    main.append(controls);

    const aside = element("aside", "question-aside");
    const navCard = element("section", "question-nav-card");
    navCard.append(
      element("h2", "", "Các câu hỏi"),
      element("p", "nav-hint", "Chọn số câu để chuyển nhanh.")
    );
    const nav = element("div", "question-navigation");
    nav.id = "question-navigation";
    navCard.append(nav);
    const legend = element("div", "nav-legend");
    legend.append(
      element("span", "legend-current", "Đang xem"),
      element("span", "legend-answered", "Đã trả lời")
    );
    navCard.append(legend);
    const note = element("div", "exam-aside-note");
    note.append(
      element("strong", "", "Câu trả lời được lưu tạm"),
      element("p", "", "Bạn có thể chuyển qua lại giữa các câu trước khi nộp bài.")
    );
    aside.append(navCard, note);
    workspace.append(main, aside);
    content.append(intro, workspace);
    renderActiveQuestion();
  }

  async function openExam(examId, button = null) {
    message();
    if (button) button.disabled = true;

    try {
      const exam = await api(
        `/api/ui/exams/${encodeURIComponent(examId)}?student_id=${encodeURIComponent(STUDENT_ID)}`
      );
      if (!Array.isArray(exam.questions) || !exam.questions.length) {
        throw new Error("Đề kiểm tra hiện chưa có câu hỏi.");
      }
      const content = $("#exam-detail");
      content.replaceChildren();
      state.active = exam;
      state.questionIndex = 0;
      state.answers = { ...(drafts.get(examId) || {}) };
      if (exam.completed) renderReview(exam);
      else renderTakeExam(exam);
      showDetail(true);
    } catch (error) {
      message(error instanceof Error ? error.message : String(error), true);
    } finally {
      if (button) button.disabled = false;
    }
  }

  async function submitExam(examId) {
    if (state.submitting || !state.active) return;
    const questions = state.active.questions;
    const answered = questions.filter((question) =>
      Object.prototype.hasOwnProperty.call(state.answers, question.id)).length;
    const unanswered = questions.length - answered;
    if (unanswered && !window.confirm(`Bạn còn ${unanswered} câu chưa trả lời. Bạn vẫn muốn nộp bài?`)) {
      return;
    }

    const submit = $("#submit-exam");
    state.submitting = true;
    submit.disabled = true;
    message();
    try {
      await api(
        `/api/ui/exams/${encodeURIComponent(examId)}/submit?student_id=${encodeURIComponent(STUDENT_ID)}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ answers: state.answers })
        }
      );
      drafts.delete(examId);
      await loadExams();
      await openExam(examId);
    } catch (error) {
      message(error instanceof Error ? error.message : String(error), true);
    } finally {
      state.submitting = false;
      const button = $("#submit-exam");
      if (button) button.disabled = false;
    }
  }

  async function loadExams() {
    const refresh = $("#refresh");
    const list = $("#exam-list");
    refresh.disabled = true;
    message();
    try {
      const data = await api(`/api/ui/exams?student_id=${encodeURIComponent(STUDENT_ID)}`);
      state.exams = Array.isArray(data.exams) ? data.exams : [];
      $("#demo-banner").hidden = !data.demo;
      renderStats();
      renderFilters();
      renderCards();
    } catch (error) {
      const detail = error instanceof Error ? error.message : String(error);
      message(`Không thể tải bài luyện tập: ${detail}`, true);
      list.replaceChildren(element("div", "exam-empty", "Không thể tải danh sách đề."));
    } finally {
      refresh.disabled = false;
    }
  }

  $("#back").addEventListener("click", () => {
    showDetail(false);
    message();
    renderCards();
  });
  $("#refresh").addEventListener("click", loadExams);
  ["#subject", "#status-filter", "#sort"].forEach((selector) => {
    $(selector).addEventListener("change", renderCards);
  });
  $("#search").addEventListener("input", renderCards);
  loadExams();
})();
