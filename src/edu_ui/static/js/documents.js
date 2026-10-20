(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const STUDENT_ID = 'hs_002'; // Chỉ để demo; production dùng phiên đăng nhập.
  const MAX_FILE_SIZE = 30 * 1024 * 1024;
  const subjects = ['Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lí', 'Hóa học', 'Sinh học', 'Lịch sử', 'Địa lí', 'Giáo dục kinh tế và pháp luật', 'Tin học', 'Công nghệ', 'Giáo dục quốc phòng và an ninh', 'Giáo dục thể chất', 'Âm nhạc', 'Mĩ thuật', 'Hoạt động trải nghiệm, hướng nghiệp', 'Khác'];
  const seriesLabels = {ket_noi:'Kết nối tri thức với cuộc sống', chan_troi:'Chân trời sáng tạo', canh_dieu:'Cánh Diều', khac:'Khác'};
  let catalog = [];
  const status = (message, error=false) => { $('status').textContent = message; $('status').className = error ? 'error' : 'success'; };
  const element = (tag, text, cls) => { const x=document.createElement(tag); if (text !== undefined) x.textContent=text; if(cls) x.className=cls; return x; };
  async function api(path, opts={}) { const r=await fetch(path,opts); const d=await r.json().catch(()=>({})); if(!r.ok) throw new Error(typeof d.detail==='string'?d.detail:`HTTP ${r.status}`); return d; }
  function fillSubjects(id) {
    const sel=$(id); sel.replaceChildren();
    for(const name of subjects){ const opt=document.createElement('option'); opt.value=name; opt.textContent=name; sel.append(opt); }
  }
  fillSubjects('book-subject'); fillSubjects('private-subject');
  $('book-subject').value='Toán';
  $('private-subject').addEventListener('change',()=>{ $('custom-subject-wrap').hidden=$('private-subject').value!=='Khác'; });
  function setTab(which){
    $('book-panel').hidden=which!=='book'; $('private-panel').hidden=which!=='private';
    $('tab-book').classList.toggle('active',which==='book'); $('tab-private').classList.toggle('active',which==='private');
  }
  $('tab-book').addEventListener('click',()=>setTab('book'));
  $('tab-private').addEventListener('click',()=>setTab('private'));
  document.querySelectorAll('.soon').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();status('Trang này đang phát triển.');}));

  async function loadCatalog(){
    const series=$('series').value; const subject=$('book-subject').value;
    const d=await api(`/api/ui/books?${new URLSearchParams({series,subject})}`);
    catalog=d.books||[];
    const list=$('book-suggestions'); list.replaceChildren();
    catalog.forEach(book=>{ const option=document.createElement('option');option.value=book.title;list.append(option); });
  }
  ['series','book-subject'].forEach(id=>$(id).addEventListener('change',()=>{ $('book-name').value='';loadCatalog().catch(e=>status(e.message,true)); }));
  function showPreview(book){
    $('confirmed-book').hidden=false; $('book-preview').hidden=true;
    $('preview-title').textContent=book.display_name;
    $('preview-meta').textContent=`${book.subject} · ${seriesLabels[book.series]||book.series}`;
    $('preview-note').textContent=`Tên sách: ${book.title}`;
    $('preview-rag').textContent=book.rag_ready?'RAG đã sẵn sàng':'Chưa có chỉ mục RAG';
    $('cover-title').textContent=book.title;
    $('cover-series').textContent=seriesLabels[book.series]||book.series;
    // Không tự lấy ảnh không xác thực; chỉ sử dụng URL bìa có trong danh mục.
    const img=$('cover-image');img.hidden=true;img.removeAttribute('src');$('cover-fallback').hidden=false;
    if (typeof book.cover_url==='string' && /^https:\/\//.test(book.cover_url)) {
      img.onload=()=>{img.hidden=false;$('cover-fallback').hidden=true;};
      img.onerror=()=>{img.hidden=true;$('cover-fallback').hidden=false;};
      img.src=book.cover_url;
    }
  }
  $('book-form').addEventListener('submit',async e=>{
    e.preventDefault();
    const title=$('book-name').value.trim();if(!title)return;
    const existing=catalog.find(b=>b.title.toLocaleLowerCase('vi')===title.toLocaleLowerCase('vi'));
    const body={student_id:STUDENT_ID,book_id:existing?.book_id||null,title,series:$('series').value,subject:$('book-subject').value,
      display_name:$('display-name').value.trim()||title,description:$('description').value.trim()};
    const btn=$('confirm-book');btn.disabled=true;
    try {
      const book=await api('/api/ui/books/attach',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      showPreview(book);await loadMine();status('Đã xác nhận và lưu tên sách. Có thể chọn PDF để xem trước (chưa upload).');
    }catch(err){status(err.message,true);}finally{btn.disabled=false;}
  });
  function wireDrop(zoneId, inputId, infoId, types){
    const zone=$(zoneId),input=$(inputId),info=$(infoId);
    const display=(files)=>{
      info.replaceChildren();const valid=[];
      for(const f of files){
        const ext=f.name.split('.').pop()?.toLowerCase();
        if(!types.includes(ext)){ info.append(element('p',`Không hỗ trợ: ${f.name}`,'error'));continue; }
        if(f.size>MAX_FILE_SIZE){info.append(element('p',`${f.name} vượt 30 MB`,'error'));continue;}
        valid.push(f);info.append(element('p',`${f.name} — ${(f.size/1024/1024).toFixed(2)} MB`));
      }
      if(valid.length)info.append(element('p','Đã chọn file trên trình duyệt; chưa gửi lên backend.','muted'));
    };
    zone.addEventListener('click',()=>input.click());
    zone.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();input.click();}});
    input.addEventListener('change',()=>display([...input.files]));
    zone.addEventListener('dragover',e=>{e.preventDefault();zone.classList.add('dragging');});
    zone.addEventListener('dragleave',()=>zone.classList.remove('dragging'));
    zone.addEventListener('drop',e=>{e.preventDefault();zone.classList.remove('dragging');display([...e.dataTransfer.files]);});
  }
  wireDrop('book-drop','book-file','book-file-info',['pdf']);
  wireDrop('private-drop','private-file','private-file-info',['pdf','docx','txt','jpg','jpeg','png']);
  async function loadMine(){
    const d=await api(`/api/ui/books/mine?student_id=${encodeURIComponent(STUDENT_ID)}`);
    const box=$('my-books');box.replaceChildren();
    if(!d.documents?.length){box.append(element('p','Chưa có sách nào.','muted'));return;}
    for(const b of d.documents){
      const card=element('article',undefined,'saved-book');card.append(element('strong',b.display_name));
      card.append(element('p',`${b.title} · ${b.subject} · ${seriesLabels[b.series]||b.series}`,'muted'));
      const actions=element('div',undefined,'actions');
      const see=element('button','Xem sách');see.addEventListener('click',()=>{setTab('book');showPreview(b);});actions.append(see);
      const remove=element('button','Gỡ sách');remove.addEventListener('click',async()=>{
        if(!confirm(`Gỡ sách "${b.display_name}"?`))return;
        try{await api(`/api/ui/books/mine/${encodeURIComponent(b.document_id)}?student_id=${encodeURIComponent(STUDENT_ID)}`,{method:'DELETE'});await loadMine();status('Đã gỡ sách.');}catch(err){status(err.message,true);}
      });actions.append(remove);card.append(actions);box.append(card);
    }
  }
  $('refresh').addEventListener('click',()=>loadMine().catch(e=>status(e.message,true)));
  Promise.all([loadCatalog(),loadMine()]).catch(e=>status(e.message,true));
})();
