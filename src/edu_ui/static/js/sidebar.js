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
    closeHistoryMenu();
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
      const row = document.createElement('div');
      row.className = 'history-row';
      const link = document.createElement('a');
      link.className = 'history-item';
      link.href = `/?conversation=${encodeURIComponent(conversation.id)}`;
      link.textContent = conversation.title;
      link.title = conversation.title;
      if (conversation.id === activeId) {
        link.setAttribute('aria-current', 'page');
      }
      const more = document.createElement('button');
      more.type = 'button';
      more.className = 'history-more';
      more.dataset.historyMore = conversation.id;
      more.textContent = '⋯';
      more.title = 'Tùy chọn cuộc trò chuyện';
      more.setAttribute('aria-label', `Tùy chọn: ${conversation.title}`);
      more.setAttribute('aria-haspopup', 'true');
      more.setAttribute('aria-expanded', 'false');
      more.setAttribute('aria-controls', 'history-context-menu');
      row.append(link, more);
      return row;
    });
    historyList.replaceChildren(...links);
  }

  // Attach to body so the menu isn't clipped by the scrolling history list.
  const historyMenu = document.createElement('div');
  historyMenu.id = 'history-context-menu';
  historyMenu.className = 'history-context-menu';
  historyMenu.hidden = true;
  let menuTrigger = null;
  for (const [action, label] of [['rename', 'Đổi tên'], ['delete', 'Xóa cuộc trò chuyện']]) {
    const item = document.createElement('button');
    item.type = 'button';
    item.dataset.historyAction = action;
    item.textContent = label;
    historyMenu.append(item);
  }
  document.body.append(historyMenu);

  function closeHistoryMenu(restoreFocus = false) {
    if (!menuTrigger) return;
    const previous = menuTrigger;
    previous.setAttribute('aria-expanded', 'false');
    historyMenu.hidden = true;
    menuTrigger = null;
    if (restoreFocus && previous.isConnected) previous.focus();
  }

  historyList?.addEventListener('click', (event) => {
    const trigger = event.target.closest('[data-history-more]');
    if (!trigger) return;
    const alreadyOpen = menuTrigger === trigger;
    closeHistoryMenu();
    if (alreadyOpen) return;
    menuTrigger = trigger;
    trigger.setAttribute('aria-expanded', 'true');
    historyMenu.querySelectorAll('button').forEach(button => {
      button.dataset.conversationId = trigger.dataset.historyMore;
    });
    historyMenu.hidden = false;
    const rect = trigger.getBoundingClientRect();
    const box = historyMenu.getBoundingClientRect();
    historyMenu.style.left = `${Math.max(8, Math.min(rect.right - box.width, innerWidth - box.width - 8))}px`;
    historyMenu.style.top = `${Math.max(8, Math.min(rect.bottom + 5, innerHeight - box.height - 8))}px`;
    historyMenu.querySelector('button').focus();
  });
  document.addEventListener('click', event => {
    if (!historyMenu.contains(event.target) && !event.target.closest('[data-history-more]')) closeHistoryMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuTrigger) { event.preventDefault(); closeHistoryMenu(true); }
  });
  window.addEventListener('resize', () => closeHistoryMenu());
  document.addEventListener('scroll', () => closeHistoryMenu(), true);

  historyMenu.addEventListener('click', (event) => {
    const button = event.target.closest('[data-history-action]');
    if (!button) return;
    const id = button.dataset.conversationId;
    const action = button.dataset.historyAction;
    closeHistoryMenu(true);
    const conversation = getHistory().find(item => item.id === id);
    if (!conversation) return;
    let title;
    if (action === 'rename') {
      title = window.prompt('Tên cuộc trò chuyện:', conversation.title);
      if (title === null) return;
      title = title.trim().slice(0, 120);
      if (!title) { showNotice('Tên cuộc trò chuyện không được để trống.'); return; }
    } else if (!window.confirm(`Xóa lịch sử “${conversation.title}” trên thiết bị này? Lộ trình và bài kiểm tra đã lưu vẫn được giữ.`)) {
      return;
    }
    // Read again after the dialog to preserve any messages saved meanwhile.
    const conversations = getHistory();
    const current = conversations.find(item => item.id === id);
    if (!current) return;
    const updated = action === 'delete' ? conversations.filter(item => item.id !== id) : conversations;
    if (action === 'rename') current.title = title;
    try {
      localStorage.setItem(historyKey, JSON.stringify(updated));
    } catch {
      showNotice('Không thể lưu thay đổi lịch sử trên thiết bị này.'); return;
    }
    if (action === 'delete' && new URLSearchParams(location.search).get('conversation') === id) {
      document.dispatchEvent(new CustomEvent('eduagent:new-chat'));
    }
    document.dispatchEvent(new CustomEvent('eduagent:history-updated'));
    showNotice(action === 'delete' ? 'Đã xóa cuộc trò chuyện.' : 'Đã đổi tên cuộc trò chuyện.');
  });
  window.addEventListener('storage', (event) => {
    if (event.key === historyKey) renderHistory();
  });

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
