/* EDUAGENT chat: no avatars/icons, student left, assistant right.
   API: POST /api/ui/chat
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
    bubble.textContent = content;

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

  function formatEduTime(elapsedSeconds) {
    const whole = Math.max(
      0,
      Math.floor(elapsedSeconds)
    );

    const minutes = Math.floor(whole / 90);
    const seconds = whole % 90;

    return (
      String(minutes).padStart(2, '0') +
      ':' +
      String(seconds).padStart(2, '0')
    );
  }

  // ==========================================
  // 4. HIỆU ỨNG CHỜ BOT
  //
  // - Hiển thị 3 dấu chấm chuyển động
  // - Sau 2 giây mới hiện đồng hồ
  // - Đồng hồ cập nhật theo thời gian chờ
  // ==========================================

  function startWaiting() {
    const startedAt = performance.now();

    const waiting = appendMessage('bot');

    const dots = document.createElement('span');
    dots.className = 'typing-dots';

    dots.setAttribute('role', 'status');
    dots.setAttribute(
      'aria-label',
      'Trợ lý đang trả lời'
    );

    for (let i = 0; i < 3; i += 1) {
      dots.appendChild(
        document.createElement('span')
      );
    }

    waiting.bubble.appendChild(dots);

    connection.textContent = 'Đang trả lời...';

    let stopped = false;
    let elapsed = null;

    // Sau 2 giây mới xuất hiện đồng hồ.
    const showTimerTimeout = setTimeout(() => {
      if (stopped) return;

      elapsed = document.createElement('div');
      elapsed.className = 'elapsed';

      elapsed.setAttribute(
        'aria-label',
        'Thời gian chờ'
      );

      elapsed.textContent = formatEduTime(
        (performance.now() - startedAt) / 1000
      );

      waiting.wrap.appendChild(elapsed);

      scrollToLatest();
    }, 2000);

    // Cập nhật hiển thị mỗi 200 ms.
    // Giá trị thời gian được làm tròn xuống theo giây.
    const updateInterval = setInterval(() => {
      if (stopped || !elapsed) return;

      elapsed.textContent = formatEduTime(
        (performance.now() - startedAt) / 1000
      );
    }, 200);

    return {
      stop() {
        if (stopped) return;

        stopped = true;

        clearTimeout(showTimerTimeout);
        clearInterval(updateInterval);

        waiting.wrap.remove();

        connection.textContent = 'Sẵn sàng';
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

    if (
      !Array.isArray(sources) ||
      sources.length === 0
    ) {
      const empty = document.createElement('p');
      empty.className = 'sources-empty';

      empty.textContent =
        'Câu trả lời vừa rồi chưa có nguồn tài liệu được backend trả về.';

      sourcesList.appendChild(empty);
      return;
    }

    for (const source of sources) {
      if (
        !source ||
        typeof source !== 'object'
      ) {
        continue;
      }

      const card = document.createElement('article');
      card.className = 'source';

      // Tên tài liệu
      const title = document.createElement('strong');

      title.textContent = String(
        source.title ||
        source.document_name ||
        source.source ||
        'Tài liệu'
      );

      card.appendChild(title);

      // Metadata
      const metadata = [
        source.subject,

        source.chapter_id != null
          ? `Chương ${source.chapter_id}`
          : null,

        source.page != null
          ? `Trang ${source.page}`
          : null
      ].filter(Boolean);

      if (metadata.length) {
        const meta = document.createElement('div');
        meta.className = 'meta';

        meta.textContent = metadata.join(' · ');

        card.appendChild(meta);
      }

      // Nội dung chunk
      const snippet = document.createElement('p');
      snippet.className = 'chunk';

      snippet.textContent = String(
        source.chunk ||
        source.content ||
        source.text ||
        'Không có trích đoạn.'
      );

      card.appendChild(snippet);

      // Liên kết tài liệu nếu có
      if (
        typeof source.url === 'string' &&
        /^(https?:\/\/|\/)/i.test(source.url)
      ) {
        const link = document.createElement('a');

        link.href = source.url;
        if (/^https?:\/\//i.test(source.url)) {
          link.target = '_blank';
          link.rel = 'noopener noreferrer';
        }
        link.className = 'source-link';

        link.textContent = 'Mở tài liệu gốc ↗';

        card.appendChild(link);
      } else {
        const unavailable = document.createElement('p');
        unavailable.className = 'source-disclaimer';
        unavailable.textContent = 'Backend chưa cung cấp liên kết tài liệu gốc.';
        card.appendChild(unavailable);
      }

      sourcesList.appendChild(card);
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
      session_id: sessionId,
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

  function saveConversationMessage(role, content, sources) {
    const conversations = readConversations();
    const conversation = conversations.find(
      (item) => item.id === activeConversationId
    );
    if (!conversation) return;

    conversation.messages.push({ role, content });
    if (sources) conversation.sources = sources;
    conversation.session_id = sessionId;
    conversation.updated_at = Date.now();
    conversations.sort(
      (first, second) => (second.updated_at || 0) - (first.updated_at || 0)
    );
    writeConversations(conversations);
  }

  function restoreConversationFromUrl() {
    const conversationId = new URLSearchParams(window.location.search)
      .get('conversation');
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
    messages.replaceChildren();
    for (const message of conversation.messages) {
      if (
        message &&
        (message.role === 'user' || message.role === 'bot') &&
        typeof message.content === 'string'
      ) {
        appendMessage(message.role, message.content);
      }
    }
    renderSources(conversation.sources);
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
  // POST /api/ui/chat
  // ==========================================

  async function sendMessage() {
    if (
      activeController ||
      !input.value.trim()
    ) {
      return;
    }

    const text = input.value.trim();

    input.value = '';
    resizeComposer();

    ensureActiveConversation(text);
    $('.chat-demo')?.remove();

    // Tin nhắn học sinh nằm bên trái.
    appendMessage('user', text);
    saveConversationMessage('user', text);

    sendButton.disabled = true;
    input.disabled = true;

    // Cho phép hủy request khi tạo chat mới.
    const controller = new AbortController();

    activeController = controller;

    const currentRequest = ++requestId;

    // Bắt đầu 3 dấu chấm và đồng hồ chờ.
    const waiting = startWaiting();

    try {
      const response = await fetch('/api/ui/chat', {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({
          session_id: sessionId,
          message: text
        }),

        signal: controller.signal
      });

      const payload = await response
        .json()
        .catch(() => ({}));

      if (!response.ok) {
        throw new Error(
          payload.detail ||
          `HTTP ${response.status}`
        );
      }

      // Không xử lý kết quả request đã bị thay thế.
      if (currentRequest !== requestId) {
        return;
      }

      // Cập nhật session.
      sessionId =
        payload.session_id || sessionId;

      // Dừng hiệu ứng chờ.
      waiting.stop();

      // Tin nhắn Bot nằm bên phải.
      appendMessage(
        'bot',
        String(
          payload.answer ||
          'Trợ lý chưa có phản hồi.'
        )
      );

      // Hiển thị nguồn tài liệu bên phải.
      renderSources(payload.sources);
      saveConversationMessage(
        'bot',
        String(payload.answer || 'Trợ lý chưa có phản hồi.'),
        Array.isArray(payload.sources) ? payload.sources : []
      );

    } catch (error) {
      waiting.stop();

      if (
        error.name !== 'AbortError' &&
        currentRequest === requestId
      ) {
        appendMessage(
          'bot',
          `Không thể nhận phản hồi: ${error.message}`
        );
      }

    } finally {
      waiting.stop();

      if (currentRequest === requestId) {
        activeController = null;

        sendButton.disabled = false;
        input.disabled = false;

        input.focus();
      }
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
    sessionId = null;
    activeConversationId = null;
    window.history.replaceState(null, '', '/');
    document.dispatchEvent(new CustomEvent('eduagent:history-updated'));

    // Xóa hội thoại.
    messages.replaceChildren();
    if (demoMarkup) messages.append(demoMarkup.cloneNode(true));

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

  restoreConversationFromUrl();

})();