---
schema_version: "1.0"
document_id: "CTST_T10_CH_II"
document_type: "lesson_plan"
subject: "Toán 10"
grade: 10
textbook_series: "chan_troi_sang_tao"
volume: 1
curriculum_version: "GDPT_2018"
chapter_id: "II"
chapter_title: "Bất phương trình và hệ bất phương trình bậc nhất hai ẩn"
content_sections: ["summary", "detail"]
verification_status: "review_required"
source_ids: ["S01", "S02", "S03", "S04"]
content_origin: "eduagent_original_draft"
official_periods: null
suggested_sessions: 5
minutes_per_session: 45
---

# CHƯƠNG II. BẤT PHƯƠNG TRÌNH VÀ HỆ BẤT PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN

> **Phạm vi:** Toán 10 – Chân trời sáng tạo, tập 1. Tài liệu do EDUAGENT biên soạn để làm học liệu hỗ trợ tự học, không phải giáo án chính thức hoặc bản chép từ SGK. Tên hai bài và bài tập cuối chương được đối chiếu với mục lục [S01, S02]. Các kiến thức chuyên môn được đối chiếu từ tài liệu tham khảo [S03, S04]; đề xuất thời gian do EDUAGENT xây dựng, **không phải phân phối tiết chính thức**. Chưa qua bước duyệt độc lập bởi giáo viên.

## PHẦN A. TÓM TẮT CHƯƠNG
<!-- content_type: summary -->

### A.1. Mục tiêu chương

Học sinh hướng tới khả năng:

- Nhận biết được bất phương trình bậc nhất hai ẩn, hiểu nghiệm là một cặp số thỏa mãn bất phương trình.
- Biểu diễn chính xác miền nghiệm trên mặt phẳng tọa độ, xác định đường biên và xét việc đường biên có được lấy hay không.
- Nhận biết và biểu diễn được **miền nghiệm chung** của hệ bất phương trình bậc nhất hai ẩn.
- Thiết lập được các ràng buộc tuyến tính từ một tình huống thực tiễn; vận dụng miền nghiệm để tìm giá trị lớn nhất, nhỏ nhất của biểu thức tuyến tính trên **miền đa giác bị chặn phù hợp**.
- Trình bày và kiểm tra được lập luận: thử điểm, tô miền, giao các miền nghiệm và kiểm chứng kết quả tại các đỉnh.

**Căn cứ phạm vi kiến thức:** [S02, S03, S04]. Cách diễn đạt mục tiêu và lựa chọn hoạt động là bản biên soạn mới.

### A.2. Danh sách bài học

| Mã bài nội bộ | Tên bài theo mục lục Chân trời sáng tạo | Trọng tâm | Buổi tự học đề xuất |
|---|---|---|---:|
| II.1 | Bài 1. Bất phương trình bậc nhất hai ẩn | Khái niệm, nghiệm, biểu diễn miền nghiệm | 2 |
| II.2 | Bài 2. Hệ bất phương trình bậc nhất hai ẩn | Miền nghiệm của hệ, bài toán tối ưu tuyến tính cơ bản | 2 |
| II.R | Bài tập cuối chương II | Ôn tập, đánh giá, sửa lỗi | 1 |

Các mã `II.1`, `II.2`, `II.R` là định danh **nội bộ của EDUAGENT**. Tổng **5 buổi x 45 phút** là gợi ý tự học để Agent điều chỉnh theo năng lực; `official_periods = null` vì chưa xác minh được phân phối tiết chính thức phù hợp.

### A.3. Kiến thức trọng tâm

- **Bất phương trình bậc nhất hai ẩn:** dạng $ax+by\leq c$, $ax+by<c$, $ax+by\geq c$, $ax+by>c$ với $a,b,c\in\mathbb R$, trong đó $a,b$ không đồng thời bằng $0$; một cặp $(x_0,y_0)$ là nghiệm khi thay vào được bất đẳng thức đúng.
- **Miền nghiệm hình học:** đường thẳng $ax+by=c$ chia mặt phẳng thành hai nửa mặt phẳng; lấy một điểm thử không nằm trên đường thẳng để xác định nửa mặt phẳng nghiệm. Với dấu $\leq$, $\geq$ đường biên được lấy; với dấu $<$, $>$ đường biên không được lấy.
- **Hệ bất phương trình:** nghiệm phải thỏa mãn *tất cả* bất phương trình; miền nghiệm là giao các miền nghiệm thành phần, có thể rỗng hoặc không bị chặn.
- **Ứng dụng:** đặt ẩn theo đại lượng thực tế, xác lập điều kiện không âm nếu đại lượng yêu cầu, hệ ràng buộc tuyến tính và hàm mục tiêu $F=ax+by$. Trên miền đa giác **khép kín, bị chặn và không rỗng**, giá trị lớn nhất/nhỏ nhất của hàm tuyến tính đạt được tại ít nhất một đỉnh (nếu hàm hằng, mọi điểm đều cho cùng giá trị).

