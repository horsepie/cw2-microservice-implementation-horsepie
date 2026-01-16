-- User/Role table
-- Create CW2 schema
CREATE SCHEMA CW2;
GO
CREATE TABLE CW2.Users (
    Email VARCHAR(30) PRIMARY KEY NOT NULL,
    Username VARCHAR(30) NOT NULL,
    About_me VARCHAR(MAX) NULL,
    Location VARCHAR(50) NULL,
    Dob DATE NULL,
    Language VARCHAR(30) NULL,
    Password VARCHAR(30) NOT NULL,
    Role VARCHAR(5) NOT NULL DEFAULT 'User' CHECK (Role IN ('Admin', 'User'))
);
GO

-- Activity table
CREATE TABLE CW2.Activity (
    Activity_id TINYINT PRIMARY KEY NOT NULL,
    Activity VARCHAR(30) NOT NULL UNIQUE
);
GO

-- Favourite Activity junction
CREATE TABLE CW2.FavouriteActivity (
    Email VARCHAR(30) NOT NULL,
    Activity_id TINYINT NOT NULL,
    PRIMARY KEY (Email, Activity_id),
    FOREIGN KEY (Email) REFERENCES CW2.Users(Email),
    FOREIGN KEY (Activity_id) REFERENCES CW2.Activity(Activity_id)
);
GO
