import random
print("Welcome to number guessing game!")
num = int(input("Enter the upper limit for the guessing range: "))
random_number = random.randint(1, num)
guess = None
while guess != random_number:
    guess = int(input(f"Guess a number between 1 and {num}:"))
    if guess < random_number:
        print("The number is too low. Try again!")
    elif guess > random_number:
        print("The number is too high. Try again!")
    else:
        print("Congratulations! You've guessed the correct number!")
print(f"The random number was: {random_number}")
print("Thank you for playing the number guessing game!")