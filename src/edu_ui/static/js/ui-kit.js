/* Small shared view helpers. Mock access is isolated here for a future API adapter. */
(() => {
  'use strict';
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const pct = value => Math.max(0, Math.min(100, Math.round(Number(value) || 0)));
  const date = value => value ? new Date(value.length === 10 ? value + 'T12:00:00' : value).toLocaleString('vi-VN', value.length === 10 ? {dateStyle:'medium'} : {dateStyle:'short',timeStyle:'short'}) : 'Chưa có';
  const status = text => { const node = document.querySelector('#page-status'); if(node) node.textContent = text; };
  const chip = (label, tone='') => `<span class="uk-chip ${esc(tone)}">${esc(label)}</span>`;
  const bar = (label, value) => `<div class="uk-meter"><div><span>${esc(label)}</span><strong>${pct(value)}%</strong></div><progress max="100" value="${pct(value)}" aria-label="${esc(label)}" class="${value < 60 ? 'low' : ''}"></progress></div>`;
  const card = (title, body, action='') => `<section class="uk-card"><header><h2>${esc(title)}</h2>${action}</header>${body}</section>`;
  const edit = (section, index='') => `<button class="uk-button uk-small" data-edit="${esc(section)}" data-index="${esc(index)}">Chỉnh sửa</button>`;
  const kpi = (label, value, note='') => `<div class="uk-kpi"><span>${esc(label)}</span><strong>${esc(value)}</strong><small>${esc(note)}</small></div>`;
  const empty = message => `<p class="uk-empty">${esc(message)}</p>`;
  function tabs(container, items, render, active=items[0][0]) {
    container.innerHTML = `<div class="uk-tabs" role="tablist" aria-label="Các mục">${items.map(([id,title]) => `<button id="tab-${id}" role="tab" aria-controls="panel-main" data-tab="${id}">${esc(title)}</button>`).join('')}</div><section id="panel-main" role="tabpanel" tabindex="0"></section>`;
    const panel = container.querySelector('#panel-main');
    const buttons = [...container.querySelectorAll('[role="tab"]')];
    function select(id) {
      buttons.forEach(b => {b.setAttribute('aria-selected',String(b.dataset.tab===id)); b.tabIndex=b.dataset.tab===id?0:-1;});
      panel.setAttribute('aria-labelledby',`tab-${id}`); render(id,panel);
    }
    buttons.forEach((b,index) => {
      b.onclick=()=>select(b.dataset.tab);
      b.onkeydown=e=>{
        let next=index;
        if(e.key==='ArrowRight') next=(index+1)%buttons.length;
        else if(e.key==='ArrowLeft') next=(index+buttons.length-1)%buttons.length;
        else if(e.key==='Home') next=0; else if(e.key==='End') next=buttons.length-1; else return;
        e.preventDefault(); buttons[next].focus(); select(buttons[next].dataset.tab);
      };
    });
    select(active); return select;
  }
  async function load(kind) {
    if(!['profile','progress'].includes(kind)) throw Error('Nguồn dữ liệu không hợp lệ.');
    const controller=new AbortController(); const timer=setTimeout(()=>controller.abort(),10000);
    try {
      const response=await fetch(`/ui-demo/${kind}_demo.json`,{signal:controller.signal,cache:'no-store'});
      if(!response.ok) throw Error('Không tải được dữ liệu mẫu.');
      return await response.json();
    } finally {clearTimeout(timer);}
  }
  function download(name, data) {
    const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json;charset=utf-8'}));
    const a=document.createElement('a'); a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  window.StudentUI={esc,pct,date,status,chip,bar,card,edit,kpi,empty,tabs,download,dataSource:{load}};
})();
