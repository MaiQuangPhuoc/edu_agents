# import os
# import shutil

# # ==========================
# # CONFIG
# # ==========================
# IMAGES_DIR = r"D:\rikai\ctr\2\2"
# LABELS_DIR = r"D:\rikai\ctr\2_label_p1"
# OUTPUT_DIR = r"D:\rikai\ctr\2_miss"

# IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

# # ==========================
# # MAIN
# # ==========================

# def main():
#     if not os.path.isdir(IMAGES_DIR):
#         print(f"[!] Không tìm thấy thư mục ảnh: {IMAGES_DIR}")
#         return
#     if not os.path.isdir(LABELS_DIR):
#         print(f"[!] Không tìm thấy thư mục label: {LABELS_DIR}")
#         return

#     os.makedirs(OUTPUT_DIR, exist_ok=True)

#     # Tập hợp tên (không đuôi) của tất cả file .txt trong LABELS_DIR
#     label_names = set()
#     for f in os.listdir(LABELS_DIR):
#         if f.lower().endswith(".txt"):
#             name, _ = os.path.splitext(f)
#             label_names.add(name)

#     print(f"Tổng số file label (.txt): {len(label_names)}")

#     image_files = [
#         f for f in os.listdir(IMAGES_DIR)
#         if f.lower().endswith(IMAGE_EXTS)
#     ]
#     print(f"Tổng số ảnh: {len(image_files)}")

#     missing = []
#     for img_file in image_files:
#         name, _ = os.path.splitext(img_file)
#         if name not in label_names:
#             missing.append(img_file)

#     print(f"Số ảnh KHÔNG có label tương ứng: {len(missing)}")

#     copied = 0
#     for img_file in missing:
#         src = os.path.join(IMAGES_DIR, img_file)
#         dst = os.path.join(OUTPUT_DIR, img_file)
#         try:
#             shutil.copy2(src, dst)
#             copied += 1
#         except Exception as e:
#             print(f"  [!] Lỗi copy {img_file}: {e}")

#     print(f"\n✓ Đã copy {copied}/{len(missing)} ảnh thiếu label vào: {OUTPUT_DIR}")

#     if missing:
#         print("\nDanh sách ảnh thiếu label (tối đa 20 dòng đầu):")
#         for f in missing[:20]:
#             print(f"  - {f}")
#         if len(missing) > 20:
#             print(f"  ... và {len(missing) - 20} ảnh khác")


# if __name__ == "__main__":
#     main()



# ------------------- test model yolo -----------------
# from ultralytics import YOLO
# import cv2

# # ============ CONFIG ============
# MODEL_PATH = "ctr_p03_detector_v1-1_20260212_20260212.pt"
# IMAGE_PATH = "test.jpg"
# OUTPUT_PATH = "result_detected.jpg"
# CONF_THRESHOLD = 0.25
# # =================================

# # 1. Load model
# model = YOLO(MODEL_PATH)
# print(f"Labels: {model.names}")

# # 2. Predict
# results = model.predict(
#     source=IMAGE_PATH,
#     conf=CONF_THRESHOLD,
#     save=False
# )

# result = results[0]

# # 3. In confidence + label từng box
# print(f"\nSố box detect được: {len(result.boxes)}")
# for box in result.boxes:
#     cls_id = int(box.cls)
#     conf = box.conf.item()
#     label = model.names[cls_id]
#     xyxy = box.xyxy[0].tolist()
#     print(f"  - {label}: conf={conf:.4f}, box={xyxy}")

# # 4. Vẽ ảnh detect (có box + label + conf) và lưu ra file
# annotated_img = result.plot()  # trả về ảnh numpy (BGR)
# cv2.imwrite(OUTPUT_PATH, annotated_img)
# print(f"\n✓ Đã lưu ảnh detect tại: {OUTPUT_PATH}")