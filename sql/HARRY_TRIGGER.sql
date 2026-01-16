-- Create log table for user additions
CREATE TABLE CW2.UserLog (
    logID INT IDENTITY PRIMARY KEY,
    Email VARCHAR(30),
    Username VARCHAR(30),
    About_me VARCHAR(MAX),
    Location VARCHAR(50),
    Dob DATE,
    Language VARCHAR(30),
    Role VARCHAR(5),
    timestamp DATETIME DEFAULT GETDATE()
);
GO

-- Trigger to log new user insertions
CREATE TRIGGER CW2.tr_LogNewUser
ON CW2.Users
AFTER INSERT
AS
BEGIN
    INSERT INTO CW2.UserLog (Email, Username, About_me, Location, Dob, Language, Role)
    SELECT Email, Username, About_me, Location, Dob, Language, Role FROM inserted;
END;
GO
