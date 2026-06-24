def arithmetic_arranger(problems, show_answers=False):
    if(len(problems) > 5):
        return "Error: Too many problems."
    
    first_lines = []
    second_lines = []
    dash_lines = []
    answer_lines = []
    
    for problem in problems:
        part = problem.split()
        
        num1 = part[0]
        operator = part[1]
        num2 = part[2]
        
        if operator != "+" and operator != "-" :
            return "Error: Operator must be '+' or '-'."
        if not num1.isdigit() or not num2.isdigit() :
            return "Error: Numbers must only contain digits."
        if len(num1) > 4 or len(num2) > 4 :
            return "Error: Numbers cannot be more than four digits."
        
        width = max(len(num1), len(num2)) + 2
        top = num1.rjust(width)
        bottom = operator + " " + num2.rjust(width - 2)
        line = "-" * width
    
        first_lines.append(top)
        second_lines.append(bottom)
        dash_lines.append(line)
        
        if operator == "+":
            ans = str(int(num1) + int(num2))
        else:
            ans = str(int(num1) - int(num2))
        answer_lines.append(ans.rjust(width))
        
    row1 = "    ".join(first_lines)
    row2 = "    ".join(second_lines)
    row3 = "    ".join(dash_lines)
    row4 = "    ".join(answer_lines)
        
    if show_answers == True:
        return row1 + "\n" + row2 + "\n" + row3 + "\n" + row4
    else:
        return row1 + "\n" + row2 + "\n" + row3

print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49"])}')