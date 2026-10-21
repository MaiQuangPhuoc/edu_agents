---
schema_version: "1.0"
document_id: "CTST_T10_CH_III"
document_type: "lesson_plan"
subject: "Toán 10"
grade: 10
textbook_series: "chan_troi_sang_tao"
volume: 1
curriculum_version: "GDPT_2018"
chapter_id: "III"
chapter_title: "Hàm số bậc hai và đồ thị"
content_types: ["summary", "detail"]
lesson_ids: ["III.1", "III.2"]
official_periods: null
suggested_sessions: 5
minutes_per_session: 45
verification_status: "review_required"
source_ids: ["SRC_III_01", "SRC_III_02", "SRC_III_03"]
source_type: "authored_lesson_plan"
notes: "Giáo án tự biên soạn để tham khảo và phục vụ RAG; thời lượng tự học do EDUAGENT đề xuất, không phải phân phối tiết chính thức. Cần giáo viên kiểm duyệt trước khi dùng làm tài liệu đã xác minh."
---

# CHƯƠNG III. HÀM SỐ BẬC HAI VÀ ĐỒ THỊ

<!-- content_type: summary -->
## PHẦN A. TÓM TẮT CHƯƠNG

### A.1. Mục tiêu chương
- Nhận biết hàm số là sự phụ thuộc xác định giữa các đại lượng; xác định được tập xác định, tập giá trị của hàm số ở các tình huống phù hợp.
- Đọc, biểu diễn và khai thác thông tin từ bảng giá trị, công thức và đồ thị hàm số; nhận biết khoảng đồng biến, nghịch biến.
- Nhận biết hàm số bậc hai \(y=ax^2+bx+c\) với \(a\ne0\); xác định đỉnh, trục đối xứng, chiều mở của parabol và khảo sát sự biến thiên.
- Dùng kiến thức về hàm số bậc hai để mô tả và giải quyết một số tình huống toán học, thực tiễn phù hợp.

### A.2. Danh sách bài học
1. **Bài 1. Hàm số và đồ thị** (`lesson_id: III.1`).
2. **Bài 2. Hàm số bậc hai** (`lesson_id: III.2`).
3. **Bài tập cuối chương III** (ôn tập, không cấp `lesson_id` như một bài chính).

### A.3. Kiến thức trọng tâm
- Khái niệm hàm số, cách xác định giá trị hàm số; tập xác định và tập giá trị.
- Đồ thị hàm số trong mặt phẳng tọa độ; tính đồng biến, nghịch biến trên một khoảng.
- Hàm số bậc hai \(y=ax^2+bx+c\) (\(a\ne0\)); parabol, tọa độ đỉnh, trục đối xứng.
- Bảng biến thiên, giá trị nhỏ nhất/lớn nhất của hàm số bậc hai trên \(\mathbb R\) và trên các khoảng/đoạn xác định khi có đủ điều kiện.

### A.4. Kiến thức tiên quyết và quan hệ giữa các bài
- Cần biết biểu thức đại số, tính giá trị biểu thức, giải phương trình đơn giản, hệ trục tọa độ và cách biểu diễn điểm.
- Bài 1 tạo nền tảng về tập xác định, đồ thị, đồng biến–nghịch biến để học Bài 2.
- Bài 2 sử dụng kiến thức đồ thị hàm số để đọc đặc trưng parabol và giải các bài toán tối ưu đơn giản.

### A.5. Phân bổ thời gian đề xuất

| Nội dung | Buổi tự học đề xuất | Thời gian/buổi | Ghi chú |
|---|---:|---:|---|
| Bài 1. Hàm số và đồ thị | 2 | 45 phút | Khái niệm; đồ thị và sự biến thiên |
| Bài 2. Hàm số bậc hai | 2 | 45 phút | Parabol; biến thiên và vận dụng |
| Ôn tập cuối chương III | 1 | 45 phút | Hệ thống hóa và tự đánh giá |
| **Tổng** | **5** | | **225 phút tự học đề xuất** |

Đây là **gợi ý tự học**, không phải định mức tiết dạy được công bố của SGK. Learning Path Agent cần điều chỉnh theo năng lực, mục tiêu và lịch học của từng học sinh.

