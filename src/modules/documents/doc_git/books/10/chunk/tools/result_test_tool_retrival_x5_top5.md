============================================================
RETRIEVER + RERANKER EVALUATION (TOP-5)
============================================================

Total Queries : 135

┌─────────┬───────┬─────────┐
│ Metric  │ Count │ Rate    │
├─────────┼───────┼─────────┤
│ Top-1   │ 113   │ 83.70%  │
│ Top-2   │ 12    │ 8.89%   │
│ Top-3   │ 8     │ 5.93%   │
│ Top-4   │ 2     │ 1.48%   │
│ Top-5   │ 0     │ 0.00%   │
│ Miss    │ 0     │ 0.00%   │
├─────────┼───────┼─────────┤
│ Hit@5   │ 135   │ 100.00% │
└─────────┴───────┴─────────┘

Recall@1 = 83.70%
Recall@2 = 92.59%
Recall@3 = 98.52%
Recall@4 = 100.00%
Recall@5 = 100.00%

=====================

Query 1 [Dễ]: "8 là số chẵn" là mệnh đề đúng hay sai? (xet_menh_de)

Tool 1: xet_menh_de
Tool 2: tinh_phuong_sai_do_lech_chuan
Tool 3: sai_so_tuong_doi
Tool 4: tinh_trung_vi_mode
Tool 5: tinh_trung_binh

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.5546167492866516
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.009594297967851162
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.0049802749417722225
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.004500451497733593
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.0022681397385895252
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.
=====================

Query 2 [Dễ]: "Hà Nội là thủ đô của Việt Nam" là mệnh đề đúng hay sai? (xet_menh_de)

Tool 1: xet_menh_de
Tool 2: sai_so_tuong_doi
Tool 3: kiem_tra_tap_con
Tool 4: phu_dinh_menh_de
Tool 5: check_diem_bpt

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.20099671185016632
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.002983665559440851
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.0011084413854405284
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_2, tool_chapter_id: c_1, tool_name: phu_dinh_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: b045e31b-9f0f-4098-a81e-2e0325c7c311, _collection_name: tools, rerank_score: 0.0010281471768394113
content:
Tool viết mệnh đề phủ định của 1 mệnh đề cho trước.
Dùng khi đề bài yêu cầu: "viết mệnh đề phủ định của P", "phủ định của mệnh đề sau là gì",
"lập mệnh đề phủ định".
Ví dụ: phủ định của "Mọi số tự nhiên đều lớn hơn 0" là "Tồn tại số tự nhiên nhỏ hơn
hoặc bằng 0".
Ví dụ: phủ định của "n chia hết cho 5" là "n không chia hết cho 5".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.0003184051311109215
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.
=====================

Query 3 [Thông hiểu]: Xét mệnh đề: "Nếu một số chia hết cho 6 thì số đó chia hết cho 3" đúng hay sai? (xet_menh_de)

Tool 1: xet_menh_de
Tool 2: sai_so_tuong_doi
Tool 3: xet_dau_tam_thuc
Tool 4: phu_dinh_menh_de
Tool 5: xet_bien_thien

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.9667623043060303
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.03460362181067467
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.02407415211200714
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_2, tool_chapter_id: c_1, tool_name: phu_dinh_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: b045e31b-9f0f-4098-a81e-2e0325c7c311, _collection_name: tools, rerank_score: 0.023093663156032562
content:
Tool viết mệnh đề phủ định của 1 mệnh đề cho trước.
Dùng khi đề bài yêu cầu: "viết mệnh đề phủ định của P", "phủ định của mệnh đề sau là gì",
"lập mệnh đề phủ định".
Ví dụ: phủ định của "Mọi số tự nhiên đều lớn hơn 0" là "Tồn tại số tự nhiên nhỏ hơn
hoặc bằng 0".
Ví dụ: phủ định của "n chia hết cho 5" là "n không chia hết cho 5".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.014738857746124268
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.
=====================

Query 4 [Thông hiểu]: Khẳng định "Tổng hai số lẻ luôn là số chẵn" đúng hay sai? (xet_menh_de)

Tool 1: xet_menh_de
Tool 2: sai_so_tuong_doi
Tool 3: kiem_tra_tap_con
Tool 4: tong_hieu_vecto
Tool 5: tinh_phuong_sai_do_lech_chuan

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.43828099966049194
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.01142512820661068
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.005365267861634493
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.001299058087170124
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.0012081594904884696
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".
=====================

Query 5 [Vận dụng]: Một bạn học sinh nói: "25 là số chính phương và cũng là số nguyên tố". Khẳng định này đúng hay sai? (xet_menh_de)

Tool 1: xet_menh_de
Tool 2: sai_so_tuong_doi
Tool 3: kiem_tra_tap_con
Tool 4: hieu_tap_hop
Tool 5: phu_dinh_menh_de

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.28707101941108704
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.0011181739391759038
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.0006322562112472951
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.00028591809677891433
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_2, tool_chapter_id: c_1, tool_name: phu_dinh_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: b045e31b-9f0f-4098-a81e-2e0325c7c311, _collection_name: tools, rerank_score: 0.0002008398005273193
content:
Tool viết mệnh đề phủ định của 1 mệnh đề cho trước.
Dùng khi đề bài yêu cầu: "viết mệnh đề phủ định của P", "phủ định của mệnh đề sau là gì",
"lập mệnh đề phủ định".
Ví dụ: phủ định của "Mọi số tự nhiên đều lớn hơn 0" là "Tồn tại số tự nhiên nhỏ hơn
hoặc bằng 0".
Ví dụ: phủ định của "n chia hết cho 5" là "n không chia hết cho 5".
=====================

Query 6 [Dễ]: Viết mệnh đề phủ định của "5 là số lẻ" (phu_dinh_menh_de)

Tool 1: phu_dinh_menh_de
Tool 2: xet_menh_de
Tool 3: tich_vo_huong_vecto
Tool 4: check_diem_bpt
Tool 5: do_dai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_2, tool_chapter_id: c_1, tool_name: phu_dinh_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: b045e31b-9f0f-4098-a81e-2e0325c7c311, _collection_name: tools, rerank_score: 0.6597598195075989
content:
Tool viết mệnh đề phủ định của 1 mệnh đề cho trước.
Dùng khi đề bài yêu cầu: "viết mệnh đề phủ định của P", "phủ định của mệnh đề sau là gì",
"lập mệnh đề phủ định".
Ví dụ: phủ định của "Mọi số tự nhiên đều lớn hơn 0" là "Tồn tại số tự nhiên nhỏ hơn
hoặc bằng 0".
Ví dụ: phủ định của "n chia hết cho 5" là "n không chia hết cho 5".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.004580838605761528
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.0037156385369598866
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.0028746635653078556
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.0027789089363068342
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.
=====================

Query 7 [Dễ]: Viết mệnh đề phủ định của "x > 10" (phu_dinh_menh_de)

Tool 1: phu_dinh_menh_de
Tool 2: tinh_phuong_sai_do_lech_chuan
Tool 3: xet_dau_tam_thuc
Tool 4: tinh_trung_binh
Tool 5: tim_txd_ham_so

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_2, tool_chapter_id: c_1, tool_name: phu_dinh_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: b045e31b-9f0f-4098-a81e-2e0325c7c311, _collection_name: tools, rerank_score: 0.22056566178798676
content:
Tool viết mệnh đề phủ định của 1 mệnh đề cho trước.
Dùng khi đề bài yêu cầu: "viết mệnh đề phủ định của P", "phủ định của mệnh đề sau là gì",
"lập mệnh đề phủ định".
Ví dụ: phủ định của "Mọi số tự nhiên đều lớn hơn 0" là "Tồn tại số tự nhiên nhỏ hơn
hoặc bằng 0".
Ví dụ: phủ định của "n chia hết cho 5" là "n không chia hết cho 5".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.005518731661140919
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.003984169568866491
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.0034993940498679876
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.003059579059481621
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).
=====================

Query 8 [Thông hiểu]: Viết mệnh đề phủ định của "Mọi số nguyên đều lớn hơn 0" (phu_dinh_menh_de)

Tool 1: phu_dinh_menh_de
Tool 2: xet_menh_de
Tool 3: hieu_tap_hop
Tool 4: tim_txd_ham_so
Tool 5: xet_dau_tam_thuc

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_2, tool_chapter_id: c_1, tool_name: phu_dinh_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: b045e31b-9f0f-4098-a81e-2e0325c7c311, _collection_name: tools, rerank_score: 0.993339478969574
content:
Tool viết mệnh đề phủ định của 1 mệnh đề cho trước.
Dùng khi đề bài yêu cầu: "viết mệnh đề phủ định của P", "phủ định của mệnh đề sau là gì",
"lập mệnh đề phủ định".
Ví dụ: phủ định của "Mọi số tự nhiên đều lớn hơn 0" là "Tồn tại số tự nhiên nhỏ hơn
hoặc bằng 0".
Ví dụ: phủ định của "n chia hết cho 5" là "n không chia hết cho 5".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.00737085472792387
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.004592847544699907
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.004406469874083996
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.00378969288431108
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.
=====================

Query 9 [Thông hiểu]: Viết mệnh đề phủ định của "Tồn tại số tự nhiên n sao cho n chia hết cho 7" (phu_dinh_menh_de)

Tool 1: phu_dinh_menh_de
Tool 2: xet_menh_de
Tool 3: tich_so_voi_vecto
Tool 4: tinh_trung_vi_mode
Tool 5: tim_txd_ham_so

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_2, tool_chapter_id: c_1, tool_name: phu_dinh_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: b045e31b-9f0f-4098-a81e-2e0325c7c311, _collection_name: tools, rerank_score: 0.8531914949417114
content:
Tool viết mệnh đề phủ định của 1 mệnh đề cho trước.
Dùng khi đề bài yêu cầu: "viết mệnh đề phủ định của P", "phủ định của mệnh đề sau là gì",
"lập mệnh đề phủ định".
Ví dụ: phủ định của "Mọi số tự nhiên đều lớn hơn 0" là "Tồn tại số tự nhiên nhỏ hơn
hoặc bằng 0".
Ví dụ: phủ định của "n chia hết cho 5" là "n không chia hết cho 5".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.05040237307548523
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.004440379329025745
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.0038014771416783333
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.001722838613204658
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).
=====================

Query 10 [Vận dụng]: Cho mệnh đề P: "Nếu tam giác ABC đều thì tam giác ABC có ba góc bằng nhau". Viết mệnh đề phủ định của P (phu_dinh_menh_de)

Tool 1: phu_dinh_menh_de
Tool 2: dien_tich_tam_giac
Tool 3: dinh_ly_cosin
Tool 4: dinh_ly_sin
Tool 5: giai_tam_giac

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_2, tool_chapter_id: c_1, tool_name: phu_dinh_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: b045e31b-9f0f-4098-a81e-2e0325c7c311, _collection_name: tools, rerank_score: 0.8689663410186768
content:
Tool viết mệnh đề phủ định của 1 mệnh đề cho trước.
Dùng khi đề bài yêu cầu: "viết mệnh đề phủ định của P", "phủ định của mệnh đề sau là gì",
"lập mệnh đề phủ định".
Ví dụ: phủ định của "Mọi số tự nhiên đều lớn hơn 0" là "Tồn tại số tự nhiên nhỏ hơn
hoặc bằng 0".
Ví dụ: phủ định của "n chia hết cho 5" là "n không chia hết cho 5".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.10321615636348724
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.06935939937829971
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.061100129038095474
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.052120424807071686
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".
=====================

Query 11 [Dễ]: Cho A={1,2,3}, B={4,5}. Tìm A ∪ B (hop_tap_hop)

Tool 1: hop_tap_hop
Tool 2: giao_tap_hop
Tool 3: tong_hieu_vecto
Tool 4: tich_vo_huong_vecto
Tool 5: kiem_tra_tap_con

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.9739838242530823
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.9393855929374695
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.765113890171051
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.7346691489219666
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.5956838130950928
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).
=====================

Query 12 [Dễ]: Cho A={2,4,6}, B={1,3,5}. Tìm A ∪ B (hop_tap_hop)

Tool 1: hop_tap_hop
Tool 2: giao_tap_hop
Tool 3: hieu_tap_hop
Tool 4: tich_vo_huong_vecto
Tool 5: kiem_tra_tap_con

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.9114974737167358
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.8098422288894653
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.2258933186531067
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.17102566361427307
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.16911762952804565
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).
=====================

Query 13 [Thông hiểu]: Cho tập số tự nhiên chẵn nhỏ hơn 10 là A={0,2,4,6,8} và B={1,3,5,7,9}. Tìm A ∪ B (hop_tap_hop)

