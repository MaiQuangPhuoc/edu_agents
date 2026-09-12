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
