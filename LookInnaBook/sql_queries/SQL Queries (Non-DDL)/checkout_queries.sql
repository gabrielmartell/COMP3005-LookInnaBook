/* HERE ARE ALL QUERIES USED DURING CHECKOUT */

-- Get the users selected books, {user.userID} being the userID of the currently logged-in user
SELECT * 
FROM SelectedBooks
WHERE {user.userID} = SelectedBooks.userID

-- Check if the user is registered
SELECT registryID 
FROM Registered_User
WHERE {user.userID} = Registered_User.userID

-- Get the users banking info. {banking_choice} is the banking the user chose and {registryID} being the users registryID.
SELECT * 
FROM User_BankInfo
WHERE {registryID}=User_BankInfo.registryID
AND {banking_choice}=User_BankInfo.bankInfoID

-- Get the users banking info. {shipping_choice} is the banking the user chose and {registryID} being the users registryID.
SELECT * 
FROM User_ShipInfo
WHERE {registryID}=User_ShipInfo.registryID
AND {shipping_choice}=User_ShipInfo.shipInfoID

-- If the user instead wants new shipping and banking info, the query calls are identical from the registry_queries.sql file
SELECT max(bankInfoID) 
FROM Banking_Info
INSERT INTO Banking_Info 
VALUES({bankInfoID}, {info[0]}, {info[1]}, {info[2]})
INSERT INTO User_BankInfo 
VALUES({registryID}, {bankInfoID})

SELECT max(shipInfoID) 
FROM Shipping_Info;
INSERT INTO Shipping_Info 
VALUES({shipInfoID}, {info[0]}, {info[1]}, {info[2]}, {info[3]})
INSERT INTO User_ShipInfo 
VALUES({registryID}, {shipInfoID})

-- Once payment and shipping is dealt with, we consider the shipping company, but first we have to get the next shipping id.
SELECT max(shippingID)
FROM Shipping_Company

-- If the user decided on Express shipping, their order will be attached to this shipping_company. {shipInfoID} is the shipping info used, {d1} is the date.
-- With express shipping, it will be delivered on the same day
INSERT INTO Shipping_Company 
VALUES({shippingID}, 'Super Fast Delivery Company (SFDC)', 'Express', {shipInfoID}, 'Warehouse', {d1}, {d1})

-- If the user decided on Express shipping, their order will be attached to this shipping_company. {shipInfoID} is the shipping info used, {d1} is the date, and {d2} is a date further ahead.
-- With standard shipping, it will be delivered the next day
INSERT INTO Shipping_Company 
VALUES({shippingID}, 'Suprisingly Standard Shipping (SSS)', 'Standard', {shipInfoID}, 'Warehouse', {d1}, {d2})

-- And finally, the main component, we create an order value, getting the max order ID so we can get the next unique ID
SELECT max(orderID) 
FROM Orders

-- The status of the order will be "Processed". {registryID}, {shippingID}, {shipInfoID}, {bankInfoID} is the users' registryID, shipping company ID, shipping information ID
-- and banking info ID respectively.
INSERT INTO Orders 
VALUES({orderID}, {"Processed"}, {registryID}, {shippingID}, {shipInfoID}, {bankInfoID})

-- Add the book and the orderID to the checkoutbasket. The checkoutbasket will act as what books were bought in the order
INSERT INTO CheckoutBasket 
VALUES({book[0]},{orderID})

-- Clear the users' selected books
DELETE FROM SelectedBooks 
WHERE {book[0]} = SelectedBooks.ISBN AND
{user.userID} = SelectedBooks.userID

-- From here, this query is used when the user wants to view their orders. This query gives us the most prevelant information.
SELECT Shipping_Company.*, Orders.orderID, Orders.status, GROUP_CONCAT(Book.title) AS Package
FROM Shipping_Company, Orders, CheckoutBasket, Book, Registered_User
WHERE {user.userID}=Registered_User.userID
AND Registered_User.registryID=Orders.registryID
AND Orders.shippingID = Shipping_Company.shippingID
AND Orders.orderID = CheckoutBasket.orderID
AND CheckoutBasket.ISBN = Book.ISBN
GROUP BY Orders.orderID
                                