/* HERE ARE ALL QUERIES USED IN THE REGISTRY CREATION */

-- When the user logins with the potential input, we search for them in Users. If valid, we set a python class with the user's information so that we KNOW who is logged in.
SELECT * 
FROM Users
WHERE {username} = Users.username AND {password} = Users.password

-- After logging in, we check if they're registered or not. If not, we give a notice message.
SELECT * 
FROM Registered_User
WHERE {findUser[0][0]} = Registered_User.userID
