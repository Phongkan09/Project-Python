import copy
import random

class Hat:
    def __init__(self, **kwargs):
        self.contents = []
        # แปลง Dictionary เป็น List ลูกบอล
        for color, amount in kwargs.items():
            for i in range(amount):
                self.contents.append(color)

    def draw(self, num_balls):
        # ดักทางคนโลภ: ถ้าสั่งหยิบเยอะกว่าหรือเท่ากับของที่มี
        if num_balls >= len(self.contents):
            all_balls = self.contents.copy()
            self.contents = []
            return all_balls
        
        # กรณีหยิบปกติ: สุ่มหยิบทีละลูกแล้วลบออกจากหมวก
        drawn_balls = []
        for i in range(num_balls):
            random_index = random.randrange(len(self.contents))
            drawn_balls.append(self.contents.pop(random_index))
            
        return drawn_balls

# ฟังก์ชันอยู่นอกคลาส Hat
def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    success_count = 0

    # วนลูปทดลองตามจำนวนรอบที่กำหนด
    for _ in range(num_experiments):
        hat_copy = copy.deepcopy(hat)
        
        drawn_balls = hat_copy.draw(num_balls_drawn)
        
        is_success = True
        for color, expected_amount in expected_balls.items():
            if drawn_balls.count(color) < expected_amount:
                is_success = False
                break # ถ้ามีสีไหนไม่ถึงเกณฑ์ ถือว่าการทดลองรอบนี้ล้มเหลว ให้หยุดเช็กสีอื่นทันที
        
        if is_success:
            success_count += 1

    # คำนวณความน่าจะเป็น = จำนวนครั้งที่สำเร็จ / จำนวนครั้งที่ทดลองทั้งหมด
    return success_count / num_experiments