### A.4. Kiến thức tiên quyết và quan hệ giữa các bài

- **Cần trước chương:** đọc hiểu trục tọa độ $Oxy$, cặp số có thứ tự, phương trình đường thẳng dạng $ax+by=c$, quy tắc so sánh số thực và ý nghĩa của giao tập hợp.
- **II.1 → II.2:** biểu diễn một nửa mặt phẳng nghiệm trước, rồi lấy giao để được miền nghiệm của hệ.
- **II.2 → ứng dụng:** từ hình dạng miền nghiệm chung, nhận diện đỉnh và so sánh giá trị hàm mục tiêu.
- **Lỗi sai cần phòng tránh:** tô nhầm phía đường thẳng; kiểm tra điểm thử nằm trên đường biên; lẫn lộn giao với hợp; bỏ sót điều kiện $x,y\geq0$ khi mô hình thực tế bắt buộc; áp dụng quy tắc xét đỉnh ngoài giả thiết miền đa giác bị chặn.

### A.5. Phân bổ thời gian đề xuất

- **II.1:** 2 buổi x 45 phút, ưu tiên xác định nghiệm, vẽ đường biên và biểu diễn miền nghiệm.
- **II.2:** 2 buổi x 45 phút, ưu tiên giao miền nghiệm, thiết lập hệ ràng buộc và tối ưu tuyến tính cơ bản.
- **II.R:** 1 buổi x 45 phút, tổng hợp và xác định lỗi sai.
- **Tổng:** 5 buổi (225 phút). Đây là **kế hoạch tự học mẫu**, không phải tiết phân phối chính thức. Learning Path Agent có thể tăng số buổi khi học sinh yếu kỹ năng vẽ đồ thị hoặc đọc đề thực tế.

## PHẦN B. GIÁO ÁN CHI TIẾT
<!-- content_type: detail -->

### BÀI 1. BẤT PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN
<!-- lesson_id: II.1 -->

#### 1. Thông tin bài học

- **Tên SGK:** Bài 1. Bất phương trình bậc nhất hai ẩn.
- **Chương:** II – Bất phương trình và hệ bất phương trình bậc nhất hai ẩn.
- **Số tiết theo KHBD chính thức:** chưa xác minh (`official_periods: null`).
- **Số buổi tự học đề xuất:** 2 (`suggested_sessions: 2`).
- **Thời lượng đề xuất mỗi buổi:** 45 phút (`minutes_per_session: 45`).
- **Kiến thức cần trước:** cặp số, hệ tọa độ Descartes, đường thẳng và bất đẳng thức số.

#### 2. Mục tiêu học tập

- Nhận dạng đúng bất phương trình bậc nhất hai ẩn; phân biệt với phương trình hai ẩn và bất phương trình bậc cao hơn.
- Kiểm tra đúng một cặp số có phải nghiệm hay không bằng phép thay trực tiếp.
- Vẽ được đường biên $ax+by=c$ và chỉ ra nửa mặt phẳng nghiệm của một bất phương trình.
- Sử dụng chính xác đường biên liền/nét đứt theo dấu bất phương trình và giải thích bằng điểm thử.

#### 3. Kiến thức cần nắm

**Khái niệm.** Với $a,b,c$ là các số thực, $a,b$ không đồng thời bằng $0$, bất phương trình bậc nhất hai ẩn có một trong các dạng

$$
ax+by<c,\quad ax+by\leq c,\quad ax+by>c,\quad ax+by\geq c.
$$

Trong đó, $(x_0,y_0)$ là **nghiệm** khi thay $x=x_0$, $y=y_0$ vào bất phương trình thì thu được mệnh đề đúng. Mỗi nghiệm được biểu diễn bằng một điểm trên mặt phẳng tọa độ.

**Cách biểu diễn miền nghiệm:**

1. Vẽ đường thẳng $d: ax+by=c$ (có thể xác định bằng hai điểm phân biệt thuộc đường thẳng).
2. Chọn điểm thử $M(x_0,y_0)$ **không nằm trên** $d$; thường dùng $O(0,0)$ nếu $O\notin d$.
3. Thay tọa độ $M$ vào bất phương trình. Nếu đúng, chọn nửa mặt phẳng chứa $M$; nếu sai, chọn nửa mặt phẳng đối diện.
4. Phân biệt biên: dấu $\leq$ hoặc $\geq$ **lấy cả** $d$; dấu $<$ hoặc $>$ **không lấy** $d$.

