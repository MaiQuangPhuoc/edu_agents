# Giả lập bài test đầu vào — Toán 10

- `question_bank_toan10.json`: 60 câu (10 câu × chương I–VI), có đáp án đúng.
- `entry_test_mock.py`: Chọn 20 câu theo `StudentModel` (ưu tiên chương yếu), đánh số 1–20, xuất đề và file đáp án **riêng**.
- `output/test_student.txt`: Đề cho học sinh, **không chứa đáp án đúng**.
- `output/answer_key.json`: File chuẩn cho `entry_grade.py` (`questions`: `no`, `chapter_id`, `answer`). Không công khai file này khi triển khai UI.

Chạy thử: `python entry_test_mock.py`. Nhập câu trả lời kiểu `1-A, 2-C, 3-B`.

Sau Collect, tích hợp:
```python
from entry_test_mock import create_mock_test
info = create_mock_test(state['student_model'])
state['entry_test'] = {'subject': info['subject'], 'key_file': info['key_file']}
# Hiển thị output/test_student.txt; khi học sinh trả lời, chuyển sang grade_node(state).
```

**Lưu ý:** Đây là bộ câu hỏi giả lập dành cho kiểm thử luồng, chưa được giáo viên thẩm định; hiện chỉ hỗ trợ Toán 10, và chưa nối tự động vào `roadmap_graph.py`. Điểm mạnh/yếu sau khi chấm do `entry_grade.py` cập nhật. Với nhiều học sinh, tạo output_dir riêng cho từng phiên để tránh ghi đè file.
