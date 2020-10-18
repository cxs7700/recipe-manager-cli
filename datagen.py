import random
import dbconnect
import queries

R_FLOOR = 1
R_CEIL = 10

# recipies and ingredients will be recieved as a list of tuples, or as
# a sqlalchemy object
def gen_data(recipies, ingredients):
    requires = {}
    for recipie in recipies:
        requires[recipie] = set()
        amt = random.randint(R_FLOOR, R_CIEL) # number of ingredients
        for i in range(0, amt):
            ing = ingredients


if __name__ == "__main__":
    connection = dbconnect.Connection(dbconnect.DATABASE)
    gen_data(connection.execute_query(queries.select_recipies),
            connection.execute_query(queries.select_ingredients))
