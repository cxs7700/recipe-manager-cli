
import dbconnect as db
import queries as q
HOST = "reddwarf.cs.rit.edu"
USER = "p320_13"
PASS = "aiyohleiCahc2xahtee1"
PORT = "5432"
LANG = "postgresql"
DATABASE = "%s://%s:%s@%s:%s/%s" % (LANG, USER, PASS, HOST, PORT, USER)

# Returns True if there is a valid user ID in the database. Otherwise, returns False
def login_user(id):
    res = connect1.execute_query(q.select_users_kwargs, uid=id)
    if res is None:
        return False
    return True

def register():
    first_name = input("What is your first name?")
    last_name = input("What is your last name?")
    response = input(f'Is your name, {first_name} {last_name}, correct? (Y/N)')

    if response.upper() == "Y":
        connect1.execute_query(q.insert_user, firstname=first_name, lastname=last_name)
        user_id = connect1.execute_query(q.select_user_id_kwargs, firstname=first_name, lastname=last_name)
        id = user_id.fetchone()[0]
        login_prompt = input("Thank you, your id number is: %s. Please remember it for the next time you log in. Would you like to login? (Y/N)" % id)
        if login_prompt.upper() == "Y":
            login_user(id)
        elif login_prompt.upper() == "N":
            start()
            
    elif response.upper() == "N":
        print("We apologize for any inconvenience. Let's try again!")
        register()


def store_ingedient():
    print("Select an option to ")
    ingredient = input("Enter an ingredient: \n")

def create_new_recipe():
    input("Enter the recipe: \n")

def choice_switcher(num):
    pass

def start():
    print("Hello! Welcome to Recipe Manager!")
    id = input("Please log in with your ID number or leave blank if you are a new user.")
    
    # Loops if invalid input (integer or blank)
    while not id.isdigit() and id != "":
        id = input("Please enter a valid ID or leave blank.")
    
    # Checks if user entered a valid integer and valid id that matches a database entry
    if id.isdigit() and login_user(id) is True: 
        print(f"You are now logged in with ID {id}.")
    else:
        if id == "": 
            register()

if __name__ == "__main__":
    connect1 = db.Connection(DATABASE)
    start()
    print("Welcome to the MAIN MENU! Here are the commands:")            
    print("1. Store an ingredient in refrigerator or pantry")
    print("2. Create a recipe")
    print("3. Search for recipes using an ingredient or recipe name")
    print("4. Modify recipes ")
    num = input("Enter the number command: ")
    print(f"You have entered {num}.")
    
    # switcher = {
    #     1: store_ingedient(),
    #     2: create_new_recipe(),
    #     3: input("Enter a recipe name to search: \n"),
    #     4: input("Enter the change that you want to modify: \n")
    # }
    # register()

