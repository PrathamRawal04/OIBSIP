import random
import string

def generate_cli_password():
    print("--- Python Random Password Generator (Beginner CLI) ---")
    
    # 1. Length validation (minimum 8 characters)
    while True:
        try:
            length = int(input("Enter password length (minimum 8): "))
            if length < 8:
                print("Error: Password length must be at least 8 characters.")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid numeric integer.")

    # 2. Character type selection
    print("\nSelect character types to include:")
    use_upper = input("Include uppercase letters (A-Z)? (y/n): ").lower() == 'y'
    use_lower = input("Include lowercase letters (a-z)? (y/n): ").lower() == 'y'
    use_nums = input("Include numbers (0-9)? (y/n): ").lower() == 'y'
    use_syms = input("Include symbols (!@#$%^&*): ").lower() == 'y'

    # Ensure at least 2 types are selected
    selected_types = sum([use_upper, use_lower, use_nums, use_syms])
    if selected_types < 2:
        print("\n[Notice] You selected fewer than 2 types. Automatically enabling lowercase and numbers for security.")
        use_lower, use_nums = True, True

    # Build character pool
    char_pool = ""
    if use_upper: char_pool += string.ascii_uppercase
    if use_lower: char_pool += string.ascii_lowercase
    if use_nums: char_pool += string.digits
    if use_syms: char_pool += string.punctuation

    # Generate password
    password = "".join(random.choice(char_pool) for _ in range(length))
    print(f"\nGenerated Password: {password}")

if __name__ == "__main__":
    while True:
        generate_cli_password()
        again = input("\nGenerate another password? (y/n): ").lower()
        if again != 'y':
            print("Goodbye!")
            break
        print("\n" + "="*40 + "\n")