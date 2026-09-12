| Metric                               | Giá trị    |
| ------------------------------------ | ---------- |
| Tổng query                           | 27         |
| Tìm thấy tool đúng trong Top-3       | 26         |
| Không tìm thấy tool đúng trong Top-3 | 1          |
| Recall@3                             | **96.30%** |

================================================================================

Query 1: Xét tính đúng sai của mệnh đề: "17 là số nguyên tố" (xet_menh_de)

Tool 1: xet_menh_de
Tool 2: sai_so_tuong_doi
Tool 3: xet_bien_thien

Result Tool: ✅ ❌ ❌
================================================================================

Query 2: Viết mệnh đề phủ định của: "Mọi số tự nhiên đều chia hết cho 2" (phu_dinh_menh_de)

Tool 1: phu_dinh_menh_de
Tool 2: xet_menh_de
Tool 3: tong_hieu_vecto

Result Tool: ✅ ❌ ❌
================================================================================

Query 3: Cho A={1,2,3,4}, B={3,4,5,6}. Tìm A ∪ B (hop_tap_hop)

Tool 1: hop_tap_hop
Tool 2: giao_tap_hop
Tool 3: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌
================================================================================

Query 4: Cho A={1,2,3,4}, B={3,4,5,6}. Tìm A ∩ B (giao_tap_hop)

Tool 1: hop_tap_hop
Tool 2: giao_tap_hop
Tool 3: tich_vo_huong_vecto

Result Tool: ❌ ✅ ❌
================================================================================

Query 5: Cho A={1,2,3,4}, B={3,4}. Tìm A \ B (hieu_tap_hop)

Tool 1: hop_tap_hop
Tool 2: hieu_tap_hop
Tool 3: giao_tap_hop

Result Tool: ❌ ✅ ❌
================================================================================

Query 6: A={2,4} có là tập con của B={1,2,3,4,5} không? (kiem_tra_tap_con)

Tool 1: kiem_tra_tap_con
Tool 2: hop_tap_hop
Tool 3: giao_tap_hop

Result Tool: ✅ ❌ ❌
================================================================================

Query 7: Điểm M(2,1) có thỏa mãn bất phương trình 3x - y ≤ 6 không? (check_diem_bpt)

Tool 1: check_diem_bpt
Tool 2: kiem_tra_he_bpt
Tool 3: tim_gtln_gtnn_mien

Result Tool: ✅ ❌ ❌
================================================================================

Query 8: Tìm GTLN của F = 3x + 2y trên miền tam giác có đỉnh (0,0), (5,0), (0,4) (tim_gtln_gtnn_mien)

Tool 1: tim_gtln_gtnn_mien
Tool 2: tim_dinh_parabol
Tool 3: dien_tich_tam_giac

Result Tool: ✅ ❌ ❌
================================================================================

Query 9: Điểm (2,1) có thỏa mãn hệ {x+y≤4; x-y≥-1; x≥0} không? (kiem_tra_he_bpt)

Tool 1: kiem_tra_he_bpt
Tool 2: check_diem_bpt
Tool 3: tim_dinh_parabol

Result Tool: ✅ ❌ ❌
================================================================================

Query 10: Tìm tập xác định của hàm số y = 1/(x+3) (tim_txd_ham_so)

Tool 1: tim_txd_ham_so
Tool 2: tim_dinh_parabol
Tool 3: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌
================================================================================

Query 11: Xét tính đồng biến, nghịch biến của hàm số y = -3x + 5 trên R (xet_bien_thien)

Tool 1: xet_bien_thien
Tool 2: tim_txd_ham_so
Tool 3: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌
================================================================================

Query 12: Tìm tọa độ đỉnh của parabol y = 2x² - 8x + 6 (tim_dinh_parabol)

Tool 1: tim_dinh_parabol
Tool 2: tim_gtln_gtnn_mien
Tool 3: do_dai_vecto

Result Tool: ✅ ❌ ❌
================================================================================

Query 13: Xét dấu của tam thức f(x) = x² - 7x + 12 (xet_dau_tam_thuc)

Tool 1: xet_dau_tam_thuc
Tool 2: tim_txd_ham_so
Tool 3: xet_bien_thien

Result Tool: ✅ ❌ ❌
================================================================================

Query 14: Tính sin của góc 135° (gia_tri_luong_giac)

Tool 1: dinh_ly_sin
Tool 2: gia_tri_luong_giac
Tool 3: dinh_ly_cosin

