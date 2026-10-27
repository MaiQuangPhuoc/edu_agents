"""Run from the EDUAGENT project root with python -m ...auto_indexing."""

import argparse
import json
import logging

from .pipeline import AutoIndexingError, run_auto_indexing


def main():
    parser = argparse.ArgumentParser(description="PDF chỉ để lưu/xem; Markdown gốc dùng indexing theo Tên sách.")
    parser.add_argument("pdf", help="PDF để lưu/xem, không trích xuất nội dung")
    parser.add_argument("--book-name", required=True, help="Tên sách dùng nguyên văn làm collection_name")
    parser.add_argument("--subject", help="Môn chọn bộ Markdown gốc")
    parser.add_argument("--series", help="Bộ sách, ví dụ canh_dieu hoặc chan_troi_sang_tao")
    parser.add_argument("--original-filename", help="Tên gốc nếu file upload đã đổi tên")
    parser.add_argument("--source-root", help="Thư mục chỉ chứa Markdown giáo án gốc")
    parser.add_argument("--output-root", help="Thư mục riêng lưu job và PDF")
    parser.add_argument("--template-collection", help="Collection mẫu; mặc định dùng COLLECT_NAME, đích luôn tạo mới")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--preview", action="store_true", help="Chunk Markdown gốc, không tạo collection hoặc giữ chỗ tên")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        result = run_auto_indexing(
            args.pdf, book_name=args.book_name, source_subject=args.subject, source_series=args.series, original_filename=args.original_filename, source_root=args.source_root,
            output_root=args.output_root, template_collection=args.template_collection,
            batch_size=args.batch_size, upload=not args.preview,
        )
    except (AutoIndexingError, ValueError, FileNotFoundError) as exc:
        parser.exit(1, f"Lỗi: {exc}\nReport: {getattr(exc, 'report_path', 'chưa tạo job')}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
