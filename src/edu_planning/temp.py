from difflib import SequenceMatcher

text1 = "thứ 7 bệnh viên sẽ không hoạt dộng cho đến 15 giờ, bạn có thẻ khám lúc 17 giờ đến 20 giờ"
text2 = "lúc 18 giờ vào thứ 7 phòng khám có phục vụ khám bênh bạn có thể đi vào buổi chiều"

similarity = SequenceMatcher(
    None, text1, text2
).ratio()

print(similarity)