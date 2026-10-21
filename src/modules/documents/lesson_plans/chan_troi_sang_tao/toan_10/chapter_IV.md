---
schema_version: "1.0"
document_id: "CTST_T10_CH_IV"
document_type: "lesson_plan"
subject: "Toán 10"
grade: 10
textbook_series: "chan_troi_sang_tao"
volume: 1
curriculum_version: "GDPT_2018"
chapter_id: "IV"
chapter_title: "Hệ thức lượng trong tam giác"
content_types: ["summary", "detail"]
lesson_ids: ["IV.1", "IV.2", "IV.3"]
official_periods: null
suggested_sessions: 7
minutes_per_session: 45
verification_status: "review_required"
source_ids: ["SRC_IV_01", "SRC_IV_02", "SRC_IV_03", "SRC_IV_04"]
source_type: "authored_lesson_plan"
notes: "Nội dung tự biên soạn để hỗ trợ tự học và RAG, không sao chép nguyên giáo án nguồn; 7 buổi x 45 phút là gợi ý của EDUAGENT, không phải phân phối tiết chính thức. Chưa được giáo viên thẩm định độc lập."
---

# CHƯƠNG IV. HỆ THỨC LƯỢNG TRONG TAM GIÁC

<!-- content_type: summary -->
## PHẦN A. TÓM TẮT CHƯƠNG

### A.1. Mục tiêu chương
- Xác định và sử dụng đúng các giá trị lượng giác của góc từ \(0^\circ\) đến \(180^\circ\), chú ý dấu và trường hợp biểu thức không xác định.
- Nhận biết quan hệ giữa các giá trị lượng giác của hai góc bù nhau; sử dụng một số hệ thức lượng giác cơ bản.
- Nắm định lí côsin, định lí sin và các công thức diện tích tam giác, hiểu điều kiện áp dụng.
- Giải tam giác từ những dữ kiện thích hợp và sử dụng hệ thức lượng để xử lí bài toán đo đạc thực tế.

### A.2. Danh sách bài học
1. **Bài 1. Giá trị lượng giác của một góc từ 0° đến 180°** (`lesson_id: IV.1`).
2. **Bài 2. Định lí côsin và định lí sin** (`lesson_id: IV.2`).
3. **Bài 3. Giải tam giác và ứng dụng thực tế** (`lesson_id: IV.3`).
4. **Bài tập cuối chương IV** (ôn tập, không tính là bài chính trong `lesson_ids`).

### A.3. Kiến thức trọng tâm
- Định nghĩa \(\sin\alpha\), \(\cos\alpha\), \(\tan\alpha\), \(\cot\alpha\) với \(0^\circ\le\alpha\le180^\circ\) và điều kiện có nghĩa.
- Hệ thức \(\sin^2\alpha+\cos^2\alpha=1\), các công thức liên hệ của hai góc bù nhau và dấu của giá trị lượng giác theo miền góc.
- Trong tam giác \(ABC\), đặt \(a=BC\), \(b=CA\), \(c=AB\). Định lí côsin: \(a^2=b^2+c^2-2bc\cos A\) và các công thức tương tự.
- Định lí sin: \(\dfrac a{\sin A}=\dfrac b{\sin B}=\dfrac c{\sin C}=2R\), với \(R\) là bán kính đường tròn ngoại tiếp.
- Các biểu thức tính diện tích \(S=\tfrac12bc\sin A=\tfrac12ca\sin B=\tfrac12ab\sin C\), \(S=\dfrac{abc}{4R}\), công thức Hê-rông.
- Giải tam giác: xác định những cạnh, góc còn thiếu, chọn công thức thích hợp và kiểm tra tính khả thi của dữ kiện.

### A.4. Kiến thức tiên quyết và quan hệ giữa các bài
- Kiến thức về tam giác, góc, định lí Py-ta-go, tỉ số lượng giác của góc nhọn, phép biến đổi đại số và căn bậc hai.
- Bài 1 mở rộng khái niệm giá trị lượng giác sang góc tù, là tiền đề dùng định lí côsin và định lí sin ở Bài 2.
- Bài 2 cung cấp công cụ tính cạnh, góc và diện tích, được sử dụng có lựa chọn ở Bài 3.
- Khi giải tam giác, cần đối chiếu điều kiện cạnh dương, góc trong \((0^\circ,180^\circ)\) và tổng ba góc bằng \(180^\circ\).

