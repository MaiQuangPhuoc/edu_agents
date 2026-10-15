import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))



from src.edu_planning.lp_tools import make_lp_tools

sm = {
    "lich_hoc": {"so_buoi_tuan": 3, "lich_ban": [],
                 "khung_gio_ranh": {"thu_2": ["19:00-21:00"], "thu_4": ["19h-21h"], "thu_7": ["14:00-17:00"]}},
    "so_thich_hoc": {"thoi_luong_buoi_phut": 90},
    "muc_tieu": [{"mon_hoc": "Toán 10", "muc_tieu_diem": 8, "ngay_ket_thuc": "2027-01-10"}],
}
window = {"start_date": None, "num_weeks": 1, "first_week_no": 1, "chapter_ids": ["1", "2"]}

tools = {t.name: t for t in make_lp_tools(None, None, sm, "Toán 10", window)}
print(tools["compute_schedule"].invoke({}))
print(tools["compute_difficulty_ratio"].invoke({}))