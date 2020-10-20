select_users = """
    SELECT * FROM users;
"""

select_users_kwargs = """
    SELECT * FROM users
    WHERE users.uid = :uid;
"""
select_recipes = """
    SELECT * FROM recipes;
"""

select_ingredients = """
    SELECT iid, iname FROM ingredients;
"""

select_requires = """
    SELECT * FROM requires ORDER BY rid;
"""

insert_user = """
    INSERT INTO users (uid, firstname, lastname)
    VALUES ((SELECT COUNT(*)+1 FROM users), :firstname, :lastname);
"""

insert_ingredient = """
    INSERT INTO Ingredients (iid, iname, unit_type)
    VALUES ((SELECT COUNT(*)+1 FROM ingredients), :iname, :unit);
"""

update_user_ingredients = """
    UPDATE user_ingredients
    SET quantity = quantity + :quantity
    WHERE uid = :uid
    AND iid = :iid;
"""

select_user_ingredients = """
    SELECT ing.iid, ing.iname FROM user_ingredients ui
    LEFT JOIN ingredients ing on ing.iid = ui.iid
    WHERE ui.uid = :uid;
"""

insert_recipe = """
    INSERT INTO recipes (rid, rname) VALUES((SELECT COUNT(*)+1 FROM recipes), :rname);
"""

update_recipie = """
    UPDATE recipes
    SET rname = :rname
    WHERE rid = :rid;
"""

search_recipie = """
    SELECT DISTINCT rec.rid, rec.rname FROM recipes rec
    RIGHT JOIN requires req ON rec.rid = req.rid
    WHERE rec.rid = ?
    OR rec.rname like concat(?, '%')
    OR req.iid = ?
    ORDER BY rec.rid
    ;
"""

insert_or_update_requires = """
    INSERT INTO requires (rid, iid, quantity) VALUES(:rid, :iid, :quantity)
    ON CONFLICT (rid, iid)
    DO UPDATE SET quantity = :quantity;
"""
# Please run this directly afterwards. Will remove ingredients with quantity of 0
delete_requires_0 = """
    DELETE FROM requires
    WHERE quantity <= 0
    OR quantity is NULL;
"""

insert_or_update_step = """
    INSERT INTO steps (rid, number, direction)
    VALUES(:rid, (:number), :direction)
    ON CONFLICT (rid, number)
    DO UPDATE SET direction = :direction;
"""
# remove steps with empty directions
delete_steps_no_dir = """
    DELETE FROM steps
    WHERE direction = ''
    OR direction is NULL;
"""
#These next queries will need to be used in conjunction with one another to flatten the steps
select_steps_row_numbers = """
    SELECT ste.rid, ste.number, ste.direction, row_number() over (PARTITION BY rid ORDER BY number)
    FROM steps ste
    WHERE rid = :rid;
"""
#After we have the previous result, we can update the steps based on what the row number should be with:
update_steps_row_number = """
    UPDATE steps
    SET number = :row
    WHERE rid = :rid
    AND number = :row;
"""
