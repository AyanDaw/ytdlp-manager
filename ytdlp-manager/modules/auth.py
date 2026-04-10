import hashlib
import database

def register(username: str, password: str) -> {bool, str}:
    # Takes input from UI
    hassed_pass = hashlib.sha256(password.encode()).hexdigest()
    result = database.create_user(username = username, hashed_password = hassed_pass)
    return result

def login(username, password) -> bool:
    hassed_pass = hashlib.sha256(password.encode()).hexdigest()
    result = database.verify_user(username = username, hashed_password = hassed_pass)
    return result

def check_username(username: str) -> bool:
    return database.get_user(username) is not None

    # Step 1:
    
    # May add rules (like no 2 character) user name to avoid bot spam

    
    # print(hassed_pass) # This is for test

# def login():
# take input of username and password
# matches the username and finds in database
# takes input of password and hasses it
# if username is available matches the hassed
# for any error thows a error that takes back to the login point
# if successfull let user log in.


if __name__ == "__main__":
    register("username", "FAAAAAAAAHHHHHHH")