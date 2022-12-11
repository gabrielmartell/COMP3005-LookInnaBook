/* HERE ARE ALL QUERIES USED FOR PRINTING CODE */

-- Get the table for all of the users' selected books.
SELECT Book.ISBN, Book.title, BookAuthors.author, BookGenres.genre, Book.price, Book.pageNum, Publisher.name, Book.quantity
FROM Book, SelectedBooks
INNER JOIN BookAuthors ON BookAuthors.ISBN=Book.ISBN
INNER JOIN BookGenres ON BookGenres.ISBN=Book.ISBN
INNER JOIN Publisher ON Publisher.pID=Book.publisher
WHERE {user.userID} = SelectedBooks.userID 
AND SelectedBooks.ISBN = Book.ISBN

-- Get the table for the sorted table prints. {sort_queries} is a list of potential query options, such as ["title ASC","title DESC","author ASC","author DESC"].
-- {option} is the users' choice (which is numerical)
SELECT Book.ISBN, title, author, genre, price, pageNum, Publisher.name, quantity
FROM Book
INNER JOIN BookAuthors ON BookAuthors.ISBN=Book.ISBN
INNER JOIN BookGenres ON BookGenres.ISBN=Book.ISBN
INNER JOIN Publisher ON Publisher.pID=Book.publisher
ORDER BY {sort_queries[option-1]}

-- Get the table for the table searched. {search_queries} is a list of potential query options, such as ["=title","=author","=genre","=Publisher.name","=Book.ISBN"]
-- {option} is the users' choice (which is numerical)
-- {search_input} is the user input, such as the user putting in "Of Mice and Men" and therefore checking if it matches "title"
SELECT Book.ISBN, title, author, genre, price, pageNum, Publisher.name, quantity
FROM Book
INNER JOIN BookAuthors ON BookAuthors.ISBN=Book.ISBN
INNER JOIN BookGenres ON BookGenres.ISBN=Book.ISBN
INNER JOIN Publisher ON Publisher.pID=Book.publisher
WHERE {search_input}{search_queries[option-5]}
ORDER BY Book.ISBN ASC

-- Prints the current users' shipping info.
SELECT Shipping_Info.shipInfoID, Shipping_Info.address, Shipping_Info.province, Shipping_Info.city, Shipping_Info.postal
FROM Shipping_Info, User_ShipInfo, Registered_User 
WHERE {user.userID}=Registered_User.userID 
AND Registered_User.registryID=User_ShipInfo.registryID
AND User_ShipInfo.shipInfoID=Shipping_Info.shipInfoID

-- Prints the current users' banking info.
SELECT Banking_Info.bankInfoID, Banking_Info.name, Banking_Info.cardNum, Banking_Info.expiryDate
FROM Banking_Info, User_BankInfo, Registered_User 
WHERE {user.userID}=Registered_User.userID 
AND Registered_User.registryID=User_BankInfo.registryID
AND User_BankInfo.bankInfoID=Banking_Info.bankInfoID