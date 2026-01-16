-- User Profile View
-- Combines user information with their favourite activities for profile display
CREATE VIEW CW2.vw_UserProfile AS
SELECT
    u.Email,
    u.Username,
    u.About_me,
    u.Location,
    u.Dob,
    u.Language,
    u.Role,
    STRING_AGG(a.Activity, ', ') AS FavouriteActivities
FROM Users u
LEFT JOIN CW2.FavouriteActivity fa ON u.Email = fa.Email
LEFT JOIN CW2.Activity a ON fa.Activity_id = a.Activity_id
GROUP BY u.Email, u.Username, u.About_me, u.Location, u.Dob, u.Language, u.Role;