**Cần phân biệt:** nghiệm là **cặp số**; miền nghiệm là **tập hợp các điểm** tương ứng với toàn bộ các cặp nghiệm.

#### 4. Kiến thức cần hiểu

- Đường thẳng $ax+by=c$ là nơi hai vế bằng nhau; khi đi qua đường thẳng, dấu của biểu thức $ax+by-c$ đổi giữa hai nửa mặt phẳng. Vì vậy một điểm thử ngoài đường biên đủ để xác định nửa mặt phẳng thỏa mãn.
- Nghiệm của một bất phương trình bậc nhất hai ẩn thường là vô số cặp số, không phải một đáp án duy nhất.
- Nếu chọn điểm thử thuộc chính đường biên thì phép kiểm tra không giúp phân biệt hai phía; cần đổi điểm thử.
- Hệ số của một ẩn có thể bằng $0$ (miễn là $a,b$ không đồng thời bằng $0$), nên đường biên có thể song song với trục tọa độ.
- Khi diễn đạt điều kiện thực tế, không được bỏ qua ý nghĩa và đơn vị của các ẩn; điều kiện không âm thường phải ghi riêng nếu chúng biểu diễn số lượng.

#### 5. Hoạt động học tập

- **Hình thức:** Đọc lý thuyết, xem video bài giảng (nếu có) và luyện tập biểu diễn miền nghiệm của bất phương trình.

#### 6. Dạng bài tập và đánh giá

- **Nhận biết:** phân loại biểu thức nào là bất phương trình bậc nhất hai ẩn; nhận biết hệ số và dấu quan hệ.
- **Thông hiểu:** kiểm tra nghiệm bằng thay số; giải thích vì sao một điểm nằm trong/ngoài miền nghiệm.
- **Vận dụng:** vẽ đường biên, chọn điểm thử, biểu diễn miền nghiệm cho cả dấu nghiêm ngặt và không nghiêm ngặt; viết bất phương trình từ điều kiện bằng lời.
- **Tiêu chí tự đánh giá:** xác định được đường biên, chọn đúng phía, xử lý đúng việc lấy hoặc không lấy biên và giải thích được kết quả. Không gắn ngưỡng đạt điểm chính thức khi chưa có bài kiểm tra cụ thể.

### BÀI 2. HỆ BẤT PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN
<!-- lesson_id: II.2 -->

#### 1. Thông tin bài học

- **Tên SGK:** Bài 2. Hệ bất phương trình bậc nhất hai ẩn.
- **Chương:** II – Bất phương trình và hệ bất phương trình bậc nhất hai ẩn.
- **Số tiết theo KHBD chính thức:** chưa xác minh (`official_periods: null`).
- **Số buổi tự học đề xuất:** 2 (`suggested_sessions: 2`).
- **Thời lượng đề xuất mỗi buổi:** 45 phút (`minutes_per_session: 45`).
- **Kiến thức cần trước:** toàn bộ II.1 và cách xác định giao của các tập hợp.

#### 2. Mục tiêu học tập

- Nêu được khái niệm hệ bất phương trình bậc nhất hai ẩn và nghiệm chung của hệ.
- Biểu diễn đúng giao các miền nghiệm của những bất phương trình trong hệ.
- Kiểm tra được một điểm có thuộc miền nghiệm của hệ hay không.
- Mô hình hóa các điều kiện thực tiễn bằng hệ bất phương trình tuyến tính đơn giản; xác định được các đỉnh của miền đa giác khả thi.
- Biết cách tìm giá trị lớn nhất hoặc nhỏ nhất của $F=ax+by$ trên miền đa giác thỏa mãn giả thiết.

#### 3. Kiến thức cần nắm

**Khái niệm.** Hệ bất phương trình bậc nhất hai ẩn gồm từ hai bất phương trình bậc nhất hai ẩn trở lên cùng xét với hai ẩn $x,y$. Một cặp $(x_0,y_0)$ là **nghiệm của hệ** nếu cặp đó thỏa mãn **đồng thời tất cả** bất phương trình trong hệ.

**Biểu diễn miền nghiệm:**

1. Trên cùng một hệ trục $Oxy$, vẽ từng đường biên của các bất phương trình.
2. Xác định miền nghiệm riêng của từng bất phương trình bằng phương pháp ở II.1.
3. Lấy **giao** của các miền nghiệm, chú ý có hay không gồm mỗi đoạn biên tương ứng.
4. Nếu không tồn tại điểm nào thỏa đồng thời thì hệ **vô nghiệm**; miền nghiệm là tập rỗng.

