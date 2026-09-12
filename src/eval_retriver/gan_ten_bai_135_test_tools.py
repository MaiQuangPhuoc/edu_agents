"""
File: gan_ten_bai.py
Input : 135 dòng query gốc (numbering theo 2 khối cũ: 1-65 và 1-70)
Output: 135 dòng, renumber lại 1->135, thêm "| tên bài" vào cuối mỗi dòng
"""

import re

# ── Raw data: 2 khối gốc, giữ nguyên số cũ trong từng khối ──────────────────
RAW_BLOCK_1 = """
1. (Dễ) "8 là số chẵn" là mệnh đề đúng hay sai? | xet_menh_de_tool
2. (Dễ) "Hà Nội là thủ đô của Việt Nam" là mệnh đề đúng hay sai? | xet_menh_de_tool
3. (Thông hiểu) Xét mệnh đề: "Nếu một số chia hết cho 6 thì số đó chia hết cho 3" đúng hay sai? | xet_menh_de_tool
4. (Thông hiểu) Khẳng định "Tổng hai số lẻ luôn là số chẵn" đúng hay sai? | xet_menh_de_tool
5. (Vận dụng) Một bạn học sinh nói: "25 là số chính phương và cũng là số nguyên tố". Khẳng định này đúng hay sai? | xet_menh_de_tool
6. (Dễ) Viết mệnh đề phủ định của "5 là số lẻ" | phu_dinh_menh_de_tool
7. (Dễ) Viết mệnh đề phủ định của "x > 10" | phu_dinh_menh_de_tool
8. (Thông hiểu) Viết mệnh đề phủ định của "Mọi số nguyên đều lớn hơn 0" | phu_dinh_menh_de_tool
9. (Thông hiểu) Viết mệnh đề phủ định của "Tồn tại số tự nhiên n sao cho n chia hết cho 7" | phu_dinh_menh_de_tool
10. (Vận dụng) Cho mệnh đề P: "Nếu tam giác ABC đều thì tam giác ABC có ba góc bằng nhau". Viết mệnh đề phủ định của P | phu_dinh_menh_de_tool
11. (Dễ) Cho A={1,2,3}, B={4,5}. Tìm A ∪ B | hop_tap_hop_tool
12. (Dễ) Cho A={2,4,6}, B={1,3,5}. Tìm A ∪ B | hop_tap_hop_tool
13. (Thông hiểu) Cho tập số tự nhiên chẵn nhỏ hơn 10 là A={0,2,4,6,8} và B={1,3,5,7,9}. Tìm A ∪ B | hop_tap_hop_tool
14. (Thông hiểu) Cho A là tập nghiệm của x²=4 (A={-2,2}) và B={0,2,4}. Tìm A ∪ B | hop_tap_hop_tool
15. (Vận dụng) Lớp 10A có tập học sinh giỏi Toán A={1,2,3} và tập học sinh giỏi Văn B={2,4}. Tìm tập học sinh giỏi Toán hoặc giỏi Văn (A ∪ B) | hop_tap_hop_tool
16. (Dễ) Cho A={1,2,3,4}, B={3,4,5}. Tìm A ∩ B | giao_tap_hop_tool
17. (Dễ) Cho A={2,4,6,8}, B={4,8,12}. Tìm A ∩ B | giao_tap_hop_tool
18. (Thông hiểu) Cho A là tập ước của 12 (A={1,2,3,4,6,12}) và B là tập ước của 18 (B={1,2,3,6,9,18}). Tìm A ∩ B | giao_tap_hop_tool
19. (Thông hiểu) Cho A={x | x là số nguyên tố nhỏ hơn 10} = {2,3,5,7} và B={2,4,6,8}. Tìm A ∩ B | giao_tap_hop_tool
20. (Vận dụng) Tập điểm giỏi môn Toán A={5,6,7,8,9,10}, tập điểm giỏi môn Văn B={7,8,9,10,11}. Tìm mức điểm đạt giỏi cả hai môn (A ∩ B) | giao_tap_hop_tool
21. (Dễ) Cho A={1,2,3,4,5}, B={3,4,5}. Tìm A \\ B | hieu_tap_hop_tool
22. (Dễ) Cho A={2,4,6,8}, B={2,4}. Tìm A \\ B | hieu_tap_hop_tool
23. (Thông hiểu) Cho A là tập ước của 20 (A={1,2,4,5,10,20}) và B={1,2,4}. Tìm A \\ B | hieu_tap_hop_tool
24. (Thông hiểu) Cho A={0,1,2,...,9} và B={0,2,4,6,8}. Tìm A \\ B | hieu_tap_hop_tool
25. (Vận dụng) Tập khách hàng mua áo A={1,2,3,4,5,6}, tập khách hàng mua quần B={4,5,6}. Tìm tập khách chỉ mua áo mà không mua quần (A \\ B) | hieu_tap_hop_tool
26. (Dễ) A={1,2} có là tập con của B={1,2,3,4} không? | kiem_tra_tap_con_tool
27. (Dễ) A={3,5} có là tập con của B={1,2,3,4} không? | kiem_tra_tap_con_tool
28. (Thông hiểu) Tập nghiệm của x²-4=0 là A={-2,2}. Tập B={-2,-1,0,1,2}. A có là tập con của B không? | kiem_tra_tap_con_tool
29. (Thông hiểu) A là tập ước của 6 (A={1,2,3,6}), B là tập ước của 12 (B={1,2,3,4,6,12}). A có là tập con của B không? | kiem_tra_tap_con_tool
30. (Vận dụng) Tập học sinh giỏi Toán A={1,2,3}, tập toàn bộ học sinh lớp B={1,2,...,30}. Kiểm tra A có là tập con của B không | kiem_tra_tap_con_tool
31. (Dễ) Điểm (1,1) có thỏa mãn x+y≤5 không? | check_diem_bpt_tool
32. (Dễ) Điểm (2,3) có thỏa mãn 2x+y≥4 không? | check_diem_bpt_tool
33. (Thông hiểu) Điểm M(0,0) có thỏa mãn bất phương trình 3x-2y<6 không? | check_diem_bpt_tool
34. (Thông hiểu) Điểm A(-1,2) có thỏa mãn x-y≥-3 không? | check_diem_bpt_tool
35. (Vận dụng) Một xưởng cần thỏa ràng buộc nguyên liệu 2x+3y≤120. Kiểm tra phương án sản xuất (x=30, y=20) có khả thi không | check_diem_bpt_tool
36. (Dễ) Tìm GTLN của F=x+y trên miền tam giác có đỉnh (0,0),(4,0),(0,4) | tim_gtln_gtnn_mien_tool
37. (Dễ) Tìm GTNN của F=2x+y trên miền tam giác có đỉnh (0,0),(3,0),(0,3) | tim_gtln_gtnn_mien_tool
38. (Thông hiểu) Tìm GTLN của F=3x+4y trên miền tứ giác có đỉnh (0,0),(5,0),(5,3),(0,5) | tim_gtln_gtnn_mien_tool
39. (Thông hiểu) Tìm GTNN của F=x+2y trên miền có đỉnh (1,1),(4,1),(4,4),(1,4) | tim_gtln_gtnn_mien_tool
40. (Vận dụng) Công ty sản xuất 2 sản phẩm với lợi nhuận F=5x+4y, miền ràng buộc có đỉnh (0,0),(20,0),(15,10),(0,15). Tìm phương án cho lợi nhuận GTLN | tim_gtln_gtnn_mien_tool
41. (Dễ) Điểm (1,1) có thỏa hệ {x+y≤4; x≥0; y≥0} không? | kiem_tra_he_bpt_tool
42. (Dễ) Điểm (2,2) có thỏa hệ {x+y≤3; x≥0} không? | kiem_tra_he_bpt_tool
43. (Thông hiểu) Điểm (0,0) có thỏa hệ {x-y≥-2; x+y≤5; x≥0; y≥0} không? | kiem_tra_he_bpt_tool
44. (Thông hiểu) Điểm (3,1) có thỏa hệ {2x+y≤8; x-y≥-1; y≥0} không? | kiem_tra_he_bpt_tool
45. (Vận dụng) Phương án sản xuất (x=10,y=5) có thỏa hệ ràng buộc {x+2y≤25; 3x+y≤40; x≥0; y≥0} không? | kiem_tra_he_bpt_tool
46. (Dễ) Tìm tập xác định của y=1/(x-3) | tim_txd_ham_so_tool
47. (Dễ) Tìm tập xác định của y=√(x+2) | tim_txd_ham_so_tool
48. (Thông hiểu) Tìm tập xác định của y=1/(x²-4) | tim_txd_ham_so_tool
49. (Thông hiểu) Tìm tập xác định của y=√(5-x) | tim_txd_ham_so_tool
50. (Vận dụng) Chi phí sản xuất mô tả bởi y=1000/(x-10) với x là số sản phẩm. Tìm tập xác định để biết giá trị x hợp lệ | tim_txd_ham_so_tool
51. (Dễ) Xét tính đồng biến, nghịch biến của y=3x+1 trên R | xet_bien_thien_tool
52. (Dễ) Xét tính đồng biến, nghịch biến của y=-2x+5 trên R | xet_bien_thien_tool
53. (Thông hiểu) Xét sự biến thiên của hàm số y=x-7 trên khoảng (-5,5) | xet_bien_thien_tool
54. (Thông hiểu) Xét tính đồng biến, nghịch biến của y=(1/2)x+3 trên R | xet_bien_thien_tool
55. (Vận dụng) Doanh thu cửa hàng theo tháng là y=200x+1000 (x là tháng). Xét hàm số đồng biến hay nghịch biến trên (1,12) để biết xu hướng doanh thu | xet_bien_thien_tool
56. (Dễ) Tìm đỉnh của parabol y=x²-4x+3 | tim_dinh_parabol_tool
57. (Dễ) Tìm đỉnh của parabol y=x²+2x-3 | tim_dinh_parabol_tool
58. (Thông hiểu) Tìm đỉnh và trục đối xứng của y=2x²-8x+5 | tim_dinh_parabol_tool
59. (Thông hiểu) Tìm đỉnh của parabol y=-x²+6x-8 | tim_dinh_parabol_tool
60. (Vận dụng) Quỹ đạo vật ném lên mô tả bởi y=-5x²+20x (x là thời gian, y là độ cao). Tìm đỉnh parabol để biết thời điểm và độ cao lớn nhất | tim_dinh_parabol_tool
61. (Dễ) Xét dấu tam thức f(x)=x²-5x+6 | xet_dau_tam_thuc_tool
62. (Dễ) Xét dấu tam thức f(x)=x²-9 | xet_dau_tam_thuc_tool
63. (Thông hiểu) Xét dấu tam thức f(x)=2x²-3x+1 | xet_dau_tam_thuc_tool
64. (Thông hiểu) Xét dấu tam thức f(x)=-x²+4x-3 | xet_dau_tam_thuc_tool
65. (Vận dụng) Lợi nhuận công ty theo sản lượng x là f(x)=-x²+10x-16. Xét dấu f(x) để biết khoảng sản lượng nào công ty có lãi | xet_dau_tam_thuc_tool
"""

