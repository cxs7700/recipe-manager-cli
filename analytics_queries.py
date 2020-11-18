
"""
-- top 10 most popular ingredients
SELECT req.iid, SUM(req.quantity)
FROM requires req
RIGHT JOIN recipes rec ON req.rid = rec.rid
RIGHT JOIN dates_made dm on rec.rid = dm.rid
WHERE req.iid IS NOT NULL
GROUP BY req.iid
LIMIT 10;
"""

"""
-- top 10 users of the database (by recipes made)
SELECT uid, COUNT(rid) made
FROM dates_made
GROUP BY uid
ORDER BY made DESC
LIMIT 10;
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
-- used represents the number of ingredients (and times) the user has used that the suggested recipe contains
SELECT SUM(iur.used) used, iur.rid
FROM(
        SELECT DISTINCT req.iid, COUNT(req.iid) used, req2.rid
        FROM requires req
        RIGHT JOIN dates_made dm ON req.rid = dm.rid -- recipes user has made before
        RIGHT JOIN requires req2 ON req.iid = req2.iid -- all recipes that have common ingredients with recipes the user had made
        WHERE dm.uid = :uid
        GROUP BY req.iid, req2.rid
        ORDER BY used DESC
    ) AS iur -- Ingredients Used by Recipe
GROUP BY iur.rid
ORDER BY used DESC;
"""

"""
-- recommend based on rname
SELECT rname, rid, COUNT(rname) matches
FROM recipes,
     (
        SELECT DISTINCT regexp_split_to_table(rec.rname, E'\\s+') npart
        FROM recipes rec
        RIGHT JOIN dates_made dm on rec.rid = dm.rid
        WHERE dm.uid = :uid
    ) AS parts
WHERE rname LIKE '%' || parts.npart || '%'
GROUP BY rname, rid
ORDER BY matches DESC;
"""

"""
-- recipes user can almost make (how much is required, what's required)
WITH rir (rid, iid, required) AS( -- rid, iid, how much some user needs to buy to fulfil required iid quantity
    SELECT
           req.rid,
           req.iid,
           -- find a quantity, if it exists, in user ingredients that is the same iid as the current req, and subtract the quantity
           req.quantity - coalesce((SELECT quantity FROM user_ingredients WHERE uid = :uid AND iid = req.iid AND quantity >= 0), 0) AS required
    FROM requires req
    WHERE req.rid IN (
            -- Find all recipes that have an ingredient that the user currently has
            SELECT DISTINCT req.rid
            FROM requires req
            RIGHT JOIN user_ingredients ui on req.iid = ui.iid
            WHERE ui.uid = :uid
            AND ui.quantity > 0
        )
    ORDER BY req.rid, req.iid
)
SELECT
       rir.rid,
       rir.iid,
       rir.required
--        rir2.total
FROM rir
LEFT JOIN (
        -- the total number of missing ingredients (in terms of quantity) this recipe requires to be able to be made
        -- this is used to help order
        SELECT rid, SUM(required) total FROM rir WHERE required > 0 GROUP BY rid
    ) rir2
ON rir.rid = rir2.rid
WHERE rir.required > 0
AND total < :tlimit
ORDER BY rir2.total, rir.rid, rir.iid;
"""