Result Tool: ❌ ✅ ❌
================================================================================

Query 15: Tam giác ABC có b=8, c=5, góc A=60°. Tính cạnh a (dinh_ly_cosin - tinh_canh)

Tool 1: dinh_ly_cosin
Tool 2: dien_tich_tam_giac
Tool 3: dinh_ly_sin

Result Tool: ✅ ❌ ❌
================================================================================

Query 16: Tam giác ABC có a=10, b=7, c=6. Tính góc A (dinh_ly_cosin - tinh_goc)

Tool 1: dinh_ly_sin
Tool 2: dinh_ly_cosin
Tool 3: dien_tich_tam_giac

Result Tool: ❌ ✅ ❌
================================================================================

Query 17: Tam giác ABC có a=9, góc A=50°. Tính bán kính đường tròn ngoại tiếp (dinh_ly_sin - tinh_ban_kinh)

Tool 1: dinh_ly_sin
Tool 2: giai_tam_giac
Tool 3: dien_tich_tam_giac

Result Tool: ✅ ❌ ❌
================================================================================

Query 18: Giải tam giác ABC biết a=8, góc A=40°, góc B=70° (giai_tam_giac - biet_1_canh_2_goc)

Tool 1: giai_tam_giac
Tool 2: dinh_ly_cosin
Tool 3: dien_tich_tam_giac

Result Tool: ✅ ❌ ❌
================================================================================

Query 19: Tính diện tích tam giác có 3 cạnh a=7, b=8, c=9 (dien_tich_tam_giac - heron)

Tool 1: dien_tich_tam_giac
Tool 2: dinh_ly_cosin
Tool 3: giai_tam_giac

Result Tool: ✅ ❌ ❌
================================================================================

Query 20: Cho vectơ a=(2,5), b=(-1,3). Tính a - b (tong_hieu_vecto)

Tool 1: tong_hieu_vecto
Tool 2: goc_giua_hai_vecto
Tool 3: tich_vo_huong_vecto

Result Tool: ✅ ❌ ❌
================================================================================

Query 21: Cho vectơ a=(4,-2). Tính 5a (tich_so_voi_vecto)

Tool 1: do_dai_vecto
Tool 2: tich_vo_huong_vecto
Tool 3: goc_giua_hai_vecto

Result Tool: ❌ ❌ ❌
================================================================================

Query 22: Cho vectơ a=(3,1), b=(2,-4). Tính tích vô hướng a·b (tich_vo_huong_vecto)

Tool 1: tich_vo_huong_vecto
Tool 2: goc_giua_hai_vecto
Tool 3: tong_hieu_vecto

Result Tool: ✅ ❌ ❌
================================================================================

Query 23: Tính độ dài của vectơ a=(6,8) (do_dai_vecto)

Tool 1: do_dai_vecto
Tool 2: goc_giua_hai_vecto
Tool 3: tong_hieu_vecto

Result Tool: ✅ ❌ ❌
================================================================================

Query 24: Tính góc giữa hai vectơ a=(1,1) và b=(1,-1) (goc_giua_hai_vecto)

Tool 1: goc_giua_hai_vecto
Tool 2: tich_vo_huong_vecto
Tool 3: tong_hieu_vecto

Result Tool: ✅ ❌ ❌
================================================================================

Query 25: Đo được số gần đúng của √5 là 2.236, số đúng là 2.2360679. Tính sai số tuyệt đối (sai_so_tuong_doi - tuyet_doi)

Tool 1: sai_so_tuong_doi
Tool 2: xet_menh_de
Tool 3: tinh_phuong_sai_do_lech_chuan

Result Tool: ✅ ❌ ❌
================================================================================

Query 26: Tính số trung bình của mẫu số liệu: 5, 7, 9, 11, 13 (tinh_trung_binh)

Tool 1: tinh_trung_vi_mode
Tool 2: tinh_trung_binh
Tool 3: tinh_phuong_sai_do_lech_chuan

Result Tool: ❌ ✅ ❌
================================================================================

Query 27: Tính phương sai và độ lệch chuẩn của mẫu: 3, 5, 7, 9, 11 (tinh_phuong_sai_do_lech_chuan)

Tool 1: tinh_phuong_sai_do_lech_chuan
Tool 2: tinh_trung_vi_mode
Tool 3: do_dai_vecto

Result Tool: ✅ ❌ ❌
================================================================================