RAW_BLOCK_2 = """
1. (Dễ) Tính sin của góc 30° | gia_tri_luong_giac_tool
2. (Dễ) Tính cos của góc 60° | gia_tri_luong_giac_tool
3. (Thông hiểu) Tính tan của góc 45° | gia_tri_luong_giac_tool
4. (Thông hiểu) Tính giá trị cos của góc 150° | gia_tri_luong_giac_tool
5. (Vận dụng) Một mái nhà nghiêng tạo với phương ngang một góc 120°. Tính cos của góc này để phục vụ tính độ dốc mái | gia_tri_luong_giac_tool
6. (Dễ) Tam giác ABC có b=4, c=6, góc A=60°. Tính cạnh a | dinh_ly_cosin_tool
7. (Dễ) Tam giác ABC có b=5, c=5, góc A=90°. Tính cạnh a | dinh_ly_cosin_tool
8. (Thông hiểu) Tam giác ABC có a=7, b=5, c=6. Tính góc A | dinh_ly_cosin_tool
9. (Thông hiểu) Tam giác ABC có b=10, c=12, góc A=45°. Tính cạnh a | dinh_ly_cosin_tool
10. (Vận dụng) Hai con tàu xuất phát từ cùng 1 điểm, tàu 1 đi 5km, tàu 2 đi 8km, góc giữa 2 hướng đi là 70°. Tính khoảng cách giữa hai tàu | dinh_ly_cosin_tool
11. (Dễ) Tam giác ABC có a=8, góc A=30°. Tính bán kính đường tròn ngoại tiếp R | dinh_ly_sin_tool
12. (Dễ) Tam giác ABC có a=10, góc A=90°. Tính bán kính đường tròn ngoại tiếp R | dinh_ly_sin_tool
13. (Thông hiểu) Tam giác ABC có a=6, góc A=40°, góc B=60°. Tính cạnh b | dinh_ly_sin_tool
14. (Thông hiểu) Tam giác ABC có a=9, góc A=50°, góc B=70°. Tính cạnh b | dinh_ly_sin_tool
15. (Vận dụng) Một khu đất tam giác có cạnh a=15m nhìn dưới góc A=35°. Tính bán kính đường tròn ngoại tiếp khu đất | dinh_ly_sin_tool
16. (Dễ) Giải tam giác ABC biết a=5, góc A=30°, góc B=60° | giai_tam_giac_tool
17. (Dễ) Giải tam giác ABC biết b=6, c=8, góc A=90° | giai_tam_giac_tool
18. (Thông hiểu) Giải tam giác ABC biết a=10, góc A=45°, góc B=75° | giai_tam_giac_tool
19. (Thông hiểu) Giải tam giác ABC biết b=7, c=9, góc A=60° | giai_tam_giac_tool
20. (Vận dụng) Đo được 1 cạnh khu đất tam giác là 20m và hai góc kề cạnh đó là 50° và 65°. Giải tam giác để tính các cạnh và góc còn lại | giai_tam_giac_tool
21. (Dễ) Tính diện tích tam giác có 3 cạnh a=3, b=4, c=5 | dien_tich_tam_giac_tool
22. (Dễ) Tính diện tích tam giác biết a=6, b=8, góc C=90° | dien_tich_tam_giac_tool
23. (Thông hiểu) Tính diện tích tam giác có 3 cạnh a=5, b=6, c=7 | dien_tich_tam_giac_tool
24. (Thông hiểu) Tính diện tích tam giác biết a=7, b=9, góc C=60° | dien_tich_tam_giac_tool
25. (Vận dụng) Một khu vườn hình tam giác có 2 cạnh dài 12m và 15m, góc xen giữa 50°. Tính diện tích khu vườn | dien_tich_tam_giac_tool
26. (Dễ) Cho a=(1,2), b=(3,4). Tính a+b | tong_hieu_vecto_tool
27. (Dễ) Cho a=(5,1), b=(2,3). Tính a-b | tong_hieu_vecto_tool
28. (Thông hiểu) Cho a=(-2,3), b=(4,-1). Tính a+b | tong_hieu_vecto_tool
29. (Thông hiểu) Cho a=(0,5), b=(5,0). Tính a-b | tong_hieu_vecto_tool
30. (Vận dụng) Vật chịu 2 lực F1=(3,4) và F2=(1,-2) (Newton). Tính hợp lực F=F1+F2 | tong_hieu_vecto_tool
31. (Dễ) Cho a=(2,3). Tính 4a | tich_so_voi_vecto_tool
32. (Dễ) Cho a=(1,-1). Tính 3a | tich_so_voi_vecto_tool
33. (Thông hiểu) Cho a=(-2,5). Tính 2a | tich_so_voi_vecto_tool
34. (Thông hiểu) Cho a=(6,-4). Tính -3a | tich_so_voi_vecto_tool
35. (Vận dụng) Vectơ vận tốc ban đầu v=(2,3) m/s, tăng gấp 3 lần theo cùng hướng. Tính vectơ vận tốc mới 3v | tich_so_voi_vecto_tool
36. (Dễ) Cho a=(1,2), b=(3,4). Tính a·b | tich_vo_huong_vecto_tool
37. (Dễ) Cho a=(2,0), b=(0,3). Tính a·b | tich_vo_huong_vecto_tool
38. (Thông hiểu) Cho a=(-1,3), b=(2,4). Tính a·b | tich_vo_huong_vecto_tool
39. (Thông hiểu) Cho a=(5,-2), b=(-1,3). Tính a·b | tich_vo_huong_vecto_tool
40. (Vận dụng) Hai lực F1=(3,4) và F2=(4,-3) (Newton) tác dụng lên vật. Tính tích vô hướng F1·F2 để kiểm tra 2 lực có vuông góc không | tich_vo_huong_vecto_tool
41. (Dễ) Tính độ dài vectơ a=(3,4) | do_dai_vecto_tool
42. (Dễ) Tính độ dài vectơ a=(6,8) | do_dai_vecto_tool
43. (Thông hiểu) Tính độ dài vectơ a=(-5,12) | do_dai_vecto_tool
44. (Thông hiểu) Tính độ dài vectơ a=(1,1) | do_dai_vecto_tool
45. (Vận dụng) Người đi từ A đến B theo vectơ dịch chuyển d=(30,40) mét. Tính quãng đường thẳng từ A đến B | do_dai_vecto_tool
46. (Dễ) Tính góc giữa a=(1,0) và b=(0,1) | goc_giua_hai_vecto_tool
47. (Dễ) Tính góc giữa a=(1,1) và b=(1,0) | goc_giua_hai_vecto_tool
48. (Thông hiểu) Tính góc giữa a=(2,0) và b=(-1,1) | goc_giua_hai_vecto_tool
49. (Thông hiểu) Tính góc giữa a=(3,4) và b=(4,3) | goc_giua_hai_vecto_tool
50. (Vận dụng) Hai lực F1=(5,0) và F2=(3,3) tác dụng lên vật. Tính góc giữa hai lực để phân tích hướng hợp lực | goc_giua_hai_vecto_tool
51. (Dễ) Số gần đúng a=3.1 của số đúng 3.14. Tính sai số tuyệt đối | sai_so_tuong_doi_tool
52. (Dễ) Số gần đúng a=1.4 của số đúng √2≈1.41421. Tính sai số tuyệt đối | sai_so_tuong_doi_tool
53. (Thông hiểu) Số gần đúng a=2.24 của √5≈2.2360679. Tính sai số tương đối | sai_so_tuong_doi_tool
54. (Thông hiểu) Đo chiều dài được số gần đúng 15.2, số đúng 15.25. Tính sai số tương đối | sai_so_tuong_doi_tool
55. (Vận dụng) Đo diện tích mảnh đất, kết quả gần đúng 250m² trong khi số đúng là 253.6m². Tính sai số tương đối để đánh giá độ chính xác | sai_so_tuong_doi_tool
56. (Dễ) Tính số trung bình của mẫu: 2, 4, 6, 8, 10 | tinh_trung_binh_tool
57. (Dễ) Tính số trung bình của mẫu: 1, 2, 3, 4, 5 | tinh_trung_binh_tool
58. (Thông hiểu) Tính số trung bình của mẫu: 10, 15, 20, 25, 30, 35 | tinh_trung_binh_tool
59. (Thông hiểu) Tính số trung bình của mẫu: 3, 3, 5, 7, 9, 9 | tinh_trung_binh_tool
60. (Vận dụng) Điểm kiểm tra Toán của 6 bạn trong tổ: 7, 8, 6, 9, 7, 8. Tính điểm trung bình của tổ | tinh_trung_binh_tool
61. (Dễ) Tìm trung vị của mẫu: 1, 3, 5, 7, 9 | tinh_trung_vi_mode_tool
62. (Dễ) Tìm mốt của mẫu: 2, 2, 3, 4, 4, 4 | tinh_trung_vi_mode_tool
63. (Thông hiểu) Tìm trung vị của mẫu: 2, 4, 6, 8, 10, 12 | tinh_trung_vi_mode_tool
64. (Thông hiểu) Tìm mốt của mẫu: 5, 6, 6, 7, 8, 8, 8, 9 | tinh_trung_vi_mode_tool
65. (Vận dụng) Số khách mỗi ngày trong tuần của quán ăn: 20, 25, 22, 30, 25, 28, 25. Tìm trung vị và mốt để đánh giá lượng khách phổ biến | tinh_trung_vi_mode_tool
66. (Dễ) Tính phương sai và độ lệch chuẩn của mẫu: 2, 4, 6, 8, 10 | tinh_phuong_sai_do_lech_chuan_tool
67. (Dễ) Tính phương sai và độ lệch chuẩn của mẫu: 1, 2, 3, 4, 5 | tinh_phuong_sai_do_lech_chuan_tool
68. (Thông hiểu) Tính phương sai và độ lệch chuẩn của mẫu: 10, 12, 14, 16, 18 | tinh_phuong_sai_do_lech_chuan_tool
69. (Thông hiểu) Tính phương sai và độ lệch chuẩn của mẫu: 5, 7, 7, 9, 11, 13 | tinh_phuong_sai_do_lech_chuan_tool
70. (Vận dụng) Điểm thi của 5 học sinh: 6, 7, 8, 8, 9. Tính phương sai và độ lệch chuẩn để đánh giá mức độ đồng đều điểm số | tinh_phuong_sai_do_lech_chuan_tool
"""

