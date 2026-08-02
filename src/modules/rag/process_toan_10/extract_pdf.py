import pymupdf4llm

pdf_path = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\data_test_table.pdf"

md_path = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\data_test_table.md"

md_text = pymupdf4llm.to_markdown(pdf_path)

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_text)