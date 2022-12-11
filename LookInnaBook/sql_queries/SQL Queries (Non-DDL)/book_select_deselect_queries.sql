/* HERE ARE ALL QUERIES USED RELATED TO THE BOOK SELECTION AND DESELECTION */

/*______________________________________
SELECTING A BOOK
________________________________________
*/

-- Check if the book is valid. It is considered invalid when we don't get anything in return.  {selection} is from user input.
SELECT * 
FROM Book
WHERE {selection} = Book.ISBN

-- Check if the book isn't already selected by the user. {user.userID} is the userID from the *currently* logged in user.
SELECT * 
FROM SelectedBooks
WHERE {selection} = SelectedBooks.ISBN
AND {user.userID} = SelectedBooks.userID

-- The user has now selected the book.
INSERT INTO SelectedBooks
VALUES ({selection},{user.userID})

/*______________________________________
DESELECTING A BOOK
________________________________________
*/

-- Check if the book is valid. It is considered invalid when we don't get anything in return.  {selection} is from user input.
SELECT * 
FROM Book
WHERE {selection} = Book.ISBN

-- Check if the book IS selected by the user. {user.userID} is the userID from the *currently* logged in user.
SELECT * 
FROM SelectedBooks
WHERE {selection} = SelectedBooks.ISBN
AND {user.userID} = SelectedBooks.userID

-- The user has now deselected the book.
DELETE FROM SelectedBooks
WHERE {selection} = SelectedBooks.ISBN
AND {user.userID} = SelectedBooks.userID