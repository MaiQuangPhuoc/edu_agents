(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const STUDENT_ID = 'hs_002'; // Chỉ để demo; production dùng phiên đăng nhập.
  const MAX_FILE_SIZE = 30 * 1024 * 1024;
  const PRIVATE_DOCUMENTS_KEY = 'eduagent-private-documents';
  const subjects = ['Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lí', 'Hóa học', 'Sinh học', 'Lịch sử', 'Địa lí', 'Giáo dục kinh tế và pháp luật', 'Tin học', 'Công nghệ', 'Giáo dục quốc phòng và an ninh', 'Giáo dục thể chất', 'Âm nhạc', 'Mĩ thuật', 'Hoạt động trải nghiệm, hướng nghiệp', 'Khác'];
  const seriesLabels = {ket_noi:'Kết nối tri thức với cuộc sống', chan_troi:'Chân trời sáng tạo', canh_dieu:'Cánh Diều', khac:'Khác'};
  let catalog = [];
  let editingDocumentId = null;
  let selectedBookFile = null;
  let selectedPrivateFiles = [];
  let books = [];
  let privateDocuments = [];
  let selectedPrivateDocumentId = null;
  let previewObjectUrl = null;
  const status = (message, error=false) => { $('status').textContent = message; $('status').className = error ? 'error' : 'success'; };
  const element = (tag, text, cls) => { const x=document.createElement(tag); if (text !== undefined) x.textContent=text; if(cls) x.className=cls; return x; };
  async function api(path, opts={}) { const r=await fetch(path,opts); const d=await r.json().catch(()=>({})); if(!r.ok) throw new Error(typeof d.detail==='string'?d.detail:`HTTP ${r.status}`); return d; }
  function fillSubjects(id) {
    const sel=$(id); sel.replaceChildren();
    for(const name of subjects){ const opt=document.createElement('option'); opt.value=name; opt.textContent=name; sel.append(opt); }
  }
  fillSubjects('book-subject'); fillSubjects('private-subject');
  $('book-subject').value='Toán';
  $('private-subject').addEventListener('change',()=>{
    const custom=$('private-subject').value==='Khác';
    $('custom-subject-wrap').hidden=!custom;
    $('custom-subject').required=custom;
  });
  function setTab(which){
    $('book-panel').hidden=which!=='book'; $('private-panel').hidden=which!=='private';
    $('tab-book').classList.toggle('active',which==='book'); $('tab-private').classList.toggle('active',which==='private');
    $('tab-book').setAttribute('aria-selected',String(which==='book'));
    $('tab-private').setAttribute('aria-selected',String(which==='private'));
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
  function showPreview(book, file=null){
    $('confirmed-book').hidden=false; $('book-preview').hidden=true;
    $('preview-title').textContent=book.display_name;
    $('preview-meta').textContent=`${book.subject} · ${seriesLabels[book.series]||book.series}`;
    $('preview-note').textContent=`Tên sách: ${book.title}`;
    $('preview-rag').textContent=book.rag_ready?'RAG đã sẵn sàng':'Chưa có chỉ mục RAG';
    const fileInfo=$('book-confirmed-file-info');
    fileInfo.replaceChildren();
    if(file){
      const item=element('div',undefined,'confirmed-file-item');
      const icon=element('span',undefined,'confirmed-file-icon');
      icon.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3.5h8l4 4V20a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4.5a1 1 0 0 1 1-1Z"/><path d="M14 3.5V8h4M8 13h8M8 16h5"/></svg>';
      const name=element('div',undefined,'confirmed-file-name');
      name.append(element('span',file.name));
      name.append(element('small',`${(file.size/1024/1024).toFixed(2)} MB · PDF đã chọn`,'confirmed-file-meta'));
      item.append(icon,name);
      fileInfo.append(item,element('p','Tệp đang được xem trước trên trình duyệt; chưa được tải lên máy chủ.','confirmed-file-note'));
    }
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
  function getPrivateDocuments(){
    let stored;
    try{
      stored=JSON.parse(localStorage.getItem(PRIVATE_DOCUMENTS_KEY)||'[]');
    }catch(error){
      console.error('EDUAGENT: Không thể đọc tài liệu riêng đã lưu.',error);
      throw new Error('Không thể đọc danh sách tài liệu riêng đã lưu.');
    }
    if(!Array.isArray(stored))throw new Error('Danh sách tài liệu riêng đã lưu không hợp lệ.');
    return stored;
  }
  function savePrivateDocuments(){
    try{
      localStorage.setItem(PRIVATE_DOCUMENTS_KEY,JSON.stringify(privateDocuments));
    }catch(error){
      console.error('EDUAGENT: Không thể lưu tài liệu riêng.',error);
      throw new Error('Không thể lưu tài liệu riêng trong trình duyệt.');
    }
  }
  function createCover(title,kind,subject){
    const cover=element('span',undefined,`document-cover ${kind==='private'?'private-cover':'book-cover'}`);
    cover.append(element('span',kind==='private'?'TÀI LIỆU':'EDUAGENT','cover-brand'));
    cover.append(element('strong',title,'cover-title'));
    cover.append(element('span',subject,'cover-subject'));
    return cover;
  }
  function showPrivateDetail(document){
    selectedPrivateDocumentId=document.document_id;
    const panel=$('private-detail');
    panel.replaceChildren();
    if(previewObjectUrl){
      URL.revokeObjectURL(previewObjectUrl);
      previewObjectUrl=null;
    }
    const detail=element('article',undefined,'document-detail');
    const kind=document.kind==='private'?'private':'book';
    const subject=document.subject||'Chưa phân loại';
    const title=document.display_name||document.title||'Tài liệu';
    const meta=kind==='private'
      ?`Tài liệu riêng · ${subject}`
      :`Lớp ${document.grade||10} · ${subject} · ${seriesLabels[document.series]||document.series}`;
    const file=kind==='private'?selectedPrivateFilesById.get(document.document_id):null;
    const preview=element('div',undefined,'document-preview');
    if(file&&(file.type==='application/pdf'||/\.pdf$/i.test(file.name))){
      previewObjectUrl=URL.createObjectURL(file);
      const frame=element('iframe');
      frame.title=`Bản xem trước ${title}`;
      frame.src=previewObjectUrl;
      preview.append(frame);
    }else if(file&&(file.type.startsWith('image/')||/\.(jpg|jpeg|png)$/i.test(file.name))){
      previewObjectUrl=URL.createObjectURL(file);
      const image=element('img');
      image.src=previewObjectUrl;
      image.alt=`Bản xem trước ${title}`;
      preview.append(image);
    }else if(file&&/\.txt$/i.test(file.name)){
      const textPreview=element('pre','Đang tải nội dung…','text-preview');
      preview.append(textPreview);
      file.text().then(text=>{
        if(selectedPrivateDocumentId===document.document_id){
          textPreview.textContent=text.slice(0,30000);
          if(text.length>30000)textPreview.textContent+='\n\n… Nội dung xem trước đã được rút gọn.';
        }
      }).catch(error=>{
        console.error('EDUAGENT: Không thể xem trước tệp văn bản.',error);
        if(selectedPrivateDocumentId===document.document_id)textPreview.textContent='Không thể đọc nội dung tệp này.';
      });
    }else{
      preview.append(createCover(title,kind,subject));
      if(kind==='private'&&document.file){
        preview.append(element('p',file
          ?`Định dạng ${document.file.name.split('.').pop()?.toUpperCase()||'tài liệu'} chưa hỗ trợ xem trước trực tiếp.`
          :'File gốc chưa được lưu trên máy chủ. Hãy chọn lại file để xem nội dung.','preview-note'));
      }
    }
    const info=element('div',undefined,'document-detail-info');
    info.append(element('span',kind==='private'?'TÀI LIỆU RIÊNG':'SÁCH GIÁO KHOA','small-label'));
    info.append(element('h3',title));
    info.append(element('p',meta,'muted'));
    if(document.description)info.append(element('p',document.description,'detail-description'));
    if(kind==='private'&&document.file){
      info.append(element('p',`${document.file.name} · ${(document.file.size/1024/1024).toFixed(2)} MB`,'detail-file'));
    }
    if(kind==='book')info.append(element('p',`Tên sách: ${document.title}`,'detail-file'));
    detail.append(preview,info);
    panel.append(detail);
  }
  const selectedPrivateFilesById=new Map();
  function showPrivateDetailEmpty(){
    const empty=element('div',undefined,'detail-empty');
    empty.append(element('span','▤','detail-empty-icon'));
    empty.lastElementChild.setAttribute('aria-hidden','true');
    empty.append(element('strong','Chọn một tài liệu để xem'));
    empty.append(element('p','Tài liệu đã thêm sẽ hiển thị nội dung xem trước tại đây.'));
    $('private-detail').replaceChildren(empty);
  }
  function renderLibrary(){
    const box=$('my-books');
    box.replaceChildren();
    if(!books.length&&!privateDocuments.length){
      box.append(element('p','Chưa có sách hoặc tài liệu nào.','library-empty'));
      return;
    }
    const grid=element('div',undefined,'document-grid');
    const records=[
      ...books.map(book=>({record:book,kind:'book'})),
      ...privateDocuments.map(document=>({record:document,kind:'private'})),
    ];
    for(const {record,kind} of records){
      const id=record.document_id;
      const card=element('article',undefined,`document-card${selectedPrivateDocumentId===id?' is-selected':''}`);
      const open=element('button',undefined,'document-card-open');
      open.type='button';
      open.setAttribute('aria-label',`Xem ${record.display_name||record.title}`);
      open.setAttribute('aria-pressed',String(selectedPrivateDocumentId===id));
      open.append(createCover(record.display_name||record.title,kind,
        kind==='private'?record.subject:`LỚP ${record.grade||10} · ${record.subject}`));
      const copy=element('span',undefined,'document-card-copy');
      copy.append(element('strong',record.display_name||record.title));
      copy.append(element('span',kind==='private'
        ?`Tài liệu riêng · ${record.subject}`
        :`Lớp ${record.grade||10} · ${record.subject}`,'document-card-meta'));
      open.append(copy);
      open.addEventListener('click',()=>{
        if(kind==='private'){
          setTab('private');
          showPrivateDetail(record);
          renderLibrary();
        }else{
          setTab('book');
          showPreview(record);
          status(`Đang xem ${record.display_name||record.title}.`);
        }
      });
      card.append(open);
      if(kind==='book'){
        const actions=element('div',undefined,'document-card-actions');
        const edit=element('button','Sửa');
        edit.type='button';
        edit.addEventListener('click',()=>editBook(record).catch(error=>status(error.message,true)));
        const remove=element('button','Gỡ');
        remove.type='button';
        remove.addEventListener('click',async()=>{
          if(!confirm(`Gỡ sách "${record.display_name}"?`))return;
          try{
            await api(`/api/ui/books/mine/${encodeURIComponent(id)}?student_id=${encodeURIComponent(STUDENT_ID)}`,{method:'DELETE'});
            await loadMine();
            status('Đã gỡ sách.');
          }catch(error){status(error.message,true);}
        });
        actions.append(edit,remove);
        card.append(actions);
      }else{
        const actions=element('div',undefined,'document-card-actions');
        const remove=element('button','Gỡ tài liệu');
        remove.type='button';
        remove.addEventListener('click',()=>{
          if(!confirm(`Gỡ tài liệu "${record.display_name}"?`))return;
          const previous=privateDocuments;
          privateDocuments=privateDocuments.filter(item=>item.document_id!==id);
          try{
            savePrivateDocuments();
            selectedPrivateFilesById.delete(id);
            if(selectedPrivateDocumentId===id){
              selectedPrivateDocumentId=null;
              showPrivateDetailEmpty();
            }
            renderLibrary();
            status('Đã gỡ tài liệu khỏi danh sách trên trình duyệt.');
          }catch(error){
            privateDocuments=previous;
            status(error.message,true);
          }
        });
        actions.append(remove);
        card.append(actions);
      }
      grid.append(card);
    }
    box.append(grid);
  }
  function cancelEdit(){
    editingDocumentId=null;
    $('book-form').reset();
    $('book-subject').value='Toán';
    $('book-name').value='';
    $('confirm-book').textContent='Xác nhận sách';
    $('cancel-edit-book').hidden=true;
  }
  async function editBook(book){
    editingDocumentId=book.document_id;
    $('series').value=book.series;
    $('book-subject').value=book.subject;
    $('display-name').value=book.display_name;
    $('description').value=book.description||'';
    $('book-name').value=book.title;
    $('confirm-book').textContent='Lưu thay đổi';
    $('cancel-edit-book').hidden=false;
    setTab('book');
    await loadCatalog();
    $('book-name').value=book.title;
    $('book-form').scrollIntoView({behavior:'smooth',block:'start'});
  }
  $('book-form').addEventListener('submit',async e=>{
    e.preventDefault();
    const title=$('book-name').value.trim();if(!title)return;
    const existing=catalog.find(b=>b.title.toLocaleLowerCase('vi')===title.toLocaleLowerCase('vi'));
    const body={student_id:STUDENT_ID,book_id:existing?.book_id||null,title,series:$('series').value,subject:$('book-subject').value,
      display_name:$('display-name').value.trim()||title,description:$('description').value.trim()};
    const btn=$('confirm-book');btn.disabled=true;
    try {
      const editing=Boolean(editingDocumentId);
      const url=editing
        ? `/api/ui/books/mine/${encodeURIComponent(editingDocumentId)}`
        : '/api/ui/books/attach';
      const book=await api(url,{method:editing?'PUT':'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      cancelEdit();
      showPreview(book,editing?null:selectedBookFile);await loadMine();
      status(editing?'Đã cập nhật thông tin sách.':selectedBookFile
        ?'Đã xác nhận thông tin sách. Tệp PDF mới chỉ được chọn để xem trước, chưa tải lên máy chủ.'
        :'Đã xác nhận và lưu thông tin sách.');
    }catch(err){status(err.message,true);}finally{btn.disabled=false;}
  });
  $('cancel-edit-book').addEventListener('click',cancelEdit);
  function wireDrop(zoneId, inputId, infoId, types, onFiles=()=>{}){
    const zone=$(zoneId),input=$(inputId),info=$(infoId);
    const display=(files, message='')=>{
      info.replaceChildren();const valid=[];
      if(message)info.append(element('p',message,'muted'));
      for(const f of files){
        const ext=f.name.split('.').pop()?.toLowerCase();
        if(!types.includes(ext)){ info.append(element('p',`Không hỗ trợ: ${f.name}`,'error'));continue; }
        if(f.size>MAX_FILE_SIZE){info.append(element('p',`${f.name} vượt 30 MB`,'error'));continue;}
        valid.push(f);info.append(element('p',`${f.name} — ${(f.size/1024/1024).toFixed(2)} MB`));
      }
      if(valid.length)info.append(element('p','Đã chọn file trên trình duyệt; chưa gửi lên backend.','muted'));
      onFiles(valid);
    };
    zone.addEventListener('click',()=>input.click());
    zone.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();input.click();}});
    input.addEventListener('change',()=>display([...input.files]));
    zone.addEventListener('dragover',e=>{e.preventDefault();zone.classList.add('dragging');});
    zone.addEventListener('dragleave',e=>{
      if(!zone.contains(e.relatedTarget))zone.classList.remove('dragging');
    });
    zone.addEventListener('drop',e=>{
      e.preventDefault();zone.classList.remove('dragging');
      const dropped=[...e.dataTransfer.files];
      const files=input.multiple?dropped:dropped.slice(0,1);
      const transfer=new DataTransfer();
      files.forEach(file=>transfer.items.add(file));
      input.files=transfer.files;
      display([...input.files],dropped.length>files.length?'Chỉ tệp đầu tiên được chọn.':'');
    });
  }
  wireDrop('book-drop','book-file','book-file-info',['pdf'],files=>{
    selectedBookFile=files[0]||null;
    $('book-drop').querySelector('strong').textContent=selectedBookFile
      ?'Đã chọn sách — nhấn để thay tệp'
      :'Chọn sách hoặc kéo thả tệp vào đây';
    if(selectedBookFile&&!$('book-name').value.trim()){
      $('book-name').value=selectedBookFile.name.replace(/\.pdf$/i,'').replace(/[_-]+/g,' ').trim();
    }
    if(selectedBookFile){
      $('book-drop').classList.add('has-file');
      status(`Đã chọn ${selectedBookFile.name}. Hãy kiểm tra thông tin sách rồi xác nhận.`);
    }else{
      $('book-drop').classList.remove('has-file');
    }
  });
  wireDrop('private-drop','private-file','private-file-info',['pdf','docx','txt','jpg','jpeg','png'],files=>{
    selectedPrivateFiles=files;
    if(files.length===1&&!$('private-name').value.trim()){
      $('private-name').value=files[0].name.replace(/\.[^.]+$/,'').replace(/[_-]+/g,' ').trim();
    }
  });
  $('private-form').addEventListener('submit',event=>{
    event.preventDefault();
    const subject=$('private-subject').value==='Khác'
      ?$('custom-subject').value.trim()
      :$('private-subject').value;
    const baseName=$('private-name').value.trim();
    if(!subject){
      status('Vui lòng nhập tên môn học.',true);
      $('custom-subject').focus();
      return;
    }
    if(!baseName&&!selectedPrivateFiles.length){
      status('Vui lòng nhập tên tài liệu hoặc chọn file.',true);
      $('private-name').focus();
      return;
    }
    const files=selectedPrivateFiles.length?selectedPrivateFiles:[null];
    const added=files.map(file=>({
      document_id:`private-${Date.now()}-${Math.random().toString(36).slice(2)}`,
      kind:'private',
      display_name:file&&files.length>1
        ?`${baseName?`${baseName} · `:''}${file.name.replace(/\.[^.]+$/,'').replace(/[_-]+/g,' ').trim()}`
        :baseName||file.name.replace(/\.[^.]+$/,'').replace(/[_-]+/g,' ').trim(),
      subject,
      description:$('private-description').value.trim(),
      file:file?{name:file.name,size:file.size,type:file.type,last_modified:file.lastModified}:null,
      created_at:new Date().toISOString(),
    }));
    const previous=privateDocuments;
    privateDocuments=[...privateDocuments,...added];
    try{
      savePrivateDocuments();
    }catch(error){
      privateDocuments=previous;
      status(error.message,true);
      return;
    }
    added.forEach((document,index)=>{
      if(files[index])selectedPrivateFilesById.set(document.document_id,files[index]);
    });
    selectedPrivateDocumentId=added[0].document_id;
    showPrivateDetail(added[0]);
    renderLibrary();
    $('private-form').reset();
    $('private-subject').value='Toán';
    $('custom-subject-wrap').hidden=true;
    $('custom-subject').required=false;
    $('private-file-info').replaceChildren();
    $('private-drop').querySelector('strong').textContent='Nhấn để chọn hoặc kéo thả tài liệu vào đây';
    selectedPrivateFiles=[];
    status(added.length>1
      ?`Đã xác nhận ${added.length} tài liệu. Các file vẫn chỉ được lưu trong trình duyệt.`
      :'Đã xác nhận tài liệu. File vẫn chỉ được lưu trong trình duyệt.');
  });
  async function loadMine(){
    const d=await api(`/api/ui/books/mine?student_id=${encodeURIComponent(STUDENT_ID)}`);
    books=d.documents||[];
    privateDocuments=getPrivateDocuments();
    renderLibrary();
    if(selectedPrivateDocumentId){
      const selected=privateDocuments.find(item=>item.document_id===selectedPrivateDocumentId);
      if(selected)showPrivateDetail(selected);
      else selectedPrivateDocumentId=null;
    }
  }
  $('refresh').addEventListener('click',async()=>{
    const button=$('refresh');
    button.disabled=true;
    try{
      await loadMine();
      status('Danh sách tài liệu đã được làm mới.');
    }catch(error){status(error.message,true);}
    finally{button.disabled=false;}
  });
  Promise.all([loadCatalog(),loadMine()]).catch(e=>status(e.message,true));
})();
