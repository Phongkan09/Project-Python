import os
import sys
import io
import re
import datetime
import time
import ctypes
from prompt_toolkit import prompt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


class BackToMenu(Exception):
    """Unwinds nested menu prompts back to the main menu without growing the call stack."""
    pass


class LogoutRequested(Exception):
    """Unwinds out of the menu session back to the register/login screen."""
    pass


class Account :
    def __init__(self, account, password) :
        self.account = account
        self.password = password
        
        prefix = "." if os.name != "nt" else ""
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.current_dir, f"{prefix}accounts.txt")
        
    def register(self) :
        with open(self.file_path, "a", encoding="utf-8") as file :
            file.write(f"{self.account},{self.password}\n")
            
        if os.name == 'nt':
            ctypes.windll.kernel32.SetFileAttributesW(self.file_path, 2)
            
    def check_register(self) :
        if not os.path.exists(self.file_path):
            return True
        
        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    check_account = parts[0]
                    if self.account == check_account:
                        return False
        return True
            
    def check_login(self) :
        if not os.path.exists(self.file_path):
            print("❌ ไม่พบฐานข้อมูล กรุณาสมัครสมาชิกก่อน!")
            return False
        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    saved_account = parts[0]
                    saved_password = parts[1]

                    if (
                        self.account == saved_account
                        and str(self.password) == saved_password
                    ):
                        return True
        return False
    
###########################################################################################################################
# รหัสสินค้า (ID), ชื่อสินค้า, ราคา, และจำนวนสต็อกเริ่มต้น
class Product :
    def __init__(self, product_id, name, price, stock):
        self.product_id = str(product_id).strip()
        self.name = str(name).strip()
        self.price = float(price)
        self.stock = int(stock)

    def to_csv_format(self):
        return f"{self.product_id}, {self.name}, {self.price}, {self.stock}\n"
    
