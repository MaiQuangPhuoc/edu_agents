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
  const notice = $('#notice');
  const newChatButton = $('#new-chat');
  const sourcePanel = $('.sources-panel');
  const chatHeader = $('.chat-header');

  if (
    ![
      messages,
      form,
      input,
      sendButton,
      sourcesList,
      connection,
      newChatButton
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
        'Chưa có nguồn được backend trả về cho câu trả lời này.';

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
      const snippet = document.createElement('div');
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
        /^https?:\/\//i.test(source.url)
      ) {
        const link = document.createElement('a');

        link.href = source.url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';

        link.textContent = 'Xem nguồn tài liệu';

        card.appendChild(link);
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
    }, 3000);
  }

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

    $('.welcome')?.remove();

    // Tin nhắn học sinh nằm bên trái.
    appendMessage('user', text);

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

  newChatButton.addEventListener('click', () => {
    // Vô hiệu hóa kết quả request cũ.
    requestId += 1;

    activeController?.abort();
    activeController = null;

    // Reset session.
    sessionId = null;

    // Xóa hội thoại.
    messages.replaceChildren();

    // Xóa nguồn tài liệu.
    renderSources([]);

    connection.textContent = 'Sẵn sàng';

    sendButton.disabled = false;
    input.disabled = false;

    input.value = '';
    input.focus();

    showNotice(
      'Đã bắt đầu cuộc trò chuyện mới.'
    );
  });

  // ==========================================
  // 10. CÁC CHỨC NĂNG CHƯA TRIỂN KHAI
  // ==========================================

  document
    .querySelectorAll('[data-soon]')
    .forEach((element) => {
      element.addEventListener('click', (event) => {
        event.preventDefault();

        showNotice(
          `${element.dataset.soon}: chức năng đang được phát triển.`
        );
      });
    });

  // ==========================================
  // 11. HIỂN THỊ CỘT NGUỒN TRÊN MOBILE
  // ==========================================

  if (sourcePanel && chatHeader) {
    const toggle = document.createElement('button');

    toggle.type = 'button';
    toggle.className = 'sources-toggle';

    toggle.textContent = 'Nguồn tài liệu';

    toggle.setAttribute(
      'aria-expanded',
      'false'
    );

    chatHeader.appendChild(toggle);

    toggle.addEventListener('click', () => {
      const visible =
        sourcePanel.classList.toggle('is-open');

      toggle.setAttribute(
        'aria-expanded',
        String(visible)
      );
    });
  }

})();