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
  let bookObjectUrl = null;
  const status = (message, error=false) => { $('status').textContent = message; $('status').className = error ? 'error' : 'success'; };
  const element = (tag, text, cls) => { const x=document.createElement(tag); if (text !== undefined) x.textContent=text; if(cls) x.className=cls; return x; };
  async function api(path, opts={}) {
    const r=await fetch(path,opts); const d=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(typeof d.detail==='string'?d.detail:d.detail?.message||`HTTP ${r.status}`);
    return d;
  }
  const INDEX_STEPS=[
    ['Tiếp nhận sách','Nhận lựa chọn sách và lưu PDF nếu có.'],
    ['Đọc giáo án','Tìm các file Markdown theo môn và bộ sách.'],
    ['Chia nội dung','Tạo các chunk và giữ metadata giáo án.'],
    ['Chuẩn bị chỉ mục','Kiểm tra Qdrant, collection và mô hình embedding.'],
    ['Embedding và upload','Xử lý và ghi từng lô chunk vào Qdrant.'],
    ['Lưu kết quả','Lưu thông tin tài liệu để xem và tìm lại.'],
  ];
  const INDEX_STAGE={file_saved:0,queued:0,selecting_prepared_markdown:1,
    chunking_prepared_markdown:2,checking_qdrant_config:3,preparing_index:3,
    uploading_prepared_markdown:4,saving_document:5};
  function createIndexTracker(id,title){
    const panel=$(id);panel.hidden=false;panel.replaceChildren();
    panel.className=`indexing-progress ${id==='book-indexing-progress'?'indexing-horizontal ':''}is-running`;
    const heading=element('div',undefined,'indexing-heading');
    const left=element('div');left.append(element('span','ĐANG XỬ LÝ','indexing-eyebrow'),element('h3',title));
    const clock=element('span','00:00','indexing-clock');heading.append(left,clock);
    const note=element('p','Đang gửi thông tin sách tới máy chủ…','indexing-current');note.setAttribute('role','status');
    const track=element('div',undefined,'indexing-track');track.setAttribute('role','progressbar');
    track.setAttribute('aria-label','Các bước xử lý đã hoàn thành');track.setAttribute('aria-valuemin','0');track.setAttribute('aria-valuemax','6');
    const fill=element('span');track.append(fill);
    const counter=element('span','Bước 1 / 6','indexing-counter');
    const list=element('ol',undefined,'indexing-steps');
    const rows=INDEX_STEPS.map(([label,description],index)=>{
      const row=element('li',undefined,'indexing-step');
      const badge=element('span',String(index+1),'indexing-step-badge');badge.setAttribute('aria-hidden','true');
      const copy=element('div');const small=element('p',description);
      copy.append(element('strong',label),small);row.append(badge,copy);list.append(row);
      return {row,badge,small};
    });
    const detail=element('details',undefined,'indexing-details');
    detail.append(element('summary','Chi tiết xử lý'));
    const feed=element('div',undefined,'indexing-feed');detail.append(feed);
    panel.append(heading,note,track,counter,list,detail);
    let stage=0,finished=false,fileSaved=false,lastMessage='',fraction=0;
    const started=performance.now();
    const time=()=>{const seconds=Math.floor((performance.now()-started)/1000);clock.textContent=`${String(Math.floor(seconds/60)).padStart(2,'0')}:${String(seconds%60).padStart(2,'0')}`;};
    const timer=setInterval(time,1000);
    function draw(){
      rows.forEach(({row,badge},i)=>{
        const done=i<stage||(i===0&&fileSaved)||finished;
        row.className=`indexing-step ${done?'is-done':i===stage?'is-active':'is-pending'}`;
        badge.textContent=done?'✓':String(i+1);
      });
      const complete=finished?6:stage+fraction;
      fill.style.width=`${Math.min(100,complete/6*100)}%`;
      track.setAttribute('aria-valuenow',String(complete));
      counter.textContent=finished?'Hoàn thành 6 / 6 bước':`Bước ${stage+1} / 6`;
    }
    function log(message){
      if(!message||message===lastMessage)return;
      lastMessage=message;
      const line=element('p');line.append(element('time',clock.textContent),element('span',message));feed.append(line);
      while(feed.children.length>40)feed.firstElementChild.remove();
      feed.scrollTop=feed.scrollHeight;
    }
    draw();
    return {
      update(event){
        if(finished)return;
        if(!(event.stage in INDEX_STAGE))return;
        const next=INDEX_STAGE[event.stage];
        if(next>stage){stage=next;fraction=0;}
        if(event.stage==='file_saved'){fileSaved=true;fraction=1;}
        if(event.stage==='queued')note.textContent='Đang chờ lượt xử lý trên máy chủ…';
        else note.textContent=event.message||INDEX_STEPS[stage][0]+'…';
        if(Number.isFinite(event.current)&&event.total>0&&next===stage){
          fraction=Math.max(0,Math.min(1,event.current/event.total));
          rows[stage].small.textContent=event.message||`${event.current} / ${event.total}`;
        }else if(event.message)rows[stage].small.textContent=event.message;
        log(event.message||INDEX_STEPS[stage][0]);draw();
      },
      finish(document){
        finished=true;clearInterval(timer);time();draw();panel.classList.remove('is-running');panel.classList.add('is-complete');
        left.firstElementChild.textContent='HOÀN TẤT';
        note.textContent=`Đã lập chỉ mục ${document.indexing?.total_chunks||0} chunk. Tài liệu đã có trong thư viện.`;
        log('Đã lưu kết quả và thông tin tài liệu.');
      },
      fail(message){
        clearInterval(timer);time();panel.classList.remove('is-running');panel.classList.add('is-failed');
        rows[stage].row.classList.remove('is-active');rows[stage].row.classList.add('is-error');
        rows[stage].badge.textContent='!';left.firstElementChild.textContent='CẦN KIỂM TRA';
        note.textContent=message;log(message);detail.open=true;
      },
    };
  }
  async function indexWithProgress(url,form,id,title){
    const tracker=createIndexTracker(id,title);
    try{
      const response=await fetch(`${url}?stream=true`,{method:'POST',body:form});
      if(!response.ok){
        const error=await response.json().catch(()=>({}));
        throw new Error(typeof error.detail==='string'?error.detail:error.detail?.message||`HTTP ${response.status}`);
      }
      if(!response.headers.get('content-type')?.includes('text/event-stream')){
        const document=await response.json();tracker.finish(document);return document;
      }
      const reader=response.body.getReader(),decoder=new TextDecoder();
      let buffer='';
      try{
        while(true){
          const {value,done}=await reader.read();
          if(done)throw new Error('Kết nối tiến trình đã đóng trước khi nhận kết quả. Hãy kiểm tra thư viện trước khi nạp lại.');
          buffer+=decoder.decode(value,{stream:true});
          let boundary;
          while((boundary=buffer.indexOf('\n\n'))!==-1){
            const frame=buffer.slice(0,boundary);buffer=buffer.slice(boundary+2);
            const data=frame.split(/\r?\n/).filter(line=>line.startsWith('data:')).map(line=>line.slice(5).trim()).join('\n');
            if(!data)continue;
            const event=JSON.parse(data);
            if(event.type==='error')throw new Error(event.message||'Xử lý thất bại.');
            if(event.type==='result'){tracker.finish(event.document);return event.document;}
            if(event.type==='progress')tracker.update(event);
          }
        }
      }finally{reader.releaseLock();}
    }catch(error){tracker.fail(error.message);throw error;}
  }
  function fillSubjects(id) {
    const sel=$(id); sel.replaceChildren();
    for(const name of subjects){ const opt=document.createElement('option'); opt.value=name; opt.textContent=name; sel.append(opt); }
  }
  fillSubjects('book-subject'); fillSubjects('private-subject');
  $('book-subject').prepend(new Option('Chọn môn học',''));
  $('book-subject').value='';
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
    if(!series||!subject){catalog=[];$('book-suggestions').replaceChildren();return;}
    const d=await api(`/api/ui/books?${new URLSearchParams({series,subject})}`);
    catalog=d.books||[];
    const list=$('book-suggestions'); list.replaceChildren();
    catalog.forEach(book=>{ const option=document.createElement('option');option.value=book.title;list.append(option); });
  }
  function coverUrls(book) {
    const slug = (book.subject || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[đĐ]/g, 'd')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '_')
      .replace(/^_|_$/g, '');

    const base = `/api/ui/books/covers/${encodeURIComponent(book.series || '')}`;
    const name = `${slug}_10`;

    // Toán và Ngữ văn có hai tập.
    return ['toan', 'ngu_van'].includes(slug)
      ? [`${base}/${name}_1`, `${base}/${name}_2`]
      : [`${base}/${name}`];
  }

  function renderBookCovers(host, book, onState = () => {}) {
    host.querySelector('.volume-covers')?.remove();

    const gallery = element('span', undefined, 'volume-covers');
    gallery.hidden = true;
    host.append(gallery);
    onState(false);

    const urls = coverUrls(book);

    urls.forEach((url, index) => {
      const image = element('img');
      image.hidden = true;
      image.alt = urls.length > 1
        ? `${book.title} — Tập ${index + 1}`
        : `Bìa ${book.title}`;

      image.onload = () => {
        // Bỏ qua kết quả của lựa chọn cũ.
        if (!host.contains(gallery)) return;
        image.hidden = false;
        gallery.hidden = false;
        onState(true);
      };

      image.onerror = () => image.remove();
      gallery.append(image);
      image.src = url;
    });
  }
  function previewBookSelection(){
    const subject=$('book-subject').value,series=$('series').value;
    if(!subject||!series){$('confirmed-book').hidden=true;$('book-preview').hidden=false;showBookFile(selectedBookFile);return;}
    const title=$('book-name').value.trim()||`${subject} 10`;
    showPreview({title,display_name:$('display-name').value.trim()||title,subject,series,pending:true},selectedBookFile);
  }
  ['series','book-subject'].forEach(id=>$(id).addEventListener('change',()=>{
    $('book-name').value=$('book-subject').value?`${$('book-subject').value} 10`:'';
    previewBookSelection();loadCatalog().catch(e=>status(e.message,true));
  }));
  ['book-name','display-name'].forEach(id=>$(id).addEventListener('input',previewBookSelection));
  function showPreview(book, file=null){
    $('confirmed-book').hidden=false; $('book-preview').hidden=true;
    $('preview-title').textContent=book.display_name;
    $('preview-meta').textContent=`${book.subject} · ${seriesLabels[book.series]||book.series}`;
    $('preview-note').textContent=`Tên sách: ${book.title}`;
    $('preview-rag').textContent=book.pending?'Xem trước · Chưa xác nhận':book.rag_ready?`Đã lập chỉ mục${book.indexing?.total_chunks?` · ${book.indexing.total_chunks} đoạn`:''}`:'Chưa có chỉ mục RAG';
    const fileInfo=$('book-confirmed-file-info');
    fileInfo.replaceChildren();
    if(file){
      const item=element('div',undefined,'confirmed-file-item');
      const icon=element('span',undefined,'confirmed-file-icon');
      icon.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3.5h8l4 4V20a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4.5a1 1 0 0 1 1-1Z"/><path d="M14 3.5V8h4M8 13h8M8 16h5"/></svg>';
      const name=element('div',undefined,'confirmed-file-name');
      name.append(element('span',file.name));
      name.append(element('small',`${(file.size/1024/1024).toFixed(2)} MB · ${book.rag_ready?'PDF đã tải lên':'PDF đã chọn'}`,'confirmed-file-meta'));
      item.append(icon,name);
      fileInfo.append(item,element('p',book.rag_ready?'Đã xử lý PDF và lập chỉ mục thành công.':'Tệp sẽ được tải lên khi xác nhận.','confirmed-file-note'));
    }else if(book.uploaded_filename){
      fileInfo.append(element('p',`PDF: ${book.uploaded_filename}`,'confirmed-file-note'));
    }
    $('cover-title').textContent=book.title;
    $('cover-series').textContent=seriesLabels[book.series]||book.series;
    const img = $('cover-image');
    img.hidden = true;
    img.removeAttribute('src');

    renderBookCovers($('book-cover'), book, loaded => {
      $('cover-fallback').hidden = loaded;
      $('book-cover').classList.toggle('has-volumes', loaded);
    });
    showBookFile(file,book);
  }
  function showBookFile(file, book = null) {
    if (bookObjectUrl) {
      URL.revokeObjectURL(bookObjectUrl);
      bookObjectUrl = null;
    }

    const url = file
      ? (bookObjectUrl = URL.createObjectURL(file))
      : book?.file_url;

    const viewer = $('book-file-viewer');
    const frame = $('book-file-frame');
    const note = $('book-viewer-note');

    viewer.querySelector('.volume-covers')?.remove();
    $('book-viewer-cover').hidden = true;
    $('book-viewer-cover').removeAttribute('src');

    viewer.hidden = !url && !book;
    frame.hidden = !url;
    note.hidden = true;
    $('book-file-open').hidden = !url;

    if (url) {
      $('book-file-viewer-title').textContent = 'Xem sách vừa tải';
      $('book-file-viewer-name').textContent =
        file?.name || book.uploaded_filename;
      frame.src = url;
      $('book-file-open').href = url;
      return;
    }

    frame.removeAttribute('src');
    $('book-file-open').removeAttribute('href');
    $('book-file-viewer-title').textContent = 'Xem sách đã chọn';
    $('book-file-viewer-name').textContent = book?.title || '';

    if (book) {
      renderBookCovers(viewer, book, loaded => {
        note.hidden = false;
        note.textContent = loaded
          ? 'Ảnh bìa sách. Chưa có PDF để xem nội dung.'
          : 'Chưa tải được ảnh bìa. Bạn vẫn có thể xác nhận sách.';
      });
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
      localStorage.setItem(PRIVATE_DOCUMENTS_KEY,JSON.stringify(privateDocuments.filter(item=>!item.server_saved)));
    }catch(error){
      console.error('EDUAGENT: Không thể lưu tài liệu riêng.',error);
      throw new Error('Không thể lưu tài liệu riêng trong trình duyệt.');
    }
  }
  function createCover(title,kind,subject,book=null){
    const cover=element('span',undefined,`document-cover ${kind==='private'?'private-cover':'book-cover'}`);
    cover.append(element('span',kind==='private'?'TÀI LIỆU':'EDUAGENT','cover-brand'));
    cover.append(element('strong',title,'cover-title'));
    cover.append(element('span',subject,'cover-subject'));
    if (kind === 'book' && book) {
      renderBookCovers(cover, book, loaded => {
        cover.classList.toggle('has-cover-image', loaded);
      });
    }
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
    if(document.file_url&&document.file_url.startsWith('/api/ui/books/')){
      const frame=element('iframe');
      frame.title=`Nội dung ${title}`;
      frame.src=document.file_url;
      preview.append(frame);
      const open=element('a','Mở toàn màn hình','preview-note');
      open.href=document.file_url;open.target='_blank';open.rel='noopener';
      preview.append(open);
    }else if(file&&(file.type==='application/pdf'||/\.pdf$/i.test(file.name))){
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
    detail.append(info);
    panel.append(detail);
    $('private-file-content').replaceChildren(preview);
    if(!document.pending)$('private-preview-files').replaceChildren();
  }
  const selectedPrivateFilesById=new Map();
  function showPrivateDetailEmpty(){
    const empty=element('div',undefined,'detail-empty');
    empty.append(element('span','▤','detail-empty-icon'));
    empty.lastElementChild.setAttribute('aria-hidden','true');
    empty.append(element('strong','Chọn một tài liệu để xem'));
    empty.append(element('p','Tài liệu đã thêm sẽ hiển thị nội dung xem trước tại đây.'));
    $('private-detail').replaceChildren(empty);
    $('private-preview-files').replaceChildren();
    $('private-file-content').replaceChildren(element('p','Chọn hoặc kéo thả file ở trên để xem nội dung tại đây.','viewer-placeholder'));
    if(previewObjectUrl){URL.revokeObjectURL(previewObjectUrl);previewObjectUrl=null;}
  }
  function previewSelectedPrivateFiles(files){
    for(const key of selectedPrivateFilesById.keys()){
      if(key.startsWith('pending-private-'))selectedPrivateFilesById.delete(key);
    }
    if(!files.length){selectedPrivateDocumentId=null;showPrivateDetailEmpty();return;}
    const tabs=$('private-preview-files');
    tabs.replaceChildren();
    const records=files.map((file,index)=>{
      const record={document_id:`pending-private-${index}`,kind:'private',pending:true,
        display_name:file.name,subject:$('private-subject').value,
        file:{name:file.name,size:file.size,type:file.type}};
      selectedPrivateFilesById.set(record.document_id,file);
      const button=element('button',file.name);
      button.type='button';button.setAttribute('aria-pressed',String(index===0));
      button.addEventListener('click',()=>{
        for(const tab of tabs.children)tab.setAttribute('aria-pressed',String(tab===button));
        showPrivateDetail(record);
      });
      tabs.append(button);
      return record;
    });
    showPrivateDetail(records[0]);
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
        kind==='private'?record.subject:`LỚP ${record.grade||10} · ${record.subject}`,record));
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
        remove.addEventListener('click',async()=>{
          if(!confirm(`Gỡ tài liệu "${record.display_name}"?`))return;
          if(record.server_saved){
            try{
              await api(`/api/ui/books/mine/${encodeURIComponent(id)}?student_id=${encodeURIComponent(STUDENT_ID)}`,{method:'DELETE'});
              if(selectedPrivateDocumentId===id){selectedPrivateDocumentId=null;showPrivateDetailEmpty();}
              await loadMine();status('Đã gỡ tài liệu khỏi danh sách.');
            }catch(error){status(error.message,true);}
            return;
          }
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
    $('book-subject').value='';
    $('book-name').value='';
    $('confirm-book').textContent='Xác nhận sách';
    $('cancel-edit-book').hidden=true;
    clearBookFile();
  }
  function clearBookFile(){
    selectedBookFile=null;
    $('book-file').value='';
    $('book-file-info').replaceChildren();
    $('book-drop').classList.remove('has-file');
    $('book-drop').querySelector('strong').textContent='Chọn sách hoặc kéo thả tệp vào đây';
    $('series').disabled=false;
    $('book-subject').disabled=false;
  }
  async function editBook(book){
    clearBookFile();
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
    const file=selectedBookFile;
    const title=$('book-name').value.trim();if(!title&&!file)return;
    const existing=catalog.find(b=>b.title.toLocaleLowerCase('vi')===title.toLocaleLowerCase('vi'));
    const body={student_id:STUDENT_ID,book_id:existing?.book_id||null,title,series:$('series').value,subject:$('book-subject').value,
      display_name:$('display-name').value.trim()||title,description:$('description').value.trim()};
    const btn=$('confirm-book');
    const controls=[...$('book-form').querySelectorAll('input,select,textarea,button'),$('book-file')];
    controls.forEach(control=>control.disabled=true);
    $('book-drop').setAttribute('aria-busy','true');
    try {
      const editing=Boolean(editingDocumentId);
      let book;
      if(file||!editing){
        const form=new FormData();
        if(file)form.append('file',file,file.name);
        form.append('student_id',STUDENT_ID);
        form.append('title',title);
        form.append('subject',body.subject);
        form.append('series',body.series);
        form.append('display_name',$('display-name').value.trim());
        form.append('description',body.description);
        if(editing)form.append('document_id',editingDocumentId);
        btn.textContent='Đang xử lý…';
        status('Đang lập chỉ mục giáo án theo môn và bộ sách đã chọn.');
        book=await indexWithProgress('/api/ui/books/upload',form,'book-indexing-progress',title);
      }else{
        const url=editing?`/api/ui/books/mine/${encodeURIComponent(editingDocumentId)}`:'/api/ui/books/attach';
        book=await api(url,{method:editing?'PUT':'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      }
      cancelEdit();
      showPreview(book,file);await loadMine();
      status(book.rag_ready?'Đã xác nhận sách và lập chỉ mục thành công.':'Đã cập nhật thông tin sách.');
    }catch(err){status(err.message,true);}finally{
      controls.forEach(control=>control.disabled=false);
      $('series').disabled=false;
      $('book-subject').disabled=false;
      $('book-drop').removeAttribute('aria-busy');
      btn.textContent=editingDocumentId?'Lưu thay đổi':'Xác nhận sách';
    }
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
    zone.addEventListener('click',()=>{if(!input.disabled)input.click();});
    zone.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();if(!input.disabled)input.click();}});
    input.addEventListener('change',()=>display([...input.files]));
    zone.addEventListener('dragover',e=>{e.preventDefault();zone.classList.add('dragging');});
    zone.addEventListener('dragleave',e=>{
      if(!zone.contains(e.relatedTarget))zone.classList.remove('dragging');
    });
    zone.addEventListener('drop',e=>{
      e.preventDefault();zone.classList.remove('dragging');
      if(input.disabled)return;
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
    const normalized=(selectedBookFile?.name||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[đĐ]/g,'d').toLowerCase().replace(/[^a-z0-9]+/g,' ');
    const words=` ${normalized.trim()} `;
    const has=alias=>words.includes(` ${alias} `);
    const detectedSubjects=[['Toán',['toan']],['Lịch sử',['lich su','su']],['Ngữ văn',['ngu van','van']]]
      .filter(([,aliases])=>aliases.some(has));
    const detectedSeries=[['chan_troi',['chan troi sang tao','ctst']],['canh_dieu',['canh dieu','cd']],['ket_noi',['ket noi tri thuc','kntt']]]
      .filter(([,aliases])=>aliases.some(has));
    if(detectedSubjects.length===1)$('book-subject').value=detectedSubjects[0][0];
    if(detectedSeries.length===1)$('series').value=detectedSeries[0][0];
    $('book-subject').disabled=false;
    $('series').disabled=false;
    loadCatalog().catch(error=>status(error.message,true));
    $('book-drop').querySelector('strong').textContent=selectedBookFile
      ?'Đã chọn sách — nhấn để thay tệp'
      :'Chọn sách hoặc kéo thả tệp vào đây';
    if(selectedBookFile&&!$('book-name').value.trim()){
      $('book-name').value=selectedBookFile.name.replace(/\.pdf$/i,'').replace(/[_-]+/g,' ').trim();
    }
    previewBookSelection();
    if(selectedBookFile){
      showBookFile(selectedBookFile);
      $('book-drop').classList.add('has-file');
      status(`Đã chọn ${selectedBookFile.name}. Kiểm tra môn, bộ sách và Tên sách trước khi xác nhận.`);
    }else{
      $('book-drop').classList.remove('has-file');
    }
  });
  wireDrop('private-drop','private-file','private-file-info',['pdf','docx','txt','jpg','jpeg','png'],files=>{
    selectedPrivateFiles=files;
    previewSelectedPrivateFiles(files);
    if(files.length===1&&!$('private-name').value.trim()){
      $('private-name').value=files[0].name.replace(/\.[^.]+$/,'').replace(/[_-]+/g,' ').trim();
    }
  });
  $('private-form').addEventListener('submit',async event=>{
    event.preventDefault();
    const subject=$('private-subject').value==='Khác'?$('custom-subject').value.trim():$('private-subject').value;
    const baseName=$('private-name').value.trim();
    if(!subject){status('Vui lòng nhập tên môn học.',true);return;}
    if(!baseName&&!selectedPrivateFiles.length){status('Vui lòng nhập tên tài liệu hoặc chọn file.',true);return;}
    const files=selectedPrivateFiles.length?[...selectedPrivateFiles]:[null];
    const description=$('private-description').value.trim();
    const controls=[...$('private-form').querySelectorAll('input,select,textarea,button')];
    controls.forEach(control=>control.disabled=true);
    try{
      for(const file of files){
        const stem=file?.name.replace(/\.[^.]+$/,'').replace(/[_-]+/g,' ').trim();
        const name=files.length>1?(baseName?`${baseName} · ${stem}`:stem):baseName||stem;
        let record;
        if(file&&/\.pdf$/i.test(file.name)){
          const form=new FormData();
          form.append('file',file,file.name);form.append('student_id',STUDENT_ID);
          form.append('name',name);form.append('subject',subject);form.append('description',description);
          status(`Đang lưu và lập chỉ mục ${name}…`);
          record=await indexWithProgress('/api/ui/books/private/upload',form,'private-indexing-progress',name);
        }else{
          record={document_id:`private-${Date.now()}-${Math.random().toString(36).slice(2)}`,
            kind:'private',display_name:name,subject,description,
            file:file?{name:file.name,size:file.size,type:file.type,last_modified:file.lastModified}:null,
            created_at:new Date().toISOString()};
        }
        privateDocuments.push(record);
        if(file)selectedPrivateFilesById.set(record.document_id,file);
        savePrivateDocuments();
        showPrivateDetail(record);renderLibrary();
      }
      $('private-form').reset();$('private-subject').value='Toán';
      $('custom-subject-wrap').hidden=true;$('custom-subject').required=false;
      $('private-file-info').replaceChildren();selectedPrivateFiles=[];
      status('Đã thêm tài liệu. Chọn tài liệu trong thư viện để xem nội dung.');
    }catch(error){status(error.message,true);}
    finally{controls.forEach(control=>control.disabled=false);}
  });
  async function loadMine(){
    const d=await api(`/api/ui/books/mine?student_id=${encodeURIComponent(STUDENT_ID)}`);
    const records=d.documents||[];
    books=records.filter(item=>item.kind!=='private');
    privateDocuments=[...records.filter(item=>item.kind==='private'),...getPrivateDocuments().filter(item=>!item.server_saved)];
    renderLibrary();
    if(selectedPrivateDocumentId&&!selectedPrivateDocumentId.startsWith('pending-private-')){
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

