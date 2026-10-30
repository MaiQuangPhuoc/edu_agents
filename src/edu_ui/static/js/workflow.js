/* Shared safe Markdown, math, matrix and job UI. */
window.EduFlow = (() => {
  const element = (tag, cls = '', text) => {
    const n = document.createElement(tag); n.className = cls;
    if (text !== undefined) n.textContent = String(text); return n;
  };
  function normalizeText(value) {
    // Preserve code and LaTeX verbatim; normalize display-only prose around them.
    const protectedParts = /(```[\s\S]*?```|`[^`\n]*`|\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|(?<!\\)\$(?!\$)(?:\\.|[^$\n])+?(?<!\\)\$)/g;
    return String(value ?? '').split(protectedParts).map((part, i) => {
      if (i % 2) return part;
      part = part.replace(/\\r\\n|\\n/g, '\n').replace(/\\t/g, '  ').replace(/\r\n?/g, '\n');
      return part.split('\n').map(line => {
        if (line.length < 320 || /^\s*(?:[#>|*\-]|\d+[.)])/.test(line)) return line;
        return line.replace(/([.!?])\s+(?=\p{Lu})/gu, '$1\n\n');
      }).join('\n');
    }).join('');
  }
  function rich(tag, cls, value) {
    const node = element(tag, `${cls || ''} rich-text`.trim());
    const text = normalizeText(value);
    node.dataset.wfRaw = String(value ?? '');
    if (!window.marked || !window.DOMPurify) {
      node.textContent = text; node.style.whiteSpace = 'pre-wrap';
      document.querySelector('#render-notice')?.removeAttribute('hidden');
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
          if (!window.katex) document.querySelector('#render-notice')?.removeAttribute('hidden');
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
  async function api(url, body, signal) {
    const timeout = new AbortController();
    const abort = () => timeout.abort();
    signal?.addEventListener('abort', abort, {once: true});
    if (signal?.aborted) timeout.abort();
    const timer = setTimeout(() => timeout.abort(), 25000);
    try {
      const r = await fetch(url, {method: body === undefined ? 'GET' : 'POST', signal: timeout.signal,
        headers: {'Content-Type': 'application/json'}, ...(body === undefined ? {} : {body: JSON.stringify(body)})});
      const data = await r.json().catch(() => ({}));
      if (!r.ok) {const error = new Error(typeof data.detail === 'string' ? data.detail : `Yêu cầu không hợp lệ (${r.status})`); error.status = r.status; throw error;}
      return data;
    } catch (error) {
      if (timeout.signal.aborted && !signal?.aborted) throw new Error('Server chưa trả dữ liệu sau 25 giây. Kiểm tra terminal rồi thử tải lại trang.');
      throw error;
    } finally {clearTimeout(timer); signal?.removeEventListener('abort', abort);}
  }
  const id = () => window.crypto?.randomUUID?.() || [...window.crypto.getRandomValues(new Uint8Array(16))].map(n => n.toString(16).padStart(2, '0')).join('');
  async function poll(jid, onProgress, signal) {
    for (;;) {
      const job = await api(`/api/ui/workflows/jobs/${encodeURIComponent(jid)}`, undefined, signal);
      onProgress?.(job.steps || []);
      if (job.status === 'failed') {const error = new Error(`${job.error} (mã ${jid.slice(0, 8)})`); error.jobFailed = true; throw error;}
      if (job.status === 'completed') return job.result;
      await new Promise((resolve, reject) => {
        const abort = () => {clearTimeout(timer); reject(new DOMException('Aborted', 'AbortError'));};
        const timer = setTimeout(() => {signal?.removeEventListener('abort', abort); resolve();}, 900);
        signal?.addEventListener('abort', abort, {once: true});
        if (signal?.aborted) abort();
      });
    }
  }
  function formatEduTime(seconds) {
    const whole = Math.max(0, Math.floor(seconds));
    return `${String(Math.floor(whole / 90)).padStart(2, '0')}:${String(whole % 90).padStart(2, '0')}`;
  }
  function createProgress(node, {minMs = 3000, onTransition = () => {}} = {}) {
    node.classList.add('wf-progress', 'wf-progress-single');
    node.setAttribute('role', 'status');
    let current = null, pending = null, since = 0, timer = null, stopped = false, finishing = false, complete;
    function show(item) {
      if (current) onTransition();
      current = item; since = performance.now();
      const label = element('span', 'is-running', item.label);
      node.replaceChildren(label);
    }
    function schedule() {
      if (timer || stopped || finishing || !pending) return;
      timer = setTimeout(() => {timer = null; if (!pending || stopped || finishing) return; const next = pending; pending = null; show(next);}, Math.max(0, minMs - (performance.now() - since)));
    }
    return {
      update(steps) {
        if (stopped || finishing || !steps.length) return;
        const last = steps[steps.length - 1], item = {...last, key: `${steps.length}:${last.code}:${last.label}`};
        if (!current) {show(item); return;}
        if (item.key !== current.key) {pending = item; schedule();}
      },
      finish() {
        finishing = true; pending = null; clearTimeout(timer); timer = null;
        return new Promise(resolve => {complete = resolve; timer = setTimeout(() => {timer = null; if (current) onTransition(); resolve(); complete = null;}, current ? Math.max(0, minMs - (performance.now() - since)) : 0);});
      },
      stop() {stopped = true; clearTimeout(timer); if (complete) {complete(); complete = null;}}
    };
  }
  const progressViews = new WeakMap();
  function progress(node, steps) {
    if (!progressViews.has(node)) progressViews.set(node, createProgress(node));
    progressViews.get(node).update(steps);
  }
  const SOURCE_PREVIEW_CHARS = 180;
  function sourceInfo(source) {
    const title = String(source.title || source.document_name || source.source || '').trim();
    const content = normalizeText(source.chunk || source.content || source.text || '');
    const chapter = String(source.chapter_id || source.chapter || '');
    const type = String(source.document_type || source.source_type || source.kind || '').toLowerCase();
    const unknown = !title || /^(unknown|none|null)$/i.test(title);
    let label;
    if (/web|internet/.test(type)) label = 'Internet';
    else if (/lesson.?plan|giao.?an|giáo án/.test(type) || (unknown && /[>›]/.test(chapter + content))) label = 'Giáo án';
    else if (/sgk|textbook|sách giáo khoa/.test(type) || /^(?:\[\s*)?(?:BÀI|CHƯƠNG)\s+/iu.test(title) || /\[\s*BÀI\s+\d/iu.test(content)) label = 'Sách giáo khoa';
    else label = 'Internet';
    const description = unknown ? (chapter || content.split('\n')[0]) : title;
    return {label, title: description, content, preview: content.length > SOURCE_PREVIEW_CHARS ? content.slice(0, SOURCE_PREVIEW_CHARS).trimEnd() + '…' : content};
  }
  // Async CDN libraries never block loading an entry test. Reformat existing text on arrival.
  function refreshRich() {
    if (!window.marked || !window.DOMPurify) return;
    document.querySelectorAll('.rich-text[data-wf-raw]').forEach(node => {
      const rendered = (node.dataset.wfCompact ? compactRich : rich)(node.tagName.toLowerCase(), node.className.replace(/\brich-text\b/g, '').trim(), node.dataset.wfRaw);
      node.replaceWith(rendered);
    });
    if (window.katex) document.querySelector('#render-notice')?.setAttribute('hidden', '');
  }
  document.addEventListener('load', event => {if (event.target?.tagName === 'SCRIPT') refreshRich();}, true);
  function table(headers, rows) {
    const wrap = element('div', 'wf-table-scroll'), t = element('table', 'wf-table');
    const h = element('thead'), tr = element('tr'); headers.forEach(x => tr.append(element('th', '', x))); h.append(tr);
    const b = element('tbody'); rows.forEach(row => {const r = element('tr'); row.forEach(x => r.append(rich('td', '', String(x ?? '—')))); b.append(r);});
    t.append(h, b); wrap.append(t); return wrap;
  }
  function matrix(data) {
    const box = element('section', 'wf-matrix');
    box.append(element('h3', '', 'Ma trận đề kiểm tra'));
    const stats = element('div', 'wf-stats');
    const diff = data.tong_do_kho || {};
    [['Tổng câu', data.tong_so_cau], ['Dễ', diff.de], ['Trung bình', diff.trung_binh], ['Khó', diff.kho]].forEach(([label, value]) => {
      const c = element('div'); c.append(element('strong', '', value ?? 0), element('span', '', label)); stats.append(c);
    }); box.append(stats);
    box.append(table(['Chương', 'Số câu'], (data.chuong || []).map(c => [c.ten, c.so_cau])));
    (data.chuong || []).forEach(c => {
      const d = element('details', 'wf-details'); d.append(element('summary', '', `${c.ten} · ${c.so_cau} câu`));
      d.append(table(['Chủ đề', 'Câu', 'Dễ', 'TB', 'Khó'], (c.bai_hoc || []).map(l => [l.ten, l.so_cau, l.do_kho?.de || 0, l.do_kho?.trung_binh || 0, l.do_kho?.kho || 0])));
      (c.bai_hoc || []).forEach(l => {d.append(element('h4', '', l.ten)); (l.dang_bai || []).forEach(x => d.append(rich('p', '', `${x.ten} — **${x.so_cau} câu**`)));});
      box.append(d);
    }); return box;
  }
  function safeResourceURL(value) {
    try {const u = new URL(value); return ['http:', 'https:'].includes(u.protocol) ? u.href : null;} catch {return null;}
  }
  function copyLinkButton(url) {
    const b = element('button', 'wf-copy-link', 'Sao chép'); b.type = 'button'; b.setAttribute('aria-label', 'Sao chép liên kết');
    b.addEventListener('click', async () => {
      try {
        if (!navigator.clipboard?.writeText) throw new Error('clipboard unavailable');
        await navigator.clipboard.writeText(url); b.textContent = 'Đã sao chép';
        setTimeout(() => b.textContent = 'Sao chép', 1800);
      } catch {
        let field = b.parentNode.querySelector('.wf-link-value');
        if (!field) {field = element('input', 'wf-link-value'); field.readOnly = true; field.value = url; field.setAttribute('aria-label', 'Liên kết để sao chép'); b.parentNode.append(field);}
        field.focus(); field.select(); b.textContent = 'Nhấn Ctrl+C';
      }
    }); return b;
  }
  function compactRich(tag, cls, text) {
    const node = rich(tag, cls, text); node.dataset.wfCompact = 'true';
    // The raw text remains available in its collapsed original version.
    node.querySelectorAll('a[href]').forEach(a => {
      const url = safeResourceURL(a.getAttribute('href'));
      if (!url) {a.removeAttribute('href'); return;}
      a.title = a.textContent;
      a.textContent = /youtube|youtu\.be|vimeo|video/i.test(url + ' ' + a.title) ? 'Video' : 'Tài liệu';
      a.classList.add('wf-short-link'); a.after(copyLinkButton(url));
    });
    return node;
  }
  function expandableText(title, text, max = 180) {
    const box = element('section', 'wf-outline-summary'); box.append(element('h4', '', title));
    const value = String(text || 'Chưa có thông tin.');
    if (value.length <= max) box.append(compactRich('div', '', value));
    else {
      const preview = compactRich('div', 'wf-outline-preview', value); box.append(preview);
      const details = element('details', 'wf-outline-more'), summary = element('summary', '', 'Xem đầy đủ');
      details.append(summary, compactRich('div', '', value));
      details.addEventListener('toggle', () => {preview.hidden = details.open; summary.textContent = details.open ? 'Thu gọn' : 'Xem đầy đủ';}); box.append(details);
    } return box;
  }
  function legacyOutline(text) {
    // Display-only compatibility for the exact headings emitted by _format_roadmap.
    // Never reconstruct a backend planning state from this text.
    const value = normalizeText(text);
    const goal = value.match(/^\*\*Mục tiêu tổng:\*\*\s*(.*)$/m);
    const strategy = value.match(/^\*\*Chiến lược:\*\*\s*(.*)$/m);
    const matches = [...value.matchAll(/^\*\*Giai đoạn\s+(\d+):\s*(.*?)\*\*\s*(?:\(([^\n]*)\))?\s*$/gm)];
    if (!goal || !strategy || !matches.length) return null;
    const assumptionsAt = value.search(/^\*\*(?:Điểm mình đang giả định|Giả định)/m);
    const endPrompt = value.search(/^Bạn thấy sườn này thế nào/m);
    const end = Math.min(...[assumptionsAt, endPrompt, value.length].filter(x => x >= 0));
    const phases = matches.map((m, index) => ({thu_tu: Number(m[1]), ten: m[2], mon_hoc: m[3] || '', body: value.slice(m.index + m[0].length, matches[index + 1]?.index ?? end).trim()}));
    const assumptions = assumptionsAt >= 0 ? value.slice(assumptionsAt, endPrompt >= 0 ? endPrompt : value.length).split('\n').filter(line => /^-\s/.test(line)).map(line => line.replace(/^-\s+/, '')) : [];
    const before = value.slice(0, goal.index).trim();
    return {goal: goal[1], strategy: strategy[1], phases, assumptions, assessment: before ? {summary: before} : null, legacy: true};
  }
  function skeletonCard(data, fullText = '') {
    const card = element('section', 'wf-skeleton'); card.setAttribute('aria-label', 'Sườn lộ trình học');
    const phases = Array.isArray(data.phases) ? data.phases : [], assessment = data.assessment;
    const header = element('header', 'wf-skeleton-heading'), titles = element('div');
    titles.append(element('p', 'study-kicker', 'SƯỜN LỘ TRÌNH'), element('h3', '', 'Kế hoạch học tập đề xuất'));
    header.append(titles, element('span', 'wf-outline-badge', `${phases.length} giai đoạn`)); card.append(header);
    if (assessment) card.append(element('p', 'wf-outline-score', assessment.summary ? 'Kết quả đầu vào · xem trong tab bên dưới' : `Bài đầu vào: ${assessment.correct ?? '—'}/${assessment.total ?? '—'} câu đúng`));
    if (data.legacy) card.append(element('p', 'study-muted', 'Bản xem từ nội dung hội thoại đã lưu.'));
    const tabs = element('div', 'wf-outline-tabs'); tabs.setAttribute('role', 'tablist'); tabs.setAttribute('aria-label', 'Các mục của sườn lộ trình');
    const panelArea = element('div'), panels = [], buttons = [], prefix = 'outline-' + id();
    const sections = [['Tổng quan', 'overview'], ['Kết quả đầu vào', 'assessment'], ['Các giai đoạn', 'phases'], [`Giả định (${(data.assumptions || []).length})`, 'assumptions']];
    function select(index, focus = false) {
      panels.forEach((p, i) => {p.hidden = i !== index; buttons[i].setAttribute('aria-selected', String(i === index)); buttons[i].tabIndex = i === index ? 0 : -1;});
      if (focus) buttons[index].focus();
    }
    sections.forEach(([title, key], index) => {
      const button = element('button', '', title); button.type = 'button'; button.id = `${prefix}-tab-${key}`;
      button.setAttribute('role', 'tab'); button.setAttribute('aria-controls', `${prefix}-${key}`);
      button.addEventListener('click', () => select(index));
      button.addEventListener('keydown', e => {
        let next;
        if (e.key === 'ArrowRight') next = (index + 1) % sections.length;
        if (e.key === 'ArrowLeft') next = (index + sections.length - 1) % sections.length;
        if (e.key === 'Home') next = 0;
        if (e.key === 'End') next = sections.length - 1;
        if (next !== undefined) {e.preventDefault(); select(next, true);}
      });
      tabs.append(button); buttons.push(button);
      const panel = element('section', 'wf-outline-panel'); panel.id = `${prefix}-${key}`; panel.setAttribute('role', 'tabpanel'); panel.setAttribute('aria-labelledby', button.id);
      panels.push(panel); panelArea.append(panel);
    }); card.append(tabs, panelArea);
    const overview = panels[0];
    const summaryGrid = element('div', 'wf-outline-summary-grid');
    summaryGrid.append(expandableText('Mục tiêu tổng', data.goal), expandableText('Chiến lược', data.strategy)); overview.append(summaryGrid);
    const tableBox = table(['Giai đoạn', 'Môn học', 'Phạm vi', ''], phases.map(p => [p.ten, p.mon_hoc, (p.chapters || []).map(c => `Chương ${c.chapter_id}`).join(', ') || 'Xem chi tiết', '']));
    tableBox.querySelectorAll('tbody tr').forEach((tr, index) => {
      const b = element('button', 'wf-outline-view', 'Xem'); b.type = 'button'; b.setAttribute('aria-label', `Xem giai đoạn ${index + 1}`);
      b.addEventListener('click', () => {phaseSelect.value = String(index); renderPhase(index); select(2, true);}); tr.lastElementChild.append(b);
    }); overview.append(tableBox);
    const results = panels[1];
    if (!assessment) results.append(element('p', 'study-muted', 'Chưa có kết quả đầu vào được lưu trong phiên này.'));
    else if (assessment.summary) results.append(compactRich('div', '', assessment.summary));
    else {
      results.append(element('h4', '', `${assessment.correct ?? '—'}/${assessment.total ?? '—'} câu đúng`));
      results.append(table(['Chương', 'Đúng / tổng', 'Tỉ lệ', 'Đánh giá'], (assessment.chapters || []).map(c => [c.chapter_id, `${c.correct ?? '—'}/${c.total ?? '—'}`, Number.isFinite(c.ratio) ? `${Math.round(c.ratio * 100)}%` : '—', c.level || '—'])));
      results.append(element('p', 'study-muted', 'Kết quả phản ánh các câu hỏi đã làm, được dùng để điều chỉnh trọng tâm học.'));
    }
    const phasePanel = panels[2], phaseLabel = element('label', 'wf-outline-select-label', 'Chọn giai đoạn'), phaseSelect = element('select', 'wf-outline-select'), phaseBody = element('div');
    phaseSelect.setAttribute('aria-label', 'Chọn giai đoạn');
    phases.forEach((p, index) => {const option = element('option', '', `${p.thu_tu ?? index + 1}. ${p.ten || 'Giai đoạn'}`); option.value = String(index); phaseSelect.append(option);});
    phaseLabel.append(phaseSelect); phasePanel.append(phaseLabel, phaseBody);
    function renderPhase(index) {
      phaseBody.replaceChildren(); const p = phases[index]; if (!p) return;
      phaseBody.append(element('h4', '', p.ten || `Giai đoạn ${index + 1}`));
      if (p.body) {phaseBody.append(compactRich('div', 'wf-phase-legacy', p.body)); return;}
      phaseBody.append(expandableText('Mục tiêu giai đoạn', p.muc_tieu));
      (p.chapters || []).forEach(chapter => {
        const d = element('details', 'wf-outline-chapter');
        const lessons = Array.isArray(chapter.lessons) ? chapter.lessons : [];
        d.append(element('summary', '', `Chương ${chapter.chapter_id} · ${lessons.length} bài học`));
        const list = element('ul'); lessons.forEach(lesson => list.append(compactRich('li', '', lesson))); d.append(list);
        if (chapter.ly_do) d.append(expandableText('Lý do phân bổ', chapter.ly_do)); phaseBody.append(d);
      });
      phaseBody.append(expandableText('Hoàn thành khi', p.tieu_chi_hoan_thanh));
      if (p.resources?.length) {
        const list = element('div', 'wf-outline-resources'); list.append(element('h4', '', 'Tài nguyên tham khảo'));
        p.resources.forEach((r, index) => {
          const row = element('div', 'wf-outline-resource'), url = safeResourceURL(r.url), label = r.loai === 'video' ? 'Video' : r.loai === 'giao_trinh' ? 'Giáo trình' : 'Tài liệu';
          if (url) {
            const a = element('a', 'wf-short-link', `${label} ${index + 1}`); a.href = url; a.title = r.tieu_de || label; a.target = '_blank'; a.rel = 'noopener noreferrer';
            row.append(a, copyLinkButton(url));
          } else row.append(element('span', '', `${label} ${index + 1} · chưa có liên kết`));
          if (r.tieu_de) row.append(element('span', 'wf-resource-title', r.tieu_de));
          if (r.ghi_chu) row.append(compactRich('p', 'study-muted', r.ghi_chu)); list.append(row);
        }); phaseBody.append(list);
      }
    }
    phaseSelect.addEventListener('change', () => renderPhase(Number(phaseSelect.value))); renderPhase(0);
    const assumptions = panels[3];
    if (!data.assumptions?.length) assumptions.append(element('p', 'study-muted', 'Không có giả định bổ sung.'));
    (data.assumptions || []).forEach((text, i) => assumptions.append(expandableText(`Điểm cần kiểm chứng ${i + 1}`, text, 150)));
    if (fullText) {
      const raw = element('details', 'wf-outline-original'); raw.append(element('summary', '', 'Xem bản văn đầy đủ'), compactRich('div', '', fullText)); card.append(raw);
    }
    select(0); return card;
  }
  function decorate(bubble, payload, send) {
    if (!payload.skeleton) {
      const original = payload.answer || bubble.querySelector('[data-wf-raw]')?.dataset.wfRaw || '';
      const legacy = legacyOutline(original);
      if (legacy) {
        payload = {...payload, skeleton: legacy, full_text: original};
        bubble.replaceChildren(rich('div', '', 'Sườn lộ trình · chọn mục bên dưới để xem chi tiết.'));
      }
    }
    if (payload.skeleton) {
      bubble.classList.add('wf-skeleton-bubble'); bubble.closest('.message')?.classList.add('wf-skeleton-message');
      bubble.append(skeletonCard(payload.skeleton, payload.full_text));
    }
    if (payload.matrix) bubble.append(matrix(payload.matrix));
    if (payload.interests?.length) {
      const box = element('form', 'wf-interests');
      payload.interests.forEach((row, i) => {
        const label = element('label', 'wf-interest');
        label.append(element('span', '', `${i + 1}. ${row.lesson} › ${row.section}`));
        const select = element('select'); select.required = true; select.setAttribute('aria-label', row.section);
        [['', 'Chưa chọn'], ['0', '0 · Không quan tâm'], ['1', '1 · Ít quan tâm'], ['2', '2 · Bình thường'], ['3', '3 · Quan tâm cao']].forEach(([value, text]) => {const op=element('option', '', text); op.value=value; select.append(op);});
        label.append(select); box.append(label);
      });
      const b = element('button', 'wf-primary', 'Gửi đánh giá'); b.type = 'submit'; box.append(b);
      box.addEventListener('submit', e => {e.preventDefault(); const value = [...box.querySelectorAll('select')].map(s => s.value).join(','); send(value, `Đánh giá mức quan tâm: ${value}`, payload);}); bubble.append(box);
    }
    const actions = element('div', 'wf-actions');
    (payload.actions || []).forEach(a => {
      if (a.url && /^\/(study|roadmap|exams)\?/.test(a.url)) {
        const link = element('a', 'wf-primary', a.label); link.href = a.url; actions.append(link);
      } else if (a.compose) {
        const b = element('button', 'wf-primary wf-secondary', a.label); b.type = 'button';
        b.addEventListener('click', () => document.dispatchEvent(new CustomEvent('eduagent:compose', {detail: {placeholder: 'Bạn muốn điều chỉnh mục nào trong sườn lộ trình?'}}))); actions.append(b);
      } else if (a.value) {
        const b = element('button', 'wf-primary', a.label); b.type='button';
        b.addEventListener('click', () => send(a.value, a.label, payload)); actions.append(b);
      }
    });
    (payload.suggestions || []).slice(0, 3).forEach((q, i) => {
      const b = element('button', `wf-suggestion tone-${i}`, q); b.type='button';
      b.addEventListener('click', () => send(q, q, null)); actions.append(b);
    });
    bubble.append(actions);
    bubble.dataset.revision = payload.revision ?? -1;
  }
  return {element, rich, skeletonCard, legacyOutline, normalizeText, sourceInfo, formatEduTime, createProgress, api, id, poll, progress, table, matrix, decorate};
})();
