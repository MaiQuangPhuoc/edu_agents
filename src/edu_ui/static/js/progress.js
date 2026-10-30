(() => {
  'use strict';
  const U=window.StudentUI,root=document.querySelector('#page-content');if(!root)return;
  let data,subject='',order='weak',activity='all';
  const tabs=[['overview','Tổng quan'],['subjects','Theo môn & chương'],['tests','Bài test'],['activity','Hoạt động'],['ai','AI theo dõi'],['reports','Báo cáo']];
  function subjectSelect(){return `<select class="uk-select" id="progress-subject" aria-label="Lọc môn học"><option value="">Tất cả môn</option>${data.subjects.map(s=>`<option ${subject===s.name?'selected':''} value="${U.esc(s.name)}">${U.esc(s.name)}</option>`).join('')}</select>`;}
  function trend(attempts){
    if(!attempts.length)return U.empty('Chưa có bài test mẫu khớp bộ lọc.');
    const sorted=[...attempts].sort((a,b)=>a.submitted_at.localeCompare(b.submitted_at));
    const points=sorted.map((a,i)=>({x:sorted.length===1?260:45+i*430/(sorted.length-1),y:160-U.pct(a.percent)*1.25,a}));
    return `<svg class="progress-trend" viewBox="0 0 520 205" role="img" aria-label="Xu hướng điểm test mẫu từ 0 đến 10">${[0,50,100].map(v=>`<line x1="35" x2="490" y1="${160-v*1.25}" y2="${160-v*1.25}" stroke="currentColor" opacity=".12"/><text x="5" y="${165-v*1.25}">${v/10}</text>`).join('')}<polyline points="${points.map(p=>`${p.x},${p.y}`).join(' ')}" fill="none" stroke="currentColor" stroke-width="3"/>${points.map(p=>`<circle cx="${p.x}" cy="${p.y}" r="5" fill="currentColor"><title>${U.esc(p.a.title)}: ${p.a.percent/10}/10</title></circle><text x="${p.x}" y="${p.y-13}" text-anchor="middle">${p.a.percent/10}</text><text x="${p.x}" y="190" text-anchor="middle">${U.esc(p.a.submitted_at.slice(5,10).split('-').reverse().join('/'))}</text>`).join('')}</svg>`;
  }
  function table(head,rows){return `<div class="uk-table-wrap"><table class="uk-table"><thead><tr>${head.map(h=>`<th scope="col">${U.esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.join('')}</tbody></table></div>`;}
  function overview(){
    const complete=data.subjects.reduce((sum,s)=>sum+s.completed,0),total=data.subjects.reduce((sum,s)=>sum+s.total,0);
    const average=data.attempts.length?data.attempts.reduce((sum,a)=>sum+a.percent,0)/data.attempts.length/10:null;
    return `<div class="uk-stats">${U.kpi('Buổi đã học',`${complete}/${total}`)}${U.kpi('Hoàn thành',total?Math.round(complete/total*100)+'%':'0%')}${U.kpi('Chuỗi ngày học',data.streak+' ngày')}${U.kpi('Điểm TB bài test',average===null?'—':average.toFixed(1)+'/10','Trung bình các lượt làm mẫu')}</div><div class="uk-grid">`+
      U.card('Tiến độ theo môn',data.subjects.map(s=>{const percent=U.pct(s.completed/s.total*100);return `<div class="progress-subject"><div class="progress-ring" style="--percent:${percent}%" role="img" aria-label="${U.esc(s.name)} hoàn thành ${percent}%"><span>${percent}%</span></div><div><h3>${U.esc(s.name)}</h3><p>${s.completed}/${s.total} buổi đã học</p></div></div>`;}).join(''))+
      U.card('Tuần học minh họa',`<p class="uk-muted">Tuần 26/10–01/11/2026; mốc dữ liệu: ${U.date(data.as_of)}.</p>${data.week.map(s=>`<div class="uk-row"><div><strong>${U.esc(s.lesson)}</strong><p class="uk-muted">${U.esc(s.subject)} · ${U.date(s.date)} · ${U.esc(s.time)}</p></div>${U.chip(s.completed?'Đã học':'Sắp tới',s.completed?'':'warm')}</div>`).join('')}<a class="uk-button" href="/schedule">Mở lịch học thật</a>`)+`</div>`;
  }
  function subjects(){
    const cards=data.subjects.filter(s=>!subject||s.name===subject).map(s=>{
      const chapters=[...s.chapters];if(order==='weak')chapters.sort((a,b)=>a.muc_nam-b.muc_nam);
      return U.card(s.name,chapters.map(c=>U.bar(c.ten,c.muc_nam*100)+(c.muc_nam<.6?'<p class="uk-muted">Gợi ý minh họa: ôn kiến thức nền và luyện một nhóm bài ngắn.</p>':'')).join(''));
    });
    return `<div class="uk-actions">${subjectSelect()}<select id="chapter-order" class="uk-select" aria-label="Sắp xếp chương"><option value="weak" ${order==='weak'?'selected':''}>Yếu nhất trước</option><option value="original" ${order==='original'?'selected':''}>Thứ tự chương</option></select></div><p class="uk-muted">Mức nắm là số liệu mẫu; chưa được cập nhật từ bài học thật.</p><div class="uk-grid">${cards.join('')||U.empty('Chưa có dữ liệu môn này.')}</div>`;
  }
  function tests(){
    const attempts=data.attempts.filter(a=>!subject||a.subject===subject);
    const mistakes=data.mistakes.filter(a=>!subject||a.subject===subject);
    return `<div class="uk-actions">${subjectSelect()}<a class="uk-button" href="/exams">Đến trang làm bài test</a></div><div class="uk-grid" style="margin-top:18px">`+
      U.card('Xu hướng điểm mẫu',trend(attempts))+U.card('Chủ đề hay sai',mistakes.map(m=>`<div class="uk-row"><div><strong>${U.esc(m.topic)}</strong><p class="uk-muted">${U.esc(m.subject)}</p></div>${U.chip(m.count+' lỗi mẫu','warm')}</div>`).join('')||U.empty('Chưa có thống kê lỗi.'))+`</div>`+
      U.card('Các lượt làm mẫu',attempts.length?table(['Bài test','Môn học','Kết quả','Điểm','Thời gian'],[...attempts].sort((a,b)=>b.submitted_at.localeCompare(a.submitted_at)).map(a=>`<tr><td>${U.esc(a.title)}</td><td>${U.esc(a.subject)}</td><td>${a.correct}/${a.total}</td><td>${a.percent/10}/10</td><td>${U.date(a.submitted_at)}</td></tr>`)):U.empty('Chưa có lượt làm phù hợp.'));
  }
  function activities(){
    const labels={qa:'Hỏi đáp',exam:'Bài test',session:'Buổi học'};
    const events=data.activities.filter(e=>activity==='all'||e.type===activity).sort((a,b)=>b.at.localeCompare(a.at));
    return `<div class="uk-actions"><select id="activity-type" class="uk-select" aria-label="Lọc loại hoạt động">${[['all','Tất cả hoạt động'],...Object.entries(labels)].map(([v,l])=>`<option value="${v}" ${activity===v?'selected':''}>${l}</option>`).join('')}</select></div><div style="margin-top:18px">`+U.card('Dòng thời gian mẫu',events.length?`<div class="progress-timeline">${events.map(e=>`<article class="progress-event">${U.chip(labels[e.type])}<small class="uk-muted">${U.date(e.at)}</small><h3>${U.esc(e.title)}</h3><p>${U.esc(e.detail)}</p></article>`).join('')}</div>`:U.empty('Không có hoạt động thuộc loại đã chọn.'))+'</div>';
  }
  function render(id,panel){
    panel.innerHTML=id==='overview'?overview():id==='subjects'?subjects():id==='tests'?tests():id==='activity'?activities():window.ProgressFuture.render(id,data);
    panel.querySelector('#progress-subject')?.addEventListener('change',e=>{subject=e.target.value;render(id,panel);});
    panel.querySelector('#chapter-order')?.addEventListener('change',e=>{order=e.target.value;render(id,panel);});
    panel.querySelector('#activity-type')?.addEventListener('change',e=>{activity=e.target.value;render(id,panel);});
  }
  async function init(){
    U.status('Đang tải dữ liệu mẫu…');
    try{data=await U.dataSource.load('progress');U.tabs(root,tabs,render);U.status('Toàn bộ số liệu, cảnh báo và báo cáo trên trang này là minh họa.');}
    catch(error){U.status(error.name==='AbortError'?'Tải dữ liệu quá lâu. Vui lòng thử lại.':error.message);root.innerHTML='<button class="uk-button">Thử lại</button>';root.querySelector('button').onclick=init;}
  }
  init();
})();
