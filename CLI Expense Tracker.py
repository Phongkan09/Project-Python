import os
import sys
import io
import datetime
import time
import ctypes
from prompt_toolkit import prompt

"""
exe file, os, sys, ctypes, set file, 'nt'
"""


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")


class Account:
    def __init__(self, account, password):
        self.account = str(account)
        self.password = password
        prefix = "." if os.name != "nt" else ""
        if getattr(sys, 'frozen', False):
            self.current_dir = os.path.dirname(sys.executable) # กรณีเป็น .exe
        else:
            self.current_dir = os.path.dirname(os.path.abspath(__file__)) # กรณีเป็น .py
        self.file_path = os.path.join(self.current_dir, f"{prefix}accounts.txt")

    def check_register(self):  # Check accounts
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

    def register(self):  # buil account
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(f"{self.account},{self.password}\n")
            
        if os.name == 'nt':
            ctypes.windll.kernel32.SetFileAttributesW(self.file_path, 2)

    def check_login(self):
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


class Transaction:
    def __init__(self, description, amount, date, account):
        self.description = description
        self.amount = amount
        self.date = date
        self.account = account
        prefix = "." if os.name != "nt" else ""
        if getattr(sys, 'frozen', False):
            self.current_dir = os.path.dirname(sys.executable) # กรณีเป็น .exe
        else:
            self.current_dir = os.path.dirname(os.path.abspath(__file__)) # กรณีเป็น .py
        self.file_data = os.path.join(self.current_dir, f"{prefix}{self.account}_data.txt")

    def income(self):
        self.type = "income"
        with open(self.file_data, "a", encoding="utf-8") as file:
            file.write(f"{self.date},{self.description},{self.amount},{self.type}\n")
            
        if os.name == 'nt':
            ctypes.windll.kernel32.SetFileAttributesW(self.file_data, 2)

    def expense(self):
        self.type = "expense"
        with open(self.file_data, "a", encoding="utf-8") as file:
            file.write(f"{self.date},{self.description},{self.amount},{self.type}\n")
            
        if os.name == 'nt':
            ctypes.windll.kernel32.SetFileAttributesW(self.file_data, 2)

    def show_balance(self):
        total_income = 0
        total_expense = 0
        
        if not os.path.exists(self.file_data):
            print(f"\n💳 ยอดเงินคงเหลือของ {self.account}: 0.00 บาท (ยังไม่มีประวัติการทำรายการ)")
            return
        with open(self.file_data, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    amount = parts[2]
                    type = parts[3]
                    if type == "income":
                        total_income += int(amount)
                    elif type == "expense":
                        total_expense += int(amount)
        
        total_balance = total_income - total_expense
        
        print("\n\t\t==== 📊 สรุปยอดบัญชี ====")
        print(f"\t\tชื่อบัญชี: {self.account}")
        print(f"\t\t📈 รายรับทั้งหมด: {total_income:,.2f} บาท")
        print(f"\t\t📉 รายจ่ายทั้งหมด: {total_expense:,.2f} บาท")
        print(f"\t\t💳 ยอดเงินคงเหลือ: {total_balance:,.2f} บาท")
        print("\t\t=======================\n")
    
    def show_history(self):
        if not os.path.exists(self.file_data):
            print(f"\n\t\t\t❌ ยังไม่มีประวัติการทำรายการสำหรับบัญชี {self.account}")
            return
        
        print("\n==== ประวัติการทำรายการ ====")
        print(f"{'วันที่และเวลา':<22} | {'รายละเอียด':<15} | {'จำนวนเงิน':<10} | {'ประเภท'}")
        print("-" * 70)
        
        with open(self.file_data, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    trans_date = parts[0]
                    trans_desc = parts[1]
                    trans_amount = float(parts[2])
                    trans_type = "รายรับ 🟢" if parts[3] == "income" else "รายจ่าย 🔴"
                    
                    print(f"{trans_date:<22} | {trans_desc:<15} | {trans_amount:<10,.2f} | {trans_type}")
                    
        print("=" * 70 + "\n")
                

#####################################################################################################################

def line():
    print("__________________________________________________________\n")


def register():
    while True:
        out_loop = False
        while True:  # register name
            line()
            print("-- หมายเหตุ --")
            print("""               
                - ถ้าต้องการกลับหน้าเดิม ให้พิมพ์ 0 ในช่อง <ชื่อบัญชี>
                - รหัสผ่านเป็นตัวเลขเท่านั้น
                """)
            user_acc = input("ชื่อบัญชี: ").strip()
            if user_acc == "0":
                print("\n⬅️ ยกเลิกการสมัคร กลับสู่หน้าหลัก...")
                line()
                out_loop = True
                break
            if user_acc != "":
                break
            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            
        if out_loop:
            break
            
        while True:  # register password
            user_pass = input("รหัสผ่าน: ").strip()
            if user_pass == "":
                print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            elif not user_pass.isdigit():
                print("❌ รหัสผ่านต้องเป็น 'ตัวเลข' เท่านั้น กรุณาลองอีกครั้ง...\n")
            else:
                break
                
        act = Account(user_acc, user_pass)
        if act.check_register():  # เงื่อนไข check ชื่อซ้ำ
            act.register()
            print("✅ สมัครสมาชิกสำเร็จ กรุณาเข้าสู่ระบบอีกครั้ง")
            line()
            break
        else:
            print("❌ ชื่อนี้มีผู้ใช้แล้ว กรุณาตั้งใหม่")


def login():
    while True:
        out_loop = False
        while True:
            line()
            print("""-- หมายเหตุ --
                                    
                - ถ้าต้องการกลับหน้าเดิม ให้พิมพ์ 0 ในช่อง <ชื่อบัญชี>
                - รหัสผ่านเป็นตัวเลขเท่านั้น
                """)
            user_acc = input("ชื่อบัญชี: ").strip()
            if user_acc == "0":
                print("\n⬅️ ยกเลิกการเข้าสู่ระบบ กลับสู่หน้าหลัก...")
                line()
                out_loop = True
                break
            if user_acc != "":
                break
            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            
        if out_loop:
            break
            
        while True: # login password
            user_pass = input("รหัสผ่าน: ").strip()  
            if user_pass == "":
                print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
            elif not user_pass.isdigit():
                print("❌ รหัสผ่านต้องเป็นตัวเลขเท่านั้น...\n")
            else:
                break
                
        act = Account(user_acc, user_pass)
        if act.check_login():  # เงื่อนไข check ชื่อและรหัสผ่าน
            line()
            print(f"✅ ยินดีต้อนรับ {act.account} เข้าสู่ระบบ!")
            transaction(user_acc)
        else:
            print("❌ ชื่อบัญชีหรือรหัสผ่านไม่ถูกต้อง!")


def reg_login():
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
                sys.exit()
            case _:
                line()
                print("❌ Code ไม่ถูกต้อง กรุณาลองอีกครั้ง")
                line()


#############################################################################################################


def transaction(account_name):
    while True:
        print("\t\t\t=== เมนูธุรกรรม ===")
        print("""
            --- Code ---
            [1] เพิ่มรายรับ
            [2] เพิ่มรายจ่าย
            [3] ดูสรุปยอดรวม (Balance)
            [4] ดูประวัติการทำรายการทั้งหมด
            [5] logout
            [0] ออกจากโปรแกรม
            """)
        code = input("Code : ").strip()
        match code:
            case "1":
                line()
                while True:
                    while True:
                        out_loop = False
                        print("\t\t\t--- เพิ่มรายการ <รายรับ> ---")
                        print("""
                                -- หมายเหตุ --
                                
                            - ถ้าต้องการยกเลิกรายการ ให้พิมพ์ 0 ในช่อง <Description>
                            - ถ้าไม่ต้องการใส่ Description สามารถพิมพ์ - ในช่อง <Description>
                            - ในส่วน amount ใส่แค่ตัวเลข
                            """)
                        description = input("Description: ").strip()
                        if description == "0":
                            print("\n⬅️ ยกเลิกการทำรายการ กลับสู่หน้าหลัก...")
                            line()
                            out_loop = True
                            break
                        if description != "":
                            break
                        print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
                        line()
                    if out_loop:
                        break

                    while True:
                        amount = input("Amount: ").strip()
                        if amount == "":
                            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
                        elif not amount.isdigit():
                            print("❌ ต้องเป็น 'ตัวเลข' เท่านั้น กรุณาลองอีกครั้ง...\n")
                        else:
                            break
                        line()
                    print("\n-- ทวนรายการ --")
                    print(f"{description}\t {amount}\n")
                    line()
                    out_loop = False

                    while True:
                        print("""
                            --- Code ---
                            [1] แก้ไข
                            [2] ดำเนินการต่อ
                            [0] ออกจากรายการ (ยกเลิกรายการ)
                            """)
                        code = input("Code : ").strip()
                        match code:
                            case "1":
                                line()
                                while True:
                                    print("-- แก้ไข --")
                                    description = prompt("Description: ", default=description)
                                    if description.strip() == "":
                                        print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
                                        line()
                                        continue
                                    break
                                while True:
                                    amount = prompt("Amount: ", default=str(amount))
                                    if amount.strip() == "":
                                        print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
                                        line()
                                        continue
                                    elif not amount.isdigit():
                                        print("❌ ต้องเป็น 'ตัวเลข' เท่านั้น กรุณาลองอีกครั้ง...\n")
                                        line()
                                        continue
                                        
                                    print("\n-- ทวนรายการ --")
                                    print(f"{description}\t {amount}\n")
                                    break
                            case "2":
                                line()
                                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                print("✅ ดำเนินการต่อ...")
                                tra = Transaction(description, amount, date, account_name)
                                tra.income()
                                print("✅ ทำรายการสำเร็จ")
                                line()
                                time.sleep(1)
                                out_loop = True
                                break
                            case "0":
                                line()
                                print("⬅️ ยกเลิกการทำรายการ กลับสู่หน้าหลัก...")
                                line()
                                out_loop = True
                                break
                            case _:
                                line()
                                print("❌ Code ไม่ถูกต้อง กรุณาลองอีกครั้ง")
                                line()
                                continue
                        if out_loop:
                            break
                    if out_loop:
                        break
            case "2":
                line()
                while True:
                    while True:
                        out_loop = False
                        print("\t\t\t--- เพิ่มรายการ <รายจ่าย> ---")
                        print("""
                                -- หมายเหตุ --
                                
                            - ถ้าต้องการยกเลิกรายการ ให้พิมพ์ 0 ในช่อง <Description>
                            - ถ้าไม่ต้องการใส่ Description สามารถพิมพ์ - ในช่อง <Description>
                            - ในส่วน amount ใส่แค่ตัวเลข
                            """)
                        description = input("Description: ").strip()
                        if description == "0":
                            print("\n⬅️ ยกเลิกการทำรายการ กลับสู่หน้าหลัก...")
                            line()
                            out_loop = True
                            break
                        if description != "":
                            break
                        print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
                        line()
                    if out_loop:
                        break

                    while True:
                        amount = input("Amount: ").strip()
                        if amount == "":
                            print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
                        elif not amount.isdigit():
                            print("❌ ต้องเป็น 'ตัวเลข' เท่านั้น กรุณาลองอีกครั้ง...\n")
                        else:
                            break
                        line()
                    print("\n-- ทวนรายการ --")
                    print(f"{description}\t {amount}\n")
                    line()
                    out_loop = False

                    while True:
                        print("""
                            --- Code ---
                            [1] แก้ไข
                            [2] ดำเนินการต่อ
                            [0] ออกจากรายการ (ยกเลิกรายการ)
                            """)
                        code = input("Code : ").strip()
                        match code:
                            case "1":
                                line()
                                while True:
                                    print("-- แก้ไข --")
                                    description = prompt("Description: ", default=description)
                                    if description.strip() == "":
                                        print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
                                        line()
                                        continue
                                    break
                                while True:
                                    amount = prompt("Amount: ", default=str(amount))
                                    if amount.strip() == "":
                                        print("❌ ห้ามปล่อยว่าง กรุณาลองอีกครั้ง...\n")
                                        line()
                                        continue
                                    elif not amount.isdigit():
                                        print("❌ ต้องเป็น 'ตัวเลข' เท่านั้น กรุณาลองอีกครั้ง...\n")
                                        line()
                                        continue
                                        
                                    print("\n-- ทวนรายการ --")
                                    print(f"{description}\t {amount}\n")
                                    break
                            case "2":
                                line()
                                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                print("✅ ดำเนินการต่อ...")
                                tra = Transaction(description, amount, date, account_name)
                                tra.expense()
                                print("✅ ทำรายการสำเร็จ")
                                line()
                                time.sleep(1)
                                out_loop = True
                                break
                            case "0":
                                line()
                                print("⬅️ ยกเลิกการทำรายการ กลับสู่หน้าหลัก...")
                                line()
                                out_loop = True
                                break
                            case _:
                                line()
                                print("❌ Code ไม่ถูกต้อง กรุณาลองอีกครั้ง")
                                line()
                                continue
                        if out_loop:
                            break
                    if out_loop:
                        break
            case "3":
                line()
                tra = Transaction("-", 0, "-", account_name)
                tra.show_balance()
                line()
                
                sys.stdout.flush()
                time.sleep(3)
            case "4":
                line()
                tra = Transaction("-", 0, "-", account_name)
                tra.show_history()
                line()
                
                sys.stdout.flush()
                input("กด Enter เพื่อกลับสู่เมนูหลัก...")
            case "5":
                line()
                print("👋 กำลังออกจากระบบ... กลับสู่หน้าหลัก")
                line()
                time.sleep(1)
                break
            case "0":
                line()
                print("ปิดระบบ ขอบคุณที่ใช้บริการครับ!")
                line()
                sys.exit()
            case _:
                line()
                print("❌ Code ไม่ถูกต้อง กรุณาลองอีกครั้ง")
                line()

reg_login()