Tool 1: hop_tap_hop
Tool 2: giao_tap_hop
Tool 3: kiem_tra_tap_con
Tool 4: hieu_tap_hop
Tool 5: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.8736987709999084
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.7202554941177368
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.20968219637870789
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.17573672533035278
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.035727012902498245
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 14 [Thông hiểu]: Cho A là tập nghiệm của x²=4 (A={-2,2}) và B={0,2,4}. Tìm A ∪ B (hop_tap_hop)

Tool 1: hop_tap_hop
Tool 2: giao_tap_hop
Tool 3: kiem_tra_tap_con
Tool 4: tich_vo_huong_vecto
Tool 5: hieu_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.8260433077812195
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.6988509297370911
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.1974572092294693
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.1941027045249939
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.11361747235059738
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.
=====================

Query 15 [Vận dụng]: Lớp 10A có tập học sinh giỏi Toán A={1,2,3} và tập học sinh giỏi Văn B={2,4}. Tìm tập học sinh giỏi Toán hoặc giỏi Văn (A ∪ B) (hop_tap_hop)

Tool 1: hop_tap_hop
Tool 2: giao_tap_hop
Tool 3: hieu_tap_hop
Tool 4: kiem_tra_tap_con
Tool 5: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.44186344742774963
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.1857701689004898
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.163859561085701
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.11769959330558777
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.00596309220418334
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 16 [Dễ]: Cho A={1,2,3,4}, B={3,4,5}. Tìm A ∩ B (giao_tap_hop)

Tool 1: giao_tap_hop
Tool 2: hop_tap_hop
Tool 3: tich_vo_huong_vecto
Tool 4: tong_hieu_vecto
Tool 5: hieu_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.9694896340370178
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.9662315845489502
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.8361325263977051
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.6914945840835571
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.634630560874939
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.
=====================

Query 17 [Dễ]: Cho A={2,4,6,8}, B={4,8,12}. Tìm A ∩ B (giao_tap_hop)

Tool 1: giao_tap_hop
Tool 2: hop_tap_hop
Tool 3: hieu_tap_hop
Tool 4: kiem_tra_tap_con
Tool 5: tong_hieu_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.7655632495880127
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.6705521941184998
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.14576581120491028
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.14484800398349762
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.0908399298787117
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).
=====================

Query 18 [Thông hiểu]: Cho A là tập ước của 12 (A={1,2,3,4,6,12}) và B là tập ước của 18 (B={1,2,3,6,9,18}). Tìm A ∩ B (giao_tap_hop)

Tool 1: giao_tap_hop
Tool 2: hop_tap_hop
Tool 3: hieu_tap_hop
Tool 4: kiem_tra_tap_con
Tool 5: tong_hieu_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.8213357925415039
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.7538005709648132
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.35006558895111084
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.1910363882780075
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.12904663383960724
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).
=====================

Query 19 [Thông hiểu]: Cho A={x | x là số nguyên tố nhỏ hơn 10} = {2,3,5,7} và B={2,4,6,8}. Tìm A ∩ B (giao_tap_hop)

Tool 1: giao_tap_hop
Tool 2: hop_tap_hop
Tool 3: hieu_tap_hop
Tool 4: tong_hieu_vecto
Tool 5: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.7979051470756531
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.7341275215148926
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.27784985303878784
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.10462352633476257
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.09381797164678574
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 20 [Vận dụng]: Tập điểm giỏi môn Toán A={5,6,7,8,9,10}, tập điểm giỏi môn Văn B={7,8,9,10,11}. Tìm mức điểm đạt giỏi cả hai môn (A ∩ B) (giao_tap_hop)

Tool 1: giao_tap_hop
Tool 2: hop_tap_hop
Tool 3: kiem_tra_tap_con
Tool 4: hieu_tap_hop
Tool 5: tinh_trung_binh

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.13179440796375275
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.04461914673447609
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.01786300353705883
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.011332950554788113
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.003874437417834997
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.
=====================

Query 21 [Dễ]: Cho A={1,2,3,4,5}, B={3,4,5}. Tìm A \ B (hieu_tap_hop)

Tool 1: hieu_tap_hop
Tool 2: giao_tap_hop
Tool 3: hop_tap_hop
Tool 4: tich_vo_huong_vecto
Tool 5: tong_hieu_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.909842848777771
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.9025520086288452
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.8303719162940979
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.7749658226966858
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.7402300834655762
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).
=====================

Query 22 [Dễ]: Cho A={2,4,6,8}, B={2,4}. Tìm A \ B (hieu_tap_hop)

Tool 1: hieu_tap_hop
Tool 2: giao_tap_hop
Tool 3: hop_tap_hop
Tool 4: tong_hieu_vecto
Tool 5: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.7107055187225342
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.4898584187030792
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.3786097764968872
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.17163071036338806
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.10893699526786804
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 23 [Thông hiểu]: Cho A là tập ước của 20 (A={1,2,4,5,10,20}) và B={1,2,4}. Tìm A \ B (hieu_tap_hop)

Tool 1: hieu_tap_hop
Tool 2: hop_tap_hop
Tool 3: giao_tap_hop
Tool 4: tong_hieu_vecto
Tool 5: kiem_tra_tap_con

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.5376407504081726
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.4312649965286255
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.340433806180954
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.2560005486011505
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.15949223935604095
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).
=====================

Query 24 [Thông hiểu]: Cho A={0,1,2,...,9} và B={0,2,4,6,8}. Tìm A \ B (hieu_tap_hop)

Tool 1: hieu_tap_hop
Tool 2: hop_tap_hop
Tool 3: tong_hieu_vecto
Tool 4: giao_tap_hop
Tool 5: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.819940984249115
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.6126287579536438
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.5495262145996094
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.4630066454410553
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.300348162651062
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 25 [Vận dụng]: Tập khách hàng mua áo A={1,2,3,4,5,6}, tập khách hàng mua quần B={4,5,6}. Tìm tập khách chỉ mua áo mà không mua quần (A \ B) (hieu_tap_hop)

Tool 1: hieu_tap_hop
Tool 2: kiem_tra_tap_con
Tool 3: hop_tap_hop
Tool 4: giao_tap_hop
Tool 5: tim_txd_ham_so

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.12331606447696686
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.03471606969833374
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.030873548239469528
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.03042113222181797
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.0026617669500410557
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).
=====================

Query 26 [Dễ]: A={1,2} có là tập con của B={1,2,3,4} không? (kiem_tra_tap_con)

Tool 1: kiem_tra_tap_con
Tool 2: giao_tap_hop
Tool 3: hop_tap_hop
Tool 4: hieu_tap_hop
Tool 5: tong_hieu_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.9887862205505371
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.8671412467956543
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.8552737832069397
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.6767838597297668
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.5753372311592102
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).
=====================

Query 27 [Dễ]: A={3,5} có là tập con của B={1,2,3,4} không? (kiem_tra_tap_con)

Tool 1: kiem_tra_tap_con
Tool 2: hop_tap_hop
Tool 3: giao_tap_hop
Tool 4: tich_vo_huong_vecto
Tool 5: hieu_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.7861129641532898
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.43475908041000366
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.30587807297706604
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.12884502112865448
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.07770902663469315
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.
=====================

Query 28 [Thông hiểu]: Tập nghiệm của x²-4=0 là A={-2,2}. Tập B={-2,-1,0,1,2}. A có là tập con của B không? (kiem_tra_tap_con)

Tool 1: kiem_tra_tap_con
Tool 2: hieu_tap_hop
Tool 3: hop_tap_hop
Tool 4: giao_tap_hop
Tool 5: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.9674369692802429
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.07593262195587158
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.04236162081360817
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.03755980730056763
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.03084842674434185
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 29 [Thông hiểu]: A là tập ước của 6 (A={1,2,3,6}), B là tập ước của 12 (B={1,2,3,4,6,12}). A có là tập con của B không? (kiem_tra_tap_con)

Tool 1: kiem_tra_tap_con
Tool 2: hieu_tap_hop
Tool 3: hop_tap_hop
Tool 4: giao_tap_hop
Tool 5: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.9853106737136841
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.1251407414674759
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.08273531496524811
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.05533384159207344
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.011335867457091808
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 30 [Vận dụng]: Tập học sinh giỏi Toán A={1,2,3}, tập toàn bộ học sinh lớp B={1,2,...,30}. Kiểm tra A có là tập con của B không (kiem_tra_tap_con)

Tool 1: kiem_tra_tap_con
Tool 2: hop_tap_hop
Tool 3: hieu_tap_hop
Tool 4: giao_tap_hop
Tool 5: kiem_tra_he_bpt

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.9891303777694702
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.16314154863357544
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.1108657494187355
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.10041549801826477
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_9, tool_chapter_id: c_2, tool_name: kiem_tra_he_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 90dafa58-3c37-4dbd-aee8-7a4e3874f1fe, _collection_name: tools, rerank_score: 0.008595914579927921
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn đồng thời TẤT CẢ các bất phương trình trong 1
hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền nghiệm của hệ hay không).
Dùng khi đề bài cho nhiều bất phương trình cùng lúc (hệ) và hỏi 1 điểm có là nghiệm của
hệ đó không.
Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra từng bpt.
=====================

Query 31 [Dễ]: Điểm (1,1) có thỏa mãn x+y≤5 không? (check_diem_bpt)

Tool 1: check_diem_bpt
Tool 2: kiem_tra_he_bpt
Tool 3: tich_vo_huong_vecto
Tool 4: tim_dinh_parabol
Tool 5: tim_gtln_gtnn_mien

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.9411343336105347
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_9, tool_chapter_id: c_2, tool_name: kiem_tra_he_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 90dafa58-3c37-4dbd-aee8-7a4e3874f1fe, _collection_name: tools, rerank_score: 0.9308637380599976
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn đồng thời TẤT CẢ các bất phương trình trong 1
hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền nghiệm của hệ hay không).
Dùng khi đề bài cho nhiều bất phương trình cùng lúc (hệ) và hỏi 1 điểm có là nghiệm của
hệ đó không.
Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra từng bpt.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.015549360774457455
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.0015366640873253345
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.0006755936774425209
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".
=====================

Query 32 [Dễ]: Điểm (2,3) có thỏa mãn 2x+y≥4 không? (check_diem_bpt)

Tool 1: check_diem_bpt
Tool 2: kiem_tra_he_bpt
Tool 3: tich_vo_huong_vecto
Tool 4: tim_gtln_gtnn_mien
Tool 5: tim_dinh_parabol

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.830547034740448
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_9, tool_chapter_id: c_2, tool_name: kiem_tra_he_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 90dafa58-3c37-4dbd-aee8-7a4e3874f1fe, _collection_name: tools, rerank_score: 0.5602337121963501
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn đồng thời TẤT CẢ các bất phương trình trong 1
hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền nghiệm của hệ hay không).
Dùng khi đề bài cho nhiều bất phương trình cùng lúc (hệ) và hỏi 1 điểm có là nghiệm của
hệ đó không.
Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra từng bpt.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.05644110217690468
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.004911391530185938
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.004377419129014015
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.
=====================

Query 33 [Thông hiểu]: Điểm M(0,0) có thỏa mãn bất phương trình 3x-2y<6 không? (check_diem_bpt)

Tool 1: check_diem_bpt
Tool 2: kiem_tra_he_bpt
Tool 3: tim_gtln_gtnn_mien
Tool 4: xet_dau_tam_thuc
Tool 5: tinh_trung_binh

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.8494817018508911
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_9, tool_chapter_id: c_2, tool_name: kiem_tra_he_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 90dafa58-3c37-4dbd-aee8-7a4e3874f1fe, _collection_name: tools, rerank_score: 0.35552728176116943
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn đồng thời TẤT CẢ các bất phương trình trong 1
hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền nghiệm của hệ hay không).
Dùng khi đề bài cho nhiều bất phương trình cùng lúc (hệ) và hỏi 1 điểm có là nghiệm của
hệ đó không.
Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra từng bpt.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.0263285581022501
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.0007685679011046886
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.0004932198207825422
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.
=====================

Query 34 [Thông hiểu]: Điểm A(-1,2) có thỏa mãn x-y≥-3 không? (check_diem_bpt)

Tool 1: kiem_tra_he_bpt
Tool 2: check_diem_bpt
Tool 3: tich_vo_huong_vecto
Tool 4: tim_dinh_parabol
Tool 5: kiem_tra_tap_con

