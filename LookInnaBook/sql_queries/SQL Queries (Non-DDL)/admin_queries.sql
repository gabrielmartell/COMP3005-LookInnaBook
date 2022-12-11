/* HERE ARE ALL QUERIES USED IN THE ADMIN/OWNER MENU INTERFACE */

-- From here, we can determine the price of the book and the publisher's cut from book sales. Calculations are done on the interface.
SELECT Book.Price, Book.PublisherCut
FROM CheckoutBasket, Book
WHERE CheckoutBasket.ISBN=Book.ISBN;

-- From here, we can determine how much *each* book brought in, defined in GROSS profit
SELECT Book.title, CheckoutBasket.ISBN, COUNT(CheckoutBasket.ISBN)*(Book.price) AS Occurence
FROM CheckoutBasket, Book, BookAuthors
WHERE CheckoutBasket.ISBN=Book.ISBN
AND BookAuthors.ISBN=Book.ISBN
GROUP BY CheckoutBasket.ISBN
ORDER BY COUNT(CheckoutBasket.ISBN) DESC;

-- From here, we can determine how much *each* author brought in, defined in GROSS profit
SELECT BookAuthors.author, SUM(Book.price), COUNT(CheckoutBasket.ISBN)  
FROM CheckoutBasket, Book, BookAuthors
WHERE CheckoutBasket.ISBN=Book.ISBN
AND BookAuthors.ISBN=Book.ISBN
GROUP BY BookAuthors.author
ORDER BY SUM(Book.price) DESC

-- From here, we can determine how much *each* genre brought in, defined in GROSS profit
SELECT BookGenres.genre, SUM(Book.price), COUNT(CheckoutBasket.ISBN)  
FROM CheckoutBasket, Book, BookGenres
WHERE CheckoutBasket.ISBN=Book.ISBN
AND BookGenres.ISBN=Book.ISBN
GROUP BY BookGenres.genre
ORDER BY SUM(Book.price) DESC

-- Check if the publisher exists, we need this information so we can direct our email to someone.
SELECT Publisher.name
FROM Publisher
WHERE {bookInfo[0][4]} = Publisher.pID

-- In a for loop, check if the there was any of the specific book sales from the last month
-- Check if {bookInfo[0][0]}, book info where the book's quantity is less than the threshold of 5
-- The {date} is formatted as DD/MM/YYYY and iterates through the days
SELECT Shipping_Company.shippingID, Shipping_Company.departureDate
FROM Shipping_Company, Orders, CheckoutBasket 
WHERE {bookInfo[0][0]}=CheckoutBasket.ISBN
AND {date}=Shipping_Company.departureDate
AND Shipping_Company.shippingID=Orders.shippingID
AND Orders.orderID=CheckoutBasket.orderID

-- Get the publisher information, this is for printing them.
SELECT *
FROM Publisher

-- Get the publishers' phone numbers, because there can be multiple prominent numbers.
SELECT PublisherPhones.contactNum
FROM PublisherPhones
WHERE {publis[0]} = PublisherPhones.pid