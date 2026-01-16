-- CREATE: Insert new user
CREATE PROCEDURE CW2.usp_InsertUser
    @Email VARCHAR(30),
    @Username VARCHAR(30),
    @About_me VARCHAR(MAX) = NULL,
    @Location VARCHAR(50) = NULL,
    @Dob DATE = NULL,
    @Language VARCHAR(30) = NULL,
    @Password VARCHAR(30),
    @Role VARCHAR(5) = 'User'
AS
BEGIN
    INSERT INTO CW2.Users (Email, Username, About_me, Location, Dob, Language, Password, Role)
    VALUES (@Email, @Username, @About_me, @Location, @Dob, @Language, @Password, @Role);
END;
GO

-- READ: Get user by email
CREATE PROCEDURE CW2.usp_GetUser
    @Email VARCHAR(30)
AS
BEGIN
    SELECT * FROM CW2.Users WHERE Email = @Email;
END;
GO

-- UPDATE: Update user details
CREATE PROCEDURE CW2.usp_UpdateUser
    @Email VARCHAR(30),
    @Username VARCHAR(30) = NULL,
    @About_me VARCHAR(MAX) = NULL,
    @Location VARCHAR(50) = NULL,
    @Dob DATE = NULL,
    @Language VARCHAR(30) = NULL,
    @Password VARCHAR(30) = NULL,
    @Role VARCHAR(5) = NULL
AS
BEGIN
    UPDATE CW2.Users
    SET Username = ISNULL(@Username, Username),
        About_me = ISNULL(@About_me, About_me),
        Location = ISNULL(@Location, Location),
        Dob = ISNULL(@Dob, Dob),
        Language = ISNULL(@Language, Language),
        Password = ISNULL(@Password, Password),
        Role = ISNULL(@Role, Role)
    WHERE Email = @Email;
END;
GO

-- DELETE: Delete user
CREATE PROCEDURE CW2.usp_DeleteUser
    @Email VARCHAR(30)
AS
BEGIN
    DELETE FROM CW2.Users WHERE Email = @Email;
END;
GO
