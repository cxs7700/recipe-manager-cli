import random
import dbconnect
import queries

R_FLOOR = 1
R_CEIL = 10
sentences = {
        1: [
            "let %s sit",
            "boil %s, then bring to a simmer",
            "grate %s",
            "finely chop %s",
            ],
        2: [
            "mix %s and %s",
            "knead %s and %s together",
            "combine %s and %s",
            ]
        }

# recipes and ingredients will be recieved as a list of tuples, or as
# a sqlalchemy object
def gen_data(requires, ingredients):
    steps = {}
    cur = requires[0][0] # initial rid
    cur_rec = []
    for item in requires:
        if item[0] == cur:
            cur_rec.append(item[1])
        else:
            steps[cur] = []
            while cur_rec:
                r = random.randrange(1, 2) # 1 or 2 ingredients
                if r > len(cur_rec):
                    r = len(cur_rec)

                step = sentences[r][random.randrange(0, len(sentences[r]))]
                ings = [ingredients[cur_rec.pop() - 1][1] for _ in range(0, r)] # look through ingredients to get the appropriate one based on iid
                ings = tuple(ings)
                step = step % ings
                steps[cur].append(step)
            cur = item[0]
    return steps


if __name__ == "__main__":
    connection = dbconnect.Connection(dbconnect.DATABASE)
    requires = connection.execute_query(queries.select_requires) # ordered on rid
    ingredients = connection.execute_query(queries.select_ingredients) # ordered on iid
    requires = [i for i in requires]
    ingredients = [i for i in ingredients]
    steps = gen_data(requires, ingredients)
    print(steps)