# ── Mapping số thứ tự (1-135) -> tên bài SGK ────────────────────────────────
BAI_MAPPING = {}
def _fill(rng, ten_bai):
    for i in rng:
        BAI_MAPPING[i] = ten_bai

_fill(range(1, 11), "Bài 1. Mệnh đề")
_fill(range(11, 26), "Bài 3. Các phép toán trên tập hợp")
_fill(range(26, 31), "Bài 2. Tập hợp")
_fill(range(31, 36), "Bài 1. Bất phương trình bậc nhất hai ẩn")
_fill(range(36, 46), "Bài 2. Hệ bất phương trình bậc nhất hai ẩn")
_fill(range(46, 56), "Bài 1. Hàm số và đồ thị")
_fill(range(56, 66), "Bài 2. Hàm số bậc hai")
_fill(range(66, 71), "Bài 1. Giá trị lượng giác của một góc từ 0° đến 180°")
_fill(range(71, 81), "Bài 2. Định lí cosin và định lí sin")
_fill(range(81, 91), "Bài 3. Giải tam giác và ứng dụng thực tế")
_fill(range(91, 96), "Bài 2. Tổng và hiệu của hai vectơ")
_fill(range(96, 101), "Bài 3. Tích của một số với một vectơ")
_fill(range(101, 106), "Bài 4. Tích vô hướng của hai vectơ")
_fill(range(106, 111), "Bài 1. Khái niệm vectơ")
_fill(range(111, 116), "Bài 4. Tích vô hướng của hai vectơ")
_fill(range(116, 121), "Bài 1. Số gần đúng và sai số")
_fill(range(121, 131), "Bài 3. Các số đặc trưng đo xu thế trung tâm của mẫu số liệu")
_fill(range(131, 136), "Bài 4. Các số đặc trưng đo mức độ phân tán của mẫu số liệu")

