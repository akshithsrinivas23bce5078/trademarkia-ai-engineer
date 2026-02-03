print("Pattern printing using loops")
print("--------------------------------")
print("Choose a pattern to print:")
print("1. Right-Angled Triangle")
print("2. Square")
print("3. Pyramid")
print("4. Diamond")
print("5. Exit")
choice = int(input("Enter your choice (1-5): "))
while choice != 5:
    if choice == 1:
        rows = int(input("Enter the number of rows for the triangle: "))
        for i in range(1, rows + 1):
            print('*' * i)
    elif choice == 2:
        size = int(input("Enter the size of the square: "))
        for i in range(size):
            print('* ' * size)  
    elif choice == 3:
        rows = int(input("Enter the number of rows for the pyramid: "))
        for i in range(rows):
            print(' ' * (rows - i - 1) + '* ' * (i + 1))    
    elif choice == 4:
        rows = int(input("Enter the number of rows for the diamond: "))
        for i in range(rows):
            print(' ' * (rows - i - 1) + '* ' * (i + 1))
        for i in range(rows - 2, -1, -1):
            print(' ' * (rows - i - 1) + '* ' * (i + 1))
    elif choice == 5:
        print("Exiting the program. Goodbye!")
    else:
        print("Invalid choice! Please select a valid option.")
    
    choice = int(input("\nEnter your choice (1-5): "))