### A.5. Phân bổ thời gian đề xuất

| Nội dung | Buổi tự học đề xuất | Thời gian/buổi | Ghi chú |
|---|---:|---:|---|
| Bài 1. Giá trị lượng giác của một góc từ 0° đến 180° | 2 | 45 phút | Khái niệm, dấu, quan hệ góc bù |
| Bài 2. Định lí côsin và định lí sin | 2 | 45 phút | Định lí, diện tích, cách chọn công thức |
| Bài 3. Giải tam giác và ứng dụng thực tế | 2 | 45 phút | Phân tích dữ kiện và vận dụng |
| Ôn tập cuối chương IV | 1 | 45 phút | Luyện tập tổng hợp và đánh giá |
| **Tổng** | **7** | | **315 phút tự học đề xuất** |

Đây là **gợi ý tự học của EDUAGENT**, không phải số tiết chính thức của SGK hoặc phân phối chương trình của trường. Learning Path Agent có thể điều chỉnh theo năng lực và lịch học cá nhân.

<!-- content_type: detail -->
## PHẦN B. GIÁO ÁN CHI TIẾT

<!-- lesson_id: IV.1 -->
### BÀI 1. GIÁ TRỊ LƯỢNG GIÁC CỦA MỘT GÓC TỪ 0° ĐẾN 180°

#### 1. Thông tin bài học
- `lesson_id`: `IV.1`
- Số tiết theo kế hoạch dạy học chính thức: **chưa xác minh** (`official_periods: null`).
- Số buổi tự học đề xuất: **2** (`suggested_sessions: 2`).
- Thời lượng mỗi buổi đề xuất: **45 phút** (`minutes_per_session: 45`).

#### 2. Mục tiêu học tập
- Nhận biết và tính được các giá trị lượng giác của một góc trong khoảng \([0^\circ,180^\circ]\), kể cả những góc đặc biệt.
- Xác định đúng dấu của sin, cos, tan, cot tùy theo góc; nhận biết trường hợp tan hoặc cot không xác định.
- Sử dụng các công thức liên hệ giữa hai góc bù nhau và hệ thức lượng giác cơ bản để biến đổi, tính toán.
- Vận dụng giá trị lượng giác trong các bài toán hình học có góc tù.

#### 3. Kiến thức cần nắm
**Định nghĩa thông qua đường tròn đơn vị.** Với góc \(\alpha\in[0^\circ,180^\circ]\), tia tạo góc \(\alpha\) với trục hoành dương cắt nửa đường tròn đơn vị tại \(M(x;y)\). Khi đó

\[
\cos\alpha=x,\qquad \sin\alpha=y.
\]

Khi \(\cos\alpha\ne0\), đặt \(\tan\alpha=\dfrac{\sin\alpha}{\cos\alpha}\). Khi \(\sin\alpha\ne0\), đặt \(\cot\alpha=\dfrac{\cos\alpha}{\sin\alpha}\).

**Dấu và điểm đặc biệt.** Trên \([0^\circ,180^\circ]\), \(\sin\alpha\ge0\). Cos dương với \(0^\circ\le\alpha<90^\circ\), bằng 0 tại \(90^\circ\), âm với \(90^\circ<\alpha\le180^\circ\). Tan không xác định tại \(90^\circ\); cot không xác định tại \(0^\circ\) và \(180^\circ\).

**Các giá trị đặc biệt.**