# ── Parse + renumber ─────────────────────────────────────────────────────
LINE_RE = re.compile(r"^\d+\.\s*(.*)$")

def parse_block(raw: str) -> list[str]:
    lines = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        m = LINE_RE.match(line)
        if m:
            lines.append(m.group(1))
    return lines

def main():
    all_lines = parse_block(RAW_BLOCK_1) + parse_block(RAW_BLOCK_2)
    assert len(all_lines) == 135, f"Expect 135 dòng, got {len(all_lines)}"

    out_lines = []
    for idx, content in enumerate(all_lines, start=1):
        ten_bai = BAI_MAPPING[idx]
        out_lines.append(f"{idx}. {content} | {ten_bai}")

    output_path = "135_queries_with_bai.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

    print(f"Đã ghi {len(out_lines)} dòng vào {output_path}")


if __name__ == "__main__":
    main()




# BAI_MAPPING = {
#     # 1-5: xet_menh_de_tool
#     1: "Bài 1. Mệnh đề", 2: "Bài 1. Mệnh đề", 3: "Bài 1. Mệnh đề",
#     4: "Bài 1. Mệnh đề", 5: "Bài 1. Mệnh đề",
#     # 6-10: phu_dinh_menh_de_tool
#     6: "Bài 1. Mệnh đề", 7: "Bài 1. Mệnh đề", 8: "Bài 1. Mệnh đề",
#     9: "Bài 1. Mệnh đề", 10: "Bài 1. Mệnh đề",
#     # 11-15: hop_tap_hop_tool
#     11: "Bài 3. Các phép toán trên tập hợp", 12: "Bài 3. Các phép toán trên tập hợp",
#     13: "Bài 3. Các phép toán trên tập hợp", 14: "Bài 3. Các phép toán trên tập hợp",
#     15: "Bài 3. Các phép toán trên tập hợp",
#     # 16-20: giao_tap_hop_tool
#     16: "Bài 3. Các phép toán trên tập hợp", 17: "Bài 3. Các phép toán trên tập hợp",
#     18: "Bài 3. Các phép toán trên tập hợp", 19: "Bài 3. Các phép toán trên tập hợp",
#     20: "Bài 3. Các phép toán trên tập hợp",
#     # 21-25: hieu_tap_hop_tool
#     21: "Bài 3. Các phép toán trên tập hợp", 22: "Bài 3. Các phép toán trên tập hợp",
#     23: "Bài 3. Các phép toán trên tập hợp", 24: "Bài 3. Các phép toán trên tập hợp",
#     25: "Bài 3. Các phép toán trên tập hợp",
#     # 26-30: kiem_tra_tap_con_tool
#     26: "Bài 2. Tập hợp", 27: "Bài 2. Tập hợp", 28: "Bài 2. Tập hợp",
#     29: "Bài 2. Tập hợp", 30: "Bài 2. Tập hợp",
#     # 31-35: check_diem_bpt_tool
#     31: "Bài 1. Bất phương trình bậc nhất hai ẩn", 32: "Bài 1. Bất phương trình bậc nhất hai ẩn",
#     33: "Bài 1. Bất phương trình bậc nhất hai ẩn", 34: "Bài 1. Bất phương trình bậc nhất hai ẩn",
#     35: "Bài 1. Bất phương trình bậc nhất hai ẩn",
#     # 36-40: tim_gtln_gtnn_mien_tool
#     36: "Bài 2. Hệ bất phương trình bậc nhất hai ẩn", 37: "Bài 2. Hệ bất phương trình bậc nhất hai ẩn",
#     38: "Bài 2. Hệ bất phương trình bậc nhất hai ẩn", 39: "Bài 2. Hệ bất phương trình bậc nhất hai ẩn",
#     40: "Bài 2. Hệ bất phương trình bậc nhất hai ẩn",
#     # 41-45: kiem_tra_he_bpt_tool
#     41: "Bài 2. Hệ bất phương trình bậc nhất hai ẩn", 42: "Bài 2. Hệ bất phương trình bậc nhất hai ẩn",
#     43: "Bài 2. Hệ bất phương trình bậc nhất hai ẩn", 44: "Bài 2. Hệ bất phương trình bậc nhất hai ẩn",
#     45: "Bài 2. Hệ bất phương trình bậc nhất hai ẩn",
#     # 46-50: tim_txd_ham_so_tool
#     46: "Bài 1. Hàm số và đồ thị", 47: "Bài 1. Hàm số và đồ thị",
#     48: "Bài 1. Hàm số và đồ thị", 49: "Bài 1. Hàm số và đồ thị",
#     50: "Bài 1. Hàm số và đồ thị",
#     # 51-55: xet_bien_thien_tool
#     51: "Bài 1. Hàm số và đồ thị", 52: "Bài 1. Hàm số và đồ thị",
#     53: "Bài 1. Hàm số và đồ thị", 54: "Bài 1. Hàm số và đồ thị",
#     55: "Bài 1. Hàm số và đồ thị",
#     # 56-60: tim_dinh_parabol_tool
#     56: "Bài 2. Hàm số bậc hai", 57: "Bài 2. Hàm số bậc hai",
#     58: "Bài 2. Hàm số bậc hai", 59: "Bài 2. Hàm số bậc hai",
#     60: "Bài 2. Hàm số bậc hai",
#     # 61-65: xet_dau_tam_thuc_tool
#     61: "Bài 2. Hàm số bậc hai", 62: "Bài 2. Hàm số bậc hai",
#     63: "Bài 2. Hàm số bậc hai", 64: "Bài 2. Hàm số bậc hai",
#     65: "Bài 2. Hàm số bậc hai",
#     # 66-70: gia_tri_luong_giac_tool
#     66: "Bài 1. Giá trị lượng giác của một góc từ 0° đến 180°",
#     67: "Bài 1. Giá trị lượng giác của một góc từ 0° đến 180°",
#     68: "Bài 1. Giá trị lượng giác của một góc từ 0° đến 180°",
#     69: "Bài 1. Giá trị lượng giác của một góc từ 0° đến 180°",
#     70: "Bài 1. Giá trị lượng giác của một góc từ 0° đến 180°",
#     # 71-75: dinh_ly_cosin_tool
#     71: "Bài 2. Định lí cosin và định lí sin", 72: "Bài 2. Định lí cosin và định lí sin",
#     73: "Bài 2. Định lí cosin và định lí sin", 74: "Bài 2. Định lí cosin và định lí sin",
#     75: "Bài 2. Định lí cosin và định lí sin",
#     # 76-80: dinh_ly_sin_tool
#     76: "Bài 2. Định lí cosin và định lí sin", 77: "Bài 2. Định lí cosin và định lí sin",
#     78: "Bài 2. Định lí cosin và định lí sin", 79: "Bài 2. Định lí cosin và định lí sin",
#     80: "Bài 2. Định lí cosin và định lí sin",
#     # 81-85: giai_tam_giac_tool
#     81: "Bài 3. Giải tam giác và ứng dụng thực tế", 82: "Bài 3. Giải tam giác và ứng dụng thực tế",
#     83: "Bài 3. Giải tam giác và ứng dụng thực tế", 84: "Bài 3. Giải tam giác và ứng dụng thực tế",
#     85: "Bài 3. Giải tam giác và ứng dụng thực tế",
#     # 86-90: dien_tich_tam_giac_tool
#     86: "Bài 3. Giải tam giác và ứng dụng thực tế", 87: "Bài 3. Giải tam giác và ứng dụng thực tế",
#     88: "Bài 3. Giải tam giác và ứng dụng thực tế", 89: "Bài 3. Giải tam giác và ứng dụng thực tế",
#     90: "Bài 3. Giải tam giác và ứng dụng thực tế",
#     # 91-95: tong_hieu_vecto_tool
#     91: "Bài 2. Tổng và hiệu của hai vectơ", 92: "Bài 2. Tổng và hiệu của hai vectơ",
#     93: "Bài 2. Tổng và hiệu của hai vectơ", 94: "Bài 2. Tổng và hiệu của hai vectơ",
#     95: "Bài 2. Tổng và hiệu của hai vectơ",
#     # 96-100: tich_so_voi_vecto_tool
#     96: "Bài 3. Tích của một số với một vectơ", 97: "Bài 3. Tích của một số với một vectơ",
#     98: "Bài 3. Tích của một số với một vectơ", 99: "Bài 3. Tích của một số với một vectơ",
#     100: "Bài 3. Tích của một số với một vectơ",
#     # 101-105: tich_vo_huong_vecto_tool
#     101: "Bài 4. Tích vô hướng của hai vectơ", 102: "Bài 4. Tích vô hướng của hai vectơ",
#     103: "Bài 4. Tích vô hướng của hai vectơ", 104: "Bài 4. Tích vô hướng của hai vectơ",
#     105: "Bài 4. Tích vô hướng của hai vectơ",
#     # 106-110: do_dai_vecto_tool
#     106: "Bài 1. Khái niệm vectơ", 107: "Bài 1. Khái niệm vectơ",
#     108: "Bài 1. Khái niệm vectơ", 109: "Bài 1. Khái niệm vectơ",
#     110: "Bài 1. Khái niệm vectơ",
#     # 111-115: goc_giua_hai_vecto_tool
#     111: "Bài 4. Tích vô hướng của hai vectơ", 112: "Bài 4. Tích vô hướng của hai vectơ",
#     113: "Bài 4. Tích vô hướng của hai vectơ", 114: "Bài 4. Tích vô hướng của hai vectơ",
#     115: "Bài 4. Tích vô hướng của hai vectơ",
#     # 116-120: sai_so_tuong_doi_tool
#     116: "Bài 1. Số gần đúng và sai số", 117: "Bài 1. Số gần đúng và sai số",
#     118: "Bài 1. Số gần đúng và sai số", 119: "Bài 1. Số gần đúng và sai số",
#     120: "Bài 1. Số gần đúng và sai số",
#     # 121-125: tinh_trung_binh_tool
#     121: "Bài 3. Các số đặc trưng đo xu thế trung tâm của mẫu số liệu",
#     122: "Bài 3. Các số đặc trưng đo xu thế trung tâm của mẫu số liệu",
#     123: "Bài 3. Các số đặc trưng đo xu thế trung tâm của mẫu số liệu",
#     124: "Bài 3. Các số đặc trưng đo xu thế trung tâm của mẫu số liệu",
#     125: "Bài 3. Các số đặc trưng đo xu thế trung tâm của mẫu số liệu",
#     # 126-130: tinh_trung_vi_mode_tool
#     126: "Bài 3. Các số đặc trưng đo xu thế trung tâm của mẫu số liệu",
#     127: "Bài 3. Các số đặc trưng đo xu thế trung tâm của mẫu số liệu",
#     128: "Bài 3. Các số đặc trưng đo xu thế trung tâm của mẫu số liệu",
#     129: "Bài 3. Các số đặc trưng đo xu thế trung tâm của mẫu số liệu",
#     130: "Bài 3. Các số đặc trưng đo xu thế trung tâm của mẫu số liệu",
#     # 131-135: tinh_phuong_sai_do_lech_chuan_tool
#     131: "Bài 4. Các số đặc trưng đo mức độ phân tán của mẫu số liệu",
#     132: "Bài 4. Các số đặc trưng đo mức độ phân tán của mẫu số liệu",
#     133: "Bài 4. Các số đặc trưng đo mức độ phân tán của mẫu số liệu",
#     134: "Bài 4. Các số đặc trưng đo mức độ phân tán của mẫu số liệu",
#     135: "Bài 4. Các số đặc trưng đo mức độ phân tán của mẫu số liệu",
# }