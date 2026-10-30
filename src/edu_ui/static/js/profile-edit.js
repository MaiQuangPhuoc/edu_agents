/* Draft-only card editing. No profile API writes in this UI phase. */
(() => {
  'use strict';
  const U=window.StudentUI;
  const field=(key,label,type='text',extra='')=>({key,label,type,extra});
  window.ProfileEdit={open(data,section,index,onSave){
    const copy=structuredClone(data); let target,fields,title;
    if(section==='identity') {
      target=copy.ca_nhan; title='Thông tin cá nhân';
      fields=[field('ho_ten','Họ tên','text','maxlength="100" required'),field('khoi_lop','Khối lớp','number','min="1" max="12" step="1" required'),field('so_thich','Sở thích (ngăn cách bằng dấu phẩy)')];
    } else if(section==='goal') {
      target=copy.muc_tieu[index]; title=`Mục tiêu ${target.mon_hoc}`;
      fields=[field('diem_muc_tieu','Điểm mục tiêu','number','min="0" max="10" step="0.1" required'),field('han_chot','Hạn chót','date','required'),field('uu_tien','Ưu tiên','priority'),field('dang_bai','Dạng bài cần tập trung','text','maxlength="300"')];
    } else if(section==='ability') {
      target=copy.nang_luc[index]; title=`Năng lực ${target.mon_hoc}`;
      fields=[field('diem_hien_tai','Điểm hiện tại','number','min="0" max="10" step="0.1" required'),field('manh','Điểm mạnh (ngăn cách bằng dấu phẩy)'),field('yeu','Điểm yếu (ngăn cách bằng dấu phẩy)')];
    } else if(section==='preferences') {
      target=copy.so_thich_hoc; title='Cách học yêu thích';
      fields=[field('tai_lieu','Dùng tài liệu','checkbox'),field('video','Dùng video','checkbox'),field('bai_tap','Bài tập sau buổi','checkbox'),field('tom_tat','Tóm tắt cuối buổi','checkbox')];
    } else if(section==='schedule') {
      target=copy.lich_hoc; title='Lịch học mỗi tuần';
      fields=[field('thoi_luong','Số phút mỗi buổi','number','min="15" max="240" step="5" required')];
      for(let day=0;day<7;day++) {
        const slot=target.slots.find(s=>s.day===day);
        target[`day_${day}`]=Boolean(slot); target[`start_${day}`]=slot?.start||'19:00';
        fields.push(field(`day_${day}`,['Thứ 2','Thứ 3','Thứ 4','Thứ 5','Thứ 6','Thứ 7','Chủ nhật'][day],'checkbox'),field(`start_${day}`,'Giờ bắt đầu','time','required'));
      }
    } else return;
    const dialog=document.createElement('dialog'); dialog.className='uk-dialog';
    dialog.setAttribute('aria-labelledby','edit-dialog-title');
    dialog.innerHTML=`<form><h2 id="edit-dialog-title">${U.esc(title)}</h2><p class="uk-muted">Chỉ cập nhật bản nháp trong trang này.</p>${fields.map(f=>{
      const v=target[f.key]; const label=U.esc(f.label);
      if(f.type==='checkbox') return `<label><input name="${f.key}" type="checkbox" ${v?'checked':''}>${label}</label>`;
      if(f.type==='priority') return `<label>${label}<select name="${f.key}">${['Cao','Vừa','Thấp'].map(x=>`<option ${x===v?'selected':''}>${x}</option>`).join('')}</select></label>`;
      return `<label>${label}<input name="${f.key}" type="${f.type}" value="${U.esc(Array.isArray(v)?v.join(', '):v)}" ${f.extra}></label>`;
    }).join('')}<p id="edit-error" role="alert" class="uk-muted"></p><div class="uk-actions"><button type="button" class="uk-button" data-cancel>Hủy</button><button class="uk-button primary" type="submit">Lưu bản nháp</button></div></form>`;
    let dirty=false;
    function cancel(){if(!dirty||confirm('Bỏ các thay đổi chưa lưu trong hộp thoại?'))dialog.close();}
    dialog.addEventListener('input',()=>{dirty=true;});
    dialog.querySelector('[data-cancel]').onclick=cancel;
    dialog.addEventListener('cancel',e=>{e.preventDefault();cancel();});
    dialog.addEventListener('close',()=>dialog.remove());
    dialog.querySelector('form').onsubmit=e=>{
      e.preventDefault();
      for(const f of fields){
        const input=dialog.querySelector(`[name="${f.key}"]`);
        target[f.key]=f.type==='checkbox'?input.checked:f.type==='number'?Number(input.value):Array.isArray(target[f.key])?input.value.split(',').map(x=>x.trim()).filter(Boolean):input.value.trim();
      }
      if(section==='identity'&&!target.ho_ten){dialog.querySelector('#edit-error').textContent='Vui lòng nhập họ tên.';return;}
      if(section==='schedule'){
        const slots=[];
        for(let day=0;day<7;day++){
          if(target[`day_${day}`]){
            const start=target[`start_${day}`];const [h,m]=start.split(':').map(Number);const end=h*60+m+target.thoi_luong;
            if(end>=1440){dialog.querySelector('#edit-error').textContent='Buổi học cần kết thúc trước 24:00.';return;}
            slots.push({day,start,end:`${String(Math.floor(end/60)).padStart(2,'0')}:${String(end%60).padStart(2,'0')}`});
          }
          delete target[`day_${day}`];delete target[`start_${day}`];
        }
        target.slots=slots;target.so_buoi=slots.length;
      }
      onSave(copy); dirty=false;dialog.close();
    };
    document.body.append(dialog);dialog.showModal();
  }};
})();