<!-- content_type: detail -->
## PHẦN B. GIÁO ÁN CHI TIẾT

<!-- lesson_id: III.1 -->
### BÀI 1. HÀM SỐ VÀ ĐỒ THỊ

#### 1. Thông tin bài học
- `lesson_id`: `III.1`
- Số tiết theo kế hoạch dạy học chính thức: **chưa xác minh** (`official_periods: null`).
- Số buổi tự học đề xuất: **2** (`suggested_sessions: 2`).
- Thời lượng mỗi buổi đề xuất: **45 phút** (`minutes_per_session: 45`).

#### 2. Mục tiêu học tập
- Phát biểu được ý nghĩa của hàm số: mỗi giá trị \(x\) thuộc tập xác định ứng với đúng một giá trị \(y\).
- Tìm được tập xác định của một số hàm số cơ bản cho bằng công thức; phân biệt tập xác định và tập giá trị.
- Đọc và mô tả được đồ thị của hàm số; xác định tọa độ điểm thuộc đồ thị khi biết giá trị của biến.
- Xác định được khoảng đồng biến và nghịch biến từ đồ thị hoặc từ các công thức đơn giản có đủ điều kiện.

#### 3. Kiến thức cần nắm
**Khái niệm hàm số.** Cho tập \(D\subseteq\mathbb R\). Hàm số \(y=f(x)\) xác định trên \(D\) là một quy tắc gán cho mỗi \(x\in D\) đúng một số thực \(f(x)\). Tập \(D\) là **tập xác định**; tập các giá trị thực sự nhận được \(\{f(x):x\in D\}\) là **tập giá trị**.

**Các cách cho hàm số.** Hàm số có thể được biểu diễn bằng công thức, bảng giá trị hoặc các mô tả/đồ thị phù hợp. Nếu cho bằng công thức, cần xét điều kiện để biểu thức có nghĩa trong tập số thực (chẳng hạn mẫu khác 0; biểu thức dưới căn bậc hai không âm).

**Đồ thị.** Đồ thị của \(y=f(x)\) là tập hợp các điểm \((x;f(x))\) với \(x\in D\) trên mặt phẳng tọa độ. Điểm \((a;b)\) thuộc đồ thị khi và chỉ khi \(a\in D\) và \(b=f(a)\).

**Sự biến thiên.** Hàm số **đồng biến** trên khoảng \(K\subseteq D\) nếu với mọi \(x_1,x_2\in K\), \(x_1<x_2\) thì \(f(x_1)<f(x_2)\). Hàm số **nghịch biến** nếu điều kiện tương ứng là \(f(x_1)>f(x_2)\). Cần phân biệt tính đồng biến/nghịch biến với dấu dương/âm của giá trị hàm số.

#### 4. Kiến thức cần hiểu
- Vì sao một giá trị đầu vào không thể cho hai đầu ra khác nhau trong cùng một hàm số.
- Vì sao xác định tập xác định trước khi tính giá trị, vẽ đồ thị hoặc xét sự biến thiên.
- Tính đồng biến/nghịch biến phản ánh chiều thay đổi của \(f(x)\) khi \(x\) tăng, **không** khẳng định hàm số luôn dương hay luôn âm.
- Khi chỉ có một số điểm của bảng giá trị, không được kết luận chắc chắn tính đơn điệu trên toàn khoảng nếu không có thêm căn cứ.

#### 5. Hoạt động học tập
Đọc lý thuyết và tài liệu SGK, xem video bài giảng phù hợp (nếu có), luyện đọc đồ thị và làm bài tập về tập xác định, tập giá trị, tính đồng biến–nghịch biến.

#### 6. Dạng bài tập và đánh giá
- **Nhận biết:** Xác định một quan hệ có phải hàm số hay không; chỉ ra tập xác định từ mô tả hoặc công thức đơn giản.
- **Thông hiểu:** Tính giá trị hàm số tại điểm đã cho; xét một điểm có thuộc đồ thị không; đọc khoảng biến thiên trên đồ thị.
- **Vận dụng:** Xử lý bài toán biểu diễn mối quan hệ giữa hai đại lượng bằng bảng/công thức/đồ thị; giải thích ý nghĩa của khoảng đồng biến, nghịch biến.
- **Tiêu chí hoàn thành:** Phân biệt đúng tập xác định và tập giá trị; đọc được đồ thị; nêu có căn cứ khoảng đồng biến, nghịch biến.

