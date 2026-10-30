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
      const rendered = rich(node.tagName.toLowerCase(), node.className.replace(/\brich-text\b/g, '').trim(), node.dataset.wfRaw);
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
  function decorate(bubble, payload, send) {
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
  return {element, rich, normalizeText, sourceInfo, formatEduTime, createProgress, api, id, poll, progress, table, matrix, decorate};
})();