**Tối ưu biểu thức tuyến tính trên miền đa giác:**

- Thiết lập hệ ràng buộc, bao gồm những điều kiện về dấu và giới hạn của các đại lượng nếu bài toán yêu cầu.
- Xác định miền khả thi. Trong trường hợp miền này là **đa giác khép kín, không rỗng và bị chặn**, tìm các tọa độ đỉnh từ giao của các đường biên.
- Tính $F=ax+by$ tại từng đỉnh; so sánh các giá trị để chọn giá trị lớn nhất/nhỏ nhất. Nếu $F$ không đổi dọc theo một cạnh tối ưu, ngoài các đỉnh tương ứng còn có các điểm trên cạnh đạt cùng giá trị.
- Nếu đề bài yêu cầu số lượng **nguyên**, bước tối ưu trên miền liên tục chưa đủ kết luận nghiệm nguyên tối ưu; phải kiểm tra thêm ràng buộc nguyên.

#### 4. Kiến thức cần hiểu

- Miền nghiệm của hệ là **giao**, không phải hợp, vì các điều kiện phải đúng đồng thời.
- Không phải hệ nào cũng có nghiệm và không phải miền nghiệm nào cũng bị chặn. Quy tắc so sánh trên các đỉnh phải được dùng đúng giả thiết; không áp dụng máy móc khi miền mở hoặc không bị chặn.
- Điểm giao của hai đường biên chỉ là **đỉnh ứng viên**; phải kiểm tra xem nó có thuộc toàn bộ miền khả thi hay không.
- Điều kiện $x\geq0$, $y\geq0$ chỉ được thêm khi có căn cứ từ ngữ cảnh hoặc giả thiết toán học, không tự động áp vào mọi hệ bất phương trình.
- Khi kết quả tối ưu đạt ở đỉnh, cần diễn giải ngược về đại lượng thực tế và kiểm tra đơn vị, các ràng buộc, tính nguyên nếu có.

#### 5. Hoạt động học tập

- **Hình thức:** Đọc lý thuyết, xem video bài giảng (nếu có) và làm bài tập tìm miền nghiệm, bài toán tối ưu.

#### 6. Dạng bài tập và đánh giá

- **Nhận biết:** xác định hệ bất phương trình bậc nhất hai ẩn; kiểm tra cặp số có phải nghiệm chung.
- **Thông hiểu:** biểu diễn miền nghiệm từng bất phương trình và miền giao; đọc hình để nhận diện các điều kiện biên.
- **Vận dụng:** chuyển bài toán thực tế thành ràng buộc tuyến tính; tìm và kiểm tra các đỉnh, đánh giá $F$ tại các đỉnh, kết luận giá trị lớn nhất/nhỏ nhất khi đủ giả thiết.
- **Tiêu chí tự đánh giá:** giải thích rõ từng bước từ mô hình hóa → vẽ miền → kiểm tra đỉnh → tối ưu → đối chiếu điều kiện; nhận biết được khi nào phương pháp xét đỉnh chưa áp dụng trực tiếp.

### BÀI TẬP CUỐI CHƯƠNG II — ÔN TẬP VÀ TỰ ĐÁNH GIÁ
<!-- lesson_id: II.R -->

#### 1. Thông tin bài học

- **Vị trí SGK:** Bài tập cuối chương II.
- **Số tiết theo KHBD chính thức:** chưa xác minh (`official_periods: null`).
- **Số buổi tự học đề xuất:** 1 (`suggested_sessions: 1`).
- **Thời lượng đề xuất:** 45 phút (`minutes_per_session: 45`).
- **Phạm vi:** kiến thức của Bài 1 và Bài 2; không đưa thêm khái niệm mới.

#### 2. Mục tiêu học tập

- Củng cố nhận dạng bất phương trình, nghiệm, miền nghiệm và miền nghiệm của hệ.
- Giải quyết được bài tổng hợp có ràng buộc tuyến tính và mục tiêu tối ưu cơ bản khi đủ điều kiện.
- Phát hiện và tự sửa được những lỗi sai phổ biến trong biểu diễn biên, xác định miền giao và chọn đỉnh.

#### 3. Kiến thức cần nắm