| \(\alpha\) | \(0^\circ\) | \(30^\circ\) | \(45^\circ\) | \(60^\circ\) | \(90^\circ\) | \(120^\circ\) | \(135^\circ\) | \(150^\circ\) | \(180^\circ\) |
|---|---|---|---|---|---|---|---|---|---|
| \(\sin\alpha\) | \(0\) | \(\tfrac12\) | \(\tfrac{\sqrt2}2\) | \(\tfrac{\sqrt3}2\) | \(1\) | \(\tfrac{\sqrt3}2\) | \(\tfrac{\sqrt2}2\) | \(\tfrac12\) | \(0\) |
| \(\cos\alpha\) | \(1\) | \(\tfrac{\sqrt3}2\) | \(\tfrac{\sqrt2}2\) | \(\tfrac12\) | \(0\) | \(-\tfrac12\) | \(-\tfrac{\sqrt2}2\) | \(-\tfrac{\sqrt3}2\) | \(-1\) |

**Hệ thức cơ bản và góc bù.**

\[
\sin^2\alpha+\cos^2\alpha=1;\qquad
\sin(180^\circ-\alpha)=\sin\alpha;\qquad
\cos(180^\circ-\alpha)=-\cos\alpha.
\]

Với các giá trị được xác định, \(\tan(180^\circ-\alpha)=-\tan\alpha\), \(\cot(180^\circ-\alpha)=-\cot\alpha\). Ngoài ra, \(1+\tan^2\alpha=\dfrac1{\cos^2\alpha}\) khi \(\cos\alpha\ne0\).

#### 4. Kiến thức cần hiểu
- Giá trị cos có thể âm khi góc tù; điều đó không mâu thuẫn với \(\sin^2\alpha+\cos^2\alpha=1\).
- Các công thức góc bù giúp chuyển giá trị lượng giác của góc tù về góc nhọn quen thuộc.
- Không được tính tan hoặc cot tại các góc khiến mẫu số bằng 0; phải kiểm tra miền xác định trước khi sử dụng hệ thức.
- Giá trị lượng giác của góc trong tam giác phụ thuộc vào số đo góc, không phụ thuộc kích thước tam giác.

#### 5. Hoạt động học tập
Đọc lý thuyết SGK, xem video bài giảng (nếu có) và làm bài tập về giá trị lượng giác, dấu, góc bù và công thức lượng giác cơ bản.

#### 6. Dạng bài tập và đánh giá
- **Nhận biết:** Xác định giá trị lượng giác của các góc đặc biệt, chỉ ra các giá trị không xác định.
- **Thông hiểu:** Tính giá trị lượng giác của góc tù từ góc bù; xét dấu và vận dụng hệ thức \(\sin^2\alpha+\cos^2\alpha=1\).
- **Vận dụng:** Tính biểu thức có nhiều giá trị lượng giác hoặc xác định giá trị lượng giác còn lại từ một giá trị đã biết và điều kiện của góc.
- **Tiêu chí hoàn thành:** Đúng dấu, đúng điều kiện xác định, sử dụng đúng hệ thức và giải thích được phép biến đổi.

<!-- lesson_id: IV.2 -->
### BÀI 2. ĐỊNH LÍ CÔSIN VÀ ĐỊNH LÍ SIN

#### 1. Thông tin bài học
- `lesson_id`: `IV.2`
- Số tiết theo kế hoạch dạy học chính thức: **chưa xác minh** (`official_periods: null`).
- Số buổi tự học đề xuất: **2** (`suggested_sessions: 2`).
- Thời lượng mỗi buổi đề xuất: **45 phút** (`minutes_per_session: 45`).

#### 2. Mục tiêu học tập
- Phát biểu và vận dụng được định lí côsin, hệ quả định lí côsin và định lí sin trong tam giác.
- Phân biệt tình huống phù hợp để tính cạnh hoặc góc bằng từng định lí.
- Sử dụng được các công thức diện tích tam giác liên quan đến cạnh, góc và bán kính đường tròn nội tiếp, ngoại tiếp.
- Kiểm tra được tính hợp lí của kết quả về cạnh, góc và diện tích.

#### 3. Kiến thức cần nắm
**Quy ước.** Với tam giác không suy biến \(ABC\), đặt \(a=BC>0\), \(b=CA>0\), \(c=AB>0\); các góc \(A,B,C\) lần lượt đối diện \(a,b,c\), \(A+B+C=180^\circ\).

**Định lí côsin.**

