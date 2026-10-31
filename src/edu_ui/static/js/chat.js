/* EDUAGENT chat: no avatars/icons, student left, assistant right.
   API: POST /api/ui/workflows
   Request:  {message, session_id}
   Response: {answer, session_id, sources?}
*/

(() => {
  'use strict';

  const $ = (selector) => document.querySelector(selector);

  const messages = $('#messages');
  const form = $('#chat-form');
  const input = $('#chat-input');
  const sendButton = $('#send');
  const sourcesList = $('#sources');
  const connection = $('#connection');
  const notice = $('#toast');
  const sourcePanel = $('.sources-panel');
  const chatHeader = $('.chat-header');
  const actionMenu = $('#action-menu');
  const actionToggle = $('#action-toggle');
  const voiceButton = $('#voice-input');
  const demoMarkup = $('.chat-demo')?.cloneNode(true);
  const demoSourcesMarkup = sourcesList?.cloneNode(true);
  const appShell = $('.app-shell');
  const historyKey = 'eduagent-chat-history';

  if (
    ![
      messages,
      form,
      input,
      sendButton,
      sourcesList,
      connection,
      actionMenu,
      actionToggle,
      voiceButton,
      appShell
    ].every(Boolean)
  ) {
    console.error(
      'EDUAGENT: HTML thiếu thành phần cần thiết cho chat.'
    );
    return;
  }

  const F = window.EduFlow;
  if (!F || !$('#workflow-chip') || !$('#workflow-options')) {
    connection.textContent = 'Giao diện chưa đồng bộ';
    const warning = $('#render-notice') || document.createElement('p');
    warning.hidden = false;
    warning.textContent = 'Thiếu file giao diện mới. Cập nhật chat.html, chat.js và workflow.js, sau đó nhấn Ctrl+F5.';
    if (!warning.parentNode) form.before(warning);
    return;
  }
  let mode = 'qa', revision = 0;
  const chip = $('#workflow-chip');
  const modeNames = {qa: 'Hỏi đáp & giải bài', exam: 'Tạo bài kiểm tra', planning: 'Lập lộ trình học'};
  function showMode() {
    chip.hidden = false; chip.dataset.mode = mode; chip.querySelector('span').textContent = modeNames[mode];
    $('#workflow-options').hidden = mode !== 'planning';
    const welcome = $('.wf-welcome-text');
    if (welcome) {welcome.replaceChildren(F.rich('div', '', mode === 'planning' ? '**Chào bạn!**\n\nMình sẽ cùng bạn xác định mục tiêu, làm bài đầu vào và xây dựng lộ trình học phù hợp.\n\nBạn muốn cải thiện môn học nào?' : mode === 'exam' ? '**Chào bạn!**\n\nBạn muốn tạo bài kiểm tra môn nào? Mình sẽ giúp bạn chọn phạm vi, số câu và độ khó.' : '**Chào bạn!**\n\nMình có thể giải thích lý thuyết, cùng bạn giải bài tập hoặc tìm tài liệu học tập.\n\nHôm nay bạn muốn học điều gì?'));}
  }
  function chooseMode(next) {
    if (activeController) {showNotice('Đang xử lý; chờ kết quả trước khi đổi chức năng.'); return;}
    if (next !== mode && (sessionId || activeConversationId)) document.dispatchEvent(new CustomEvent('eduagent:new-chat'));
    mode = next; showMode(); input.focus();
  }
  chip.querySelector('button').addEventListener('click', () => {chooseMode('qa'); if (!activeController) chip.hidden = true;});
  let sessionId = null;
  let activeController = null;
  let requestId = 0;
  let noticeTimeout;
  let recognition = null;
  const panelWidths = { sidebar: null, sources: null };
  let activeConversationId = null;

  function resizeComposer() {
    const maxHeight = 112;
    input.style.height = 'auto';
    const nextHeight = Math.min(input.scrollHeight, maxHeight);
    input.style.height = `${nextHeight}px`;
    input.style.overflowY = input.scrollHeight > maxHeight ? 'auto' : 'hidden';
  }

  function getPanelWidthBounds(name) {
    const compact = window.matchMedia('(max-width: 760px)').matches;
    const oppositeName = name === 'sidebar' ? 'sources' : 'sidebar';
    const oppositeVariable = oppositeName === 'sidebar'
      ? '--chat-sidebar-width'
      : '--chat-source-width';
    const oppositeWidth = Number.parseFloat(
      getComputedStyle(appShell).getPropertyValue(oppositeVariable)
    );
    const minimumPanelWidth = compact ? 120 : 180;
    const minimumChatWidth = compact ? 180 : 320;
    const maximumPanelWidth = Math.max(
      minimumPanelWidth,
      Math.min(
        compact ? 280 : 480,
        window.innerWidth - oppositeWidth - minimumChatWidth
      )
    );
    return { minimumPanelWidth, maximumPanelWidth };
  }

  function setPanelWidth(name, requestedWidth) {
    const variable = name === 'sidebar'
      ? '--chat-sidebar-width'
      : '--chat-source-width';
    const { minimumPanelWidth, maximumPanelWidth } = getPanelWidthBounds(name);
    const width = Math.round(
      Math.min(maximumPanelWidth, Math.max(minimumPanelWidth, requestedWidth))
    );

    panelWidths[name] = width;
    appShell.style.setProperty(variable, `${width}px`);

    const separator = document.querySelector(`[data-resize-panel="${name}"]`);
    if (separator) {
      separator.setAttribute('aria-valuemin', String(minimumPanelWidth));
      separator.setAttribute('aria-valuemax', String(maximumPanelWidth));
      separator.setAttribute('aria-valuenow', String(width));
    }
  }

  function initializePanelResize() {
    const separators = document.querySelectorAll('[data-resize-panel="sources"]');

    separators.forEach((separator) => {
      const name = separator.dataset.resizePanel;
      const variable = name === 'sidebar'
        ? '--chat-sidebar-width'
        : '--chat-source-width';
      const { minimumPanelWidth, maximumPanelWidth } = getPanelWidthBounds(name);
      separator.setAttribute('aria-valuemin', String(minimumPanelWidth));
      separator.setAttribute('aria-valuemax', String(maximumPanelWidth));
      separator.setAttribute(
        'aria-valuenow',
        String(Math.round(Number.parseFloat(
          getComputedStyle(appShell).getPropertyValue(variable)
        )))
      );

      separator.addEventListener('pointerdown', (event) => {
        if (event.button !== 0) return;
        event.preventDefault();
        separator.classList.add('is-dragging');

        const updateWidth = (pointerEvent) => {
          const requestedWidth = name === 'sidebar'
            ? pointerEvent.clientX
            : window.innerWidth - pointerEvent.clientX;
          setPanelWidth(name, requestedWidth);
        };
        const finishResize = () => {
          separator.classList.remove('is-dragging');
          window.removeEventListener('pointermove', updateWidth);
          window.removeEventListener('pointerup', finishResize);
          window.removeEventListener('pointercancel', finishResize);
        };

        updateWidth(event);
        window.addEventListener('pointermove', updateWidth);
        window.addEventListener('pointerup', finishResize, { once: true });
        window.addEventListener('pointercancel', finishResize, { once: true });
      });

      separator.addEventListener('keydown', (event) => {
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        event.preventDefault();
        const variable = name === 'sidebar'
          ? '--chat-sidebar-width'
          : '--chat-source-width';
        const currentWidth = panelWidths[name] ?? Number.parseFloat(
          getComputedStyle(appShell).getPropertyValue(variable)
        );
        const direction = event.key === 'ArrowRight' ? 1 : -1;
        setPanelWidth(name, currentWidth + direction * (event.shiftKey ? 32 : 12));
      });
    });
  }

  input.addEventListener('input', resizeComposer);
  initializePanelResize();
  resizeComposer();

  // ==========================================
  // 1. CUỘN XUỐNG TIN NHẮN MỚI NHẤT
  // ==========================================

  function scrollToLatest() {
    messages.scrollTop = messages.scrollHeight;
  }

  // ==========================================
  // 2. HIỂN THỊ TIN NHẮN
  // User bên trái, Bot bên phải
  // Không avatar, không icon
  // ==========================================

  function appendMessage(role, content = '') {
    const wrap = document.createElement('div');
    wrap.className = `message ${role}`;

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    // Dùng textContent để tránh HTML injection.
    if (role === 'bot') bubble.append(F.rich('div', '', content));
    else bubble.textContent = content;

    wrap.appendChild(bubble);
    messages.appendChild(wrap);

    scrollToLatest();

    return { wrap, bubble };
  }

  // ==========================================
  // 3. ĐỒNG HỒ EDUAGENT
  // 90 giây thực tế = 1 phút UI
  //
  // 00:00 -> 00:89 -> 01:00
  // ==========================================

  const formatEduTime = F.formatEduTime;

  // ==========================================
  // 4. HIỆU ỨNG CHỜ BOT
  //
  // - Hiển thị 3 dấu chấm chuyển động
  // - Sau 2 giây mới hiện đồng hồ
  // - Đồng hồ cập nhật theo thời gian chờ
  // ==========================================

  function startWaiting() {
    const startedAt = performance.now();
    let deductions = 0, stopped = false;
    const waiting = appendMessage('bot'); waiting.wrap.classList.add('wf-waiting');
    const progress = document.createElement('div'); waiting.bubble.append(progress);
    const patienceNote = F.element('div', 'wf-waiting-note', 'Vẫn đang tiếp tục suy luận, xin lỗi bạn đã phải chờ nhé.');
    patienceNote.hidden = true;
    waiting.bubble.append(patienceNote);
    const elapsed = document.createElement('div'); elapsed.className = 'elapsed'; elapsed.hidden = true;
    elapsed.setAttribute('aria-label', 'Thời gian hiển thị đã quy đổi');
    elapsed.title = 'Đồng hồ giao diện: 90 giây thực = 1 phút hiển thị; giảm 2 giây khi chuyển bước.';
    waiting.wrap.append(elapsed);
    const stages = F.createProgress(progress, {minMs: 3000, onTransition: () => {deductions += 2; updateTime();}});
    function updateTime() {elapsed.textContent = formatEduTime(Math.max(0, (performance.now() - startedAt) / 1000 - deductions));}
    const show = setTimeout(() => {if (!stopped) {elapsed.hidden = false; updateTime();}}, 2000);
    const patienceTimer = setTimeout(() => {if (!stopped) patienceNote.hidden = false;}, 25000);
    const clock = setInterval(updateTime, 200);
    connection.textContent = 'Đang hỗ trợ bạn…';
    return {
      progress: steps => stages.update(steps),
      finish: () => stages.finish(),
      stop() {
        if (stopped) return; stopped = true; stages.stop(); clearTimeout(show); clearTimeout(patienceTimer); clearInterval(clock);
        waiting.wrap.remove(); connection.textContent = 'Sẵn sàng';
      }
    };
  }

  // ==========================================
  // 5. HIỂN THỊ NGUỒN TÀI LIỆU RETRIEVAL
  //
  // Cột bên phải:
  // - Tên tài liệu
  // - Môn học
  // - Chương
  // - Trang
  // - Nội dung chunk
  // - URL nếu có
  // ==========================================

  function renderSources(sources) {
    sourcesList.replaceChildren();
    if (!Array.isArray(sources) || !sources.length) {
      sourcesList.append(F.element('p', 'sources-empty', 'Tài liệu liên quan sẽ xuất hiện ở đây khi câu trả lời có nguồn tham khảo.')); return;
    }
    for (const source of sources) {
      if (!source || typeof source !== 'object') continue;
      const info = F.sourceInfo(source), card = F.element('article', 'source wf-source-card');
      card.dataset.sourceKind = info.label;
      card.append(F.element('strong', 'wf-source-kind', info.label));
      if (info.title) card.append(F.element('p', 'wf-source-caption', info.title.slice(0, 90) + (info.title.length > 90 ? '…' : '')));
      if (source.subject || source.page != null) card.append(F.element('p', 'meta', [source.subject, source.page != null ? `Trang ${source.page}` : ''].filter(Boolean).join(' · ')));
      card.append(F.element('p', 'chunk', info.preview || 'Chưa có trích đoạn.'));
      if (info.content.length > 180 || info.title.length > 90) {
        const full = F.element('details', 'wf-source-full'); full.append(F.element('summary', '', 'Xem đầy đủ'));
        if (info.title) full.append(F.element('p', 'wf-source-caption', info.title));
        full.append(F.rich('div', '', info.content)); card.append(full);
      }
      if (typeof source.url === 'string' && /^https?:\/\//i.test(source.url)) {
        const link = F.element('a', 'source-link', 'Mở nguồn ↗'); link.href = source.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; card.append(link);
      }
      sourcesList.append(card);
    }
  }

  // ==========================================
  // 6. THÔNG BÁO NGẮN
  // ==========================================

  function showNotice(message) {
    if (!notice) return;

    clearTimeout(noticeTimeout);

    notice.textContent = message;
    notice.hidden = false;

    noticeTimeout = setTimeout(() => {
      notice.hidden = true;
    }, 3500);
  }

  function readConversations() {
    try {
      const stored = localStorage.getItem(historyKey);
      const conversations = stored ? JSON.parse(stored) : [];
      return Array.isArray(conversations) ? conversations : [];
    } catch (error) {
      console.error('EDUAGENT: Không thể đọc lịch sử trò chuyện.', error);
      showNotice('Không thể đọc lịch sử trò chuyện đã lưu.');
      return [];
    }
  }

  function writeConversations(conversations) {
    try {
      localStorage.setItem(historyKey, JSON.stringify(conversations));
      document.dispatchEvent(new CustomEvent('eduagent:history-updated'));
    } catch (error) {
      console.error('EDUAGENT: Không thể lưu lịch sử trò chuyện.', error);
      showNotice('Không thể lưu cuộc trò chuyện trên thiết bị này.');
    }
  }

  function getActiveConversation() {
    return readConversations().find(
      (conversation) => conversation.id === activeConversationId
    );
  }

  function ensureActiveConversation(title) {
    if (activeConversationId) {
      const current = getActiveConversation();
      if (current) return current;
    }

    const conversations = readConversations();
    const conversation = {
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      title: title.slice(0, 64),
      session_id: sessionId, mode, revision,
      messages: [],
      sources: []
    };
    activeConversationId = conversation.id;
    conversations.unshift(conversation);
    writeConversations(conversations.slice(0, 30));
    window.history.replaceState(
      null,
      '',
      `/?conversation=${encodeURIComponent(conversation.id)}`
    );
    return conversation;
  }

  function saveConversationMessage(role, content, sources, payload = null) {
    const conversations = readConversations();
    const conversation = conversations.find(
      (item) => item.id === activeConversationId
    );
    if (!conversation) return;

    conversation.messages.push({ role, content, payload });
    conversation.mode = mode; conversation.revision = revision; conversation.lp_verify = $('#verify-resources').checked;
    if (sources) conversation.sources = sources;
    conversation.session_id = sessionId;
    conversation.updated_at = Date.now();
    conversations.sort(
      (first, second) => (second.updated_at || 0) - (first.updated_at || 0)
    );
    writeConversations(conversations);
  }

  function restoreConversationFromUrl() {
    const params = new URLSearchParams(window.location.search);
    const workflow = params.get('workflow');
    const conversationId = params.get('conversation') || (workflow && readConversations().find(c => c.session_id === workflow)?.id);
    if (!conversationId) return;

    const conversation = readConversations().find(
      (item) => item.id === conversationId
    );
    if (!conversation || !Array.isArray(conversation.messages)) {
      showNotice('Không tìm thấy cuộc trò chuyện đã lưu.');
      return;
    }

    activeConversationId = conversation.id;
    sessionId = conversation.session_id || null;
    mode = conversation.mode || 'qa'; revision = conversation.revision || 0; $('#verify-resources').checked = Boolean(conversation.lp_verify); showMode();
    messages.replaceChildren();
    for (const message of conversation.messages) {
      if (
        message &&
        (message.role === 'user' || message.role === 'bot') &&
        typeof message.content === 'string'
      ) {
        const rendered = appendMessage(message.role, message.content);
        if (message.role === 'bot') F.decorate(rendered.bubble, message.payload || {answer: message.content}, actionSend);
      }
    }
    renderSources(conversation.sources);
    void refreshSession();
  }

  function setPanelVisible(name, visible) {
    const body = document.body;
    const classByName = {
      sidebar: 'sidebar-hidden',
      sources: 'sources-hidden',
      header: 'chat-header-hidden'
    };
    const buttons = document.querySelectorAll(`[data-toggle-view="${name}"]`);
    if (!classByName[name] || buttons.length === 0) return;

    const isCompact = window.matchMedia('(max-width: 760px)').matches;
    if (visible && isCompact && name === 'sidebar') {
      setPanelVisible('sources', false);
    } else if (visible && isCompact && name === 'sources') {
      setPanelVisible('sidebar', false);
    }
    body.classList.toggle(classByName[name], !visible);
    if (name === 'sidebar' || name === 'sources') {
      const variable = name === 'sidebar'
        ? '--chat-sidebar-width'
        : '--chat-source-width';
      if (!visible) {
        appShell.style.removeProperty(variable);
      } else if (panelWidths[name] !== null) {
        setPanelWidth(name, panelWidths[name]);
      }
    }
    const label = {
      sidebar: 'thanh điều hướng',
      sources: 'tài liệu tham khảo',
      header: 'đầu trang'
    }[name];

    buttons.forEach((button) => {
      button.setAttribute(
        'aria-label',
        `${visible ? 'Thu gọn' : 'Mở rộng'} ${label}`
      );
      button.setAttribute('title', `${visible ? 'Thu gọn' : 'Mở rộng'} ${label}`);
      button.setAttribute('aria-expanded', String(visible));
    });
  }

  function isPanelVisible(name) {
    const hiddenClasses = {
      sidebar: 'sidebar-hidden',
      sources: 'sources-hidden',
      header: 'chat-header-hidden'
    };
    return !document.body.classList.contains(hiddenClasses[name]);
  }

  document.querySelectorAll('[data-toggle-view]').forEach((button) => {
    button.addEventListener('click', () => {
      const name = button.dataset.toggleView;
      setPanelVisible(name, !isPanelVisible(name));
    });
  });

  const compactPanels = window.matchMedia('(max-width: 760px)');
  compactPanels.addEventListener('change', (event) => {
    if (event.matches) {
      setPanelVisible('sidebar', false);
      setPanelVisible('sources', false);
    }
  });

  actionToggle.addEventListener('click', () => {
    const isOpen = actionMenu.hidden;
    actionMenu.hidden = !isOpen;
    actionToggle.setAttribute('aria-expanded', String(isOpen));
  });

  document.addEventListener('click', (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;

    if (target.closest('[data-start-chat]')) {
      const text = mode === 'planning' ? 'tôi muốn tạo lộ trình học, hãy hỗ trợ tôi' : mode === 'exam' ? 'tôi muốn tạo bài kiểm tra, hãy hỗ trợ tôi' : 'Chào bạn, hãy hỗ trợ tôi học tập.';
      actionSend(text, 'Thử bắt đầu cuộc trò chuyện', null); return;
    }
    const modeButton = target.closest('[data-mode]');
    if (modeButton && modeButton.closest('#action-menu')) {chooseMode(modeButton.dataset.mode); actionMenu.hidden = true; actionToggle.setAttribute('aria-expanded', 'false'); return;}

    const promptButton = target.closest('[data-action-prompt], [data-prompt]');
    if (promptButton) {
      input.value =
        promptButton.dataset.actionPrompt || promptButton.dataset.prompt || '';
      actionMenu.hidden = true;
      actionToggle.setAttribute('aria-expanded', 'false');
      input.focus();
      input.dispatchEvent(new Event('input', { bubbles: true }));
      return;
    }

    if (target.closest('[data-demo-source]')) {
      showNotice('Tài liệu này chỉ là minh họa; hiện chưa có tệp gốc để mở.');
      return;
    }

    if (!actionMenu.hidden && !target.closest('.composer')) {
      actionMenu.hidden = true;
      actionToggle.setAttribute('aria-expanded', 'false');
    }
  });

  voiceButton.addEventListener('click', () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      showNotice('Trình duyệt này chưa hỗ trợ nhập bằng giọng nói.');
      return;
    }

    if (recognition) {
      recognition.stop();
      return;
    }

    recognition = new SpeechRecognition();
    recognition.lang = 'vi-VN';
    recognition.interimResults = true;
    voiceButton.classList.add('voice-input-active');
    voiceButton.setAttribute('aria-label', 'Dừng nhập bằng giọng nói');

    recognition.addEventListener('result', (event) => {
      const transcript = Array.from(event.results)
        .map((result) => result[0].transcript)
        .join('');
      input.value = transcript;
      input.dispatchEvent(new Event('input', { bubbles: true }));
    });
    recognition.addEventListener('error', (event) => {
      showNotice(`Không thể nhận giọng nói: ${event.error}`);
    });
    recognition.addEventListener('end', () => {
      recognition = null;
      voiceButton.classList.remove('voice-input-active');
      voiceButton.setAttribute('aria-label', 'Nhập bằng giọng nói');
      input.focus();
    });
    try {
      recognition.start();
    } catch (error) {
      recognition = null;
      voiceButton.classList.remove('voice-input-active');
      voiceButton.setAttribute('aria-label', 'Nhập bằng giọng nói');
      showNotice(`Không thể bắt đầu nhập giọng nói: ${error.message}`);
    }
  });

  // ==========================================
  // 7. GỬI TIN NHẮN ĐẾN FASTAPI
  //
  // POST /api/ui/workflows
  // ==========================================

  document.addEventListener('eduagent:compose', e => {
    if (activeController) return;
    input.placeholder = e.detail?.placeholder || 'Nhập yêu cầu của bạn…'; input.focus();
  });
  function updateCurrentSkeleton(payload) {
    const all = readConversations(), c = all.find(x => x.id === activeConversationId);
    if (!c) return;
    const last = [...c.messages].reverse().find(m => m.role === 'bot');
    if (!last || last.payload?.skeleton) return;
    last.content = payload.answer; last.payload = payload; writeConversations(all);
    const bubble = [...messages.querySelectorAll('.message.bot .bubble')].pop();
    if (bubble) {bubble.replaceChildren(F.rich('div', '', payload.answer)); F.decorate(bubble, payload, actionSend);}
  }
  function actionSend(value, label, payload) {
    if (activeController) return;
    if (payload && (payload.session_id !== sessionId || payload.revision !== revision)) {
      showNotice('Nút này thuộc bước cũ. Hãy dùng thao tác ở phản hồi mới nhất.'); return;
    }
    input.value = value; void sendMessage(label);
  }
  function storeSubmission(body) {
    const all = readConversations(), c = all.find(x => x.id === activeConversationId);
    if (c) {c.pending_request = body; c.session_id = sessionId; c.mode = mode; c.revision = revision; writeConversations(all);}
  }
  function storePending(jobId) {
    const all = readConversations(), c = all.find(x => x.id === activeConversationId);
    if (c) {c.pending_request = null; c.pending_job = jobId; c.session_id = sessionId; c.mode = mode; c.revision = revision; writeConversations(all);}
  }
  function acceptResult(payload) {
    sessionId = payload.session_id || sessionId; revision = payload.revision ?? revision;
    const answer = String(payload.answer || 'Đã xử lý xong.');
    const rendered = appendMessage('bot', answer);
    F.decorate(rendered.bubble, payload, actionSend);
    renderSources(payload.sources);
    saveConversationMessage('bot', answer, payload.sources || [], payload);
    storePending(null);
  }
  async function refreshSession() {
    if (!sessionId || activeController) return;
    const expected = sessionId;
    try {
      const pending = getActiveConversation()?.pending_request;
      if (pending) {
        const job = await F.api(`/api/ui/workflows/${sessionId}/messages`, pending);
        if (sessionId !== expected || activeController) return;
        storePending(job.job_id); await watchJob(job.job_id); return;
      }
      const snapshot = await F.api(`/api/ui/workflows/${sessionId}`);
      if (sessionId !== expected) return;
      $('#verify-resources').checked = Boolean(snapshot.lp_verify);
      if (snapshot.student_id) localStorage.setItem('eduagent-student-id', snapshot.student_id);
      if (snapshot.busy || getActiveConversation()?.pending_job) {
        const jid = snapshot.last_job || getActiveConversation()?.pending_job;
        if (jid && !activeController) await watchJob(jid);
      } else if (snapshot.revision > revision) acceptResult(snapshot);
      else if (snapshot.revision === revision && snapshot.skeleton) updateCurrentSkeleton(snapshot);
    } catch (e) {if (e.status) storeSubmission(null); showNotice(e.message);}
  }
  async function watchJob(jid) {
    const controller = new AbortController(), current = ++requestId;
    activeController = controller; sendButton.disabled = input.disabled = true;
    const waiting = startWaiting();
    try {
      const result = await F.poll(jid, waiting.progress, controller.signal);
      await waiting.finish();
      if (current === requestId) acceptResult(result);
    } catch (e) {
      if (e.name !== 'AbortError' && current === requestId) {
        showNotice(e.message); appendMessage('bot', e.message);
        if (e.jobFailed) {storePending(null); const last = [...(getActiveConversation()?.messages || [])].reverse().find(m => m.role === 'user'); if (last) {input.value = last.content; resizeComposer();}}
        // Keep the job id for reconnect; reloading can fetch its final state.
      }
    } finally {
      waiting.stop();
      if (current === requestId) {activeController = null; sendButton.disabled = input.disabled = false;}
    }
  }
  async function sendMessage(displayLabel) {
    if (activeController || !input.value.trim()) return;
    if (getActiveConversation()?.pending_request) {showNotice('Đang khôi phục lượt gửi trước.'); void refreshSession(); return;}
    const text = input.value.trim();
    // Only explicit requests switch workflows; short follow-up answers stay in their branch.
    const normalized = text.toLowerCase();
    if (/^(tôi|mình|em) (muốn|cần) (tạo|lập) (một )?(bài (test|kiểm tra)|đề (thi|kiểm tra))/.test(normalized)) chooseMode('exam');
    else if (/^(tôi|mình|em) (muốn|cần) (tạo|lập) (một )?lộ trình/.test(normalized)) chooseMode('planning');
    input.value = ''; resizeComposer(); ensureActiveConversation(text); $('.chat-demo')?.remove();
    appendMessage('user', displayLabel || text); saveConversationMessage('user', displayLabel || text);
    const controller = new AbortController(), current = ++requestId;
    activeController = controller; sendButton.disabled = input.disabled = true;
    try {
      if (!sessionId) {
        const created = await F.api('/api/ui/workflows', {mode}, controller.signal);
        if (current !== requestId) return;
        sessionId = created.session_id; revision = created.revision;
        localStorage.setItem('eduagent-student-id', created.student_id);
      }
      const requestKey = F.id();
      const body = {message: text, revision, request_id: requestKey, lp_verify: $('#verify-resources').checked};
      storeSubmission(body);
      const job = await F.api(`/api/ui/workflows/${sessionId}/messages`, body, controller.signal);
      if (current !== requestId) return;
      storePending(job.job_id);
      activeController = null;
      await watchJob(job.job_id);
    } catch (e) {
      if (e.name !== 'AbortError' && current === requestId) {
        if (e.status) storeSubmission(null);
        appendMessage('bot', `Không thể gửi: ${e.message}`); input.value = text; resizeComposer();
      }
    } finally {
      if (current === requestId) {activeController = null; sendButton.disabled = input.disabled = false;}
    }
  }

  // ==========================================
  // 8. BẮT SỰ KIỆN GỬI TIN NHẮN
  // ==========================================

  form.addEventListener('submit', (event) => {
    event.preventDefault();

    void sendMessage();
  });

  // Enter để gửi.
  // Shift + Enter để xuống dòng.
  input.addEventListener('keydown', (event) => {
    if (
      event.key === 'Enter' &&
      !event.shiftKey &&
      !event.isComposing
    ) {
      event.preventDefault();

      void sendMessage();
    }
  });

  // ==========================================
  // 9. TẠO CUỘC TRÒ CHUYỆN MỚI
  // ==========================================

  document.addEventListener('eduagent:new-chat', () => {
    // Vô hiệu hóa kết quả request cũ.
    requestId += 1;

    activeController?.abort();
    activeController = null;

    // Reset session.
    sessionId = null; revision = 0; mode = 'qa'; showMode();
    activeConversationId = null;
    window.history.replaceState(null, '', '/');
    document.dispatchEvent(new CustomEvent('eduagent:history-updated'));

    // Xóa hội thoại.
    messages.replaceChildren();
    if (demoMarkup) messages.append(demoMarkup.cloneNode(true));
    showMode();

    // Xóa nguồn tài liệu.
    renderSources([]);
    if (demoSourcesMarkup) {
      sourcesList.replaceChildren(
        ...Array.from(demoSourcesMarkup.childNodes, (node) => node.cloneNode(true))
      );
    }

    connection.textContent = 'Sẵn sàng';

    sendButton.disabled = false;
    input.disabled = false;

    input.value = '';
    resizeComposer();
    input.focus();

    showNotice(
      'Đã bắt đầu cuộc trò chuyện mới.'
    );
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      actionMenu.hidden = true;
      actionToggle.setAttribute('aria-expanded', 'false');
      if (window.matchMedia('(max-width: 760px)').matches) {
        setPanelVisible('sidebar', false);
        setPanelVisible('sources', false);
      }
    }
  });

  if (sourcePanel && chatHeader) {
    const isCompact = compactPanels.matches;
    document.querySelectorAll('[data-toggle-view]').forEach((button) => {
      const name = button.dataset.toggleView;
      const shouldCollapse = isCompact &&
        (name === 'sidebar' || name === 'sources');
      setPanelVisible(name, shouldCollapse ? false : isPanelVisible(name));
    });
  }

  showMode();
  restoreConversationFromUrl();
  const requestedMode = new URLSearchParams(location.search).get('mode');
  if (!activeConversationId && ['qa', 'exam', 'planning'].includes(requestedMode)) chooseMode(requestedMode);
  async function readiness() {
    try {
      const data = await F.api('/api/ui/workflows/readiness');
      if (!activeController) connection.textContent = data.status === 'ready' ? 'Sẵn sàng' : data.status === 'failed' ? 'Chưa kết nối được AI' : 'Đang chuẩn bị trợ lý…';
      if (data.status === 'loading' || data.status === 'idle') setTimeout(readiness, 1500);
    } catch {if (!activeController) connection.textContent = 'Kiểm tra kết nối server';}
  }
  void readiness();
  window.addEventListener('focus', () => {void refreshSession();});

})();