Result Tool: ❌ ✅ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_9, tool_chapter_id: c_2, tool_name: kiem_tra_he_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 90dafa58-3c37-4dbd-aee8-7a4e3874f1fe, _collection_name: tools, rerank_score: 0.9314978718757629
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn đồng thời TẤT CẢ các bất phương trình trong 1
hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền nghiệm của hệ hay không).
Dùng khi đề bài cho nhiều bất phương trình cùng lúc (hệ) và hỏi 1 điểm có là nghiệm của
hệ đó không.
Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra từng bpt.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.39760175347328186
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.018464084714651108
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.009863906539976597
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.008320671506226063
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).
=====================

Query 35 [Vận dụng]: Một xưởng cần thỏa ràng buộc nguyên liệu 2x+3y≤120. Kiểm tra phương án sản xuất (x=30, y=20) có khả thi không (check_diem_bpt)

Tool 1: tim_gtln_gtnn_mien
Tool 2: kiem_tra_he_bpt
Tool 3: check_diem_bpt
Tool 4: tich_vo_huong_vecto
Tool 5: kiem_tra_tap_con

Result Tool: ❌ ❌ ✅ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.015612377785146236
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_9, tool_chapter_id: c_2, tool_name: kiem_tra_he_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 90dafa58-3c37-4dbd-aee8-7a4e3874f1fe, _collection_name: tools, rerank_score: 0.004814114421606064
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn đồng thời TẤT CẢ các bất phương trình trong 1
hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền nghiệm của hệ hay không).
Dùng khi đề bài cho nhiều bất phương trình cùng lúc (hệ) và hỏi 1 điểm có là nghiệm của
hệ đó không.
Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra từng bpt.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.0025417106226086617
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.00021676240430679172
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_6, tool_chapter_id: c_1, tool_name: kiem_tra_tap_con_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: f20aebc4-efa4-448d-8d9f-4c2a5f65f12e, _collection_name: tools, rerank_score: 0.00013857532758265734
content:
Tool kiểm tra tập hợp A có phải là tập con của tập hợp B hay không (A ⊂ B).
Dùng khi đề bài hỏi "A có là tập con của B không?", "chứng minh A ⊂ B", "kiểm tra
quan hệ tập con".
Ví dụ: "A={1,2} có là tập con của B={1,2,3} không?" → Đúng (True).
=====================

Query 36 [Dễ]: Tìm GTLN của F=x+y trên miền tam giác có đỉnh (0,0),(4,0),(0,4) (tim_gtln_gtnn_mien)

Tool 1: tim_gtln_gtnn_mien
Tool 2: tim_dinh_parabol
Tool 3: dien_tich_tam_giac
Tool 4: xet_dau_tam_thuc
Tool 5: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.976911723613739
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.025956936180591583
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.004003098234534264
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.0032647778280079365
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.0027713174931705
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 37 [Dễ]: Tìm GTNN của F=2x+y trên miền tam giác có đỉnh (0,0),(3,0),(0,3) (tim_gtln_gtnn_mien)

Tool 1: tim_gtln_gtnn_mien
Tool 2: tim_dinh_parabol
Tool 3: xet_dau_tam_thuc
Tool 4: xet_bien_thien
Tool 5: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.9815773367881775
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.033658143132925034
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.0053770216181874275
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.005119885317981243
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.004187257494777441
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 38 [Thông hiểu]: Tìm GTLN của F=3x+4y trên miền tứ giác có đỉnh (0,0),(5,0),(5,3),(0,5) (tim_gtln_gtnn_mien)

Tool 1: tim_gtln_gtnn_mien
Tool 2: tim_dinh_parabol
Tool 3: tich_vo_huong_vecto
Tool 4: xet_dau_tam_thuc
Tool 5: xet_bien_thien

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.8420343995094299
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.01973685249686241
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.0020344897639006376
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.0018094392726197839
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.001650540274567902
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.
=====================

Query 39 [Thông hiểu]: Tìm GTNN của F=x+2y trên miền có đỉnh (1,1),(4,1),(4,4),(1,4) (tim_gtln_gtnn_mien)

Tool 1: tim_gtln_gtnn_mien
Tool 2: tim_dinh_parabol
Tool 3: tich_vo_huong_vecto
Tool 4: check_diem_bpt
Tool 5: do_dai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.9067621231079102
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.09262796491384506
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.00903247855603695
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.008254088461399078
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.004434952512383461
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.
=====================

Query 40 [Vận dụng]: Công ty sản xuất 2 sản phẩm với lợi nhuận F=5x+4y, miền ràng buộc có đỉnh (0,0),(20,0),(15,10),(0,15). Tìm phương án cho lợi nhuận GTLN (tim_gtln_gtnn_mien)

Tool 1: tim_gtln_gtnn_mien
Tool 2: tim_dinh_parabol
Tool 3: hop_tap_hop
Tool 4: tich_vo_huong_vecto
Tool 5: check_diem_bpt

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.6900286674499512
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 7.447479583788663e-05
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 3.2640888093737885e-05
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 3.1043600756675005e-05
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 2.8695974833681248e-05
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.
=====================

Query 41 [Dễ]: Điểm (1,1) có thỏa hệ {x+y≤4; x≥0; y≥0} không? (kiem_tra_he_bpt)

Tool 1: kiem_tra_he_bpt
Tool 2: check_diem_bpt
Tool 3: tich_vo_huong_vecto
Tool 4: tim_dinh_parabol
Tool 5: goc_giua_hai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_9, tool_chapter_id: c_2, tool_name: kiem_tra_he_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 90dafa58-3c37-4dbd-aee8-7a4e3874f1fe, _collection_name: tools, rerank_score: 0.982588529586792
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn đồng thời TẤT CẢ các bất phương trình trong 1
hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền nghiệm của hệ hay không).
Dùng khi đề bài cho nhiều bất phương trình cùng lúc (hệ) và hỏi 1 điểm có là nghiệm của
hệ đó không.
Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra từng bpt.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.8342311382293701
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.025034260004758835
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.008771340362727642
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.0034015211276710033
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 42 [Dễ]: Điểm (2,2) có thỏa hệ {x+y≤3; x≥0} không? (kiem_tra_he_bpt)

Tool 1: kiem_tra_he_bpt
Tool 2: check_diem_bpt
Tool 3: tich_vo_huong_vecto
Tool 4: tim_dinh_parabol
Tool 5: xet_dau_tam_thuc

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_9, tool_chapter_id: c_2, tool_name: kiem_tra_he_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 90dafa58-3c37-4dbd-aee8-7a4e3874f1fe, _collection_name: tools, rerank_score: 0.9478034973144531
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn đồng thời TẤT CẢ các bất phương trình trong 1
hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền nghiệm của hệ hay không).
Dùng khi đề bài cho nhiều bất phương trình cùng lúc (hệ) và hỏi 1 điểm có là nghiệm của
hệ đó không.
Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra từng bpt.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.8186730742454529
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.022218937054276466
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.013431963510811329
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.01127597875893116
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.
=====================

Query 43 [Thông hiểu]: Điểm (0,0) có thỏa hệ {x-y≥-2; x+y≤5; x≥0; y≥0} không? (kiem_tra_he_bpt)

Tool 1: kiem_tra_he_bpt
Tool 2: check_diem_bpt
Tool 3: tim_gtln_gtnn_mien
Tool 4: tich_vo_huong_vecto
Tool 5: tim_dinh_parabol

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_9, tool_chapter_id: c_2, tool_name: kiem_tra_he_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 90dafa58-3c37-4dbd-aee8-7a4e3874f1fe, _collection_name: tools, rerank_score: 0.9356958866119385
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn đồng thời TẤT CẢ các bất phương trình trong 1
hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền nghiệm của hệ hay không).
Dùng khi đề bài cho nhiều bất phương trình cùng lúc (hệ) và hỏi 1 điểm có là nghiệm của
hệ đó không.
Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra từng bpt.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.9038072824478149
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.02436221018433571
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.015303997322916985
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.0017645999323576689
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.
=====================

Query 44 [Thông hiểu]: Điểm (3,1) có thỏa hệ {2x+y≤8; x-y≥-1; y≥0} không? (kiem_tra_he_bpt)

Tool 1: kiem_tra_he_bpt
Tool 2: check_diem_bpt
Tool 3: tim_dinh_parabol
Tool 4: tich_vo_huong_vecto
Tool 5: xet_bien_thien

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_9, tool_chapter_id: c_2, tool_name: kiem_tra_he_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 90dafa58-3c37-4dbd-aee8-7a4e3874f1fe, _collection_name: tools, rerank_score: 0.7688652276992798
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn đồng thời TẤT CẢ các bất phương trình trong 1
hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền nghiệm của hệ hay không).
Dùng khi đề bài cho nhiều bất phương trình cùng lúc (hệ) và hỏi 1 điểm có là nghiệm của
hệ đó không.
Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra từng bpt.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.30849018692970276
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.020046589896082878
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.012216979637742043
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.003684840863570571
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.
=====================

Query 45 [Vận dụng]: Phương án sản xuất (x=10,y=5) có thỏa hệ ràng buộc {x+2y≤25; 3x+y≤40; x≥0; y≥0} không? (kiem_tra_he_bpt)

Tool 1: kiem_tra_he_bpt
Tool 2: check_diem_bpt
Tool 3: tim_gtln_gtnn_mien
Tool 4: tich_vo_huong_vecto
Tool 5: hop_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_9, tool_chapter_id: c_2, tool_name: kiem_tra_he_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 90dafa58-3c37-4dbd-aee8-7a4e3874f1fe, _collection_name: tools, rerank_score: 0.05034082382917404
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn đồng thời TẤT CẢ các bất phương trình trong 1
hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền nghiệm của hệ hay không).
Dùng khi đề bài cho nhiều bất phương trình cùng lúc (hệ) và hỏi 1 điểm có là nghiệm của
hệ đó không.
Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra từng bpt.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.011136706918478012
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.004237225279211998
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.0012242932571098208
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.0004133058537263423
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.
=====================

Query 46 [Dễ]: Tìm tập xác định của y=1/(x-3) (tim_txd_ham_so)

Tool 1: tim_txd_ham_so
Tool 2: tich_vo_huong_vecto
Tool 3: tim_dinh_parabol
Tool 4: xet_dau_tam_thuc
Tool 5: kiem_tra_he_bpt

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.5616235136985779
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.0444444939494133
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.028061656281352043
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.007380084600299597
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_9, tool_chapter_id: c_2, tool_name: kiem_tra_he_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 90dafa58-3c37-4dbd-aee8-7a4e3874f1fe, _collection_name: tools, rerank_score: 0.006356004625558853
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn đồng thời TẤT CẢ các bất phương trình trong 1
hệ bất phương trình bậc nhất hai ẩn hay không (có thuộc miền nghiệm của hệ hay không).
Dùng khi đề bài cho nhiều bất phương trình cùng lúc (hệ) và hỏi 1 điểm có là nghiệm của
hệ đó không.
Ví dụ: "Điểm (1,1) có thỏa mãn hệ {x+y≤3; x-y≥-2; x≥0} không?" → kiểm tra từng bpt.
=====================

Query 47 [Dễ]: Tìm tập xác định của y=√(x+2) (tim_txd_ham_so)

Tool 1: tim_txd_ham_so
Tool 2: tich_vo_huong_vecto
Tool 3: tim_dinh_parabol
Tool 4: check_diem_bpt
Tool 5: xet_dau_tam_thuc

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.8997538089752197
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.08617213368415833
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.03111078217625618
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.009682334959506989
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.007246040273457766
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.
=====================

Query 48 [Thông hiểu]: Tìm tập xác định của y=1/(x²-4) (tim_txd_ham_so)

Tool 1: tim_txd_ham_so
Tool 2: tich_vo_huong_vecto
Tool 3: do_dai_vecto
Tool 4: tim_dinh_parabol
Tool 5: check_diem_bpt

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.6466882228851318
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.16020411252975464
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.04148668050765991
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.03518093749880791
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.007308891974389553
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.
=====================

Query 49 [Thông hiểu]: Tìm tập xác định của y=√(5-x) (tim_txd_ham_so)

Tool 1: tim_txd_ham_so
Tool 2: do_dai_vecto
Tool 3: xet_dau_tam_thuc
Tool 4: tich_vo_huong_vecto
Tool 5: tim_dinh_parabol

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.5443482398986816
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.03781890124082565
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.013614699244499207
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.012946941889822483
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.007717832922935486
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.
=====================

Query 50 [Vận dụng]: Chi phí sản xuất mô tả bởi y=1000/(x-10) với x là số sản phẩm. Tìm tập xác định để biết giá trị x hợp lệ (tim_txd_ham_so)

