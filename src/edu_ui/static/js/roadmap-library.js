/* Library and calendar share the same canonical plan/session IDs and JSON progress. */
(() => {
  'use strict';
  const app = document.querySelector('#roadmap-app'), root = document.querySelector('#rl-root'), status = document.querySelector('#rl-status');
  const F = window.EduFlow;
  if (!F) {status.textContent = 'Thiếu workflow.js. Cập nhật đủ file rồi nhấn Ctrl+F5.'; return;}
  const {element: el, rich} = F;
  const calendarMode = app.dataset.page === 'schedule';
  const dialog = document.querySelector('#rl-completion-dialog');
  let planData = null, catalogData = null, completionTarget = null, loading = false, requestGeneration = 0;
  const statusLabels = {not_started: 'Chưa bắt đầu', in_progress: 'Đang học', window_completed: 'Đã học hết phần đã soạn', completed: 'Hoàn thành lộ trình'};
  const typeLabels = {lesson: 'Học kiến thức', review: 'Ôn tập', assessment: 'Đánh giá'};
  const difficultyLabels = {easy: 'Cơ bản', medium: 'Trung bình', hard: 'Nâng cao'};
  const base = '/api/ui/roadmaps';
  const params = () => new URLSearchParams(location.search);
  const safeGet = key => {try {return JSON.parse(localStorage.getItem(key) || 'null');} catch {return null;}};
  const safeSet = (key, value) => {try {localStorage.setItem(key, JSON.stringify(value));} catch {}};
  function notice(text = '', error = false) {status.textContent = text; status.className = error ? 'rl-status rl-error' : 'rl-status';}
  async function api(url, body, method) {
    if (!method || method === 'POST') return F.api(url, body);
    const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 25000);
    try {
      const r = await fetch(url, {method, signal: controller.signal, headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
      const data = await r.json().catch(() => ({}));
      if (!r.ok) {const e = new Error(typeof data.detail === 'string' ? data.detail : `Không xử lý được yêu cầu (${r.status})`); e.status = r.status; throw e;}
      return data;
    } catch (e) {if (e.name === 'AbortError') throw new Error('Server chưa phản hồi. Tải lại để kiểm tra trạng thái trước khi xác nhận tiếp.'); throw e;}
    finally {clearTimeout(timer);}
  }

  function go(query, page = calendarMode ? '/schedule' : '/roadmap', replace = false) {
    const q = new URLSearchParams(query); history[replace ? 'replaceState' : 'pushState']({}, '', page + (q.size ? '?' + q : '')); void load();
  }
  function link(text, href, cls = 'rl-button rl-quiet') {const a = el('a', cls, text); a.href = href; return a;}
  function button(text, handler, cls = 'rl-button') {const b = el('button', cls, text); b.type = 'button'; b.addEventListener('click', handler); return b;}
  function dateLabel(value) {
    if (!value) return 'Chưa có ngày';
    const d = new Date(value + 'T00:00:00'); return Number.isNaN(d.getTime()) ? value : d.toLocaleDateString('vi-VN', {weekday: 'short', day: '2-digit', month: '2-digit', year: 'numeric'});
  }
  function completedLabel(value) {if (!value) return 'Chưa ghi nhận thời điểm'; const d = new Date(value); return Number.isNaN(d.getTime()) ? value : d.toLocaleString('vi-VN');}
  function timeLabel(s) {
    const start = s.start_time || 'Chưa có giờ';
    if (!/^\d\d:\d\d$/.test(start) || !Number.isFinite(s.minutes)) return start;
    const [h, m] = start.split(':').map(Number), end = h * 60 + m + s.minutes;
    return `${start} – ${String(Math.floor(end / 60) % 24).padStart(2, '0')}:${String(end % 60).padStart(2, '0')}${end >= 1440 ? ' (+1 ngày)' : ''}`;
  }
  function flat(data) {return (data.weeks || []).flatMap(w => (w.sessions || []).map((s, i) => ({...s, week_no: w.week_no, session_no: i + 1})));}
  function subject(data) {return data.subject || 'Chưa xác định môn';}
  function shortQuery(changes) {const p = params(); Object.entries(changes).forEach(([k,v]) => v === '' || v == null ? p.delete(k) : p.set(k, v)); return Object.fromEntries(p);}
  function pageHeader(kicker, title, description, actions = []) {
    const header = el('header', 'rl-heading'), copy = el('div'); copy.append(el('p', 'rl-kicker', kicker), el('h1', '', title), el('p', 'rl-muted', description));
    const right = el('div', 'rl-actions'); actions.forEach(a => right.append(a)); header.append(copy, right); root.append(header);
  }
  function filter(label, values, selected, onChange) {
    const l = el('label', 'rl-filter'), select = el('select'); l.append(el('span', '', label));
    values.forEach(([value, text]) => {const o = el('option', '', text); o.value = value; select.append(o);}); select.value = selected || '';
    select.addEventListener('change', () => onChange(select.value)); l.append(select); return l;
  }
  function empty(text) {const box = el('div', 'rl-empty'); box.append(el('h3', '', 'Chưa có nội dung phù hợp'), el('p', '', text)); return box;}
  function stats(entries) {const box = el('div', 'rl-stats'); entries.forEach(([value,label])=>{const item = el('div'); item.append(el('strong','',value),el('span','',label));box.append(item);}); return box;}
  function progress(info) {const outer=el('div','rl-progress'), bar=el('span');bar.style.width=`${info.progress_percent || 0}%`;outer.append(bar);outer.setAttribute('aria-label',`${info.completed_count}/${info.session_count} buổi chi tiết đã học`);return outer;}

  async function library() {
    const p = params(), generation = ++requestGeneration;
    const data = await api(base + '?' + new URLSearchParams({subject:p.get('subject')||'',status:p.get('status')||'',q:p.get('q')||'',sort:p.get('sort')||'newest'}));
    if (generation !== requestGeneration) return; catalogData = data; root.replaceChildren();
    pageHeader('THƯ VIỆN CỦA BẠN', 'Lộ trình học', 'Mỗi mục là một lộ trình riêng. Lọc theo môn, chọn một kế hoạch rồi mở từng buổi học.', [link('Lịch học & Buổi học', '/schedule'+(p.get('subject')?'?'+new URLSearchParams({subject:p.get('subject')}):'')), link('+ Tạo lộ trình', '/?mode=planning', 'rl-button')]);
    const toolbar = el('form','rl-toolbar');
    toolbar.append(filter('Môn học', [['','Tất cả môn'],...data.subjects.map(s=>[s,s])],p.get('subject'), value=>go(shortQuery({subject:value}))));
    toolbar.append(filter('Tiến độ', [['','Tất cả tiến độ'],...Object.entries(statusLabels)],p.get('status'),value=>go(shortQuery({status:value}))));
    toolbar.append(filter('Sắp xếp', [['newest','Mới nhất'],['start_date','Ngày bắt đầu'],['progress','Tiến độ giảm dần']],p.get('sort')||'newest',value=>go(shortQuery({sort:value}))));
    const search=el('label','rl-filter rl-search');search.append(el('span','','Tìm lộ trình'));const input=el('input');input.placeholder='Tên lộ trình hoặc môn học…';input.value=p.get('q')||'';search.append(input);toolbar.append(search,button('Tìm',()=>go(shortQuery({q:input.value.trim()})),'rl-button rl-quiet'));
    toolbar.addEventListener('submit',e=>{e.preventDefault();go(shortQuery({q:input.value.trim()}));});root.append(toolbar);
    const plans=data.roadmaps||[];root.append(el('p','rl-muted',`${plans.length} lộ trình đang hiển thị · học sinh ${data.student_id}`));
    if(!plans.length){root.append(empty('Bạn có thể tạo lộ trình từ trang Trợ lý AI, hoặc thay đổi bộ lọc.'));return;}
    for(const name of [...new Set(plans.map(subject))]){
      const group=el('section','rl-subject-group');const title=el('h2','',name);group.append(title);const grid=el('div','rl-plan-grid');
      plans.filter(x=>subject(x)===name).forEach(plan=>{
        const card=el('article','rl-plan-card'), tag=el('span','rl-tag',statusLabels[plan.status]||'Chưa bắt đầu');
        card.append(tag,el('h3','',plan.title||'Lộ trình học'),el('p','rl-muted',`${dateLabel(plan.schedule.start_date)} → ${dateLabel(plan.schedule.end_date)}`));
        if(plan.goal)card.append(el('p','rl-muted',plan.goal.slice(0,130)+(plan.goal.length>130?'…':'')));
        if(plan.created_at)card.append(el('p','rl-muted',`Tạo lúc ${completedLabel(plan.created_at)}`));
        card.append(el('p','rl-plan-facts',`${plan.schedule.total_weeks||'—'} tuần tổng quan · ${plan.session_count} buổi đã soạn`),progress(plan),el('p','rl-muted',`${plan.completed_count}/${plan.session_count} buổi chi tiết đã học`));
        const actions=el('div','rl-actions');actions.append(link('Mở lộ trình',`/roadmap?plan=${encodeURIComponent(plan.plan_id)}`,'rl-button'),link('Toàn thể',`/roadmap?plan=${encodeURIComponent(plan.plan_id)}&view=overview`));card.append(actions);grid.append(card);
      });group.append(grid);root.append(group);
    }
  }

  function completionButton(s, planId, version) {
    const b=button(s.completed?'✓ Đã học':'○ Chưa học',()=>openCompletion(s,planId,version),'rl-mark'+(s.completed?' is-completed':''));b.setAttribute('aria-pressed',String(Boolean(s.completed)));b.title=s.completed?'Bấm để bỏ đánh dấu đã học':'Bấm để xác nhận đã học xong';return b;
  }
  function openCompletion(s, planId, version) {
    completionTarget={s,planId,version,completed:!s.completed};
    document.querySelector('#rl-dialog-title').textContent=s.completed?'Bỏ đánh dấu đã học?':'Xác nhận đã học xong?';
    document.querySelector('#rl-dialog-description').textContent=`${s.lesson} · ${dateLabel(s.date)} · ${timeLabel(s)}. ${s.completed?'Thời điểm xác nhận cũ sẽ được xóa.':'Hệ thống sẽ lưu trạng thái và thời điểm bạn xác nhận.'}`;
    document.querySelector('#rl-dialog-error').textContent='';document.querySelector('#rl-confirm-completion').textContent=s.completed?'Bỏ đánh dấu':'Xác nhận đã học';dialog.showModal();
  }
  document.querySelector('#rl-confirm-completion').addEventListener('click',async()=>{
    if(!completionTarget||loading)return;loading=true;const b=document.querySelector('#rl-confirm-completion');b.disabled=true;
    const {s,planId,version,completed}=completionTarget;
    try {await api(`${base}/${planId}/sessions/${encodeURIComponent(s.session_id)}/completion`,{completed,expected_version:version},'PUT');dialog.close();await load();notice(completed?'Đã lưu: buổi học hoàn thành.':'Đã bỏ đánh dấu buổi học.');}
    catch(e){if(e.status===409){dialog.close();await load();notice(e.message,true);}else document.querySelector('#rl-dialog-error').textContent=e.message;}
    finally {loading=false;b.disabled=false;}
  });

  function planNavigation(data, info, view) {
    const headerActions=[link('Tất cả lộ trình','/roadmap'),link('Lịch của lộ trình',`/schedule?plan=${data.plan_id}`)];
    pageHeader(subject(data),data.title||'Lộ trình học',`${dateLabel(data.schedule?.start_date)} → ${dateLabel(data.schedule?.end_date)}`,headerActions);
    root.append(stats([[data.schedule?.total_weeks||'—','Tuần tổng quan'],[info.session_count,'Buổi đã soạn'],[info.completed_count,'Buổi đã học'],[`${info.progress_percent}%`,'Tiến độ phần đã soạn']]));
    const nav=el('nav','rl-view-nav');nav.setAttribute('aria-label','Chế độ xem lộ trình');
    [['sessions','Các buổi học'],['overview','Lộ trình toàn thể']].forEach(([value,label])=>{const a=link(label,`/roadmap?plan=${data.plan_id}&view=${value}`,value===view?'rl-button':'rl-button rl-quiet');if(value===view)a.setAttribute('aria-current','page');nav.append(a);});
    nav.append(button('Tải PDF toàn thể',()=>printPlan(data),'rl-button rl-quiet'));root.append(nav);
    if(!info.fully_detailed)root.append(el('p','rl-notice',`Hiện có ${info.detailed_weeks} tuần với buổi chi tiết. Khung tổng quan còn các tuần/giai đoạn khác; tiến độ chỉ tính trên ${info.session_count} buổi đã được soạn.`));
  }
  async function planPage() {
    const p=params(), pid=p.get('plan'),generation=++requestGeneration;
    const data=await api(`${base}/${encodeURIComponent(pid)}`);if(generation!==requestGeneration)return;planData=data;root.replaceChildren();
    if(p.get('session')){sessionPage(data.path,data.summary,p.get('session'));return;}
    const view=p.get('view')==='overview'?'overview':'sessions';planNavigation(data.path,data.summary,view);
    if(view==='overview')root.append(overview(data.path));else sessionList(data.path,data.summary);
  }
  function overview(data) {
    const area=el('section','rl-overview');
    if(data.overview?.muc_tieu_tong){const box=el('div','rl-card');box.append(el('h2','','Mục tiêu và chiến lược'),rich('p','',data.overview.muc_tieu_tong),rich('p','',data.overview.chien_luoc||''));area.append(box);}
    (data.outline||[]).forEach(phase=>{
      const box=el('article','rl-card');box.append(el('h2','',`Giai đoạn ${phase.phase}`));
      box.append(F.table(['Tuần','Mục tiêu','Bài học','Hoạt động'],(phase.weeks||[]).map(w=>[w.week_no,w.goal,(w.lessons||[]).map(l=>`Chương ${l.chapter_id}: ${l.lesson}`).join('\n'),(w.activity_types||[]).join(', ')])));area.append(box);
    });
    if(data.assumptions?.length){const d=el('details','rl-card');d.append(el('summary','','Giả định và điểm cần kiểm chứng'));data.assumptions.forEach(x=>d.append(rich('p','',x)));area.append(d);}return area;
  }
  function allWeekNumbers(data) {return [...new Set([...(data.outline||[]).flatMap(p=>(p.weeks||[]).map(w=>w.week_no)),...(data.weeks||[]).map(w=>w.week_no)])].sort((a,b)=>a-b);}
  function sessionList(data, info) {
    const chosen=params().get('week')||'',layout=el('div','rl-study-layout'),sidebar=el('aside','rl-week-list');sidebar.append(el('h3','','Chọn tuần'));
    const weeks=allWeekNumbers(data);[['','Tất cả buổi'],...weeks.map(w=>[String(w),`Tuần ${w}`])].forEach(([value,label])=>{
      const b=button(label,()=>go({plan:data.plan_id,view:'sessions',week:value}),'rl-week-button'+(chosen===value?' active':''));sidebar.append(b);
    });const main=el('section','rl-session-grid');let items=flat(data);if(chosen)items=items.filter(s=>String(s.week_no)===chosen);
    items.forEach(s=>{
      const card=el('article','rl-session-card'),top=el('div','rl-card-top');top.append(el('span','rl-kicker',`TUẦN ${s.week_no} · BUỔI ${s.session_no}`),completionButton(s,data.plan_id,data.progress_version||0));card.append(top);
      card.append(el('h3','',s.lesson),el('p','rl-date',dateLabel(s.date)),el('p','rl-muted',`${timeLabel(s)} · ${s.minutes} phút`));
      const tags=el('div','rl-tags');tags.append(el('span','rl-tag',typeLabels[s.type]||s.type||'Buổi học'),el('span','rl-tag',difficultyLabels[s.difficulty]||s.difficulty||''));card.append(tags);
      if(s.completed)card.append(el('p','rl-completed-at',`Xác nhận lúc ${completedLabel(s.completed_at)}`));
      card.append(link('Xem buổi học',`/roadmap?plan=${data.plan_id}&session=${s.session_id}`,'rl-button'));main.append(card);
    });
    if(!items.length)main.append(empty(chosen?'Tuần này thuộc khung tổng quan, chưa có buổi học chi tiết được soạn.':'Lộ trình này chưa có buổi học chi tiết.'));
    layout.append(sidebar,main);root.append(layout);
  }

  function listBlock(title, values) {const box=el('section','rl-card');box.append(el('h3','',title));const ul=el('ul');(values||[]).forEach(x=>ul.append(rich('li','',x)));if(values?.length)box.append(ul);else box.append(el('p','rl-muted','Chưa có nội dung được lưu.'));return box;}
  function resources(values) {
    const area=el('div','rl-resource-list');
    (values||[]).forEach(r=>{
      const card=el('article','rl-resource');let url=null;try{const u=new URL(r.url);if(['http:','https:'].includes(u.protocol))url=u.href;}catch{}
      const label=r.type==='video'?'Video':'Tài liệu';card.append(el('span','rl-tag',label),el('h3','',r.title||r.tieu_de||label));if(r.note||r.ghi_chu)card.append(rich('p','rl-muted',r.note||r.ghi_chu));
      if(url){const actions=el('div','rl-actions');actions.append(link(`Mở ${label.toLowerCase()} ↗`,url,'rl-button rl-quiet'));
        actions.querySelector('a').target='_blank';actions.querySelector('a').rel='noopener noreferrer';
        actions.append(button('Sao chép link',async e=>{try{await navigator.clipboard.writeText(url);e.target.textContent='Đã sao chép';}catch{const input=el('input','rl-url');input.value=url;input.readOnly=true;actions.append(input);input.focus();input.select();}},'rl-button rl-quiet'));card.append(actions);
      }else card.append(el('p','rl-muted','Tài nguyên chưa có liên kết hợp lệ.'));area.append(card);
    });if(!values?.length)area.append(empty('Buổi học này chưa có tài nguyên được lưu.'));return area;
  }
  function sessionPage(data, info, sessionId) {
    const s=flat(data).find(x=>x.session_id===sessionId);if(!s){root.append(empty('Không tìm thấy buổi học này trong lộ trình.'));return;}
    const savedCalendar = new URLSearchParams(params().get('return_query') || '');
    const returnTo=params().get('return')==='schedule'?(savedCalendar.size?'/schedule?'+savedCalendar:`/schedule?plan=${data.plan_id}`):`/roadmap?plan=${data.plan_id}&week=${s.week_no}`;
    pageHeader(`${subject(data)} · TUẦN ${s.week_no} · BUỔI ${s.session_no}`,s.lesson,`${dateLabel(s.date)} · ${timeLabel(s)} · ${s.minutes} phút`,[link('← Quay lại',returnTo),link('Xem lộ trình toàn thể',`/roadmap?plan=${data.plan_id}&view=overview`)]);
    const actions=el('div','rl-session-actions');actions.append(completionButton(s,data.plan_id,data.progress_version||0),el('span','rl-muted',s.completed?`Xác nhận hoàn thành: ${completedLabel(s.completed_at)}`:'Chưa xác nhận đã học xong'));root.append(actions);
    const tab=params().get('tab')||'knowledge',nav=el('nav','rl-view-nav');[['knowledge','Nội dung'],['activities','Hoạt động'],['resources','Tài nguyên'],['practice','Luyện tập']].forEach(([value,label])=>{
      const b=button(label,()=>go(shortQuery({tab:value})),tab===value?'rl-button':'rl-button rl-quiet');b.setAttribute('aria-pressed',String(tab===value));nav.append(b);
    });root.append(nav);const content=el('section','rl-session-content');
    if(tab==='resources')content.append(resources(s.resources));
    else if(tab==='activities'){
      const list=el('div','rl-activity-list');let offset=0;
      (s.activities||[]).forEach((a,index)=>{const item=el('article','rl-activity');item.append(el('span','rl-activity-time',`${offset}–${offset+(a.minutes||0)} phút`),el('div',''));const body=item.lastElementChild;body.append(el('p','rl-kicker',`HOẠT ĐỘNG ${index+1}`),rich('div','',a.content),el('p','rl-muted',`${a.minutes||0} phút · ${difficultyLabels[a.difficulty]||a.difficulty||''}`));offset+=a.minutes||0;list.append(item);});
      content.append(list.children.length?list:empty('Chưa có hoạt động chi tiết.'));
    }else if(tab==='practice')renderPractice(content,data,s);
    else{const columns=el('div','rl-content-columns');columns.append(listBlock('Trọng tâm buổi học',s.key_points),listBlock('Cần nắm',s.must_know),listBlock('Cần hiểu',s.must_understand));content.append(columns);
      if(s.related?.length)content.append(listBlock('Kiến thức liên quan',s.related.map(r=>`${r.lesson} — ${r.relation}`)));
      if(s.assessment)content.append(el('p','rl-notice',`Phạm vi đánh giá: chương ${(s.assessment.chapter_ids||[]).join(', ')} · ${s.assessment.num_questions||'—'} câu.`));
    }root.append(content);
  }

  function renderPractice(content,data,s) {
    if(!data.subject){content.append(empty('Lộ trình cũ chưa xác định được môn học. Cần bổ sung trường subject trong JSON lộ trình trước khi tạo bài ôn tập.'));return;}
    if(!s.exam_enabled){content.append(empty('Buổi này chưa bật tạo bài kiểm tra. Bạn vẫn có thể học và luyện theo tài nguyên đã lưu.'));return;}
    const area=el('section','rl-card');area.append(el('h2','','Bài ôn tập theo buổi'),el('p','rl-muted','Tạo đề dựa trên đúng môn và bài học của buổi này.'));
    const key=`eduagent-library-practice-${data.plan_id}-${s.session_id}`,saved=safeGet(key);
    function showResult(result){if(typeof result.exam_url!=='string'||!/^\/exams\?/.test(result.exam_url))throw new Error('Liên kết bài kiểm tra không hợp lệ.');const a=link('Làm bài test',result.exam_url,'rl-button');area.append(a);if(Array.isArray(result.tests))area.append(resources(result.tests));}
    if(saved?.result){showResult(saved.result);content.append(area);return;}
    const start=button(saved?.job_id?'Tiếp tục chờ bài kiểm tra':'Tạo bài ôn tập',async()=>{
      start.disabled=true;const progressNode=el('div');area.append(progressNode);
      try{
        let record=safeGet(key);
        if(!record?.job_id){const context=await api(`${base}/${data.plan_id}/practice-context`,{});const job=await api(`/api/ui/workflows/${context.session_id}/practice`,{week_no:s.week_no,session_no:s.session_no,revision:context.revision,request_id:F.id()});record={job_id:job.job_id};safeSet(key,record);}
        const result=await F.poll(record.job_id,steps=>F.progress(progressNode,steps));safeSet(key,{result});showResult(result);start.remove();progressNode.remove();
      }catch(e){notice(e.message,true);safeSet(key,null);start.disabled=false;start.textContent='Thử tạo lại bài ôn tập';}
    });area.append(start);content.append(area);
  }

  async function calendar() {
    const p=params(),generation=++requestGeneration;
    const [libraryData,data]=await Promise.all([api(base),api(`${base}/calendar?`+p.toString())]);if(generation!==requestGeneration)return;root.replaceChildren();
    pageHeader('LỊCH HỌC & BUỔI HỌC','Các buổi học của bạn','Ngày giờ dự kiến theo lộ trình. Dấu đã học và thời điểm xác nhận được lưu chung với thư viện lộ trình.',[link('Thư viện lộ trình','/roadmap')]);
    const bar=el('form','rl-toolbar');bar.append(filter('Môn học',[['','Tất cả môn'],...libraryData.subjects.map(s=>[s,s])],p.get('subject'),v=>go(shortQuery({subject:v}))));
    bar.append(filter('Lộ trình',[['','Tất cả lộ trình'],...libraryData.roadmaps.map(x=>[x.plan_id,x.title])],p.get('plan_id')||p.get('plan'),v=>go(shortQuery({plan_id:v,plan:null}))));
    bar.append(filter('Trạng thái',[['','Tất cả buổi'],['pending','Chưa học'],['completed','Đã học']],p.get('status'),v=>go(shortQuery({status:v}))));
    for(const [key,label] of [['date_from','Từ ngày'],['date_to','Đến ngày']]){const l=el('label','rl-filter');l.append(el('span','',label));const input=el('input');input.type='date';input.value=p.get(key)||'';input.addEventListener('change',()=>go(shortQuery({[key]:input.value})));l.append(input);bar.append(l);}bar.addEventListener('submit',e=>e.preventDefault());root.append(bar);
    root.append(el('p','rl-muted',`${data.sessions.length} buổi phù hợp`));
    const groups=new Map();data.sessions.forEach(s=>{const key=s.date||'';if(!groups.has(key))groups.set(key,[]);groups.get(key).push(s);});
    groups.forEach((items,date)=>{const day=el('section','rl-calendar-day');day.append(el('h2','',dateLabel(date)));
      items.forEach(s=>{const row=el('article','rl-calendar-row');row.append(el('div','rl-calendar-time',timeLabel(s)));const info=el('div','rl-calendar-copy');info.append(link(s.lesson,`/roadmap?plan=${s.plan_id}&session=${s.session_id}&return=schedule&return_query=${encodeURIComponent(location.search.slice(1))}`,'rl-session-link'),el('p','rl-muted',`${s.subject||'Chưa xác định môn'} · Tuần ${s.week_no}, buổi ${s.session_no} · ${s.minutes} phút`),el('p','rl-muted',s.plan_title||''));row.append(info,completionButton(s,s.plan_id,s.progress_version));if(s.completed)info.append(el('p','rl-completed-at',`Xác nhận lúc ${completedLabel(s.completed_at)}`));day.append(row);});root.append(day);
    });if(!data.sessions.length)root.append(empty('Không có buổi học trong khoảng thời gian và bộ lọc đã chọn.'));
  }
  function printPlan(data) {
    const copy=el('section','rl-print-document');copy.append(el('h1','',data.title||'Lộ trình học'),el('p','',`${subject(data)} · ${dateLabel(data.schedule?.start_date)} → ${dateLabel(data.schedule?.end_date)}`),overview(data));
    flat(data).forEach(s=>{const box=el('article','rl-print-session');box.append(el('h2','',`Tuần ${s.week_no} · Buổi ${s.session_no}: ${s.lesson}`),el('p','',`${dateLabel(s.date)} · ${timeLabel(s)} · ${s.minutes} phút · ${s.completed?'Đã học':'Chưa học'}`),listBlock('Trọng tâm',s.key_points),listBlock('Cần nắm',s.must_know),listBlock('Cần hiểu',s.must_understand));if(s.activities?.length)box.append(F.table(['Hoạt động','Phút'],s.activities.map(a=>[a.content,a.minutes])));if(s.resources?.length)box.append(resources(s.resources));copy.append(box);});copy.querySelectorAll('details').forEach(d=>d.open=true);document.body.append(copy);document.body.classList.add('rl-printing');const clean=()=>{copy.remove();document.body.classList.remove('rl-printing');};window.addEventListener('afterprint',clean,{once:true});window.print();
  }
  async function load() {
    const p=params();notice('Đang tải dữ liệu…');
    try{
      if(calendarMode){const args=p.get('plan');if(args){history.replaceState({},'', '/schedule?'+new URLSearchParams({...Object.fromEntries(p),plan_id:args}));const u=new URL(location.href);u.searchParams.delete('plan');history.replaceState({},'',u);}await calendar();}
      else if(p.get('session')&&!p.get('plan')){
        try{const imported=await api(`${base}/from-session/${encodeURIComponent(p.get('session'))}`,{});go({plan:imported.plan_id},'/roadmap',true);return;}
        catch{go({},'/roadmap',true);notice('Phiên chat không còn trong bộ nhớ. Hãy mở lộ trình đã lưu trong thư viện.');return;}
      }else if(p.get('plan'))await planPage();else await library();
      notice('');
    }catch(e){notice(e.message,true);if(!root.children.length)root.append(link('Về thư viện lộ trình','/roadmap'));}
  }
  window.addEventListener('popstate',()=>void load());
  document.addEventListener('visibilitychange',()=>{if(!document.hidden&&!dialog.open)void load();});
  void load();
})();
