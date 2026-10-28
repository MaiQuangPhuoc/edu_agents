(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const STUDENT_ID = 'hs_002';
  const state = {exams: [], active: null, answers: {}, reminders: 0, submitting: false, request: 0};
  const memoryDrafts = new Map();
  const element = (tag, cls, text) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = String(text);
    return node;
  };
  const reducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function message(text = '', error = false) {
    $('#message').textContent = text;
    $('#message').classList.toggle('error-message', error);
  }
  async function api(url, options) {
    const response = await fetch(url, options);
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : `HTTP ${response.status}`);
    return data;
  }
  const draftKey = id => `eduagent-exam:${STUDENT_ID}:${id}`;
  function readDraft(id) {
    try {return JSON.parse(sessionStorage.getItem(draftKey(id)) || 'null') || memoryDrafts.get(id) || {};}
    catch {return memoryDrafts.get(id) || {};}
  }
  function saveDraft() {
    if (!state.active) return;
    const draft = {answers: {...state.answers}, reminders: state.reminders};
    memoryDrafts.set(state.active.exam_id, draft);
    try {sessionStorage.setItem(draftKey(state.active.exam_id), JSON.stringify(draft));} catch {}
  }
  function forgetDraft(id) {
    memoryDrafts.delete(id);
    try {sessionStorage.removeItem(draftKey(id));} catch {}
  }

  // Protect LaTeX before Markdown parses backslashes, underscores and asterisks.
  // HTML is sanitized BEFORE inserting KaTeX's own generated math markup.
  function rich(tag, cls, value) {
    const node = element(tag, `${cls || ''} rich-text`.trim());
    const text = String(value ?? '');
    if (!window.marked || !window.DOMPurify) {
      node.textContent = text;
      $('#render-notice').hidden = false;
      return node;
    }
    const maths = [];
    const nonce = `EDUMATH${Math.random().toString(36).slice(2)}X`;
    const protectedText = text.replace(/\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|(?<!\\)\$(?!\$)(?:\\.|[^$\n])+?(?<!\\)\$/g, raw => {
      const block = raw.startsWith('$$') || raw.startsWith('\\[');
      const trim = raw.startsWith('$') && !block ? 1 : 2;
      const key = `${nonce}${maths.length}END`;
      maths.push({raw, body: raw.slice(trim, -trim), block});
      return key;
    });
    node.innerHTML = DOMPurify.sanitize(marked.parse(protectedText, {gfm: true, breaks: true}), {
      USE_PROFILES: {html: true},
      FORBID_TAGS: ['img', 'style', 'input', 'button', 'iframe', 'form'],
      FORBID_ATTR: ['style', 'id']
    });
    const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
    const texts = [];
    while (walker.nextNode()) texts.push(walker.currentNode);
    const pattern = new RegExp(`${nonce}(\\d+)END`, 'g');
    for (const textNode of texts) {
      const original = textNode.nodeValue;
      if (!original.includes(nonce)) continue;
      const fragment = document.createDocumentFragment();
      let offset = 0;
      original.replace(pattern, (token, index, position) => {
        fragment.append(document.createTextNode(original.slice(offset, position)));
        const math = maths[Number(index)];
        const span = element('span', math.block ? 'math-block' : 'math-inline');
        if (window.katex && !textNode.parentElement.closest('code,pre')) {
          try {katex.render(math.body, span, {displayMode: math.block, throwOnError: false, trust: false, strict: 'warn', maxExpand: 1000});}
          catch {span.textContent = math.raw;}
        } else {
          span.textContent = math.raw;
          if (!window.katex) $('#render-notice').hidden = false;
        }
        fragment.append(span);
        offset = position + token.length;
        return token;
      });
      fragment.append(document.createTextNode(original.slice(offset)));
      textNode.replaceWith(fragment);
    }
    node.querySelectorAll('a').forEach(link => {link.target = '_blank'; link.rel = 'noopener noreferrer';});
    return node;
  }
  function showDetail(visible) {
    $('#list-view').hidden = visible;
    $('#detail-view').hidden = !visible;
    window.scrollTo({top: 0, behavior: 'instant'});
  }
  function setExamURL(exam = null) {
    const url = new URL(location.href);
    url.searchParams.delete('exam'); url.searchParams.delete('view');
    if (exam) {url.searchParams.set('exam', exam.exam_id); url.searchParams.set('view', exam.completed ? 'result' : 'take');}
    if (url.href !== location.href) history.pushState({}, '', url);
  }
  function renderStats() {
    const done = state.exams.filter(e => e.completed).length;
    $('#total-count').textContent = state.exams.length;
    $('#pending-count').textContent = state.exams.length - done;
    $('#completed-count').textContent = done;
  }
  function renderFilters() {
    const subject = $('#subject'), previous = subject.value;
    subject.replaceChildren(new Option('Tất cả môn', ''));
    [...new Set(state.exams.map(e => e.subject))].sort((a,b) => a.localeCompare(b, 'vi'))
      .forEach(name => subject.add(new Option(name, name)));
    subject.value = [...subject.options].some(o => o.value === previous) ? previous : '';
  }
  function examCard(exam, index) {
    const row = element('article', 'exam-row');
    row.append(element('span', 'exam-row-index', String(index + 1).padStart(2, '0')));
    const copy = element('div', 'exam-row-copy');
    copy.append(element('h3', 'exam-row-title', exam.title));
    const chapter = element('p', 'exam-row-chapter', exam.chapter || 'Ôn tập tổng hợp');
    chapter.title = chapter.textContent;
    copy.append(chapter);
    row.append(copy);
    const footer = element('div', 'exam-card-footer');
    footer.append(element('span', 'exam-question-count', `${exam.question_count} câu hỏi`));
    footer.append(element('span', `exam-status${exam.completed ? ' is-complete' : ''}`, exam.completed ? 'Đã hoàn thành' : 'Chưa làm'));
    const button = element('button', 'start-exam-button', exam.completed ? 'Xem kết quả ↗' : 'Bắt đầu →');
    button.type = 'button';
    button.addEventListener('click', () => openExam(exam.exam_id, button));
    row.append(footer, button);
    return row;
  }
  function renderCards() {
    const list = $('#exam-list'), subject = $('#subject').value, status = $('#status-filter').value;
    const search = $('#search').value.trim().toLocaleLowerCase('vi');
    const visible = state.exams.filter(exam => (!subject || exam.subject === subject)
      && (!status || (status === 'done' ? exam.completed : !exam.completed))
      && [exam.title, exam.subject, exam.chapter, ...(exam.topics || [])].join(' ').toLocaleLowerCase('vi').includes(search));
    visible.sort((a,b) => $('#sort').value === 'subject'
      ? a.subject.localeCompare(b.subject, 'vi') || a.title.localeCompare(b.title, 'vi', {numeric: true})
      : String(b.last_activity || b.created_at || '').localeCompare(String(a.last_activity || a.created_at || '')));
    list.querySelectorAll('.subject-rail').forEach(rail => rail._observer?.disconnect());
    list.replaceChildren();
    $('#library-caption').textContent = `${visible.length} / ${state.exams.length} đề · Chia theo môn học`;
    if (!visible.length) {
      const empty = element('div', 'exam-empty');
      empty.append(element('strong', '', state.exams.length ? 'Không có đề phù hợp' : 'Chưa có đề kiểm tra'));
      empty.append(element('p', '', state.exams.length ? 'Thử thay đổi từ khóa hoặc bộ lọc.' : 'Thêm JSON vào src/test_exam, ví dụ toan_de_01.json hoặc lich_su_de_01.json.'));
      list.append(empty); return;
    }
    const groups = new Map();
    visible.forEach(exam => {if (!groups.has(exam.subject)) groups.set(exam.subject, []); groups.get(exam.subject).push(exam);});
    let groupIndex = 0;
    for (const [name, exams] of groups) {
      const section = element('section', 'subject-section');
      const headingId = `subject-heading-${groupIndex}`, railId = `subject-rail-${groupIndex++}`;
      section.setAttribute('aria-labelledby', headingId);
      const heading = element('header', 'subject-heading');
      const intro = element('div', 'subject-intro');
      const title = element('h3', '', name); title.id = headingId;
      intro.append(title, element('span', 'subject-count', `${exams.length} đề`));
      const actions = element('div', 'subject-actions');
      const prev = element('button', 'rail-arrow', '←'), next = element('button', 'rail-arrow', '→');
      for (const [button, label] of [[prev, 'Xem đề trước'], [next, 'Xem đề tiếp']]) {
        button.type = 'button'; button.setAttribute('aria-label', `${label} môn ${name}`); button.setAttribute('aria-controls', railId);
      }
      actions.append(prev, next); heading.append(intro, actions);
      const rail = element('div', 'subject-rail'); rail.id = railId; rail.tabIndex = 0;
      rail.setAttribute('role', 'region'); rail.setAttribute('aria-label', `Danh sách đề ${name}, cuộn ngang để xem thêm`);
      exams.forEach((exam,index) => rail.append(examCard(exam,index)));
      const update = () => {prev.disabled = rail.scrollLeft < 2; next.disabled = rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 2;};
      const scroll = direction => rail.scrollBy({left: direction * rail.clientWidth, behavior: reducedMotion() ? 'instant' : 'smooth'});
      prev.addEventListener('click', () => scroll(-1)); next.addEventListener('click', () => scroll(1));
      rail.addEventListener('scroll', update, {passive: true});
      rail.addEventListener('keydown', event => {
        if (event.target !== rail || !['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
        event.preventDefault(); scroll(event.key === 'ArrowRight' ? 1 : -1);
      });
      section.append(heading, rail); list.append(section);
      requestAnimationFrame(update);
      if (window.ResizeObserver) {const observer = new ResizeObserver(update); observer.observe(rail); rail._observer = observer;}
    }
  }
  function jumpTo(index, focus = true) {
    const card = document.getElementById(`taking-question-${index + 1}`);
    if (!card) return;
    card.scrollIntoView({behavior: reducedMotion() ? 'instant' : 'smooth', block: 'center'});
    if (focus) card.focus({preventScroll: true});
  }
  function renderTakeExam(exam) {
    const content = $('#exam-detail');
    const intro = element('header', 'taking-heading');
    intro.append(element('p', 'exam-eyebrow', `${exam.subject} · LUYỆN TẬP`), element('h1', '', exam.title), element('p', '', exam.chapter));
    const layout = element('div', 'exam-workspace');
    const workspace = element('section', 'question-workspace');
    const progress = element('div', 'question-progress');
    const copy = element('div', 'progress-copy');
    const count = element('span'); count.id = 'question-progress-count';
    copy.append(element('strong', '', 'Tiến độ làm bài'), count);
    const track = element('div', 'progress-track');
    const bar = element('span'); bar.id = 'question-progress-bar'; track.append(bar); progress.append(copy, track);
    const questions = element('div', 'taking-question-list'); questions.id = 'taking-question-list';
    exam.questions.forEach((question, index) => {
      const card = element('article', 'taking-question-card'); card.id = `taking-question-${index + 1}`;
      card.tabIndex = -1; card.setAttribute('aria-labelledby', `question-title-${index + 1}`);
      const heading = element('div', 'taking-question-heading');
      heading.append(element('span', 'question-number', `Câu ${String(index + 1).padStart(2, '0')}`), element('span', 'question-state', 'Chưa trả lời'));
      const text = rich('div', 'taking-question-text', question.text); text.id = `question-title-${index + 1}`;
      const options = element('div', 'answer-options'); options.setAttribute('role', 'group'); options.setAttribute('aria-labelledby', text.id);
      Object.entries(question.options).forEach(([key, value]) => {
        const label = element('label', 'answer-option');
        const radio = element('input'); radio.type = 'radio'; radio.name = `exam-answer-${question.id}`; radio.value = key;
        radio.checked = state.answers[question.id] === key; label.classList.toggle('is-selected', radio.checked);
        radio.addEventListener('change', () => {
          state.answers[question.id] = key; saveDraft();
          options.querySelectorAll('.answer-option').forEach(option => option.classList.toggle('is-selected', option.querySelector('input').checked));
          updateAnswerProgress(exam);
        });
        label.append(radio, element('span', 'option-key', key), rich('span', 'option-copy', value)); options.append(label);
      });
      card.append(heading, text, options); questions.append(card);
    });
    const controls = element('div', 'taking-controls');
    const warning = element('p', 'submit-hint', 'Bạn được nhắc tới câu còn trống tối đa 3 lần trước khi nộp.');
    warning.id = 'submit-warning'; warning.setAttribute('role', 'status'); warning.setAttribute('aria-live', 'polite');
    const submit = element('button', 'submit-button', 'Nộp bài →'); submit.id = 'submit-exam'; submit.type = 'button';
    submit.addEventListener('click', () => submitExam(exam.exam_id));
    controls.append(warning, submit); workspace.append(progress, questions, controls);
    const aside = element('aside', 'question-nav-card');
    aside.append(element('span', 'exam-eyebrow', 'BẢNG CÂU HỎI'), element('h2', '', `${exam.questions.length} câu hỏi`), element('p', 'nav-hint', 'Chọn số câu để chuyển nhanh.'));
    const navigation = element('nav', 'question-navigation'); navigation.setAttribute('aria-label', 'Chuyển đến câu hỏi');
    exam.questions.forEach((q,index) => {
      const button = element('button', 'question-jump', index + 1); button.type = 'button';
      button.dataset.question = q.id; button.addEventListener('click', () => jumpTo(index)); navigation.append(button);
    });
    aside.append(navigation, element('p', 'nav-hint', 'Ô xanh: đã trả lời · Ô hồng: còn trống sau khi kiểm tra.'));
    layout.append(workspace, aside); content.append(intro, layout); updateAnswerProgress(exam);
  }
  function updateAnswerProgress(exam) {
    const answered = exam.questions.filter(q => Object.hasOwn(state.answers, q.id)).length;
    $('#question-progress-count').textContent = `${answered} / ${exam.questions.length} câu đã trả lời`;
    $('#question-progress-bar').style.width = `${answered / exam.questions.length * 100}%`;
    $('#taking-question-list').querySelectorAll('.taking-question-card').forEach((card,index) => {
      const done = Object.hasOwn(state.answers, exam.questions[index].id);
      card.classList.toggle('is-unanswered', state.reminders > 0 && !done);
      card.querySelector('.taking-question-heading').classList.toggle('is-answered', done);
      card.querySelector('.question-state').textContent = done ? 'Đã trả lời' : 'Chưa trả lời';
    });
    document.querySelectorAll('.question-jump').forEach(button => {
      const done = Object.hasOwn(state.answers, button.dataset.question);
      button.classList.toggle('is-answered', done); button.classList.toggle('is-missing', state.reminders > 0 && !done);
      button.setAttribute('aria-label', `Câu ${button.textContent}: ${done ? 'đã trả lời' : 'chưa trả lời'}`);
    });
  }
  function renderReview(exam) {
    const content = $('#exam-detail'), result = exam.result, selected = result.answers || {}, correctAnswers = result.correct_answers || {};
    const blank = exam.questions.filter(q => !Object.hasOwn(selected, q.id)).length;
    const wrong = result.total - result.correct - blank;
    const heading = element('header', 'result-heading');
    heading.append(element('p', 'exam-eyebrow', `${exam.subject} · KẾT QUẢ BÀI LÀM`), element('h1', '', exam.title), element('p', '', 'Đối chiếu đáp án và xem lời giải cho từng câu.'));
    const summary = element('section', 'result-summary');
    const score = element('div', 'result-score');
    const ring = element('div', 'score-ring'); ring.style.setProperty('--score', `${result.percent}%`);
    ring.append(element('strong', '', `${(result.correct / result.total * 10).toFixed(1)}`), element('span', '', '/ 10 điểm'));
    const copy = element('div'); copy.append(element('h2', '', result.correct === result.total ? 'Hoàn thành xuất sắc!' : 'Bạn đã hoàn thành bài kiểm tra'), element('p', '', `${result.correct} / ${result.total} câu đúng · ${result.percent}%`));
    score.append(ring, copy); summary.append(score);
    const stats = element('div', 'result-breakdown');
    [[result.correct, 'Trả lời đúng', 'correct'], [wrong, 'Trả lời sai', 'wrong'], [blank, 'Chưa trả lời', 'blank']].forEach(([count,label,cls]) => {
      const item = element('div', cls); item.append(element('strong', '', count), element('span', '', label)); stats.append(item);
    }); summary.append(stats);
    const toolbar = element('div', 'review-toolbar'); toolbar.append(element('h2', '', 'Xem lại từng câu'));
    const filter = element('select'); filter.setAttribute('aria-label', 'Lọc kết quả câu hỏi');
    [['all','Tất cả câu'],['wrong','Câu trả lời sai'],['blank','Câu chưa trả lời'],['correct','Câu trả lời đúng']].forEach(([value,text]) => filter.add(new Option(text,value)));
    toolbar.append(filter);
    const list = element('div', 'review-list');
    exam.questions.forEach((question,index) => {
      const answer = correctAnswers[question.id], chosen = selected[question.id];
      const type = chosen === undefined ? 'blank' : chosen === answer ? 'correct' : 'wrong';
      const card = element('article', `review-card review-${type}`); card.dataset.result = type;
      const top = element('div', 'review-question-heading');
      top.append(element('strong', '', `Câu ${String(index+1).padStart(2,'0')}`), element('span', `review-result is-${type}`, type === 'blank' ? 'Chưa trả lời' : type === 'correct' ? 'Chính xác' : 'Chưa chính xác'));
      card.append(top, rich('div','review-question',question.text));
      const options = element('div', 'review-options');
      Object.entries(question.options).forEach(([key,value]) => {
        const option = element('div', `review-option${key === answer ? ' is-correct' : key === chosen ? ' is-wrong' : ''}`);
        const body = element('div', 'review-option-body'); body.append(rich('div','option-copy',value));
        if (key === answer || key === chosen) body.append(element('span','option-state', key === answer ? (key === chosen ? '✓ Bạn chọn · Đáp án đúng' : '✓ Đáp án đúng') : '× Bạn đã chọn'));
        option.append(element('span','option-key',key),body); options.append(option);
      });
      card.append(options);
      if (question.explanation) {
        const details = element('details', 'explanation'); details.open = type !== 'correct';
        details.append(element('summary', '', 'Lời giải chi tiết'), rich('div','explanation-copy',question.explanation)); card.append(details);
      }
      list.append(card);
    });
    const empty = element('p', 'review-empty', 'Không có câu thuộc nhóm này.'); empty.hidden = true;
    filter.addEventListener('change', () => {
      let count = 0;
      list.querySelectorAll('.review-card').forEach(card => {card.hidden = filter.value !== 'all' && card.dataset.result !== filter.value; if (!card.hidden) count++;});
      empty.hidden = count > 0;
    });
    content.append(heading, summary, toolbar, list, empty);
  }
  async function openExam(id, button = null, updateURL = true) {
    const request = ++state.request;
    message(); if (button) button.disabled = true;
    try {
      const exam = await api(`/api/ui/exams/${encodeURIComponent(id)}?student_id=${STUDENT_ID}`);
      if (request !== state.request) return;
      if (!Array.isArray(exam.questions) || !exam.questions.length) throw new Error('Đề chưa có câu hỏi.');
      state.active = exam; state.answers = {}; state.reminders = 0;
      if (!exam.completed) {
        const draft = readDraft(id);
        exam.questions.forEach(q => {if (Object.hasOwn(q.options,draft.answers?.[q.id])) state.answers[q.id] = draft.answers[q.id];});
        state.reminders = Math.max(0, Math.min(3, Number(draft.reminders) || 0));
      }
      $('#exam-detail').replaceChildren();
      if (exam.completed) renderReview(exam); else renderTakeExam(exam);
      showDetail(true); if (updateURL) setExamURL(exam);
      $('#detail-context').textContent = exam.completed ? 'KẾT QUẢ BÀI KIỂM TRA' : 'ĐANG LÀM BÀI';
    } catch (error) {if (request === state.request) message(error.message, true);}
    finally {if (button) button.disabled = false;}
  }
  async function submitExam(id) {
    if (state.submitting || !state.active || state.active.exam_id !== id) return;
    const exam = state.active;
    const missing = exam.questions.map((q,index) => ({q,index})).filter(({q}) => !Object.hasOwn(state.answers,q.id));
    if (missing.length && state.reminders < 3) {
      const target = missing[state.reminders % missing.length];
      state.reminders++; saveDraft(); updateAnswerProgress(exam);
      $('#submit-warning').textContent = `Còn ${missing.length} câu chưa trả lời · Nhắc ${state.reminders}/3. ${state.reminders === 3 ? 'Lần bấm Nộp bài tiếp theo sẽ nộp cả các câu còn trống.' : 'Hãy kiểm tra câu được đánh dấu.'}`;
      jumpTo(target.index); return;
    }
    state.submitting = true;
    const button = $('#submit-exam'); button.disabled = true; button.textContent = 'Đang chấm bài…';
    // Snapshot prevents a late radio change from changing the submitted answers.
    const answers = {...state.answers};
    $('#taking-question-list').querySelectorAll('input').forEach(input => input.disabled = true);
    try {
      const response = await api(`/api/ui/exams/${encodeURIComponent(id)}/submit?student_id=${STUDENT_ID}`, {
        method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({answers})
      });
      forgetDraft(id);
      const completed = {...exam, completed:true, result:response.result};
      const old = state.exams.find(e => e.exam_id === id);
      if (old) {old.completed = true; old.last_activity = response.result.submitted_at;}
      if (state.active?.exam_id === id && !$('#detail-view').hidden) {
        state.active = completed; $('#exam-detail').replaceChildren();
        renderReview(completed); showDetail(true); setExamURL(completed);
        $('#detail-context').textContent = 'KẾT QUẢ BÀI KIỂM TRA';
        // Fetch the submitted exam so explanations are included only after grading.
        await openExam(id);
      }
      renderStats(); renderCards();
    } catch (error) {
      message(error.message, true);
      if (state.active?.exam_id === id && $('#submit-exam')) {
        $('#submit-exam').disabled = false; $('#submit-exam').textContent = 'Nộp bài →';
        $('#taking-question-list').querySelectorAll('input').forEach(input => input.disabled = false);
      }
    } finally {state.submitting = false;}
  }
  async function loadExams() {
    $('#refresh').disabled = true; message();
    try {
      const data = await api(`/api/ui/exams?student_id=${STUDENT_ID}`);
      state.exams = Array.isArray(data.exams) ? data.exams : [];
      $('#demo-banner').hidden = true;
      renderStats(); renderFilters(); renderCards();
    } catch (error) {message(`Không tải được đề: ${error.message}`,true);}
    finally {$('#refresh').disabled = false;}
  }
  $('#back').addEventListener('click', () => {state.request++; state.active = null; showDetail(false);setExamURL();message();renderCards();});
  $('#refresh').addEventListener('click',loadExams);
  ['#subject','#status-filter','#sort'].forEach(id => $(id).addEventListener('change',renderCards));
  $('#search').addEventListener('input',renderCards);
  window.addEventListener('popstate', () => {
    const id = new URL(location.href).searchParams.get('exam');
    if (id) openExam(id,null,false);
    else {state.request++;state.active=null;showDetail(false);message();renderCards();}
  });
  loadExams().then(() => {const id = new URL(location.href).searchParams.get('exam');if (id) openExam(id,null,false);});
})();
