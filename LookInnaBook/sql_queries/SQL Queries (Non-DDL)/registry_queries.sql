/* HERE ARE ALL QUERIES USED IN THE REGISTRY CREATION */

-- From here, we determine if the the user is already registered. {user.userID} is from the Users' ID from the interface (which in turn, is also queried)
SELECT registryID 
FROM Registered_User
WHERE {user.userID}=Registered_User.userID

-- If they're not registered, get the max registryID which determines the users' new registryID
SELECT max(registryID) 
FROM Registered_User

-- Add them as a registered_user
INSERT INTO Registered_User 
VALUES({registryID}, {user.userID})

-- Get banking info and shipping info, the variable {info} derives from user input
-- Add to Banking_Info and Shipping_Info, and then add to the respective User_ShippingInfo and User_BankingInfo (because they can have multiple shipping and banking information)
SELECT max(bankInfoID) 
FROM Banking_Info
INSERT INTO Banking_Info 
VALUES({bankID}, {info[0]}, {info[1]}, {info[2]})                        
INSERT INTO User_BankInfo 
VALUES({registryID}, {bankID})         

SELECT max(shipInfoID) 
FROM Shipping_Info
INSERT INTO Shipping_Info 
VALUES({shipID}, {info[0]}, {info[1]}, {info[2]}, {info[3]})
INSERT INTO User_ShipInfo 
VALUES({registryID}, {shipID})