\[
\begin{aligned}
a^2&=b^2+c^2-2bc\cos A,\\
b^2&=c^2+a^2-2ca\cos B,\\
c^2&=a^2+b^2-2ab\cos C.
\end{aligned}
\]

Khi biết ba cạnh, có thể tính góc thông qua

\[
\cos A=\frac{b^2+c^2-a^2}{2bc},\qquad
\cos B=\frac{c^2+a^2-b^2}{2ca},\qquad
\cos C=\frac{a^2+b^2-c^2}{2ab}.
\]

Khi \(A=90^\circ\), công thức đầu trở thành \(a^2=b^2+c^2\) (định lí Py-ta-go).

**Định lí sin.** Gọi \(R>0\) là bán kính đường tròn ngoại tiếp tam giác. Khi đó

\[
\frac a{\sin A}=\frac b{\sin B}=\frac c{\sin C}=2R.
\]

Vì \(A,B,C\in(0^\circ,180^\circ)\), các mẫu số sin trong công thức đều dương. Có thể suy ra \(a=2R\sin A\) và các công thức tương tự.

**Diện tích tam giác.** Gọi \(S\) là diện tích, \(r>0\) là bán kính đường tròn nội tiếp, \(p=(a+b+c)/2\) là nửa chu vi. Ta có

\[
S=\frac12bc\sin A=\frac12ca\sin B=\frac12ab\sin C,
\]

\[
S=\frac{abc}{4R}=pr=\sqrt{p(p-a)(p-b)(p-c)}.
\]

Công thức Hê-rông áp dụng cho bộ cạnh thỏa mãn bất đẳng thức tam giác nghiêm ngặt.

#### 4. Kiến thức cần hiểu
- Định lí côsin đặc biệt phù hợp khi biết hai cạnh và góc xen giữa, hoặc biết ba cạnh để tính góc.
- Định lí sin liên hệ một cạnh với góc đối diện; không được ghép nhầm cạnh với góc kề.
- Khi chỉ biết hai cạnh và một góc không xen giữa (SSA), có thể có 0, 1 hoặc 2 tam giác thỏa mãn; không mặc nhiên chọn nghiệm góc nhọn của hàm arcsin.
- Diện tích phải dương và có đơn vị diện tích; khi chọn công thức phải xem dữ kiện đang có.

#### 5. Hoạt động học tập
Đọc lý thuyết SGK, xem video (nếu có) và luyện bài tập về định lí côsin, định lí sin và các công thức diện tích tam giác.

#### 6. Dạng bài tập và đánh giá
- **Nhận biết:** Gọi đúng các cặp cạnh–góc đối diện; nhận diện công thức định lí côsin, sin và công thức diện tích.
- **Thông hiểu:** Tính cạnh khi biết hai cạnh, góc xen giữa; tính góc khi biết ba cạnh; tính diện tích từ hai cạnh và góc xen giữa.
- **Vận dụng:** Kết hợp nhiều hệ thức để suy ra đại lượng chưa biết, tính \(R\), \(r\) hoặc diện tích từ các dữ kiện tương thích.
- **Tiêu chí hoàn thành:** Lựa chọn đúng định lí, thiết lập biểu thức đúng, xét điều kiện hình học và đơn vị hợp lí.

<!-- lesson_id: IV.3 -->
### BÀI 3. GIẢI TAM GIÁC VÀ ỨNG DỤNG THỰC TẾ

#### 1. Thông tin bài học
- `lesson_id`: `IV.3`
- Số tiết theo kế hoạch dạy học chính thức: **chưa xác minh** (`official_periods: null`).
- Số buổi tự học đề xuất: **2** (`suggested_sessions: 2`).
- Thời lượng mỗi buổi đề xuất: **45 phút** (`minutes_per_session: 45`).

#### 2. Mục tiêu học tập
- Hiểu bài toán giải tam giác là tìm các cạnh, góc còn thiếu từ những dữ kiện đã cho.
- Lập được trình tự giải cho các tình huống biết một cạnh và hai góc, hai cạnh và góc xen giữa, hoặc ba cạnh.
- Nhận diện trường hợp dữ kiện không xác định duy nhất một tam giác và kiểm tra sự phù hợp của các nghiệm.
- Chuyển bài toán đo đạc thực tế thành mô hình tam giác và diễn giải kết quả theo đơn vị, độ chính xác thích hợp.