Tool 1: tim_txd_ham_so
Tool 2: tinh_trung_binh
Tool 3: hop_tap_hop
Tool 4: tim_gtln_gtnn_mien
Tool 5: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.09402938932180405
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.0031345586758106947
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.0016420682659372687
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.0015530702657997608
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.001171987154521048
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 51 [Dễ]: Xét tính đồng biến, nghịch biến của y=3x+1 trên R (xet_bien_thien)

Tool 1: xet_bien_thien
Tool 2: tim_txd_ham_so
Tool 3: dinh_ly_sin
Tool 4: xet_menh_de
Tool 5: xet_dau_tam_thuc

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.823616623878479
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.02953852340579033
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.003950531594455242
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.0035819632466882467
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.0025528883561491966
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.
=====================

Query 52 [Dễ]: Xét tính đồng biến, nghịch biến của y=-2x+5 trên R (xet_bien_thien)

Tool 1: xet_bien_thien
Tool 2: check_diem_bpt
Tool 3: xet_dau_tam_thuc
Tool 4: do_dai_vecto
Tool 5: dinh_ly_sin

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.8038012385368347
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.006879348773509264
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.00684735644608736
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.00496581569314003
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.004266509786248207
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".
=====================

Query 53 [Thông hiểu]: Xét sự biến thiên của hàm số y=x-7 trên khoảng (-5,5) (xet_bien_thien)

Tool 1: xet_bien_thien
Tool 2: xet_dau_tam_thuc
Tool 3: tim_txd_ham_so
Tool 4: xet_menh_de
Tool 5: sai_so_tuong_doi

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.20391656458377838
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.007822270505130291
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.0023958964738994837
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.0022066328674554825
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.0005686200456693769
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.
=====================

Query 54 [Thông hiểu]: Xét tính đồng biến, nghịch biến của y=(1/2)x+3 trên R (xet_bien_thien)

Tool 1: xet_bien_thien
Tool 2: tim_txd_ham_so
Tool 3: tim_gtln_gtnn_mien
Tool 4: dinh_ly_sin
Tool 5: xet_dau_tam_thuc

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.9374043941497803
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.0251106396317482
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.010636933147907257
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.005553681403398514
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.002918151905760169
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.
=====================

Query 55 [Vận dụng]: Doanh thu cửa hàng theo tháng là y=200x+1000 (x là tháng). Xét hàm số đồng biến hay nghịch biến trên (1,12) để biết xu hướng doanh thu (xet_bien_thien)

Tool 1: xet_bien_thien
Tool 2: tim_txd_ham_so
Tool 3: tinh_trung_vi_mode
Tool 4: tim_dinh_parabol
Tool 5: tich_so_voi_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.48307204246520996
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.00093702448066324
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.00043510267278179526
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.0003667622513603419
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.00017078743258025497
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).
=====================

Query 56 [Dễ]: Tìm đỉnh của parabol y=x²-4x+3 (tim_dinh_parabol)

Tool 1: tim_dinh_parabol
Tool 2: tim_gtln_gtnn_mien
Tool 3: do_dai_vecto
Tool 4: tich_vo_huong_vecto
Tool 5: hop_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.9917020201683044
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.16393539309501648
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.019599327817559242
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.00818343460559845
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.0011222765315324068
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.
=====================

Query 57 [Dễ]: Tìm đỉnh của parabol y=x²+2x-3 (tim_dinh_parabol)

Tool 1: tim_dinh_parabol
Tool 2: tim_gtln_gtnn_mien
Tool 3: do_dai_vecto
Tool 4: tich_vo_huong_vecto
Tool 5: xet_bien_thien

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.9628150463104248
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.12453929334878922
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.029297757893800735
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.016024019569158554
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.0027406811714172363
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.
=====================

Query 58 [Thông hiểu]: Tìm đỉnh và trục đối xứng của y=2x²-8x+5 (tim_dinh_parabol)

Tool 1: tim_dinh_parabol
Tool 2: tim_gtln_gtnn_mien
Tool 3: tim_txd_ham_so
Tool 4: tich_vo_huong_vecto
Tool 5: check_diem_bpt

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.8069367408752441
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.024357473477721214
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.014874188229441643
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.013568690046668053
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.005480241030454636
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.
=====================

Query 59 [Thông hiểu]: Tìm đỉnh của parabol y=-x²+6x-8 (tim_dinh_parabol)

Tool 1: tim_dinh_parabol
Tool 2: do_dai_vecto
Tool 3: tim_gtln_gtnn_mien
Tool 4: tich_vo_huong_vecto
Tool 5: hop_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.7824466824531555
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.02243630401790142
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.009681817144155502
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.004645583685487509
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.0011646943166851997
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.
=====================

Query 60 [Vận dụng]: Quỹ đạo vật ném lên mô tả bởi y=-5x²+20x (x là thời gian, y là độ cao). Tìm đỉnh parabol để biết thời điểm và độ cao lớn nhất (tim_dinh_parabol)

Tool 1: tim_dinh_parabol
Tool 2: tim_gtln_gtnn_mien
Tool 3: do_dai_vecto
Tool 4: giai_tam_giac
Tool 5: check_diem_bpt

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.3168942928314209
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.005187330301851034
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.0014768610708415508
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.0006863698945380747
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_7, tool_chapter_id: c_2, tool_name: check_diem_bpt_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Bất phương trình bậc nhất hai ẩn, _id: 83caa0c2-d72f-41a5-aa70-08395ce2b58c, _collection_name: tools, rerank_score: 0.0003140443004667759
content:
Tool kiểm tra 1 điểm (x0, y0) có thỏa mãn bất phương trình bậc nhất hai ẩn ax + by (dấu) c
hay không.
Dùng khi đề bài hỏi: "điểm M(x0,y0) có là nghiệm của bất phương trình sau không?",
"kiểm tra điểm sau có thuộc miền nghiệm không".
Ví dụ: "Điểm (1,2) có thỏa mãn 2x + y ≤ 5 không?" → 2*1+2=4 ≤ 5 → Đúng.
=====================

Query 61 [Dễ]: Xét dấu tam thức f(x)=x²-5x+6 (xet_dau_tam_thuc)

Tool 1: xet_dau_tam_thuc
Tool 2: xet_bien_thien
Tool 3: tinh_trung_binh
Tool 4: tim_gtln_gtnn_mien
Tool 5: tim_txd_ham_so

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.993760883808136
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.009596037678420544
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.008119960315525532
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.00673132436349988
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.0045743766240775585
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).
=====================

Query 62 [Dễ]: Xét dấu tam thức f(x)=x²-9 (xet_dau_tam_thuc)

Tool 1: xet_dau_tam_thuc
Tool 2: xet_bien_thien
Tool 3: tim_gtln_gtnn_mien
Tool 4: tim_txd_ham_so
Tool 5: giai_tam_giac

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.8005260825157166
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.006431944202631712
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.004913302604109049
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.004262600094079971
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.0021269062999635935
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".
=====================

Query 63 [Thông hiểu]: Xét dấu tam thức f(x)=2x²-3x+1 (xet_dau_tam_thuc)

Tool 1: xet_dau_tam_thuc
Tool 2: tim_gtln_gtnn_mien
Tool 3: xet_bien_thien
Tool 4: xet_menh_de
Tool 5: tim_txd_ham_so

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.7593250870704651
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.013750498183071613
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.01292762067168951
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.008501756004989147
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.005258976481854916
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).
=====================

Query 64 [Thông hiểu]: Xét dấu tam thức f(x)=-x²+4x-3 (xet_dau_tam_thuc)

Tool 1: xet_dau_tam_thuc
Tool 2: tim_gtln_gtnn_mien
Tool 3: tim_dinh_parabol
Tool 4: xet_bien_thien
Tool 5: tim_txd_ham_so

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.828877329826355
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.021509384736418724
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_12, tool_chapter_id: c_3, tool_name: tim_dinh_parabol_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: b3a5f457-e8fa-4bf2-8693-1a7c05c11fbe, _collection_name: tools, rerank_score: 0.019056126475334167
content:
Tool tìm tọa độ đỉnh và trục đối xứng của parabol y = ax² + bx + c.
Dùng khi đề bài hỏi: "tìm đỉnh của parabol", "trục đối xứng của đồ thị hàm số bậc hai
là gì", "xác định điểm cực đại/cực tiểu của hàm bậc hai".
Ví dụ: "Tìm đỉnh của y = x² - 4x + 3" → Đỉnh I(2, -1), trục đối xứng x=2.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.01575259119272232
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.005963476374745369
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).
=====================

Query 65 [Vận dụng]: Lợi nhuận công ty theo sản lượng x là f(x)=-x²+10x-16. Xét dấu f(x) để biết khoảng sản lượng nào công ty có lãi (xet_dau_tam_thuc)

Tool 1: xet_dau_tam_thuc
Tool 2: xet_bien_thien
Tool 3: do_dai_vecto
Tool 4: sai_so_tuong_doi
Tool 5: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.21836455166339874
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_11, tool_chapter_id: c_3, tool_name: xet_bien_thien_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: d3adc29a-242e-4f07-ab43-4aa69aa1f6e6, _collection_name: tools, rerank_score: 0.0011213708203285933
content:
Tool xét tính đồng biến, nghịch biến của hàm số trên 1 khoảng cho trước.
Dùng khi đề bài hỏi: "hàm số đồng biến hay nghịch biến trên khoảng nào", "xét sự biến
thiên của hàm số".
Ví dụ: "Xét tính đồng biến, nghịch biến của y=2x+3 trên R" → đồng biến vì hệ số góc >0.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.000505054893437773
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.00033127577626146376
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.00030948634957894683
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 66 [Dễ]: Tính sin của góc 30° (gia_tri_luong_giac)

Tool 1: dinh_ly_sin
Tool 2: gia_tri_luong_giac
Tool 3: dinh_ly_cosin
Tool 4: goc_giua_hai_vecto
Tool 5: dien_tich_tam_giac

Result Tool: ❌ ✅ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.25247764587402344
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_14, tool_chapter_id: c_4, tool_name: gia_tri_luong_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giá trị lượng giác của một góc từ 0° đến 180°, _id: f6237aa0-821e-4007-a0e0-83fd698a9f78, _collection_name: tools, rerank_score: 0.15983106195926666
content:
Tool tính giá trị lượng giác (sin, cos, tan, cot) của 1 góc từ 0° đến 180°.
Dùng khi đề bài hỏi: "tính sin/cos/tan/cot của góc α", "giá trị lượng giác của góc
120° là bao nhiêu".
Ví dụ: "Tính sin150°" → sin150° = 1/2.
Ví dụ: "Tính cos120°" → cos120° = -1/2.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.07439639419317245
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.008688543923199177
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.006093927659094334
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).
=====================

Query 67 [Dễ]: Tính cos của góc 60° (gia_tri_luong_giac)

Tool 1: dinh_ly_cosin
Tool 2: dien_tich_tam_giac
Tool 3: gia_tri_luong_giac
Tool 4: giai_tam_giac
Tool 5: goc_giua_hai_vecto

Result Tool: ❌ ❌ ✅ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.8637426495552063
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.34272098541259766
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_14, tool_chapter_id: c_4, tool_name: gia_tri_luong_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giá trị lượng giác của một góc từ 0° đến 180°, _id: f6237aa0-821e-4007-a0e0-83fd698a9f78, _collection_name: tools, rerank_score: 0.20233866572380066
content:
Tool tính giá trị lượng giác (sin, cos, tan, cot) của 1 góc từ 0° đến 180°.
Dùng khi đề bài hỏi: "tính sin/cos/tan/cot của góc α", "giá trị lượng giác của góc
120° là bao nhiêu".
Ví dụ: "Tính sin150°" → sin150° = 1/2.
Ví dụ: "Tính cos120°" → cos120° = -1/2.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.18237020075321198
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.14600223302841187
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 68 [Thông hiểu]: Tính tan của góc 45° (gia_tri_luong_giac)

Tool 1: dinh_ly_sin
Tool 2: gia_tri_luong_giac
Tool 3: dinh_ly_cosin
Tool 4: goc_giua_hai_vecto
Tool 5: dien_tich_tam_giac

Result Tool: ❌ ✅ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.4718919098377228
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_14, tool_chapter_id: c_4, tool_name: gia_tri_luong_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giá trị lượng giác của một góc từ 0° đến 180°, _id: f6237aa0-821e-4007-a0e0-83fd698a9f78, _collection_name: tools, rerank_score: 0.1431586593389511
content:
Tool tính giá trị lượng giác (sin, cos, tan, cot) của 1 góc từ 0° đến 180°.
Dùng khi đề bài hỏi: "tính sin/cos/tan/cot của góc α", "giá trị lượng giác của góc
120° là bao nhiêu".
Ví dụ: "Tính sin150°" → sin150° = 1/2.
Ví dụ: "Tính cos120°" → cos120° = -1/2.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.02558329328894615
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.008098497986793518
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.006114279385656118
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).
=====================