class Inventory :
    def __init__(self):
        if getattr(sys, 'frozen', False):
            self.current_dir = os.path.dirname(sys.executable)
        else:
            self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
        prefix = "." if os.name != "nt" else ""
        self.inv_file = os.path.join(self.current_dir, f"{prefix}inventory.txt")
        self.sales_file = os.path.join(self.current_dir, f"{prefix}sales_history.txt")
        
    def add_new_product(self, product):
        if not is_valid_product_id(product.product_id):
            line()
            print(f"\n❌ รหัสสินค้า '{product.product_id}' ต้องมีตัวอักษรได้แค่ 1 ตัวด้านหน้าเท่านั้น และส่วนที่เหลือต้องเป็นตัวเลขทั้งหมด")
            line()
            return False

        if os.path.exists(self.inv_file):
            with open(self.inv_file, "r", encoding="utf-8") as file:
                for existing_line in file:
                    parts = existing_line.strip().split(",")
                    if len(parts) >= 1:
                        saved_id = parts[0]
                        if product.product_id == saved_id:
                            line()
                            print(f"❌ รหัสสินค้า '{product.product_id}' มีอยู่ในระบบแล้ว กรุณาใช้รหัสอื่น!")
                            line()
                            return False
        with open(self.inv_file, "a", encoding="utf-8") as file :
            file.write(product.to_csv_format())
            
        if os.name == 'nt':
            ctypes.windll.kernel32.SetFileAttributesW(self.inv_file, 2)
            
        print(f"\n✅ เพิ่มสินค้า '{product.name}' ลงคลังสำเร็จ!")
        return True
    
    def view_inventory(self):
        print("=" * 100 + "\n")
        line()
        print("\t\t\t\t--- 📦 คลังสินค้าทั้งหมด ---\t\t")
        line()
        if not os.path.exists(self.inv_file):
            print("\tยังไม่มีสินค้าในคลัง กรุณาเพิ่มสินค้าก่อน\n")
            line()
            sys.stdout.flush()
            time.sleep(1.2)
            return
        print(f"{'รหัสสินค้า':<10} | {'ชื่อสินค้า':<25} | {'ราคา (บาท)':<10} | {'สต็อกคงเหลือ':<12} | {'สถานะ'}")
        line()
        with open(self.inv_file, "r", encoding="utf-8") as file:
            for part in file:
                parts = part.strip().split(",")
                if len(parts) >= 4:
                    prod_id = parts[0]
                    prod_name = parts[1]
                    price = float(parts[2])
                    stock = int(parts[3])

                    if stock == 0:
                        status = "❌ หมด! (Out of Stock)"
                    elif stock < 5:
                        status = "⚠️ Low Stock!"
                    else :
                        status = "🟢 ปกติ"
                    print(f"{prod_id:<10} | {prod_name:<25} | {price:<10.2f} | {stock:<12} | {status}")
        print("\n")
        print("=" * 100 + "\n")
        sys.stdout.flush()
        time.sleep(1.5)

    def view_sales_history(self):
        print("=" * 100 + "\n")
        line()
        print("\t\t\t\t--- 🧾 ประวัติการขายทั้งหมด ---\t\t")
        line()
        if not os.path.exists(self.sales_file):
            print("\tยังไม่มีประวัติการขาย\n")
            line()
            sys.stdout.flush()
            time.sleep(1.2)
            return
        print(f"{'วันที่/เวลา':<20} | {'รหัสสินค้า':<10} | {'ชื่อสินค้า':<25} | {'จำนวน':<8} | {'ยอดรวม (บาท)'}")
        line()
        with open(self.sales_file, "r", encoding="utf-8") as file:
            for entry in file:
                parts = entry.strip().split(",")
                if len(parts) >= 5:
                    timestamp = parts[0]
                    prod_id = parts[1]
                    prod_name = parts[2]
                    qty = parts[3]
                    total = float(parts[4])
                    print(f"{timestamp:<20} | {prod_id:<10} | {prod_name:<25} | {qty:<8} | {total:.2f}")
        print("\n")
        print("=" * 100 + "\n")
        sys.stdout.flush()
        time.sleep(1.5)

    def check_inv_stock(self, id):
        if not os.path.exists(self.inv_file):
            line()
            print("❌ ยังไม่มีสินค้าในคลัง กรุณาเพิ่มสินค้าก่อน")
            line()
            return False
        with open(self.inv_file, "r", encoding="utf-8") as file:
            for inv_line in file:
                parts = inv_line.strip().split(",")
                if len(parts) >= 4:
                    prod_id = parts[0]
                    prod_name = parts[1]
                    up_stock = int(parts[3])
                    if id == prod_id: 
                        line()
                        return f"✅ พบสินค้า: {prod_name} (สต็อกปัจจุบัน: {up_stock} ชิ้น)"
                        
        # ถ้าวนลูปจนจบไฟล์แล้วหลุดลงมาตรงนี้ แปลว่า "ไม่เจอ!"
        line()
        print("❌ ไม่พบสินค้ารหัสนี้ กรุณาลองอีกครั้ง...")
        line()
        return False
                
    def update_inv_stock(self, code, id, amount):
        if not is_valid_int_value(amount):
            print("❌ จำนวนต้องเป็นตัวเลขจำนวนเต็มเท่านั้น!")
            return False

        if not os.path.exists(self.inv_file):
            print("❌ ยังไม่มีสินค้าในคลัง กรุณาเพิ่มสินค้าก่อน")
            return False

        amount = int(amount)
        lines = []
        is_success = False

        # 1. ดูดข้อมูลมาพัก
        with open(self.inv_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        updated_lines = []
        # 2. ซักให้สะอาด (หาบรรทัดที่จะแก้ แล้วบวกลบเลข)
        for line_data in lines:
            parts = line_data.strip().split(",")
            if len(parts) >= 4 and parts[0] == id:
                prod_id = parts[0]
                prod_name = parts[1]
                price = float(parts[2])
                stock = int(parts[3])

                if code == "1":
                    stock += amount
                    is_success = True
                    print(f"\n✅ เพิ่มสต็อก '{prod_name}' จำนวน {amount} ชิ้น สำเร็จ! (สต็อกใหม่: {stock})")
                elif code == "2":
                    if stock >= amount:
                        stock -= amount
                        is_success = True
                        print(f"\n✅ ลดสต็อก '{prod_name}' จำนวน {amount} ชิ้น สำเร็จ! (สต็อกใหม่: {stock})")
                    else:
                        print(f"\n❌ สต็อกไม่พอ! (มีอยู่แค่ {stock} ชิ้น)")
                        line()
                        return False
                elif code == "3":
                    if stock >= amount:
                        stock -= amount
                        is_success = True
                        current_time = datetime.datetime.now()
                        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                        
                        print(f"\n✅ อัปเดตการขายสินค้า '{prod_name}' จำนวน {amount} ชิ้น สำเร็จ! (สต็อกใหม่: {stock})")
                        self.sale_record = f"{timestamp},{prod_id},{prod_name},{amount},{price * amount}\n"
                        line()
                    else:
                        print(f"\n❌ สินค้าในคลังไม่เพียงพอ! (มีอยู่แค่ {stock} ชิ้น)")
                        print("กรุณาลองอีกครั้ง...")
                        line()
                        return False

                updated_lines.append(f"{prod_id},{prod_name},{price},{stock}\n")
            else:
                updated_lines.append(line_data)

        # 3. สาดทับที่เดิม
        if is_success:
            with open(self.inv_file, "w", encoding="utf-8") as file:
                file.writelines(updated_lines)
            return True
            
        return False
    
    def save_sale_history(self):
        with open(self.sales_file, "a", encoding="utf-8") as file:
            file.writelines(self.sale_record)
        print("✅ บันทึกข้อมูลการขายเสร็จสิ้น กำลังกลับหน้าเมนูหลัก...")
    
                        
                
                    
                    
###########################################################################################################################
    
def line() :
    print("______________________________________________________________________________________________________\n")


def is_valid_product_id(product_id):
    return bool(re.fullmatch(r"[A-Za-z]?\d+", str(product_id).strip()))


def is_valid_int_value(value):
    return bool(re.fullmatch(r"\d+", str(value).strip()))


def register():
    while True:
        out_loop = False
        while True:  # register name
            line()
            print("\t\t-- หมายเหตุ --")
            print("""               
            - ถ้าต้องการกลับหน้าเดิม ให้พิมพ์ 0 ในช่อง <ชื่อบัญชี>
            - รหัสผ่านเป็นตัวเลขเท่านั้น
                """)
            user_acc = input("ชื่อบัญชี: ").strip()
            if user_acc == "0":
                print("\n⬅️ ยกเลิกการสมัคร กลับสู่หน้าหลัก...")
                line()
                out_loop = True
                sys.stdout.flush()
                time.sleep(1)
                break
            if user_acc != "":
                break
            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            sys.stdout.flush()
            time.sleep(0.5)

        if out_loop:
            break

        while True:  # register password
            user_pass = input("รหัสผ่าน: ").strip()
            if user_pass == "":
                print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
                sys.stdout.flush()
                time.sleep(0.5)
            elif not user_pass.isdigit():
                print("❌ รหัสผ่านต้องเป็น 'ตัวเลข' เท่านั้น กรุณาลองอีกครั้ง...\n")
                sys.stdout.flush()
                time.sleep(0.5)
            else:
                break

        account = Account(user_acc, user_pass)
        if account.check_register():  # เงื่อนไข check ชื่อซ้ำ
            account.register()
            print("✅ สมัครสมาชิกสำเร็จ กรุณาเข้าสู่ระบบอีกครั้ง")
            line()
            sys.stdout.flush()
            time.sleep(1)
            break
        else:
            print("❌ ชื่อนี้มีผู้ใช้แล้ว กรุณาตั้งใหม่")
            sys.stdout.flush()
            time.sleep(0.8)


def login():
    while True:
        out_loop = False
        while True:
            line()
            print("\t\t-- หมายเหตุ --")
            print("""
            - ถ้าต้องการกลับหน้าเดิม ให้พิมพ์ 0 ในช่อง <ชื่อบัญชี>
            - รหัสผ่านเป็นตัวเลขเท่านั้น
                """)
            user_acc = input("ชื่อบัญชี: ").strip()
            if user_acc == "0":
                print("\n⬅️ ยกเลิกการเข้าสู่ระบบ กลับสู่หน้าหลัก...")
                line()
                out_loop = True
                sys.stdout.flush()
                time.sleep(1)
                break
            if user_acc != "":
                break
            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            sys.stdout.flush()
            time.sleep(0.5)

        if out_loop:
            break

        while True: # login password
            user_pass = input("รหัสผ่าน: ").strip()
            if user_pass == "":
                print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
                sys.stdout.flush()
                time.sleep(0.5)
            elif not user_pass.isdigit():
                print("❌ รหัสผ่านต้องเป็นตัวเลขเท่านั้น...\n")
                sys.stdout.flush()
                time.sleep(0.5)
            else:
                break

        account = Account(user_acc, user_pass)
        if account.check_login():  # เงื่อนไข check ชื่อและรหัสผ่าน
            line()
            print(f"✅ ยินดีต้อนรับ {account.account} เข้าสู่ระบบ!")
            sys.stdout.flush()
            time.sleep(1)
            try:
                while True:
                    try:
                        menu()
                    except BackToMenu:
                        continue
            except LogoutRequested:
                return  # กลับไปหน้า Register/Login
        else:
            print("❌ ชื่อบัญชีหรือรหัสผ่านไม่ถูกต้อง!")
            sys.stdout.flush()
            time.sleep(0.5)

def reg_login() : 
    while True:
        print("=== ระบบ Expense Tracker ===")
        print("""
            --- Code ---
            [1] : Register
            [2] : Login
            [0] : Exit
            """)
        code = input("Code : ").strip()
        match code:
            case "1":
                register()
            case "2":
                login() 
            case "0":
                line()
                print("ปิดระบบ")
                line()
                sys.stdout.flush()
                time.sleep(1)
                sys.exit()
            case _:
                line()
                print("❌ Code ไม่ถูกต้อง กรุณาลองอีกครั้ง")
                line()
                sys.stdout.flush()
                time.sleep(0.5)
                
###########################################################################################################################
                
def menu() :
    while True :
        print("\t\t--- Main Menu ---")
        print("""
            [1] เพิ่มสินค้าใหม่
            [2] อัปเดตสต็อก
            [3] บันทึกการขาย
            [4] ดูคลังสินค้า
            [5] ดูประวัติยอดขาย
            [6] Logout
            [0] ออกจากระบบ
            """)
        code_menu = input("เลือกรายการ : ")
        match code_menu:
            case "1":
                add_Product(code_menu)
            case "2":
                check_code(code_menu)
            case "3":
                check_code(code_menu)
            case "4":
                view_all = Inventory()
                view_all.view_inventory()
            case "5":
                view_sales = Inventory()
                view_sales.view_sales_history()
            case "6":
                line()
                print("⌛ กำลังออกจากระบบ...")
                line()
                sys.stdout.flush()
                time.sleep(0.8)
                raise LogoutRequested()
            case "0":
                line()
                print("ปิดระบบ")
                line()
                sys.stdout.flush()
                time.sleep(1)
                sys.exit()
            case _:
                line()
                print("❌ Code ไม่ถูกต้อง กรุณาลองอีกครั้ง")
                line()
                sys.stdout.flush()
                time.sleep(0.5)
                
                
                
def sub_menu(code_menu, id=None, name=None,price=None, stock=None):
    out_loop = False
    while True :
        match code_menu:
            case "1":
                print(">> โปรดเลือกรายการต่อไป\n")
                print("""
                    [1] แก้ไขรายการสินค้า
                    [2] ดำเนินการเพิ่มสินค้า
                    [0] ยกเลิกการทำรายการ
                    """)
                code = input("Code : ")
                match code:
                    case "1":
                        line()
                        id, name, price, stock = edit(code_menu, id, name, price, stock)
                    case "2":
                        new_item = Product(id, name, price, stock)
                        manager = Inventory()
                        if manager.add_new_product(new_item):
                            line()
                            print("⌛ ทำรายการเสร็จสิ้น กลับสู่เมนูหลัก...")
                            line()
                            sys.stdout.flush()
                            time.sleep(1)
                            raise BackToMenu()
                    case "0":
                        line()
                        print("⌛ ยกเลิกการทำรายการ กลับสู่เมนูหลัก...")
                        line()
                        sys.stdout.flush()
                        time.sleep(0.8)
                        raise BackToMenu()
                    case _:
                        line()
                        print("❌ Code ไม่ถูกต้อง กรุณาลองอีกครั้ง")
                        line()
                        sys.stdout.flush()
                        time.sleep(0.5)
            case "2":
                print(">> โปรดเลือกรายการต่อไป\n")
                print("""
                    [1] เพิ่มสต็อก
                    [2] ลดสต็อก
                    [0] ยกเลิกการทำรายการ
                    """)
                code = input("Code : ").strip()
                if code in ["1", "2"]:
                    line()
                    action_text = "เพิ่ม" if code == "1" else "ลด"
                    amount = input(f"ต้องการ{action_text}สต็อก (ชิ้น) : ")
                    
                    update = Inventory()
                    if update.update_inv_stock(code, id, amount): # ส่งค่าไปอัปเดตไฟล์
                        line()
                        print("⌛ ทำรายการเสร็จสิ้น กลับสู่เมนูหลัก...")
                        line()
                        sys.stdout.flush()
                        time.sleep(1)
                        raise BackToMenu()
                elif code == "0":
                    line()
                    print("⌛ ยกเลิกการทำรายการ กลับสู่เมนูหลัก...")
                    line()
                    sys.stdout.flush()
                    time.sleep(0.8)
                    raise BackToMenu()
                else:
                    line()
                    print("❌ Code ไม่ถูกต้อง กรุณาลองอีกครั้ง")
                    line()
                    sys.stdout.flush()
                    time.sleep(0.5)
            case "3":
                while True:
                    sale = input("\tระบุจำนวนการขาย : ")
                    if sale == "":
                        print("\n❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...")
                        sys.stdout.flush()
                        time.sleep(0.5)
                        line()
                    elif not is_valid_int_value(sale):
                        print("\n❌ จำนวนการขาย ต้องเป็นตัวเลขจำนวนเต็มเท่านั้น กรุณาลองอีกครั้ง...")
                        sys.stdout.flush()
                        time.sleep(0.5)
                        line()
                    else:
                        sale_stock = Inventory()
                        if sale_stock.update_inv_stock("3", id, sale):
                            print("⌛ กำลังบันทึกข้อมูลการขาย...\n")
                            sys.stdout.flush()
                            time.sleep(0.5)
                            sale_stock.save_sale_history()
                            sys.stdout.flush()
                            time.sleep(0.8)
                            out_loop = True
                            line()
                        break
                    
                if out_loop:
                    break

def edit(code_menu, id, name, price, stock) :
    print("-- แก้ไข --")
    while True:    
        id = prompt("รหัสสินค้า : ", default=id)
        if id != "":
            break
        else :
            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            sys.stdout.flush()
            time.sleep(0.5)
    while True:
        name = prompt("ชื่อสินค้า : ", default=name)
        if name != "":
            break
        else :
            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            sys.stdout.flush()
            time.sleep(0.5)
    while True:
        price = prompt("ราคาต่อชิ้น (บาท) : ", default=price)
        if price == "":
            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            sys.stdout.flush()
            time.sleep(0.5)
        elif not is_valid_int_value(price):
            print("❌ ราคา ต้องเป็นจำนวนเต็มบวกเท่านั้น เช่น 10, 100, 250\n")
            sys.stdout.flush()
            time.sleep(0.5)
        else:
            break
    while True:
        stock = prompt("สต็อกเริ่มต้น (ชิ้น) : ", default=stock)
        if stock == "":
            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            sys.stdout.flush()
            time.sleep(0.5)
        elif not is_valid_int_value(stock):
            print("❌ สต็อก ต้องเป็นจำนวนเต็มบวกเท่านั้น เช่น 1, 10, 100\n")
            sys.stdout.flush()
            time.sleep(0.5)
        else:
            break
    line()
    print("ตรวจสอบรายการของท่าน >>\n")
    print("\t-- Product --")
    print(f"ID : {id}")
    print(f"Name : {name}")
    print(f"Price : {price} บาท")
    print(f"Stock : {stock} ชิ้น")
    line()
    sys.stdout.flush()
    time.sleep(1.5)
    return id, name, price, stock
            
def check_back(code_menu) :
    while True :
        match code_menu:
            case "1":
                line()
                print("-- เพิ่มสินค้าใหม่ --")
            case "2":
                line()
                print("-- อัปเดตสต็อก --")
            case "3":
                line()
                print("-- บันทึกการขาย --")
        
        print("\t\t-- หมายเหตุ --")
        print("""
        - พิมพ์ 1 เมื่อต้องการทำรายการต่อ
        - พิมพ์ 0 เมื่อต้องการยกเลิกการทำรายการ หรือ กลับหน้า Menu
            """)
        check = input("<<< Back ? : ")
        match check :
            case "1":
                line()
                break
            case "0":
                line()
                print("⌛ กำลังกลับหน้าเมนู...")
                line()
                sys.stdout.flush()
                time.sleep(0.8)
                raise BackToMenu()
            case _ :
                line()
                print("❌ Code ไม่ถูกต้อง กรุณาลองอีกครั้ง")
                line()
                sys.stdout.flush()
                time.sleep(0.5)
    
######################################################################################################################  
                    
def add_Product(code_menu) :
    check_back(code_menu)
    while True:    
        prod_id = input("รหัสสินค้า : ").strip()
        if prod_id == "":
            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            sys.stdout.flush()
            time.sleep(0.5)
        elif not is_valid_product_id(prod_id):
            print("❌ รหัสสินค้า ต้องมีตัวอักษรได้แค่ 1 ตัวด้านหน้าเท่านั้น และส่วนที่เหลือต้องเป็นตัวเลขทั้งหมด\n")
            sys.stdout.flush()
            time.sleep(0.5)
        else:
            break
    while True:
        prod_name = input("ชื่อสินค้า : ")
        if prod_name != "":
            break
        else :
            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            sys.stdout.flush()
            time.sleep(0.5)
    while True:
        prod_price = input("ราคาต่อชิ้น (บาท) : ")
        if prod_price == "":
            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            sys.stdout.flush()
            time.sleep(0.5)
        elif not is_valid_int_value(prod_price):
            print("❌ ราคา ต้องเป็นจำนวนเต็มบวกเท่านั้น เช่น 10, 100, 250\n")
            sys.stdout.flush()
            time.sleep(0.5)
        else:
            break
    while True:
        prod_stock = input("สต็อกเริ่มต้น (ชิ้น) : ")
        if prod_stock == "":
            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            sys.stdout.flush()
            time.sleep(0.5)
        elif not is_valid_int_value(prod_stock):
            print("❌ สต็อก ต้องเป็นจำนวนเต็มบวกเท่านั้น เช่น 1, 10, 100\n")
            sys.stdout.flush()
            time.sleep(0.5)
        else:
            break
    
    line()
    print("ตรวจสอบรายการของท่าน >>\n")
    print("\t-- Product --")
    print(f"ID : {prod_id}")
    print(f"Name : {prod_name}")
    print(f"Price : {prod_price} บาท")
    print(f"Stock : {prod_stock} ชิ้น\n")
    line()
    sys.stdout.flush()
    time.sleep(1.5)

    sub_menu(code_menu, prod_id, prod_name, prod_price, prod_stock)
    
def check_code(code_menu):
    check_back(code_menu)
    while True :
        id = input("โปรดระบุรหัสสินค้าที่ต้องการอัปเดตข้อมูล : ").strip()
        update = Inventory()
        
        # เก็บผลลัพธ์ไว้ในตัวแปร result จะได้ไม่ต้องเรียกฟังก์ชันซ้ำ
        result = update.check_inv_stock(id) 
        
        if result: # ถ้าเจอสินค้า (result ไม่ใช่ False)
            print(result)
            line()
            sub_menu(code_menu, id)
            break # หลุดจากลูปเพื่อไป sub_menu


if __name__ == "__main__":
    reg_login()
