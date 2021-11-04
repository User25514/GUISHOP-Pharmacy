def Calculator():
    print("Welcome to the Calculator")
    print("Enter your first number: ")
    num1 = float(input())
    print("Enter your second number: ")
    num2 = float(input())
    print("Enter your operator: ")
    operator = input()
    if operator == "+":
        print("The answer is: " + str(num1 + num2))
    elif operator == "-":
        print("The answer is: " + str(num1 - num2))
    elif operator == "*":
        print("The answer is: " + str(num1 * num2))
    elif operator == "/":
        print("The answer is: " + str(num1 / num2))
    else:
        print("Invalid operator")
Calculator()