Query 69 [Thông hiểu]: Tính giá trị cos của góc 150° (gia_tri_luong_giac)

Tool 1: gia_tri_luong_giac
Tool 2: dinh_ly_cosin
Tool 3: goc_giua_hai_vecto
Tool 4: dinh_ly_sin
Tool 5: dien_tich_tam_giac

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_14, tool_chapter_id: c_4, tool_name: gia_tri_luong_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giá trị lượng giác của một góc từ 0° đến 180°, _id: f6237aa0-821e-4007-a0e0-83fd698a9f78, _collection_name: tools, rerank_score: 0.9789302349090576
content:
Tool tính giá trị lượng giác (sin, cos, tan, cot) của 1 góc từ 0° đến 180°.
Dùng khi đề bài hỏi: "tính sin/cos/tan/cot của góc α", "giá trị lượng giác của góc
120° là bao nhiêu".
Ví dụ: "Tính sin150°" → sin150° = 1/2.
Ví dụ: "Tính cos120°" → cos120° = -1/2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.05644691735506058
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.052420537918806076
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.009934729896485806
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.007082223426550627
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).
=====================

Query 70 [Vận dụng]: Một mái nhà nghiêng tạo với phương ngang một góc 120°. Tính cos của góc này để phục vụ tính độ dốc mái (gia_tri_luong_giac)

Tool 1: gia_tri_luong_giac
Tool 2: goc_giua_hai_vecto
Tool 3: dinh_ly_cosin
Tool 4: dinh_ly_sin
Tool 5: do_dai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_14, tool_chapter_id: c_4, tool_name: gia_tri_luong_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giá trị lượng giác của một góc từ 0° đến 180°, _id: f6237aa0-821e-4007-a0e0-83fd698a9f78, _collection_name: tools, rerank_score: 0.8469776511192322
content:
Tool tính giá trị lượng giác (sin, cos, tan, cot) của 1 góc từ 0° đến 180°.
Dùng khi đề bài hỏi: "tính sin/cos/tan/cot của góc α", "giá trị lượng giác của góc
120° là bao nhiêu".
Ví dụ: "Tính sin150°" → sin150° = 1/2.
Ví dụ: "Tính cos120°" → cos120° = -1/2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.09339256584644318
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.009339746087789536
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.0030162325128912926
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.0017505850410088897
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.
=====================

Query 71 [Dễ]: Tam giác ABC có b=4, c=6, góc A=60°. Tính cạnh a (dinh_ly_cosin)

Tool 1: dien_tich_tam_giac
Tool 2: dinh_ly_sin
Tool 3: dinh_ly_cosin
Tool 4: giai_tam_giac
Tool 5: goc_giua_hai_vecto

Result Tool: ❌ ❌ ✅ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.9918597340583801
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.989392876625061
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.9888866543769836
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.8545466661453247
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.18492449820041656
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 72 [Dễ]: Tam giác ABC có b=5, c=5, góc A=90°. Tính cạnh a (dinh_ly_cosin)

Tool 1: dinh_ly_cosin
Tool 2: dien_tich_tam_giac
Tool 3: dinh_ly_sin
Tool 4: goc_giua_hai_vecto
Tool 5: giai_tam_giac

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.9910749197006226
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.9607388973236084
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.9060015082359314
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.8289787173271179
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.5649570226669312
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".
=====================

Query 73 [Thông hiểu]: Tam giác ABC có a=7, b=5, c=6. Tính góc A (dinh_ly_cosin)

Tool 1: dinh_ly_cosin
Tool 2: dien_tich_tam_giac
Tool 3: dinh_ly_sin
Tool 4: giai_tam_giac
Tool 5: goc_giua_hai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.9896474480628967
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.9713690280914307
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.9590088725090027
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.8265944719314575
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.35647475719451904
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 74 [Thông hiểu]: Tam giác ABC có b=10, c=12, góc A=45°. Tính cạnh a (dinh_ly_cosin)

Tool 1: dinh_ly_sin
Tool 2: dinh_ly_cosin
Tool 3: dien_tich_tam_giac
Tool 4: giai_tam_giac
Tool 5: goc_giua_hai_vecto

Result Tool: ❌ ✅ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.9881399869918823
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.9511305093765259
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.8507885336875916
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.6543076038360596
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.29425346851348877
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 75 [Vận dụng]: Hai con tàu xuất phát từ cùng 1 điểm, tàu 1 đi 5km, tàu 2 đi 8km, góc giữa 2 hướng đi là 70°. Tính khoảng cách giữa hai tàu (dinh_ly_cosin)

Tool 1: goc_giua_hai_vecto
Tool 2: giai_tam_giac
Tool 3: dinh_ly_cosin
Tool 4: tich_vo_huong_vecto
Tool 5: gia_tri_luong_giac

Result Tool: ❌ ❌ ✅ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.04157686233520508
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.017815783619880676
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.007664046715945005
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.004567516501992941
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_14, tool_chapter_id: c_4, tool_name: gia_tri_luong_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giá trị lượng giác của một góc từ 0° đến 180°, _id: f6237aa0-821e-4007-a0e0-83fd698a9f78, _collection_name: tools, rerank_score: 0.004152604378759861
content:
Tool tính giá trị lượng giác (sin, cos, tan, cot) của 1 góc từ 0° đến 180°.
Dùng khi đề bài hỏi: "tính sin/cos/tan/cot của góc α", "giá trị lượng giác của góc
120° là bao nhiêu".
Ví dụ: "Tính sin150°" → sin150° = 1/2.
Ví dụ: "Tính cos120°" → cos120° = -1/2.
=====================

Query 76 [Dễ]: Tam giác ABC có a=8, góc A=30°. Tính bán kính đường tròn ngoại tiếp R (dinh_ly_sin)

Tool 1: dinh_ly_sin
Tool 2: dinh_ly_cosin
Tool 3: dien_tich_tam_giac
Tool 4: giai_tam_giac
Tool 5: gia_tri_luong_giac

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.9856675863265991
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.1785314679145813
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.1524328589439392
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.08985818177461624
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_14, tool_chapter_id: c_4, tool_name: gia_tri_luong_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giá trị lượng giác của một góc từ 0° đến 180°, _id: f6237aa0-821e-4007-a0e0-83fd698a9f78, _collection_name: tools, rerank_score: 0.01579393446445465
content:
Tool tính giá trị lượng giác (sin, cos, tan, cot) của 1 góc từ 0° đến 180°.
Dùng khi đề bài hỏi: "tính sin/cos/tan/cot của góc α", "giá trị lượng giác của góc
120° là bao nhiêu".
Ví dụ: "Tính sin150°" → sin150° = 1/2.
Ví dụ: "Tính cos120°" → cos120° = -1/2.
=====================

Query 77 [Dễ]: Tam giác ABC có a=10, góc A=90°. Tính bán kính đường tròn ngoại tiếp R (dinh_ly_sin)

Tool 1: dinh_ly_sin
Tool 2: goc_giua_hai_vecto
Tool 3: dien_tich_tam_giac
Tool 4: dinh_ly_cosin
Tool 5: giai_tam_giac

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.986375093460083
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.17378897964954376
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.1466730833053589
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.09774039685726166
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.08199849724769592
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".
=====================

Query 78 [Thông hiểu]: Tam giác ABC có a=6, góc A=40°, góc B=60°. Tính cạnh b (dinh_ly_sin)

Tool 1: dinh_ly_sin
Tool 2: dien_tich_tam_giac
Tool 3: dinh_ly_cosin
Tool 4: giai_tam_giac
Tool 5: goc_giua_hai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.9920980930328369
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.9823440313339233
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.9728693962097168
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.8175262212753296
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.3963351845741272
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 79 [Thông hiểu]: Tam giác ABC có a=9, góc A=50°, góc B=70°. Tính cạnh b (dinh_ly_sin)

Tool 1: dinh_ly_cosin
Tool 2: giai_tam_giac
Tool 3: dinh_ly_sin
Tool 4: dien_tich_tam_giac
Tool 5: goc_giua_hai_vecto

Result Tool: ❌ ❌ ✅ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.9652669429779053
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.9140356779098511
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.869450569152832
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.8199353814125061
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.47349122166633606
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 80 [Vận dụng]: Một khu đất tam giác có cạnh a=15m nhìn dưới góc A=35°. Tính bán kính đường tròn ngoại tiếp khu đất (dinh_ly_sin)

Tool 1: dinh_ly_sin
Tool 2: dinh_ly_cosin
Tool 3: dien_tich_tam_giac
Tool 4: giai_tam_giac
Tool 5: goc_giua_hai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.9779437780380249
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.0931866243481636
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.08135917782783508
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.02692429907619953
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.008362434804439545
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 81 [Dễ]: Giải tam giác ABC biết a=5, góc A=30°, góc B=60° (giai_tam_giac)

Tool 1: dinh_ly_cosin
Tool 2: dien_tich_tam_giac
Tool 3: giai_tam_giac
Tool 4: dinh_ly_sin
Tool 5: goc_giua_hai_vecto

Result Tool: ❌ ❌ ✅ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.9115684032440186
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.8796853423118591
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.8556869626045227
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.22616897523403168
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.014690148644149303
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 82 [Dễ]: Giải tam giác ABC biết b=6, c=8, góc A=90° (giai_tam_giac)

Tool 1: giai_tam_giac
Tool 2: dien_tich_tam_giac
Tool 3: dinh_ly_sin
Tool 4: dinh_ly_cosin
Tool 5: goc_giua_hai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.7019422054290771
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.6985597610473633
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.6789699792861938
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.6160374283790588
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.34048992395401
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 83 [Thông hiểu]: Giải tam giác ABC biết a=10, góc A=45°, góc B=75° (giai_tam_giac)

Tool 1: giai_tam_giac
Tool 2: dinh_ly_cosin
Tool 3: dinh_ly_sin
Tool 4: dien_tich_tam_giac
Tool 5: goc_giua_hai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.7822006940841675
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.7778094410896301
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.6790369749069214
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.539258599281311
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.01451172586530447
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 84 [Thông hiểu]: Giải tam giác ABC biết b=7, c=9, góc A=60° (giai_tam_giac)

Tool 1: giai_tam_giac
Tool 2: dinh_ly_cosin
Tool 3: dien_tich_tam_giac
Tool 4: dinh_ly_sin
Tool 5: goc_giua_hai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.9903682470321655
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.9199522733688354
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.7495742440223694
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.2503703236579895
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.01230896357446909
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 85 [Vận dụng]: Đo được 1 cạnh khu đất tam giác là 20m và hai góc kề cạnh đó là 50° và 65°. Giải tam giác để tính các cạnh và góc còn lại (giai_tam_giac)

Tool 1: giai_tam_giac
Tool 2: dinh_ly_cosin
Tool 3: dinh_ly_sin
Tool 4: dien_tich_tam_giac
Tool 5: goc_giua_hai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.9732866883277893
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.9471104145050049
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.7688767313957214
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.39520999789237976
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.03548545017838478
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 86 [Dễ]: Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5 (dien_tich_tam_giac)

Tool 1: dien_tich_tam_giac
Tool 2: dinh_ly_cosin
Tool 3: dinh_ly_sin
Tool 4: giai_tam_giac
Tool 5: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.9980202913284302
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.9184195399284363
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.3047688901424408
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.1464083045721054
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.07683801651000977
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 87 [Dễ]: Tính diện tích tam giác biết a=6, b=8, góc C=90° (dien_tich_tam_giac)

Tool 1: dien_tich_tam_giac
Tool 2: dinh_ly_cosin
Tool 3: dinh_ly_sin
Tool 4: giai_tam_giac
Tool 5: goc_giua_hai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.9533392190933228
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.44861918687820435
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.4476223289966583
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.3121051788330078
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.22223453223705292
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 88 [Thông hiểu]: Tính diện tích tam giác có 3 cạnh a=5, b=6, c=7 (dien_tich_tam_giac)

Tool 1: dien_tich_tam_giac
Tool 2: dinh_ly_cosin
Tool 3: dinh_ly_sin
Tool 4: giai_tam_giac
Tool 5: tich_so_voi_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.9930509328842163
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.9413154721260071
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.4371238648891449
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.2671874761581421
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.02284366451203823
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).
=====================

Query 89 [Thông hiểu]: Tính diện tích tam giác biết a=7, b=9, góc C=60° (dien_tich_tam_giac)

Tool 1: giai_tam_giac
Tool 2: dien_tich_tam_giac
Tool 3: dinh_ly_cosin
Tool 4: dinh_ly_sin
Tool 5: goc_giua_hai_vecto