<!-- lesson_id: III.2 -->
### BÀI 2. HÀM SỐ BẬC HAI

#### 1. Thông tin bài học
- `lesson_id`: `III.2`
- Số tiết theo kế hoạch dạy học chính thức: **chưa xác minh** (`official_periods: null`).
- Số buổi tự học đề xuất: **2** (`suggested_sessions: 2`).
- Thời lượng mỗi buổi đề xuất: **45 phút** (`minutes_per_session: 45`).

#### 2. Mục tiêu học tập
- Nhận biết được hàm số bậc hai \(y=ax^2+bx+c\), trong đó \(a\ne0\).
- Xác định đúng tọa độ đỉnh, phương trình trục đối xứng và chiều mở của parabol.
- Lập bảng biến thiên, nhận biết khoảng đồng biến/nghịch biến và cực trị của hàm số bậc hai trên \(\mathbb R\).
- Vẽ được phác họa đồ thị bằng những yếu tố đặc trưng và các điểm thích hợp; vận dụng vào bài toán có mô hình bậc hai khi các giả thiết được nêu đầy đủ.

#### 3. Kiến thức cần nắm
**Dạng tổng quát.** Hàm số bậc hai có dạng

\[
f(x)=ax^2+bx+c,\qquad a\ne0.
\]

Tập xác định của hàm số này là \(\mathbb R\). Đồ thị là một **parabol**.

**Đỉnh và trục đối xứng.** Đặt \(\Delta=b^2-4ac\), ta có đỉnh

\[
I\left(-\frac{b}{2a};-\frac{\Delta}{4a}\right),
\]

và trục đối xứng là đường thẳng \(x=-\frac{b}{2a}\). Có thể dùng dạng hoàn thành bình phương

\[
f(x)=a\left(x+\frac{b}{2a}\right)^2-\frac{\Delta}{4a}.
\]

**Chiều mở, biến thiên và giá trị cực trị.** Nếu \(a>0\), parabol mở lên, hàm số nghịch biến trên \((-\infty;-b/(2a))\), đồng biến trên \((-b/(2a);+\infty)\), có **giá trị nhỏ nhất** bằng \(-\Delta/(4a)\). Nếu \(a<0\), parabol mở xuống, hàm số đồng biến rồi nghịch biến trên các khoảng tương ứng, có **giá trị lớn nhất** bằng \(-\Delta/(4a)\).

**Các điểm đặc trưng.** Đồ thị cắt trục tung tại \((0;c)\). Giao điểm với trục hoành (nếu có) ứng với các nghiệm thực của \(ax^2+bx+c=0\); có hai, một hoặc không có giao điểm theo dấu của \(\Delta\).

**Tập giá trị trên \(\mathbb R\).** Với \(a>0\), tập giá trị là \([ -\Delta/(4a);+\infty)\); với \(a<0\), tập giá trị là \((-\infty;-\Delta/(4a)]\).

#### 4. Kiến thức cần hiểu
- Tại sao dấu của \(a\) quyết định chiều mở và việc đỉnh là điểm cao nhất hay thấp nhất.
- Vì sao trục đối xứng đi qua đỉnh và hai điểm có hoành độ đối xứng qua trục có cùng tung độ.
- Vì sao cực trị trên toàn \(\mathbb R\) chưa chắc là giá trị cực trị trên một miền xác định bị giới hạn; bài toán có điều kiện thực tế phải xét đúng miền giá trị của biến.
- Phân biệt nghiệm của phương trình bậc hai với tọa độ đỉnh của parabol; không dùng \(\Delta\) thay cho tọa độ tung độ của đỉnh.

#### 5. Hoạt động học tập
Đọc lý thuyết và tài liệu SGK, xem video về đồ thị parabol (nếu có), luyện xác định đỉnh–trục đối xứng–bảng biến thiên và làm bài tập.

