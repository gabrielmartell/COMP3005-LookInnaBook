/* HERE ARE ALL QUERIES USED RELATED TO THE BOOK ADDITION AND REMOVAL */

/*______________________________________
ADDING A BOOK
________________________________________
*/
-- Check if publisher is valid. It is considered invalid when we don't get anything in return. {publisher} is from user input.
SELECT * 
FROM Publisher
WHERE {publisher} = Publisher.pID

-- Check if the book is valid. It is considered invalid when we don't get anything in return. {ISBN} is from user input.
SELECT Book.quantity 
FROM Book
WHERE {ISBN} = Book.ISBN

/* If the book exists, increase its quantity instead. {check_ISBN[0][0]+1} is part of a list of tuples that are a result from the query above. check_ISBN is the variable name and 
accessing the index [0][0] gives us the books' current quantity in our inventory.
*/
UPDATE Book 
SET quantity = {check_ISBN[0][0]+1}
WHERE {ISBN} = Book.ISBN

-- Insert the book (if it doesnt exist), each {variable} is that of user input EXCEPT for the last variable, which is quantity, which, of course, is one.
INSERT INTO Book 
VALUES({ISBN}, {title}, {price}, {pageNum}, {publisher}, {publisherCut}, {1})

-- After book insertion, we call for loops (since authors and genres can be multiple) and in those for loops, we add the ISBN and Authors/Genres to the respective table.
INSERT INTO BookAuthors (ISBN, author)
VALUES ({ISBN}, {author})

INSERT INTO BookGenres (ISBN, genre)
VALUES ({ISBN}, {genre})

/*______________________________________
REMOVING A BOOK
________________________________________
*/

-- Check if the book exists. It is considered invalid when we don't get anything in return. {selection} is from user input.
SELECT * 
FROM Book
WHERE {selection} = Book.ISBN

-- If the book exists, subtract the quantity by one. The {quantity} and derives from the information we've gotten from the previous call. It is subtracted by one from the interface.
UPDATE Book
SET quantity = {quantity}
WHERE {selection} = Book.ISBN

-- If the quantity of the book is 0, we remove all entries in the SelectedBooks of the book so that users don't have a book with 0 quantity anymore.
DELETE FROM SelectedBooks
WHERE {selection} = SelectedBooks.ISBN

/*______________________________________
DELETING A BOOK (As in completely removing all entries)
________________________________________
*/

-- Check if the book exists. It is considered invalid when we don't get anything in return. {selection} is from user input.
SELECT * 
FROM Book
WHERE {selection} = Book.ISBN

-- Remove all existence of the book (bye bye)
DELETE FROM Book
WHERE {selection} = Book.ISBN
DELETE FROM BookGenres
WHERE {selection} = BookGenres.ISBN
DELETE FROM BookAuthors
WHERE {selection} = BookAuthors.ISBN
DELETE FROM CheckoutBasket
WHERE {selection} = CheckoutBasket.ISBN
DELETE FROM SelectedBooks
WHERE {selection} = SelectedBooks.ISBN