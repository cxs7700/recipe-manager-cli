
"""
-- how many ingredients used total?
SELECT req.iid, SUM(req.quantity)
FROM requires req
RIGHT JOIN recipes rec ON req.rid = rec.rid
RIGHT JOIN dates_made dm on rec.rid = dm.rid
GROUP BY req.iid;
"""

"""
-- how many recipies were made
SELECT rid, COUNT(rid)
FROM dates_made
GROUP BY rid;
"""

"""
-- what can a user make?
SELECT uid, rec.rid
FROM users use, recipes rec
WHERE
      use.uid = :user
      AND NOT EXISTS(
        SELECT
           req.rid,
           req.iid,
           req.quantity
        FROM requires req
        WHERE req.rid = rec.rid
    AND NOT EXISTS(
        SELECT 'x'
        FROM user_ingredients ui
        WHERE ui.uid = use.uid
        AND ui.iid = req.iid
        AND ui.quantity >= req.quantity)
    );
"""

"""
-- who makes the most stuff?
SELECT uid, rid, COUNT(rid)
FROM dates_made
GROUP BY uid, rid;
"""

"""
-- recommended recipes based on used ingredients
SELECT SUM(iur.used) used, iur.rid
FROM(
        SELECT DISTINCT req.iid, COUNT(req.iid) used, req2.rid
        FROM requires req
        RIGHT JOIN dates_made dm ON req.rid = dm.rid
        RIGHT JOIN requires req2 ON req.iid = req2.iid
        WHERE dm.uid = :uid
        GROUP BY req.iid, req2.rid
        ORDER BY used DESC
    ) AS iur -- Ingredients Used by Recipe
-- WHERE iur.rid NOT IN ( -- do we want to exclude recipes we've made before?
--     SELECT rid FROM dates_made WHERE uid = :uid
--     )
GROUP BY iur.rid
ORDER BY used DESC;
"""

"""
-- ALL ingredients we don't have enough of
SELECT
       req.rid,
       req.iid,
       req.quantity
FROM requires req
WHERE req.rid IN (
        SELECT DISTINCT req.rid
        FROM requires req
        RIGHT JOIN user_ingredients ui on req.iid = ui.iid
    )
AND NOT EXISTS(
        select 'x'
        from user_ingredients ui
        where ui.uid = ?
        and ui.iid = req.iid
        and ui.quantity >= req.quantity
    )
ORDER BY req.rid, req.iid;
"""

"""
-- recommend based on rname
SELECT DISTINCT rname, rid
FROM recipes,
     (
        SELECT DISTINCT regexp_split_to_table(rec.rname, E'\\s+') npart
        FROM recipes rec
        RIGHT JOIN requires req ON req.rid = rec.rid
        RIGHT JOIN dates_made dm on rec.rid = dm.rid
        WHERE dm.uid = :uid
    ) AS parts
WHERE rname LIKE '%' || parts.npart || '%';
"""
