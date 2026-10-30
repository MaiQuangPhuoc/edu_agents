(() => {
  'use strict';
  const F = window.EduFlow;
  const bootNotice = document.querySelector('#study-message');
  if (!F) {bootNotice.textContent = 'Thiếu thư viện workflow.js. Cập nhật đủ file rồi nhấn Ctrl+F5.'; bootNotice.className = 'study-error'; return;}
  document.documentElement.dataset.studyLoaded = 'true';
  const {element: el, rich} = F;
  const root = document.querySelector('#study-root'), notice = document.querySelector('#study-message');
  const params = new URLSearchParams(location.search);
  let sid = params.get('session'), revision = 0, busy = false;
  const view = params.get('view') || 'path';
  const url = tail => `/api/ui/workflows/${encodeURIComponent(sid)}/${tail}`;
  function status(text, error = false) {notice.textContent = text; notice.className = error ? 'study-error' : 'study-muted';}
  function button(text, click, cls = 'wf-primary') {const b = el('button', cls, text); b.type = 'button'; b.addEventListener('click', click); return b;}
  function backLink() {const a = el('a', 'study-no-print wf-primary', '← Về cuộc trò chuyện'); a.href = `/?workflow=${encodeURIComponent(sid)}`; return a;}
  function header(kicker, title, subtitle) {
    const h = el('header', 'study-top'), copy = el('div');
    copy.append(el('p', 'study-kicker', kicker), el('h1', '', title), el('p', 'study-muted', subtitle));
    h.append(copy, backLink()); root.append(h); return h;
  }
  function rememberAnswer(text) {
    try {
      const all = JSON.parse(localStorage.getItem('eduagent-chat-history') || '[]');
      const c = all.find(x => x.session_id === sid);
      if (c) {c.messages.push({role: 'user', content: text}); localStorage.setItem('eduagent-chat-history', JSON.stringify(all));}
    } catch {}
  }
  async function waitJob(jid, container) {
    const p = el('div'); container.append(p);
    return await F.poll(jid, steps => F.progress(p, steps));
  }
  async function entry() {
    status('Đang lấy câu hỏi bài kiểm tra đầu vào…');
    const data = await F.api(url('entry-test')); revision = data.revision;
    if (!Array.isArray(data.questions) || !data.questions.length) throw new Error('Bài kiểm tra chưa có câu hỏi để hiển thị. Kiểm tra entry_test.py trên server.');
    status(''); root.replaceChildren();
    header('KIỂM TRA ĐẦU VÀO', data.subject || 'Bài kiểm tra đầu vào', `${data.questions.length} câu · Kết quả dùng để điều chỉnh lộ trình học của bạn.`);
    const draftKey = `eduagent-entry-${sid}-${revision}`;
    let answers = {}; try {answers = JSON.parse(localStorage.getItem(draftKey) || '{}');} catch {}
    const nav = el('nav', 'study-nav'), form = el('form'); root.append(nav, form);
    const counts = el('span', 'study-muted');
    function update() {
      const n = data.questions.filter(q => q.options[answers[String(q.no)]] !== undefined).length;
      counts.textContent = `Đã trả lời ${n}/${data.questions.length} câu`;
      nav.querySelectorAll('button').forEach(b => b.classList.toggle('answered', Boolean(answers[b.dataset.no])));
      try {localStorage.setItem(draftKey, JSON.stringify(answers));} catch {}
    }
    data.questions.forEach(q => {
      const card = el('section', 'study-card'); card.id = `question-${q.no}`;
      const jump = button(String(q.no), () => card.scrollIntoView({behavior: 'smooth', block: 'center'}), ''); jump.dataset.no = q.no; nav.append(jump);
      card.append(el('h3', '', `Câu ${q.no}`), rich('div', '', q.question));
      const choices = el('div', 'study-answers');
      Object.entries(q.options).forEach(([key, value]) => {
        const l = el('label', 'study-option'), input = el('input'); input.type = 'radio'; input.name = `q-${q.no}`; input.value = key; input.checked = answers[String(q.no)] === key;
        input.addEventListener('change', () => {answers[String(q.no)] = key; status(''); update();});
        l.append(input, rich('span', '', `**${key}.** ${value}`)); choices.append(l);
      }); card.append(choices); form.append(card);
    });
    const bar = el('div', 'study-submit'), submit = el('button', 'wf-primary', 'Nộp bài & xây dựng lộ trình'); submit.type = 'submit'; bar.append(submit, counts); form.append(bar); update();
    form.addEventListener('submit', async e => {
      e.preventDefault(); if (busy) return;
      const missing = data.questions.find(q => !Object.hasOwn(q.options, answers[String(q.no)]));
      if (missing) {status('Bài đầu vào cần trả lời đầy đủ. Mình đã chuyển đến câu chưa làm.', true); document.getElementById(`question-${missing.no}`).scrollIntoView({behavior: 'smooth', block: 'center'}); return;}
      busy = true; submit.disabled = true;
      form.querySelectorAll('input').forEach(x => x.disabled = true);
      status('Đã gửi bài. Hệ thống đang chấm và xây dựng sườn lộ trình…');
      try {
        const job = await F.api(url('entry-test'), {answers, revision, request_id: F.id()});
        try {localStorage.setItem(`eduagent-entry-job-${sid}`, job.job_id);} catch {}
        rememberAnswer('Đã nộp bài kiểm tra đầu vào: ' + data.questions.map(q => `${q.no}-${answers[String(q.no)]}`).join(', '));
        await finishEntry(job.job_id, bar);
        localStorage.removeItem(draftKey);
      } catch (e) {status(e.message, true); submit.disabled = false; form.querySelectorAll('input').forEach(x => x.disabled = false);}
      finally {busy = false;}
    });
  }
  async function finishEntry(jid, container) {
    const result = await waitJob(jid, container);
    try {localStorage.removeItem(`eduagent-entry-job-${sid}`);} catch {}
    root.replaceChildren(); header('KẾT QUẢ ĐẦU VÀO', 'Đã xử lý bài kiểm tra', 'Quay lại trò chuyện để xem và xác nhận sườn lộ trình.');
    const box = el('section', 'study-card'); box.append(rich('div', '', result.answer || 'Đã xử lý xong.'));
    if (result.skeleton) F.decorate(box, {...result, actions: []}, () => {});
    box.append(backLink()); root.append(box); status('');
  }
  function list(title, items) {
    const box = el('div'); box.append(el('h4', '', title));
    const ul = el('ul'); (items || []).forEach(x => {ul.append(rich('li', '', x));}); box.append(ul); return box;
  }
  function resource(r) {
    let safe; try {const u = new URL(r.url); if (['https:', 'http:'].includes(u.protocol)) safe = u.href;} catch {}
    const a = el(safe ? 'a' : 'div', 'study-resource');
    if (safe) {a.href = safe; a.target = '_blank'; a.rel = 'noopener noreferrer';}
    a.append(el('strong', '', `${r.type === 'video' ? '▶ ' : '↗ '}${r.title || 'Tài liệu học tập'}`));
    if (r.note) a.append(el('p', 'study-muted', r.note)); return a;
  }
  async function path() {
    const data = await F.api(url('path')); revision = data.revision;
    const lp = data.path, schedule = lp.schedule || {};
    status(''); root.replaceChildren();
    const head = header('LỘ TRÌNH CỦA BẠN', data.subject || 'Lộ trình học cá nhân', `${schedule.start_date || ''} → ${schedule.end_date || ''} · ${schedule.total_weeks || '—'} tuần · ${schedule.sessions_per_week || '—'} buổi/tuần`);
    const printBox = el('div', 'study-no-print');
    printBox.append(button('Tải PDF lộ trình', () => {
      document.querySelectorAll('#study-root details').forEach(d => {d.dataset.wasOpen = String(d.open); d.open = true;}); window.print();
    }), el('p', 'study-muted wf-print-hint', 'Chọn “Lưu dưới dạng PDF” trong cửa sổ in.'));
    head.append(printBox);
    root.append(el('p', 'study-notice', `Khung tổng quan gồm ${(lp.outline || []).length} giai đoạn. Chi tiết hiện có: ${(lp.weeks || []).length} tuần, thuộc phần lộ trình đã được hệ thống soạn.`));
    const outline = el('section', 'study-card'); outline.append(el('h2', '', 'Tổng quan các giai đoạn'));
    (lp.outline || []).forEach(phase => {
      const d = el('details', 'wf-details'); d.append(el('summary', '', `Giai đoạn ${phase.phase}`));
      d.append(F.table(['Tuần', 'Mục tiêu', 'Bài học'], (phase.weeks || []).map(w => [w.week_no, w.goal, (w.lessons || []).map(l => l.lesson).join('\n')]))); outline.append(d);
    }); root.append(outline);
    (lp.weeks || []).forEach(week => {
      const group = el('section'); group.append(el('h2', '', `Tuần ${week.week_no}`), rich('p', 'study-muted', week.goal || ''));
      (week.sessions || []).forEach((session, index) => {
        const card = el('article', 'study-card study-session');
        card.append(el('p', 'study-kicker', `BUỔI ${index + 1} · ${session.date || ''} · ${session.start_time || ''}`), el('h3', '', session.lesson));
        const tags = el('div', 'study-tags');
        [session.minutes ? `${session.minutes} phút` : '', {lesson:'Học kiến thức',review:'Ôn tập',assessment:'Đánh giá'}[session.type] || session.type, {easy:'Cơ bản',medium:'Trung bình',hard:'Nâng cao'}[session.difficulty] || session.difficulty].filter(Boolean).forEach(t => tags.append(el('span', '', t))); card.append(tags);
        if (session.key_points?.length) card.append(list('Trọng tâm', session.key_points));
        const columns = el('div', 'study-columns');
        if (session.must_know?.length) columns.append(list('Cần nắm', session.must_know));
        if (session.must_understand?.length) columns.append(list('Cần hiểu', session.must_understand)); card.append(columns);
        if (session.activities?.length) card.append(F.table(['Hoạt động', 'Phút', 'Mức độ'], session.activities.map(a => [a.content, a.minutes, a.difficulty || '—'])));
        if (session.related?.length) card.append(list('Kiến thức liên quan', session.related.map(r => `${r.lesson} — ${r.relation}`)));
        if (session.resources?.length) {card.append(el('h4', '', 'Tài nguyên học tập')); session.resources.forEach(r => card.append(resource(r)));}
        if (session.exam_enabled) {
          const area = el('div', 'study-no-print');
          const b = button('Tạo bài ôn tập', async () => {
            if (busy) return; busy = true; b.disabled = true;
            const key = `eduagent-practice-${sid}-${week.week_no}-${index + 1}`;
            try {
              let jid = localStorage.getItem(key);
              if (!jid) {const job = await F.api(url('practice'), {week_no: week.week_no, session_no: index + 1, revision, request_id: F.id()}); jid = job.job_id; localStorage.setItem(key, jid);}
              const result = await waitJob(jid, area);
              const link = el('a', 'wf-primary', 'Làm bài test'); link.href = result.exam_url; area.append(link); b.remove();
              if (Array.isArray(result.tests)) result.tests.forEach(r => area.append(resource(r)));
            } catch (e) {status(e.message, true); b.disabled = false; localStorage.removeItem(key);}
            finally {busy = false;}
          }); area.append(b); card.append(area);
        }
        group.append(card);
      }); root.append(group);
    });
    if (lp.assumptions?.length) {const box = el('section', 'study-card'); box.append(list('Giả định và điểm cần kiểm chứng', lp.assumptions)); root.append(box);}
  }
  window.addEventListener('afterprint', () => document.querySelectorAll('details[data-was-open]').forEach(d => {d.open = d.dataset.wasOpen === 'true'; delete d.dataset.wasOpen;}));
  async function init() {
    if (!sid && view === 'path') {const data = await F.api('/api/ui/workflows/saved', {}); sid = data.session_id; history.replaceState(null, '', `/roadmap?session=${sid}`);}
    if (!sid) throw new Error('Thiếu phiên học tập. Hãy mở trang từ nút trong cuộc trò chuyện.');
    let pending = null; try {pending = localStorage.getItem(`eduagent-entry-job-${sid}`);} catch {}
    if (view === 'entry' && pending) {
      try {await finishEntry(pending, root); return;}
      catch (e) {try {localStorage.removeItem(`eduagent-entry-job-${sid}`);} catch {} throw e;}
    }
    if (view === 'entry') await entry(); else await path();
  }
  init().catch(e => status(e.message, true));
})();
