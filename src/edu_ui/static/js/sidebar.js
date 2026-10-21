(() => {
  'use strict';

  const historyKey = 'eduagent-chat-history';
  const sidebar = document.querySelector('.app-shell > .sidebar');
  const appShell = document.querySelector('.app-shell');
  const toggle = document.querySelector('#sidebar-toggle');
  const resizer = document.querySelector('[data-resize-panel="sidebar"]');
  const historyList = document.querySelector('#conversation-history');
  const notice = document.querySelector('#toast');

  if (!sidebar || !appShell || !toggle || !resizer) return;

  let savedWidth = null;
  let noticeTimeout;
  const widthVariable = document.body.classList.contains('chat-body')
    ? '--chat-sidebar-width'
    : '--sidebar-width';
  const compactLayout = window.matchMedia('(max-width: 760px)');

  function showNotice(message) {
    if (!notice) return;
    clearTimeout(noticeTimeout);
    notice.textContent = message;
    notice.hidden = false;
    noticeTimeout = setTimeout(() => {
      notice.hidden = true;
    }, 3200);
  }

  function getHistory() {
    try {
      const stored = localStorage.getItem(historyKey);
      const parsed = stored ? JSON.parse(stored) : [];
      return Array.isArray(parsed)
        ? parsed.filter((item) =>
          item &&
          typeof item.id === 'string' &&
          typeof item.title === 'string'
        )
        : [];
    } catch (error) {
      console.error('EDUAGENT: Không thể đọc lịch sử trò chuyện.', error);
      showNotice('Không thể tải lịch sử trò chuyện đã lưu.');
      return [];
    }
  }

  function renderHistory() {
    if (!historyList) return;
    const conversations = getHistory();
    const activeId = new URLSearchParams(window.location.search)
      .get('conversation');

    if (!conversations.length) {
      const empty = document.createElement('p');
      empty.className = 'history-empty';
      empty.textContent = 'Các cuộc trò chuyện mới sẽ xuất hiện ở đây.';
      historyList.replaceChildren(empty);
      return;
    }

    const links = conversations.map((conversation) => {
      const link = document.createElement('a');
      link.className = 'history-item';
      link.href = `/?conversation=${encodeURIComponent(conversation.id)}`;
      link.textContent = conversation.title;
      link.title = conversation.title;
      if (conversation.id === activeId) {
        link.setAttribute('aria-current', 'page');
      }
      return link;
    });
    historyList.replaceChildren(...links);
  }

  function setCollapsed(collapsed) {
    const current = Number.parseFloat(
      getComputedStyle(appShell).getPropertyValue(widthVariable)
    );

    if (collapsed) {
      if (!document.body.classList.contains('sidebar-hidden')) {
        savedWidth = current;
      }
      document.body.classList.add('sidebar-hidden');
      appShell.style.removeProperty(widthVariable);
    } else {
      document.body.classList.remove('sidebar-hidden');
      if (savedWidth !== null) {
        appShell.style.setProperty(widthVariable, `${savedWidth}px`);
      }
    }

    const expanded = !collapsed;
    toggle.setAttribute('aria-expanded', String(expanded));
    toggle.setAttribute(
      'aria-label',
      `${expanded ? 'Thu gọn' : 'Mở rộng'} thanh điều hướng`
    );
    toggle.title = `${expanded ? 'Thu gọn' : 'Mở rộng'} thanh điều hướng`;
  }

  function getWidthBounds() {
    const compact = compactLayout.matches;
    const minimum = compact ? 140 : 180;
    const maximum = Math.max(
      minimum,
      Math.min(compact ? 320 : 460, window.innerWidth - (compact ? 220 : 500))
    );
    return { minimum, maximum };
  }

  function setWidth(requestedWidth) {
    const { minimum, maximum } = getWidthBounds();
    const width = Math.round(Math.min(maximum, Math.max(minimum, requestedWidth)));
    savedWidth = width;
    appShell.style.setProperty(widthVariable, `${width}px`);
    resizer.setAttribute('aria-valuemin', String(minimum));
    resizer.setAttribute('aria-valuemax', String(maximum));
    resizer.setAttribute('aria-valuenow', String(width));
  }

  function resizeByPointer(event) {
    if (event.button !== 0 || document.body.classList.contains('sidebar-hidden')) return;
    event.preventDefault();
    resizer.classList.add('is-dragging');

    const move = (pointerEvent) => setWidth(pointerEvent.clientX);
    const finish = () => {
      resizer.classList.remove('is-dragging');
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', finish);
      window.removeEventListener('pointercancel', finish);
    };

    move(event);
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', finish, { once: true });
    window.addEventListener('pointercancel', finish, { once: true });
  }

  toggle.addEventListener('click', () => {
    setCollapsed(!document.body.classList.contains('sidebar-hidden'));
  });

  resizer.addEventListener('pointerdown', resizeByPointer);
  resizer.addEventListener('keydown', (event) => {
    if (
      document.body.classList.contains('sidebar-hidden') ||
      (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight')
    ) {
      return;
    }
    event.preventDefault();
    const width = savedWidth ?? Number.parseFloat(
      getComputedStyle(appShell).getPropertyValue(widthVariable)
    );
    setWidth(width + (event.key === 'ArrowRight' ? 1 : -1) * (event.shiftKey ? 32 : 12));
  });

  compactLayout.addEventListener('change', (event) => {
    setCollapsed(event.matches);
  });

  document.querySelectorAll('[data-soon]').forEach((link) => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      showNotice(`${link.dataset.soon}: chức năng đang được phát triển.`);
    });
  });

  document.addEventListener('click', (event) => {
    const newChat = event.target instanceof Element
      ? event.target.closest('#new-chat')
      : null;
    if (!newChat) return;

    if (document.body.classList.contains('chat-body')) {
      event.preventDefault();
      document.dispatchEvent(new CustomEvent('eduagent:new-chat'));
      return;
    }
    window.location.assign('/');
  });

  document.addEventListener('eduagent:history-updated', renderHistory);
  renderHistory();
  if (compactLayout.matches) setCollapsed(true);
})();
