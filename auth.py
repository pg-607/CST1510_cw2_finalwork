import bcrypt
import os
USER_DATA_FILE = "users.txt"
def hash_password(plain_text_password):
   
    # TODO: Encode the password to bytes (bcrypt requires byte strings)
    password_bytes = plain_text_password.encode('utf-8')
    
    # TODO: Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()
    
    # TODO: Hash the password using bcrypt.hashpw()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    # TODO: Decode the hash back to a string to store in a text file
    
    return hashed_password.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    
    # TODO: Encode both the plaintext password and the stored hash to byt
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    # TODO: Use bcrypt.checkpw() to verify the password
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

 # TEMPORARY TEST CODE - Remove after testing
test_password = "SecurePassword123"
# Test hashing
hashed = hash_password(test_password)
print(f"Original password: {test_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")

# Test verification with correct password
is_valid = verify_password(test_password, hashed)
print(f"\nVerification with correct password: {is_valid}")
# Test verification with incorrect password
is_invalid = verify_password("WrongPassword", hashed)
print(f"Verification with incorrect password: {is_invalid}")


def register_user(username, password):
   
    # TODO: Check if the username already exists  
    # TODO: Hash the password
    # TODO: Append the new user to the file
    # Format: username,hashed_password

    hashed_password = hash_password(password)
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed_password}\n")
        print(f"User {username} registered.")
    return True

def user_exists(username):
 # TODO: Handle the case where the file doesn't exist yet
 # TODO: Read the file and check each line for the username
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            stored_username, _ = line.strip().split(',', 1)
            if stored_username == username:
                return True
    return False

def login_user(username, password):
     # TODO: Handle the case where no users are registered yet
 # TODO: Search for the username in the file
 # TODO: If username matches, verify the password
 # TODO: If we reach here, the username was not found
    if user_exists(username) == False:
        print("Username not found.")
        return False
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            stored_username, stored_hashed_password = line.strip().split(',', 1)
            if stored_username == username:
                if verify_password(password, stored_hashed_password):
                    print(f"User {username} logged in.")
                    return True
                else:
                    print("Incorrect password.")
                    return False
                
def validate_username(username):
     #Returns: tuple: (bool, str) - (is_valid, error_message)
     #check if username already exists
    if user_exists(username):
        return (False, "Username already exists.")
    if len(username) < 3:
        return (False, "Username must be at least 3 characters long.")
    return (True, "is valid")
    
def validate_password(password):    
    if len(password) < 8:
        return (False, "Password must be at least 8 characters long.")
    return (True, "is valid")

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("  Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()

            
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Register the user
            register_user(username, password)
        
        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard)")
                
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")
        
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")
if __name__ == "__main__":
    main()