- Dạng chuẩn bất phương trình bậc nhất hai ẩn, điều kiện hệ số và phép thử nghiệm.
- Các bước biểu diễn miền nghiệm riêng, giao các miền và đọc điều kiện biên.
- Điều kiện để dùng phương pháp tính hàm mục tiêu tại các đỉnh của miền đa giác khép kín, không rỗng, bị chặn.

#### 4. Kiến thức cần hiểu

- Vẽ đúng hình nhưng quên kiểm tra toàn bộ ràng buộc có thể dẫn tới nghiệm sai.
- Kết quả tối ưu chỉ có ý nghĩa nếu miền khả thi và các điều kiện thực tế được xác định đúng.
- Có thể dùng kết quả tự đánh giá theo nhóm kỹ năng để quyết định cần ôn lại II.1 hay II.2 trước khi chuyển chương.

#### 5. Hoạt động học tập

- **Hình thức:** Ôn tập lý thuyết, đọc tài liệu và làm bài tập tổng hợp cuối chương.

#### 6. Dạng bài tập và đánh giá

- Kiểm tra theo bốn nhóm: **(1)** nhận dạng/kiểm tra nghiệm; **(2)** biểu diễn một miền nghiệm; **(3)** tìm miền nghiệm của hệ; **(4)** mô hình hóa và tối ưu cơ bản.
- Đối chiếu lời giải với điều kiện của từng bất phương trình; báo cáo số câu đúng theo nhóm kỹ năng và lỗi sai điển hình.
- Không tự quy định ngưỡng đạt chuẩn của nhà trường từ bản tài liệu tự biên soạn này.

## NGUỒN THAM KHẢO VÀ KIỂM CHỨNG

> Những nguồn sau được đối chiếu cho **danh mục và phạm vi kiến thức**, không có nghĩa toàn văn bản này đã được nhà xuất bản hay giáo viên xác nhận. Các đoạn giải thích, mục tiêu học, hoạt động và thời lượng là nội dung EDUAGENT biên soạn; cần chuyên gia Toán kiểm duyệt trước khi gắn `verified`.

- **[S01] Danh mục Chương II – Toán 10, Chân trời sáng tạo**, FQA: https://fqa.vn/giai-bai-tap-sgk/chuong/chuong-ii-bat-phuong-trinh-va-he-bat-phuong-trinh-bac-nhat-hai-an-e25887.html — xác nhận tên chương, Bài 1, Bài 2 và Bài tập cuối chương II.
- **[S02] Chương II – Toán 10, Chân trời sáng tạo**, Loigiaihay: https://loigiaihay.com/chuong-ii-bat-phuong-trinh-va-he-bat-phuong-trinh-bac-nhat-hai-an-e25887.html — đối chiếu danh mục và các chủ đề trong hai bài.
- **[S03] Tài liệu ôn tập Toán 10 CTST, Chương II** (tài liệu tham khảo giáo dục): https://file.montoan.com.vn/file-pdf/bai-tap-mon-toan-10-bo-sach-chan-troi-sang-tao-hoc-ki-1.pdf — đối chiếu định nghĩa, phép thử nghiệm và quy trình biểu diễn miền nghiệm.
- **[S04] Giải bài học Bài 2 – Hệ bất phương trình bậc nhất hai ẩn**, FQA: https://fqa.vn/giai-bai-tap-sgk/bai-tap/bai-2-he-bat-phuong-trinh-bac-nhat-hai-an-e7758/1.html — đối chiếu nội dung miền nghiệm chung và tìm cực trị biểu thức tuyến tính trên miền đa giác.

## GHI CHÚ QUẢN LÝ DỮ LIỆU

- `document_type = lesson_plan` cho tất cả các chunk thuộc giáo án này; các chunk lấy trực tiếp từ SGK sau này dùng `document_type = textbook`.
- `content_type = summary` cho Phần A; `content_type = detail` cho Phần B. **Không index phần Nguồn tham khảo và Ghi chú quản lý như chunk kiến thức**, mà lưu provenance riêng.
- Với Phần A: `lesson_id = null`. Với Phần B: `lesson_id` lấy **chính xác** từ marker HTML theo từng mục bài, lần lượt `II.1`, `II.2`, `II.R`.
- Chunk chia theo heading `###` / `####`, giữ cùng `chapter_id` và `lesson_id`; khi mục dài, tiếp tục chia theo đoạn mà không cắt công thức LaTeX.
- `verification_status = review_required` cho tới khi có bước kiểm duyệt học thuật. Có URL tham khảo **không đủ** để đổi thành `verified`.
- `source_ids` là bằng chứng mức tài liệu; truy vết từng phát biểu đòi hỏi mapping vị trí/đoạn nguồn chi tiết hơn trong pipeline tiền xử lý.