#### 6. Dạng bài tập và đánh giá
- **Nhận biết:** Nhận diện hàm số bậc hai; xác định \(a,b,c\), chiều mở và trục đối xứng.
- **Thông hiểu:** Tính tọa độ đỉnh, lập bảng biến thiên, nhận xét giá trị lớn nhất/nhỏ nhất và giao điểm với các trục.
- **Vận dụng:** Vẽ phác họa parabol; xác định công thức hàm số bậc hai khi có đủ dữ kiện; xử lý các bài toán tối ưu có miền xác định rõ ràng.
- **Tiêu chí hoàn thành:** Xác định đúng đỉnh, trục đối xứng, chiều biến thiên; giải thích được cực trị và đọc chính xác các đặc trưng đồ thị.

<!-- lesson_id: null -->
### ÔN TẬP. BÀI TẬP CUỐI CHƯƠNG III

#### 1. Thông tin ôn tập
- Nội dung: cả Bài 1 và Bài 2.
- Số buổi tự học đề xuất: **1**.
- Thời lượng đề xuất: **45 phút**.

#### 2. Mục tiêu học tập
- Hệ thống hóa khái niệm hàm số và các đặc trưng cơ bản của đồ thị.
- Kết nối việc xét tập xác định, tập giá trị, sự biến thiên với khảo sát hàm số bậc hai.
- Tự xác định phần còn yếu để điều chỉnh lộ trình học cá nhân.

#### 3. Kiến thức cần nắm
- Tập xác định, tập giá trị, giá trị hàm số, điểm thuộc đồ thị, đồng biến/nghịch biến.
- Công thức đỉnh và trục đối xứng của parabol; bảng biến thiên; dấu của \(a\), dấu của \(\Delta\) và ý nghĩa đồ thị tương ứng.

#### 4. Kiến thức cần hiểu
- Mối quan hệ giữa công thức hàm số, hình dạng đồ thị và đặc điểm biến thiên.
- Cách kiểm tra điều kiện của bài toán để chọn miền khảo sát phù hợp.

#### 5. Hoạt động học tập
Đọc lại tóm tắt kiến thức, xem tài liệu ôn tập nếu cần và làm bài tập tổng hợp của hai bài trong chương.

#### 6. Dạng bài tập và đánh giá
- Bài nhận biết định nghĩa, tập xác định và đặc trưng parabol.
- Bài thông hiểu yêu cầu đọc đồ thị, tính tọa độ đỉnh, lập bảng biến thiên.
- Bài vận dụng yêu cầu giải thích hoặc tối ưu một tình huống có điều kiện xác định rõ.
- Tiêu chí hoàn thành: Phân tích được lời giải, phát hiện và sửa lỗi nhầm lẫn về tập giá trị, khoảng biến thiên và cực trị.

## NGUỒN THAM KHẢO VÀ KIỂM CHỨNG

> Các nguồn sau được dùng để **đối chiếu tên chương, tên bài và phạm vi kiến thức công khai**. Nội dung diễn đạt của giáo án do EDUAGENT tự biên soạn. Chưa kiểm chứng độc lập với bản SGK chính thức và chưa được giáo viên thẩm định; vì vậy toàn tài liệu giữ `verification_status: review_required`.

- **SRC_III_01** — Loigiaihay, danh mục SGK Toán 10 CTST, Chương III (Bài 1, Bài 2, Bài tập cuối chương): https://loigiaihay.com/chuong-iii-ham-so-bac-hai-va-do-thi-e25925.html
- **SRC_III_02** — VietJack, danh mục SGK Toán 10 CTST, Chương III: https://vietjack.com/toan-10-ct/chuong-3-ham-so-bac-hai-va-do-thi.jsp
- **SRC_III_03** — Giáo án tham khảo Bài 1, mục tiêu kiến thức: https://giaoantronbo.com/giao-an-toan-lop-10-chan-troi-sang-tao-chuong-3-bai-1-ham-so-va-do-thi-1376/

**Ghi chú chất lượng:** Số tiết chính thức của mỗi bài chưa được đối chiếu từ kế hoạch dạy học được phê duyệt. Không được sử dụng các giá trị `suggested_sessions` làm số tiết chính thức khi chuyển sang JSON hoặc gắn metadata cho Qdrant.
