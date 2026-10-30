(() => {
  'use strict';
  const U=window.StudentUI;
  const root=document.querySelector('#page-content'); if(!root)return;
  let data,active='overview',dirty=false,baseline;
  const tabs=[['overview','Tổng quan'],['ability','Năng lực'],['goals','Mục tiêu'],['learning','Cách học & lịch'],['achievements','Thành tích'],['account','Tài khoản']];
  const tags=(values,tone='')=>values.map(x=>U.chip(x,tone)).join('');
  function weeks(deadline){return Math.max(0,Math.ceil((new Date(deadline+'T12:00:00')-new Date(data.as_of+'T12:00:00'))/604800000));}
  function identity(){
    const p=data.ca_nhan;
    const initials=p.ho_ten.split(/\s+/).slice(-2).map(x=>x[0]).join('');
    return U.card('Thông tin của bạn',`<div class="profile-identity"><span class="profile-avatar">${U.esc(initials)}</span><div><h2>${U.esc(p.ho_ten)}</h2><p>Học sinh khối ${U.esc(p.khoi_lop)}</p></div></div>`,U.edit('identity'));
  }
  function goal(g,index){return U.card(g.mon_hoc,`<p><strong>${U.esc(g.diem_muc_tieu)} / 10 điểm</strong> ${U.chip('Ưu tiên '+g.uu_tien)}</p><p>Hạn chót: ${U.date(g.han_chot)} · Còn ${weeks(g.han_chot)} tuần</p><p>${U.esc(g.dang_bai)}</p>`,U.edit('goal',index));}
  function ability(n,index){return U.card(n.mon_hoc,`<p>Điểm hiện tại: <strong>${U.esc(n.diem_hien_tai)} / 10</strong></p>${n.da_test_dau_vao?U.chip('Đã test đầu vào'):U.chip('Chưa test đầu vào','warm')}<h3>Điểm mạnh</h3>${tags(n.manh)}<h3>Cần củng cố</h3>${tags(n.yeu,'warm')}${n.chu_de.map(c=>U.bar(c.ten,c.muc_nam*100)).join('')}<p class="uk-muted">Mức nắm chương là dữ liệu mẫu, không tự đổi theo điểm bạn chỉnh.</p>`,U.edit('ability',index));}
  function learning(){
    const prefs=data.so_thich_hoc;
    const labels={tai_lieu:'Dùng tài liệu',video:'Học qua video',bai_tap:'Bài tập sau buổi',tom_tat:'Tóm tắt cuối buổi'};
    return U.card('Cách học của bạn',Object.entries(labels).map(([key,label])=>`<label class="profile-switch">${label}<input type="checkbox" role="switch" aria-label="${label}" data-preference="${key}" ${prefs[key]?'checked':''}></label>`).join(''),U.edit('preferences'))+
      U.card('Khung giờ học mỗi tuần',`<p>${data.lich_hoc.so_buoi} buổi / tuần · ${data.lich_hoc.thoi_luong} phút / buổi</p><div class="uk-table-wrap"><div class="profile-week">${['Thứ 2','Thứ 3','Thứ 4','Thứ 5','Thứ 6','Thứ 7','Chủ nhật'].map((label,day)=>{
        const slot=data.lich_hoc.slots.find(s=>s.day===day);
        return `<div class="profile-day ${slot?'active':''}"><strong>${label}</strong><small>${slot?U.esc(slot.start)+'<br>'+U.esc(slot.end):'Chưa chọn'}</small></div>`;
      }).join('')}</div></div>`,U.edit('schedule'));
  }
  function render(id,panel){
    active=id;
    if(id==='overview') panel.innerHTML=identity()+`<div class="uk-stats">${U.kpi('Môn đang học',data.nang_luc.length)}${U.kpi('Hoàn thành',Math.round(data.tien_do.completed/data.tien_do.total*100)+'%')}${U.kpi('Buổi đã học',`${data.tien_do.completed}/${data.tien_do.total}`)}${U.kpi('Chuỗi ngày học',data.tien_do.streak+' ngày')}</div><div class="uk-grid">${goal(data.muc_tieu[0],0)}${U.card('Điều bạn yêu thích',tags(data.ca_nhan.so_thich))}</div>`;
    if(id==='ability') panel.innerHTML=`<div class="uk-grid">${data.nang_luc.map(ability).join('')}</div>`;
    if(id==='goals') panel.innerHTML=`<p class="uk-muted">Số tuần tính theo ngày mẫu ${U.date(data.as_of)}.</p><div class="uk-grid">${data.muc_tieu.map(goal).join('')}</div>`;
    if(id==='learning') panel.innerHTML=learning();
    if(id==='achievements') panel.innerHTML=U.card('Thành tích · Sắp có',`<p class="uk-muted">Huy hiệu minh họa; chưa có hệ thống trao huy hiệu tự động.</p>${data.badges.map(b=>`<div class="uk-row"><span class="profile-medal" aria-hidden="true">✦</span><div><strong>${U.esc(b.title)}</strong><p>${U.esc(b.detail)}</p></div>${U.chip('Minh họa')}</div>`).join('')}`);
    if(id==='account') panel.innerHTML=U.card('Tài khoản & bản nháp',`<p>Mã học sinh mẫu: <strong>${U.esc(data.student_id)}</strong></p><p>Chỉnh sửa chưa được gửi lên hệ thống. Bạn có thể tải bản nháp để giữ lại.</p><div class="uk-actions"><button class="uk-button primary" data-download>Tải JSON bản nháp</button><button class="uk-button" data-reset>Khôi phục dữ liệu mẫu</button></div><p class="uk-muted">Phiên bản mẫu ${data.version} · Cập nhật mẫu: ${U.date(data.updated_at)}</p>`);
    panel.querySelectorAll('[data-edit]').forEach(b=>b.onclick=()=>window.ProfileEdit.open(data,b.dataset.edit,Number(b.dataset.index),updated=>{data=updated;markDirty();render(active,panel);}));
    panel.querySelectorAll('[data-preference]').forEach(input=>input.onchange=()=>{data.so_thich_hoc[input.dataset.preference]=input.checked;markDirty();});
    panel.querySelector('[data-download]')?.addEventListener('click',()=>U.download('ho-so-ban-nhap.json',data));
    panel.querySelector('[data-reset]')?.addEventListener('click',()=>{if(confirm('Khôi phục dữ liệu mẫu và bỏ mọi chỉnh sửa bản nháp?')){data=structuredClone(baseline);dirty=false;document.querySelector('#draft-label').hidden=true;U.status('Đã khôi phục dữ liệu mẫu.');render(active,panel);}});
  }
  function markDirty(){dirty=true;document.querySelector('#draft-label').hidden=false;U.status('Đã cập nhật bản nháp trong trang; chưa lưu lên hệ thống.');}
  window.addEventListener('beforeunload',event=>{if(dirty){event.preventDefault();event.returnValue='';}});
  async function init(){
    try{data=await U.dataSource.load('profile');baseline=structuredClone(data);U.tabs(root,tabs,render);U.status('Hồ sơ mẫu · Không thay đổi hồ sơ thật.');}
    catch(error){U.status(error.name==='AbortError'?'Tải dữ liệu quá lâu. Vui lòng thử lại.':error.message);root.innerHTML='<button class="uk-button" id="retry-profile">Thử lại</button>';root.querySelector('button').onclick=init;}
  }
  init();
})();
