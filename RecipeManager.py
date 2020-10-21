
import dbconnect as db
import queries as q
HOST = "reddwarf.cs.rit.edu"
USER = "p320_13"
PASS = "aiyohleiCahc2xahtee1"
PORT = "5432"
LANG = "postgresql"
DATABASE = "%s://%s:%s@%s:%s/%s" % (LANG, USER, PASS, HOST, PORT, USER)
# def login_user(uid ):

def define_name( ):
    first_name = input("What is your first name?")
    last_name = input("What is your last name?")
    response = input(f' Your name is {first_name} {last_name} correct? Y or N')

    if response.upper() == "Y":
        print("INSERT CODE FOR USERS")
        connect1.execute_query(q.insert_user, firstname=first_name, lastname=last_name)
    #    return "Thank you, your id number is: . Would you like to login is "
    elif response.upper() == "N":
        define_name()


# def store_ingedient():
#     ingredient = input("Enter an ingedient: \n")



#
# def create_new_recipe():
#     input("Enter the recipe: \n")
#
#
#
# num = input("Enter the number command: ")
#
# def choice_switcher(num):
#     pass


if __name__ == "__main__":

    connect1 = db.Connection(DATABASE)


    print("Welcome to Recipe Manager")

    # id = input("Please log in with id number or leave blank if you are a new user.")


    # num = input("Enter the number command: ")

    # print("1. Store an ingredient in refrigerator or pantry")
    #
    # print("2. Create a recipe")
    #
    # print("3. Search for recipes using an ingredient or recipe name")
    #
    # print("4. Modify recipes ")

    # switcher = {
    #     1: store_ingedient(),
    #     2: create_new_recipe(),
    #     3: input("Enter a recipe name to search: \n"),
    #     4: input("Enter the change that you want to modify: \n")
    # }
    define_name()

