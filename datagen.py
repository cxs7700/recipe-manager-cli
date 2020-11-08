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
    requires.append(None) # this guarentees the last recipie is accounted for
    steps = {}
    cur = requires[0][0] # initial rid
    cur_rec = []
    for item in requires:
        if not item or item[0] != cur:
            steps[cur] = []
            while cur_rec:
                r = random.randint(1, 2) # 1 or 2 ingredients
                if r > len(cur_rec):
                    r = len(cur_rec)

                step = sentences[r][random.randrange(0, len(sentences[r]))]
                ings = [ingredients[cur_rec.pop() - 1][1] for _ in range(0, r)] # look through ingredients to get the appropriate one based on iid
                ings = tuple(ings)
                step = step % ings
                steps[cur].append(step)
        if item: # only last item will be None
            cur_rec.append(item[1])
            cur = item[0]
    return steps

def insert_steps(steps, connection):
    for rid in steps.keys():
        for i in range(len(steps[rid])):
            connection.execute_query(queries.insert_step, rid=rid, number=(i+1), step=steps[rid][i])

def make_timestamps(numstamps, connection):
    rids = connection.execute_query("""
        SELECT rid FROM recipes;
            """)
    uids = connection.execute_query("""
        SELECT uid FROM users;
            """)
    for _ in range(numstamps):
        rrec = random.randrange(1, len(rids))
        ruser = random.randrange(1, len(uids))
        rrec = rids[rrec][0]
        ruser = uids[ruser][0]
        print("rid: %s, user: %s" % (rrec, ruser))
        connection.execute_query(queries.random_timestamp, rid=rrec, uid=ruser)

if __name__ == "__main__":
    connection = dbconnect.Connection(dbconnect.DATABASE)
    # requires = connection.execute_query(queries.select_requires) # ordered on rid
    # ingredients = connection.execute_query(queries.select_ingredients) # ordered on iid
    # requires = [i for i in requires]
    # print(len(requires))
    # ingredients = [i for i in ingredients]
    # steps = gen_data(requires, ingredients)
    # print(len(steps))
    # insert_steps(steps, connection)
    make_timestamps(300, connection)