Result Tool: ❌ ✅ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.9632601737976074
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.942012369632721
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.8880119323730469
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.09312120825052261
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.023506568744778633
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 90 [Vận dụng]: Một khu vườn hình tam giác có 2 cạnh dài 12m và 15m, góc xen giữa 50°. Tính diện tích khu vườn (dien_tich_tam_giac)

Tool 1: dien_tich_tam_giac
Tool 2: dinh_ly_cosin
Tool 3: dinh_ly_sin
Tool 4: giai_tam_giac
Tool 5: goc_giua_hai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.8170772194862366
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.6039993762969971
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.07178249955177307
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.01932811364531517
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.01158556155860424
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 91 [Dễ]: Cho a=(1,2), b=(3,4). Tính a+b (tong_hieu_vecto)

Tool 1: tong_hieu_vecto
Tool 2: hop_tap_hop
Tool 3: tich_vo_huong_vecto
Tool 4: giao_tap_hop
Tool 5: hieu_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.968467652797699
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.9411515593528748
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.869856059551239
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.6956709027290344
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.6624010801315308
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.
=====================

Query 92 [Dễ]: Cho a=(5,1), b=(2,3). Tính a-b (tong_hieu_vecto)

Tool 1: hieu_tap_hop
Tool 2: tong_hieu_vecto
Tool 3: giao_tap_hop
Tool 4: tich_vo_huong_vecto
Tool 5: goc_giua_hai_vecto

Result Tool: ❌ ✅ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.7756321430206299
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.7383889555931091
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.7376997470855713
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.4460117220878601
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.29963764548301697
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 93 [Thông hiểu]: Cho a=(-2,3), b=(4,-1). Tính a+b (tong_hieu_vecto)

Tool 1: tong_hieu_vecto
Tool 2: hieu_tap_hop
Tool 3: giao_tap_hop
Tool 4: tich_vo_huong_vecto
Tool 5: hop_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.9651182293891907
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.6073060035705566
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.561497688293457
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.5597651600837708
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.41944944858551025
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.
=====================

Query 94 [Thông hiểu]: Cho a=(0,5), b=(5,0). Tính a-b (tong_hieu_vecto)

Tool 1: tong_hieu_vecto
Tool 2: tich_vo_huong_vecto
Tool 3: goc_giua_hai_vecto
Tool 4: hieu_tap_hop
Tool 5: hop_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.5515246987342834
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.5160898566246033
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.31911855936050415
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.1347770243883133
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.12791641056537628
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.
=====================

Query 95 [Vận dụng]: Vật chịu 2 lực F1=(3,4) và F2=(1,-2) (Newton). Tính hợp lực F=F1+F2 (tong_hieu_vecto)

Tool 1: hop_tap_hop
Tool 2: giao_tap_hop
Tool 3: tim_gtln_gtnn_mien
Tool 4: tong_hieu_vecto
Tool 5: gia_tri_luong_giac

Result Tool: ❌ ❌ ❌ ✅ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.05927761644124985
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.006167234852910042
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.004142561461776495
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.003636829787865281
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_14, tool_chapter_id: c_4, tool_name: gia_tri_luong_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giá trị lượng giác của một góc từ 0° đến 180°, _id: f6237aa0-821e-4007-a0e0-83fd698a9f78, _collection_name: tools, rerank_score: 0.0020581940189003944
content:
Tool tính giá trị lượng giác (sin, cos, tan, cot) của 1 góc từ 0° đến 180°.
Dùng khi đề bài hỏi: "tính sin/cos/tan/cot của góc α", "giá trị lượng giác của góc
120° là bao nhiêu".
Ví dụ: "Tính sin150°" → sin150° = 1/2.
Ví dụ: "Tính cos120°" → cos120° = -1/2.
=====================

Query 96 [Dễ]: Cho a=(2,3). Tính 4a (tich_so_voi_vecto)

Tool 1: tong_hieu_vecto
Tool 2: tich_vo_huong_vecto
Tool 3: tich_so_voi_vecto
Tool 4: do_dai_vecto
Tool 5: hieu_tap_hop

Result Tool: ❌ ❌ ✅ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.7955334782600403
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.5056443214416504
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.3175048530101776
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.28935521841049194
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.040685731917619705
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.
=====================

Query 97 [Dễ]: Cho a=(1,-1). Tính 3a (tich_so_voi_vecto)

Tool 1: tong_hieu_vecto
Tool 2: tich_so_voi_vecto
Tool 3: do_dai_vecto
Tool 4: goc_giua_hai_vecto
Tool 5: tich_vo_huong_vecto

Result Tool: ❌ ✅ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.76833176612854
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.2623959183692932
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.2073485255241394
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.17826873064041138
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.06466040760278702
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 98 [Thông hiểu]: Cho a=(-2,5). Tính 2a (tich_so_voi_vecto)

Tool 1: tich_so_voi_vecto
Tool 2: tong_hieu_vecto
Tool 3: dinh_ly_cosin
Tool 4: tich_vo_huong_vecto
Tool 5: goc_giua_hai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.13638901710510254
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.12913958728313446
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.08998572826385498
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.08053063601255417
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.05431902036070824
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 99 [Thông hiểu]: Cho a=(6,-4). Tính -3a (tich_so_voi_vecto)

Tool 1: do_dai_vecto
Tool 2: tich_vo_huong_vecto
Tool 3: tich_so_voi_vecto
Tool 4: tong_hieu_vecto
Tool 5: dinh_ly_sin

Result Tool: ❌ ❌ ✅ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.1755000203847885
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.11128373444080353
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.05886960029602051
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.028431475162506104
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.026300670579075813
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".
=====================

Query 100 [Vận dụng]: Vectơ vận tốc ban đầu v=(2,3) m/s, tăng gấp 3 lần theo cùng hướng. Tính vectơ vận tốc mới 3v (tich_so_voi_vecto)

Tool 1: do_dai_vecto
Tool 2: tong_hieu_vecto
Tool 3: goc_giua_hai_vecto
Tool 4: tich_so_voi_vecto
Tool 5: tich_vo_huong_vecto

Result Tool: ❌ ❌ ❌ ✅ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.1294287145137787
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.05964919179677963
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.027340851724147797
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.026275983080267906
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.015161832794547081
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.
=====================

Query 101 [Dễ]: Cho a=(1,2), b=(3,4). Tính a·b (tich_vo_huong_vecto)

Tool 1: tich_vo_huong_vecto
Tool 2: tong_hieu_vecto
Tool 3: hop_tap_hop
Tool 4: hieu_tap_hop
Tool 5: giao_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.9838418960571289
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.9524649977684021
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.9494937062263489
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.8318485617637634
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.8274487853050232
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.
=====================

Query 102 [Dễ]: Cho a=(2,0), b=(0,3). Tính a·b (tich_vo_huong_vecto)

Tool 1: tich_vo_huong_vecto
Tool 2: giao_tap_hop
Tool 3: hop_tap_hop
Tool 4: hieu_tap_hop
Tool 5: tong_hieu_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.9251952171325684
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.8272227048873901
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.7907121777534485
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.7905753254890442
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.7719448804855347
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).
=====================

Query 103 [Thông hiểu]: Cho a=(-1,3), b=(2,4). Tính a·b (tich_vo_huong_vecto)

Tool 1: tich_vo_huong_vecto
Tool 2: giao_tap_hop
Tool 3: hop_tap_hop
Tool 4: tong_hieu_vecto
Tool 5: hieu_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.9397610425949097
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.7536441683769226
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.7284714579582214
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.703935444355011
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.6437854170799255
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.
=====================

Query 104 [Thông hiểu]: Cho a=(5,-2), b=(-1,3). Tính a·b (tich_vo_huong_vecto)

Tool 1: tich_vo_huong_vecto
Tool 2: tong_hieu_vecto
Tool 3: goc_giua_hai_vecto
Tool 4: giao_tap_hop
Tool 5: hieu_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.7207671999931335
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.5624071359634399
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.49619171023368835
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.47213757038116455
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.4114832580089569
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.
=====================

Query 105 [Vận dụng]: Hai lực F1=(3,4) và F2=(4,-3) (Newton) tác dụng lên vật. Tính tích vô hướng F1·F2 để kiểm tra 2 lực có vuông góc không (tich_vo_huong_vecto)

Tool 1: tich_vo_huong_vecto
Tool 2: goc_giua_hai_vecto
Tool 3: giao_tap_hop
Tool 4: tong_hieu_vecto
Tool 5: hop_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.8871501684188843
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.08050020784139633
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.006862367503345013
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.006288605742156506
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.005355601664632559
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.
=====================

Query 106 [Dễ]: Tính độ dài vectơ a=(3,4) (do_dai_vecto)

Tool 1: do_dai_vecto
Tool 2: tich_vo_huong_vecto
Tool 3: tong_hieu_vecto
Tool 4: goc_giua_hai_vecto
Tool 5: tich_so_voi_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.9963114857673645
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.37787050008773804
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.1263224333524704
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.12339814752340317
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.07062389701604843
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).
=====================

Query 107 [Dễ]: Tính độ dài vectơ a=(6,8) (do_dai_vecto)

Tool 1: do_dai_vecto
Tool 2: goc_giua_hai_vecto
Tool 3: tich_so_voi_vecto
Tool 4: tich_vo_huong_vecto
Tool 5: tong_hieu_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.8393833041191101
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.07732319831848145
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.046597182750701904
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.020832723006606102
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.017012201249599457
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).
=====================

Query 108 [Thông hiểu]: Tính độ dài vectơ a=(-5,12) (do_dai_vecto)

Tool 1: do_dai_vecto
Tool 2: goc_giua_hai_vecto
Tool 3: tich_vo_huong_vecto
Tool 4: tong_hieu_vecto
Tool 5: tich_so_voi_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.9030366539955139
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.15700474381446838
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.10200601816177368
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.03820525109767914
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.02233591303229332
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).
=====================

Query 109 [Thông hiểu]: Tính độ dài vectơ a=(1,1) (do_dai_vecto)

Tool 1: do_dai_vecto
Tool 2: goc_giua_hai_vecto
Tool 3: tich_vo_huong_vecto
Tool 4: tong_hieu_vecto
Tool 5: tich_so_voi_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.9668797254562378
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.8244178295135498
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.3344285488128662
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.24491599202156067
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.07670298218727112
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).
=====================

Query 110 [Vận dụng]: Người đi từ A đến B theo vectơ dịch chuyển d=(30,40) mét. Tính quãng đường thẳng từ A đến B (do_dai_vecto)

Tool 1: goc_giua_hai_vecto
Tool 2: do_dai_vecto
Tool 3: tong_hieu_vecto
Tool 4: tich_vo_huong_vecto
Tool 5: tich_so_voi_vecto

Result Tool: ❌ ✅ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.08554446697235107
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.06011700630187988
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.037200383841991425
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.017448795959353447
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.007856197655200958
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).
=====================

Query 111 [Dễ]: Tính góc giữa a=(1,0) và b=(0,1) (goc_giua_hai_vecto)

Tool 1: goc_giua_hai_vecto
Tool 2: tich_vo_huong_vecto
Tool 3: dinh_ly_cosin
Tool 4: tong_hieu_vecto
Tool 5: dinh_ly_sin

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.9972686767578125
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.24646541476249695
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.09666529297828674
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.07685154676437378
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.04699300229549408
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".
=====================

Query 112 [Dễ]: Tính góc giữa a=(1,1) và b=(1,0) (goc_giua_hai_vecto)

Tool 1: goc_giua_hai_vecto
Tool 2: tich_vo_huong_vecto
Tool 3: tong_hieu_vecto
Tool 4: dinh_ly_cosin
Tool 5: dinh_ly_sin

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.9857014417648315
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.3730712831020355
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.06940925121307373
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.0656052902340889
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_16, tool_chapter_id: c_4, tool_name: dinh_ly_sin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 924cce7b-c34f-4a21-afdb-c0a27048f04d, _collection_name: tools, rerank_score: 0.03708702698349953
content:
Tool áp dụng định lí sin để tính cạnh, góc, hoặc bán kính đường tròn ngoại tiếp tam giác.
Dùng khi đề bài cho 1 cạnh và góc đối diện, hỏi cạnh/góc khác hoặc bán kính R. Công
thức: a/sinA = b/sinB = c/sinC = 2R.
Ví dụ: "Tam giác ABC có a=6, góc A=45°. Tính bán kính đường tròn ngoại tiếp R".
=====================

Query 113 [Thông hiểu]: Tính góc giữa a=(2,0) và b=(-1,1) (goc_giua_hai_vecto)

