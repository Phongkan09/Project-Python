class Rectangle:
    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)
    
    def set_width(self, width):
        self.width = width
    def set_height(self, height):
        self.height = height
        
    #คำนวณพืื้นที่ (width * height$)
    def get_area(self):
        return self.width * self.height

    #คำนวณเส้นรอบรูป  (2 * width + 2 * height$)
    def get_perimeter(self):
        return 2*self.width + 2*self.height

    #คำนวณเส้นทแยงมุม ((width^2 + height^2)^{0.5})
    def get_diagonal(self):
        return ((self.width**2 + self.height**2)**0.5)

    def get_picture(self):
        if self.width > 50 or self.height > 50:
            return "Too big for picture."

        picture = ("*" * self.width + "\n") * self.height
        return picture
    
    def get_amount_inside(self, shape):
        fit_width = self.width // shape.width
        fit_height = self.height // shape.height
        
        return fit_width * fit_height
    
    def __str__(self):
        return (f"Rectangle(width={self.width}, height={self.height})")

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
        
    def set_side(self, side):
        self.width = side
        self.height = side
    
    def set_width(self, width):
        self.width = width
        self.height = width
    def set_height(self, height):
        self.height = height
        self.width = height
    
    def __str__(self):
        return (f"Square(side={self.width})")



bigbox = Rectangle(8,4)
smallbox = Rectangle(4,4)

sq = Square(10)
print(sq)