#### 3. Kiến thức cần nắm
**Giải tam giác.** Trong tam giác \(ABC\), các đại lượng cần tìm là ba cạnh \(a,b,c\) và ba góc \(A,B,C\), với tổng góc bằng \(180^\circ\) và bất đẳng thức tam giác.

**Khi biết một cạnh và hai góc (ASA/AAS).** Tính góc còn lại từ tổng góc rồi dùng định lí sin để tìm các cạnh chưa biết. Nếu hai góc đã cho có tổng không nhỏ hơn \(180^\circ\), dữ kiện không tạo được tam giác không suy biến.

**Khi biết hai cạnh và góc xen giữa (SAS).** Dùng định lí côsin tìm cạnh thứ ba; tiếp theo tính các góc còn lại bằng định lí côsin hoặc dùng định lí sin kết hợp kiểm tra góc.

**Khi biết ba cạnh (SSS).** Trước hết kiểm tra mỗi cạnh nhỏ hơn tổng hai cạnh kia; nếu hợp lệ, dùng hệ quả định lí côsin để tính các góc.

**Khi biết hai cạnh và góc đối diện một trong hai cạnh (SSA).** Không luôn xác định duy nhất một tam giác. Sau khi suy ra sin của một góc, phải xét cả hai khả năng \(\theta\) và \(180^\circ-\theta\) (nếu cả hai phù hợp) rồi kiểm tra tổng góc, cạnh và điều kiện đề bài.

**Ứng dụng thực tế.** Các bài toán đo khoảng cách không thể đo trực tiếp, chiều cao công trình hoặc vị trí điểm quan sát có thể mô hình hóa bằng một hoặc nhiều tam giác. Quy trình: vẽ hình và ghi dữ kiện → xác định đại lượng cần tìm → chọn định lí phù hợp → tính toán → kiểm tra đơn vị, độ lớn và sai số làm tròn.

**Diện tích khi có đủ dữ kiện.** Sử dụng công thức diện tích phù hợp từ Bài 2, không mặc định dữ kiện nào cũng dùng được cùng một công thức.

#### 4. Kiến thức cần hiểu
- Việc chọn định lí phụ thuộc dạng dữ kiện; không cần thuộc một quy trình duy nhất cho mọi tam giác.
- Độ dài tính được phải dương và thỏa mãn bất đẳng thức tam giác; góc phải nằm giữa \(0^\circ\) và \(180^\circ\).
- Một mô hình thực tế có thể mang giả thiết giản lược (cùng mặt phẳng, vị trí đo, làm tròn); cần ghi rõ giả thiết trước khi kết luận.
- Kết quả gần đúng khi sử dụng máy tính cần làm tròn ở bước cuối để giảm sai số tích lũy.

#### 5. Hoạt động học tập
Đọc lý thuyết SGK, xem video bài giảng (nếu có) và làm bài tập giải tam giác, đo đạc khoảng cách hoặc chiều cao trong tình huống thực tế.

#### 6. Dạng bài tập và đánh giá
- **Nhận biết:** Phân loại dữ kiện ASA/AAS, SAS, SSS và gọi tên các định lí cần dùng.
- **Thông hiểu:** Giải các tam giác có đủ điều kiện và trình bày thứ tự tính cạnh, góc hợp lí.
- **Vận dụng:** Mô hình hóa một tình huống đo đạc; thiết lập tam giác, tính đại lượng cần tìm, diễn giải theo đơn vị thực tế; phân tích trường hợp SSA khi xuất hiện.
- **Tiêu chí hoàn thành:** Tính toán đúng, kiểm tra nghiệm hình học, không bỏ sót trường hợp và diễn giải kết quả có đơn vị.

<!-- lesson_id: null -->
### ÔN TẬP. BÀI TẬP CUỐI CHƯƠNG IV