Tool 1: goc_giua_hai_vecto
Tool 2: tich_vo_huong_vecto
Tool 3: tong_hieu_vecto
Tool 4: dinh_ly_cosin
Tool 5: dien_tich_tam_giac

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.8190260529518127
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.39102545380592346
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.21231453120708466
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.1641642153263092
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.11636906117200851
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).
=====================

Query 114 [Thông hiểu]: Tính góc giữa a=(3,4) và b=(4,3) (goc_giua_hai_vecto)

Tool 1: tich_vo_huong_vecto
Tool 2: goc_giua_hai_vecto
Tool 3: dinh_ly_cosin
Tool 4: tong_hieu_vecto
Tool 5: giao_tap_hop

Result Tool: ❌ ✅ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.7118681073188782
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.4450884461402893
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.14311130344867706
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.13396546244621277
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.12193789333105087
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.
=====================

Query 115 [Vận dụng]: Hai lực F1=(5,0) và F2=(3,3) tác dụng lên vật. Tính góc giữa hai lực để phân tích hướng hợp lực (goc_giua_hai_vecto)

Tool 1: goc_giua_hai_vecto
Tool 2: tich_vo_huong_vecto
Tool 3: dinh_ly_cosin
Tool 4: hop_tap_hop
Tool 5: tong_hieu_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.121157206594944
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.019218945875763893
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_15, tool_chapter_id: c_4, tool_name: dinh_ly_cosin_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Định lí cosin và định lí sin, _id: 8141966f-0e81-4e87-b5d1-0eaf16a65e1a, _collection_name: tools, rerank_score: 0.006080893334001303
content:
Tool áp dụng định lí côsin để tính 1 cạnh hoặc 1 góc trong tam giác khi biết 2 cạnh và
góc xen giữa, hoặc biết 3 cạnh.
Dùng khi đề bài cho tam giác với 2 cạnh + góc xen giữa, hoặc 3 cạnh, hỏi cạnh/góc còn
lại. Công thức: a² = b² + c² - 2bc.cosA.
Ví dụ: "Tam giác ABC có b=5, c=7, góc A=60°. Tính cạnh a".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.00395713048055768
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.003916696645319462
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).
=====================

Query 116 [Dễ]: Số gần đúng a=3.1 của số đúng 3.14. Tính sai số tuyệt đối (sai_so_tuong_doi)

Tool 1: sai_so_tuong_doi
Tool 2: hieu_tap_hop
Tool 3: xet_menh_de
Tool 4: hop_tap_hop
Tool 5: tinh_phuong_sai_do_lech_chuan

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.9909046292304993
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.003293901216238737
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.0027877618558704853
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.0018526678904891014
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.0017385223181918263
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".
=====================

Query 117 [Dễ]: Số gần đúng a=1.4 của số đúng √2≈1.41421. Tính sai số tuyệt đối (sai_so_tuong_doi)

Tool 1: sai_so_tuong_doi
Tool 2: xet_menh_de
Tool 3: tich_vo_huong_vecto
Tool 4: tinh_phuong_sai_do_lech_chuan
Tool 5: hieu_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.8593716621398926
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.002812350634485483
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.002062128158286214
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.0018918648129329085
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.0018374737119302154
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.
=====================

Query 118 [Thông hiểu]: Số gần đúng a=2.24 của √5≈2.2360679. Tính sai số tương đối (sai_so_tuong_doi)

Tool 1: sai_so_tuong_doi
Tool 2: xet_menh_de
Tool 3: tich_vo_huong_vecto
Tool 4: hieu_tap_hop
Tool 5: tinh_trung_binh

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.6672382354736328
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.002348912414163351
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.0023376590106636286
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_5, tool_chapter_id: c_1, tool_name: hieu_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: c75e3b8b-9a03-4f2f-9de3-4ae5e4ee0821, _collection_name: tools, rerank_score: 0.0021608490496873856
content:
Tool tính hiệu (difference, A \ B) của hai tập hợp số — các phần tử thuộc A nhưng
không thuộc B.
Dùng khi đề bài hỏi "tìm A \ B", "phần tử thuộc A mà không thuộc B".
Ví dụ: "Tìm A \ B với A={1,2,3}, B={2,3}" → A \ B = {1}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.00140319240745157
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.
=====================

Query 119 [Thông hiểu]: Đo chiều dài được số gần đúng 15.2, số đúng 15.25. Tính sai số tương đối (sai_so_tuong_doi)

Tool 1: sai_so_tuong_doi
Tool 2: do_dai_vecto
Tool 3: xet_menh_de
Tool 4: tinh_phuong_sai_do_lech_chuan
Tool 5: goc_giua_hai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.770489513874054
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.010791681706905365
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.00941759254783392
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.003002149984240532
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_23, tool_chapter_id: c_5, tool_name: goc_giua_hai_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 4a9190c6-136e-4e4b-8b53-80d592f12f8d, _collection_name: tools, rerank_score: 0.0023593800142407417
content:
Tool tính góc giữa 2 vectơ dựa trên tích vô hướng và độ dài từng vectơ.
Dùng khi đề bài hỏi trực tiếp: "tính góc giữa vectơ a và vectơ b". Công thức:
cosα = (a·b) / (|a|.|b|).
Ví dụ: "Cho a=(1,0), b=(0,1). Tính góc giữa a và b" → 90°.
=====================

Query 120 [Vận dụng]: Đo diện tích mảnh đất, kết quả gần đúng 250m² trong khi số đúng là 253.6m². Tính sai số tương đối để đánh giá độ chính xác (sai_so_tuong_doi)

Tool 1: sai_so_tuong_doi
Tool 2: tinh_phuong_sai_do_lech_chuan
Tool 3: xet_menh_de
Tool 4: dien_tich_tam_giac
Tool 5: tich_so_voi_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.789689838886261
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.006118780933320522
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.004331925418227911
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_18, tool_chapter_id: c_4, tool_name: dien_tich_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 1e381965-1c2c-45d2-83d0-01a8c9eb1d87, _collection_name: tools, rerank_score: 0.00279291276820004
content:
Tool tính diện tích tam giác bằng công thức lượng giác (1/2.a.b.sinC) hoặc công thức
Heron (biết 3 cạnh).
Dùng khi đề bài hỏi: "tính diện tích tam giác ABC biết...".
Ví dụ: "Tính diện tích tam giác ABC biết a=5, b=6, góc C=60°".
Ví dụ: "Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5" (dùng công thức Heron).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.001989167183637619
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).
=====================

Query 121 [Dễ]: Tính số trung bình của mẫu: 2, 4, 6, 8, 10 (tinh_trung_binh)

Tool 1: tinh_trung_binh
Tool 2: tinh_trung_vi_mode
Tool 3: tinh_phuong_sai_do_lech_chuan
Tool 4: tich_so_voi_vecto
Tool 5: tong_hieu_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.9962809681892395
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.8083238005638123
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.5606290698051453
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.009068897925317287
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.008025071583688259
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).
=====================

Query 122 [Dễ]: Tính số trung bình của mẫu: 1, 2, 3, 4, 5 (tinh_trung_binh)

Tool 1: tinh_trung_vi_mode
Tool 2: tinh_trung_binh
Tool 3: tinh_phuong_sai_do_lech_chuan
Tool 4: tich_vo_huong_vecto
Tool 5: do_dai_vecto

Result Tool: ❌ ✅ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.8798380494117737
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.8555216789245605
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.13141538202762604
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.11533213406801224
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.0662531778216362
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.
=====================

Query 123 [Thông hiểu]: Tính số trung bình của mẫu: 10, 15, 20, 25, 30, 35 (tinh_trung_binh)

Tool 1: tinh_trung_binh
Tool 2: tinh_trung_vi_mode
Tool 3: tinh_phuong_sai_do_lech_chuan
Tool 4: tong_hieu_vecto
Tool 5: sai_so_tuong_doi

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.15691585838794708
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.06738283485174179
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.008977924473583698
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.0037303362041711807
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.0036395767237991095
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.
=====================

Query 124 [Thông hiểu]: Tính số trung bình của mẫu: 3, 3, 5, 7, 9, 9 (tinh_trung_binh)

Tool 1: tinh_trung_vi_mode
Tool 2: tinh_trung_binh
Tool 3: tich_so_voi_vecto
Tool 4: do_dai_vecto
Tool 5: tinh_phuong_sai_do_lech_chuan

Result Tool: ❌ ✅ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.937543511390686
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.43087074160575867
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.14745543897151947
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.061474502086639404
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.02766805700957775
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".
=====================

Query 125 [Vận dụng]: Điểm kiểm tra Toán của 6 bạn trong tổ: 7, 8, 6, 9, 7, 8. Tính điểm trung bình của tổ (tinh_trung_binh)

Tool 1: tinh_trung_vi_mode
Tool 2: tinh_trung_binh
Tool 3: tich_so_voi_vecto
Tool 4: tinh_phuong_sai_do_lech_chuan
Tool 5: hop_tap_hop

Result Tool: ❌ ✅ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.15145941078662872
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.12289928644895554
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.0027996886055916548
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.0025651713367551565
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.0021041277796030045
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.
=====================

Query 126 [Dễ]: Tìm trung vị của mẫu: 1, 3, 5, 7, 9 (tinh_trung_vi_mode)

Tool 1: tinh_trung_vi_mode
Tool 2: tich_so_voi_vecto
Tool 3: tinh_trung_binh
Tool 4: do_dai_vecto
Tool 5: giai_tam_giac

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.9662930965423584
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.07666204124689102
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.06146608293056488
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.03423110395669937
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_17, tool_chapter_id: c_4, tool_name: giai_tam_giac_tool, chapter_name: Hệ thức lượng trong tam giác, lesson_name: Giải tam giác và ứng dụng thực tế, _id: 2139ff82-6015-4e88-ba70-3bc597453bfa, _collection_name: tools, rerank_score: 0.01737312413752079
content:
Tool "giải tam giác" — tìm toàn bộ các cạnh và góc còn lại của tam giác khi biết 1 số
yếu tố (VD: 2 cạnh + 1 góc, hoặc 1 cạnh + 2 góc), có thể áp dụng vào bài toán thực tế
đo đạc khoảng cách, chiều cao.
Dùng khi đề bài yêu cầu "giải tam giác ABC biết...", hoặc bài toán đo khoảng cách/chiều
cao gián tiếp qua tam giác.
Ví dụ: "Giải tam giác ABC biết a=7, b=9, góc C=60°".
=====================

Query 127 [Dễ]: Tìm mốt của mẫu: 2, 2, 3, 4, 4, 4 (tinh_trung_vi_mode)

Tool 1: tinh_trung_vi_mode
Tool 2: tinh_trung_binh
Tool 3: tinh_phuong_sai_do_lech_chuan
Tool 4: tich_vo_huong_vecto
Tool 5: hop_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.9657871723175049
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.1547400802373886
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.06698350608348846
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.04059926047921181
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.03732115402817726
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.
=====================

Query 128 [Thông hiểu]: Tìm trung vị của mẫu: 2, 4, 6, 8, 10, 12 (tinh_trung_vi_mode)

Tool 1: tinh_trung_vi_mode
Tool 2: tinh_trung_binh
Tool 3: tinh_phuong_sai_do_lech_chuan
Tool 4: giao_tap_hop
Tool 5: xet_dau_tam_thuc

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.9121189117431641
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.8062746524810791
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.19733285903930664
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_4, tool_chapter_id: c_1, tool_name: giao_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: 10335607-6f53-4a09-8066-e6ebe51e8d9d, _collection_name: tools, rerank_score: 0.010354856960475445
content:
Tool tính giao (intersection, A ∩ B) của hai tập hợp số.
Dùng khi đề bài hỏi giao của 2 tập hợp, phần tử chung, "tìm A ∩ B", "tập hợp gồm các
phần tử vừa thuộc A vừa thuộc B".
Ví dụ: "Tìm A ∩ B với A={1,2,3}, B={2,3,4}" → A ∩ B = {2,3}.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_13, tool_chapter_id: c_3, tool_name: xet_dau_tam_thuc_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số bậc hai, _id: e829d836-38e0-4cf7-8356-39cdb1a7363e, _collection_name: tools, rerank_score: 0.009349506348371506
content:
Tool xét dấu của tam thức bậc hai f(x) = ax² + bx + c trên các khoảng nghiệm.
Dùng khi đề bài hỏi: "xét dấu của f(x)", "f(x) dương/âm khi nào", "giải bất phương
trình bậc hai" (thông qua xét dấu).
Ví dụ: "Xét dấu f(x) = x² - 5x + 6" → f(x)>0 khi x<2 hoặc x>3; f(x)<0 khi 2<x<3.
=====================

