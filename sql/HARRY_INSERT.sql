-- Insert demo data
INSERT INTO CW2.Users (Email, Username, About_me, Location, Dob, Language, Password, Role)
VALUES
('grace@plymouth.ac.uk', 'GraceHopper', 'Pioneer in computing', 'New York', '1906-12-09', 'English', 'ISAD123!', 'Admin'),
('tim@plymouth.ac.uk', 'TimBL', 'Inventor of the web', 'London', '1955-06-08', 'English', 'COMP2001!', 'User'),
('ada@plymouth.ac.uk', 'AdaLovelace', 'First programmer', 'London', '1815-12-10', 'English', 'insecurePassword', 'User');

INSERT INTO CW2.Activity (Activity_id, Activity)
VALUES
(1, 'Walking'),
(2, 'Skiing'),
(3, 'Birding'),
(4, 'Fishing');

INSERT INTO CW2.FavouriteActivity (Email, Activity_id)
VALUES
('tim@plymouth.ac.uk', 1),
('ada@plymouth.ac.uk', 2),
('tim@plymouth.ac.uk', 3),
('grace@plymouth.ac.uk', 4);
