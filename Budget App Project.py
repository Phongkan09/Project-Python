class Category:
    
    def __init__(self, name):
        self.name = name
        self.ledger = []
        
    def deposit(self, amount, description = ""):
        self.ledger.append({"amount" : amount, "description" : description})
    def get_balance(self):
        total = 0
        for i in self.ledger:
            total += i["amount"]
        return total
    def check_funds(self, amount):
        if self.get_balance() < amount:
            return False
        else:
            return True
    def withdraw(self, amount, description = ""):
        if self.check_funds(amount):
            self.ledger.append({"amount" : -amount, "description": description})
            return True
        else:
            return False
    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        else:
            return False
        
    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        
        for item in self.ledger:
            desc = f"{item['description'][:23]:<23}"
            amt = f"{item['amount']:>7.2f}"
            items += f"{desc}{amt}\n"
            
        total_str = f"Total: {self.get_balance()}"
        return title + items + total_str
        
        
def create_spend_chart(categories):
    spent_amounts = []
    
    # --- เฟส 1: คำนวณเงินและเปอร์เซ็นต์ ---
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])  # ดึงมาเฉพาะยอดที่จ่าย
        spent_amounts.append(spent)
        
    total_spent = sum(spent_amounts)
    
    percentages = []
    for amount in spent_amounts:
        # สูตรปัดเศษลงหาหลักสิบที่ชัวร์ที่สุด
        percent = int((amount / total_spent) * 100 // 10 * 10)
        percentages.append(percent)
        
    # --- เฟส 2: วาดแกน Y และแท่งกราฟ ---
    chart = "Percentage spent by category\n"
    for value in range(100, -1, -10):
        chart += f"{value:>3}| "
        
        for percent in percentages:
            if percent >= value:
                chart += "o  "  # <- บังคับมีตัว o และเว้นวรรค 2 ทีเป๊ะๆ
            else:
                chart += "   "  # <- บังคับเว้นวรรค 3 ทีเป๊ะๆ
        chart += "\n"
        
    # --- เฟส 3: เส้นฐานและชื่อหมวดหมู่ ---
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"
    
    max_length = 0
    for category in categories:
        if len(category.name) > max_length:
            max_length = len(category.name)
            
    for i in range(max_length):
        chart += "     "  # <- บังคับเว้นขอบซ้าย 5 ช่องเป๊ะๆ
        for category in categories:
            if i < len(category.name):
                chart += category.name[i] + "  "  # <- ตัวอักษร + เว้นวรรค 2 ที
            else:
                chart += "   "  # <- เว้นวรรค 3 ที
        
        # ป้องกันไม่ให้มี \n (ขึ้นบรรทัดใหม่) เกินมาในบรรทัดสุดท้าย
        if i < max_length - 1:
            chart += "\n"
            
    return chart