Query 129 [Thông hiểu]: Tìm mốt của mẫu: 5, 6, 6, 7, 8, 8, 8, 9 (tinh_trung_vi_mode)

Tool 1: tinh_trung_vi_mode
Tool 2: tinh_trung_binh
Tool 3: tinh_phuong_sai_do_lech_chuan
Tool 4: tich_so_voi_vecto
Tool 5: tim_txd_ham_so

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.9034991264343262
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.15654927492141724
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.05608934909105301
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_20, tool_chapter_id: c_5, tool_name: tich_so_voi_vecto_tool, chapter_name: Vectơ, lesson_name: Tích của một số với một vectơ, _id: a483a2c2-01cd-4f1d-a2dd-917679fb63a2, _collection_name: tools, rerank_score: 0.010032359510660172
content:
Tool tính tích của 1 số thực k với 1 vectơ a (k.a), theo tọa độ.
Dùng khi đề bài cho vectơ và 1 số, hỏi tích của số đó với vectơ.
Ví dụ: "Cho a=(2,3). Tính 3a" → (6,9).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.005898009054362774
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).
=====================

Query 130 [Vận dụng]: Số khách mỗi ngày trong tuần của quán ăn: 20, 25, 22, 30, 25, 28, 25. Tìm trung vị và mốt để đánh giá lượng khách phổ biến (tinh_trung_vi_mode)

Tool 1: tinh_trung_vi_mode
Tool 2: tinh_trung_binh
Tool 3: tim_gtln_gtnn_mien
Tool 4: tim_txd_ham_so
Tool 5: hop_tap_hop

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.20148244500160217
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.0004761630843859166
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_8, tool_chapter_id: c_2, tool_name: tim_gtln_gtnn_mien_tool, chapter_name: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn, lesson_name: Hệ bất phương trình bậc nhất hai ẩn, _id: 997c61f8-e74c-4550-8adf-8eb6d0534ff8, _collection_name: tools, rerank_score: 0.00021878123516216874
content:
Tool tìm giá trị lớn nhất (GTLN) hoặc giá trị nhỏ nhất (GTNN) của biểu thức F = ax + by
trên miền nghiệm là đa giác (cho bởi tọa độ các đỉnh).
Dùng khi đề bài hỏi: "tìm GTLN/GTNN của F=ax+by trên miền D", bài toán quy hoạch tuyến
tính, tối ưu hóa với ràng buộc là hệ bất phương trình.
Ví dụ: "Tìm GTLN của F=2x+3y trên miền tam giác có đỉnh (0,0), (4,0), (0,3)".

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_10, tool_chapter_id: c_3, tool_name: tim_txd_ham_so_tool, chapter_name: Hàm số bậc hai và đồ thị, lesson_name: Hàm số và đồ thị, _id: 61539591-3677-4a2e-ba49-f96de04f9fac, _collection_name: tools, rerank_score: 0.00015155972505453974
content:
Tool tìm tập xác định (TXĐ) của 1 hàm số cho trước (dạng phân thức, căn thức, đa thức).
Dùng khi đề bài hỏi: "tìm tập xác định của hàm số", "hàm số sau xác định khi nào".
Ví dụ: "Tìm TXĐ của y = 1/(x-2)" → D = R \ {2}.
Ví dụ: "Tìm TXĐ của y = √(x-1)" → D = [1, +∞).

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_3, tool_chapter_id: c_1, tool_name: hop_tap_hop_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Các phép toán trên tập hợp, _id: cda39802-d3cc-4f65-a8a4-ac44ea290606, _collection_name: tools, rerank_score: 0.00012557821173686534
content:
Tool tính hợp (union, A ∪ B) của hai tập hợp số.
Dùng khi đề bài cho 2 tập hợp và hỏi hợp của chúng, "tìm A ∪ B", "tập hợp gồm các phần
tử thuộc A hoặc thuộc B".
Ví dụ: "Tìm A ∪ B với A={1,2,3}, B={2,3,4}" → A ∪ B = {1,2,3,4}.
=====================

Query 131 [Dễ]: Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10 (tinh_phuong_sai_do_lech_chuan)

Tool 1: tinh_phuong_sai_do_lech_chuan
Tool 2: tinh_trung_binh
Tool 3: tinh_trung_vi_mode
Tool 4: sai_so_tuong_doi
Tool 5: tong_hieu_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.9243294596672058
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.8389551043510437
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.41799744963645935
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.01084779854863882
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_19, tool_chapter_id: c_5, tool_name: tong_hieu_vecto_tool, chapter_name: Vectơ, lesson_name: Tổng và hiệu của hai vectơ, _id: 2cea7756-fdd1-44f8-b8d5-1ce27029419c, _collection_name: tools, rerank_score: 0.004280185326933861
content:
Tool tính tổng (a + b) hoặc hiệu (a - b) của hai vectơ theo tọa độ.
Dùng khi đề bài cho tọa độ 2 vectơ, hỏi tổng hoặc hiệu của chúng.
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a+b" → (4,1).
Ví dụ: "Cho a=(1,2), b=(3,-1). Tính a-b" → (-2,3).
=====================

Query 132 [Dễ]: Tính phương sai và độ lệch chuẩn của mẫu: 1, 2, 3, 4, 5 (tinh_phuong_sai_do_lech_chuan)

Tool 1: tinh_phuong_sai_do_lech_chuan
Tool 2: tinh_trung_vi_mode
Tool 3: tich_vo_huong_vecto
Tool 4: tinh_trung_binh
Tool 5: do_dai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.7509151101112366
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.5054439306259155
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_21, tool_chapter_id: c_5, tool_name: tich_vo_huong_vecto_tool, chapter_name: Vectơ, lesson_name: Tích vô hướng của hai vectơ, _id: 826d5f13-43c5-487f-a0fb-5db294e424b8, _collection_name: tools, rerank_score: 0.11195459216833115
content:
Tool tính tích vô hướng (dot product) của 2 vectơ theo tọa độ, dùng để suy ra góc giữa
2 vectơ hoặc kiểm tra tính vuông góc.
Dùng khi đề bài hỏi: "tính tích vô hướng của a và b", "góc giữa 2 vectơ", "a có vuông
góc với b không". Công thức: a·b = x1.x2 + y1.y2.
Ví dụ: "Cho a=(1,2), b=(3,-4). Tính a·b" → 1*3+2*(-4) = -5.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.07533824443817139
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.03940344229340553
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.
=====================

Query 133 [Thông hiểu]: Tính phương sai và độ lệch chuẩn của mẫu: 10, 12, 14, 16, 18 (tinh_phuong_sai_do_lech_chuan)

Tool 1: tinh_phuong_sai_do_lech_chuan
Tool 2: sai_so_tuong_doi
Tool 3: tinh_trung_vi_mode
Tool 4: tinh_trung_binh
Tool 5: do_dai_vecto

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.5393615365028381
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.023764945566654205
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.010888252407312393
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.007557544857263565
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.005500027909874916
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.
=====================

Query 134 [Thông hiểu]: Tính phương sai và độ lệch chuẩn của mẫu: 5, 7, 7, 9, 11, 13 (tinh_phuong_sai_do_lech_chuan)

Tool 1: tinh_phuong_sai_do_lech_chuan
Tool 2: tinh_trung_vi_mode
Tool 3: sai_so_tuong_doi
Tool 4: do_dai_vecto
Tool 5: tinh_trung_binh

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.3757275640964508
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.09595713764429092
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.007019964512437582
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_22, tool_chapter_id: c_5, tool_name: do_dai_vecto_tool, chapter_name: Vectơ, lesson_name: Khái niệm vectơ, _id: 6f11d957-959a-4289-9d23-b93e3e01bdd0, _collection_name: tools, rerank_score: 0.006895966827869415
content:
Tool tính độ dài (độ lớn) của 1 vectơ theo tọa độ.
Dùng khi đề bài hỏi: "tính độ dài vectơ a", "|a| bằng bao nhiêu". Công thức:
|a| = √(x² + y²).
Ví dụ: "Cho a=(3,4). Tính |a|" → √(9+16) = 5.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.005974111147224903
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.
=====================

Query 135 [Vận dụng]: Điểm thi của 5 học sinh: 6, 7, 8, 8, 9. Tính phương sai và độ lệch chuẩn để đánh giá mức độ đồng đều điểm số (tinh_phuong_sai_do_lech_chuan)

Tool 1: tinh_phuong_sai_do_lech_chuan
Tool 2: tinh_trung_vi_mode
Tool 3: sai_so_tuong_doi
Tool 4: tinh_trung_binh
Tool 5: xet_menh_de

Result Tool: ✅ ❌ ❌ ❌ ❌
---------------------
chunk 1:
metadata:
 type: tool, subject: Toán 10, tool_id: t_27, tool_chapter_id: c_6, tool_name: tinh_phuong_sai_do_lech_chuan_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo mức độ phân tán của mẫu số liệu, _id: 8e795271-5786-42b0-8d7c-0882d2e281fa, _collection_name: tools, rerank_score: 0.618654727935791
content:
Tool tính phương sai (variance) và độ lệch chuẩn (standard deviation) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "tính phương sai của mẫu", "độ lệch chuẩn là bao nhiêu", "mức độ
phân tán của mẫu số liệu".
Ví dụ: "Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10".

---

chunk 2:
metadata:
 type: tool, subject: Toán 10, tool_id: t_26, tool_chapter_id: c_6, tool_name: tinh_trung_vi_mode_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 18fbce4f-15dd-4040-87b7-3e6aa2d3dabb, _collection_name: tools, rerank_score: 0.09589208662509918
content:
Tool tính số trung vị (median) hoặc mốt (mode) của 1 mẫu số liệu.
Dùng khi đề bài hỏi "số trung vị của mẫu là bao nhiêu", "mốt (giá trị xuất hiện nhiều
nhất) của mẫu số liệu".
Ví dụ: "Tính trung vị của mẫu: 1, 3, 3, 6, 7, 8, 9" → trung vị = 6.
Ví dụ: "Tìm mốt của mẫu: 1, 2, 2, 2, 3, 4" → mốt = 2.

---

chunk 3:
metadata:
 type: tool, subject: Toán 10, tool_id: t_24, tool_chapter_id: c_6, tool_name: sai_so_tuong_doi_tool, chapter_name: Thống kê, lesson_name: Số gần đúng và sai số, _id: d4aa7c90-a812-41cc-849d-4afb92daf80f, _collection_name: tools, rerank_score: 0.014488381333649158
content:
Tool tính sai số tuyệt đối và sai số tương đối giữa số gần đúng và số đúng (hoặc ước
lượng sai số tối đa).
Dùng khi đề bài cho số gần đúng và số đúng (hoặc khoảng sai số), hỏi sai số tuyệt đối
/ sai số tương đối.
Ví dụ: "Số gần đúng a=3.14 của π=3.14159. Tính sai số tuyệt đối" → |3.14159-3.14|=0.00159.

---

chunk 4:
metadata:
 type: tool, subject: Toán 10, tool_id: t_25, tool_chapter_id: c_6, tool_name: tinh_trung_binh_tool, chapter_name: Thống kê, lesson_name: Các số đặc trưng đo xu thế trung tâm của mẫu số liệu, _id: 03bdead8-8733-407a-90a1-126be442d9d8, _collection_name: tools, rerank_score: 0.007874318398535252
content:
Tool tính số trung bình (mean) của 1 mẫu số liệu.
Dùng khi đề bài cho dãy số liệu, hỏi "số trung bình", "giá trị trung bình" của mẫu.
Ví dụ: "Tính số trung bình của mẫu số liệu: 2, 4, 6, 8, 10" → (2+4+6+8+10)/5 = 6.

---

chunk 5:
metadata:
 type: tool, subject: Toán 10, tool_id: t_1, tool_chapter_id: c_1, tool_name: xet_menh_de_tool, chapter_name: Mệnh đề và tập hợp, lesson_name: Mệnh đề, _id: eb136f32-9dfb-46d2-b13c-a2986c82c34b, _collection_name: tools, rerank_score: 0.0029953555203974247
content:
Tool xác định 1 mệnh đề (câu khẳng định) là đúng hay sai.
Dùng khi đề bài hỏi: "mệnh đề sau đúng hay sai?", "xét tính đúng sai của câu sau",
"khẳng định sau đúng hay sai?".
Ví dụ: "15 chia hết cho 3 là mệnh đề đúng hay sai?" → Đúng.
Ví dụ: "Số 7 là số chẵn, đúng hay sai?" → Sai.
=====================


Tổng kết: 135/135 query có tool kỳ vọng nằm trong top-5

  - Dễ: 54/54
  - Thông hiểu: 54/54
  - Vận dụng: 27/27