#### 1. Thông tin ôn tập
- Số buổi tự học đề xuất: **1** (`suggested_sessions: 1`).
- Thời lượng đề xuất: **45 phút** (`minutes_per_session: 45`).
- Phạm vi: các kiến thức thuộc Bài 1, Bài 2 và Bài 3.

#### 2. Mục tiêu ôn tập
- Nhận diện công thức lượng giác và hệ thức lượng cần dùng từ từng dạng dữ kiện.
- Liên kết phép tính giá trị lượng giác với định lí côsin, định lí sin và các công thức diện tích.
- Giải được bài toán tổng hợp có bước kiểm tra điều kiện và ý nghĩa hình học.

#### 3. Kiến thức cần nắm
- Miền xác định, dấu và quan hệ góc bù của sin, cos, tan, cot.
- Định lí côsin, định lí sin, các công thức diện tích và bất đẳng thức tam giác.
- Các bước giải tam giác; chú ý khả năng có nhiều nghiệm trong trường hợp SSA.

#### 4. Kiến thức cần hiểu
- Vì sao cần xác định loại dữ kiện trước khi lựa chọn công thức.
- Vì sao nghiệm đại số chưa chắc thỏa mãn điều kiện hình học hoặc mô hình đo đạc.

#### 5. Hoạt động học tập
Đọc tóm tắt chương, xem lại tài liệu hoặc video cần thiết (nếu có) và luyện bài tập cuối chương với các mức độ khó khác nhau.

#### 6. Dạng bài tập và đánh giá
- **Nhận biết:** Điền công thức, kiểm tra dấu hoặc điều kiện xác định.
- **Thông hiểu:** Chọn định lí và tính cạnh, góc, diện tích với dữ kiện trực tiếp.
- **Vận dụng:** Giải bài toán nhiều bước hoặc một tình huống đo đạc có dữ kiện thực tế.
- **Tiêu chí hoàn thành:** Không nhầm cạnh với góc đối diện, tính đúng công thức, kiểm tra nghiệm và trình bày đáp số đúng đơn vị.

## NGUỒN THAM KHẢO VÀ KIỂM CHỨNG

Các nguồn dưới đây dùng để **đối chiếu danh mục bài và phạm vi kiến thức**, không phải chứng nhận rằng toàn bộ giáo án đã được giáo viên kiểm duyệt. Nội dung Markdown là bản biên soạn mới; thời lượng tự học là đề xuất của EDUAGENT.

- **SRC_IV_01 — Danh mục SGK:** VietJack, *Toán 10 Chân trời sáng tạo – Chương 4: Hệ thức lượng trong tam giác*. https://vietjack.com/toan-10-ct/chuong-4-he-thuc-luong-trong-tam-giac.jsp — đối chiếu tên chương, ba bài học và bài tập cuối chương.
- **SRC_IV_02 — Đối chiếu mục lục:** Loigiaihay, *Chương IV. Hệ thức lượng trong tam giác, Toán 10 Chân trời sáng tạo*. https://loigiaihay.com/chuong-iv-he-thuc-luong-trong-tam-giac-e25937.html — xác nhận thứ tự các bài và phạm vi bài tập.
- **SRC_IV_03 — Lý thuyết toán:** Loigiaihay, *Lý thuyết Giải tam giác và ứng dụng thực tế*. https://loigiaihay.com/ly-thuyet-giai-tam-giac-va-ung-dung-thuc-te-a109929.html — đối chiếu định lí côsin, sin và công thức diện tích.
- **SRC_IV_04 — Tài liệu chuyên đề:** *Chuyên đề IV – Toán 10 – Hệ thức lượng trong tam giác*. https://file.toan11.edu.vn/file-pdf/chuyen-de-he-thuc-luong-trong-tam-giac-toan-10-chan-troi-sang-tao.pdf — đối chiếu cách trình bày công thức Hê-rông và ứng dụng giải tam giác.

**Trạng thái:** `review_required` — kiến thức và công thức được biên soạn, đối chiếu nguồn tham khảo; chưa kiểm duyệt sư phạm độc lập và chưa xác minh số tiết chính thức của từng bài.
