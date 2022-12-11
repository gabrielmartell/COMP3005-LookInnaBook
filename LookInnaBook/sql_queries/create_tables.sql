CREATE TABLE IF NOT EXISTS Users (
    userID int NOT NULL,
    fname varchar(255),
    lname varchar(255),
    username varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL,
    PRIMARY KEY (UserID)
);

CREATE TABLE IF NOT EXISTS Registered_User (
    registryID int NOT NULL UNIQUE,
    userID int NOT NULL UNIQUE,
    PRIMARY KEY (registryID),
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

CREATE TABLE IF NOT EXISTS Publisher (
    pID int NOT NULL UNIQUE,
    name varchar(255) NOT NULL UNIQUE,
    address varchar(255) NOT NULL,
    contactEmail varchar(255),
    accountNum varchar(16) NOT NULL,
    transitNum varchar(6) NOT NULL,
    institutionNum varchar(3) NOT NULL,
    PRIMARY KEY (pID)
);

CREATE TABLE IF NOT EXISTS PublisherPhones (
    pID int NOT NULL,
    contactNum varchar(10) NOT NULL UNIQUE,
    CONSTRAINT PK_PublisherPhones PRIMARY KEY (pID,contactNum),
    FOREIGN KEY (pID) REFERENCES Publisher(pID)
);

CREATE TABLE IF NOT EXISTS Book (
    ISBN int NOT NULL UNIQUE,
    title varchar(255) NOT NULL,
    price float NOT NULL,
    pageNum int NOT NULL,
    publisher int NOT NULL,
    publisherCut int NOT NULL,
    quantity int NOT NULL,
    PRIMARY KEY (ISBN),
    FOREIGN KEY (publisher) REFERENCES Publisher(pID)
);

CREATE TABLE IF NOT EXISTS BookAuthors (
    ISBN int NOT NULL,
    author varchar(255) NOT NULL,
    CONSTRAINT PK_BookAuthors PRIMARY KEY (ISBN,author),
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);

CREATE TABLE IF NOT EXISTS BookGenres (
    ISBN int NOT NULL,
    genre varchar(255) NOT NULL,
    CONSTRAINT PK_BookAuthors PRIMARY KEY (ISBN,genre),
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);

CREATE TABLE IF NOT EXISTS Banking_Info (
    bankInfoID int NOT NULL UNIQUE,
    name varchar(255) NOT NULL,
    cardNum int NOT NULL UNIQUE,
    expiryDate varchar (5) NOT NULL,
    PRIMARY KEY (bankInfoID)
);

CREATE TABLE IF NOT EXISTS Shipping_Info (
    shipInfoID int NOT NULL UNIQUE,
    address varchar(255) NOT NULL,
    province varchar(255) NOT NULL,
    city varchar(255) NOT NULL,
    postal varchar(255) NOT NULL,
    PRIMARY KEY (shipInfoID)
);

CREATE TABLE IF NOT EXISTS User_BankInfo (
    registryID int NOT NULL,
    bankInfoID int NOT NULL,
    CONSTRAINT PK_UserBankInfo PRIMARY KEY (registryID,bankInfoID),
    FOREIGN KEY (registryID) REFERENCES Registered_User(registryID),
    FOREIGN KEY (bankInfoID) REFERENCES Banking_Info(bankInfoID)
);

CREATE TABLE IF NOT EXISTS User_ShipInfo (
    registryID int NOT NULL,
    shipInfoID int NOT NULL,
    CONSTRAINT PK_UserShipInfo PRIMARY KEY (registryID,shipInfoID),
    FOREIGN KEY (registryID) REFERENCES Registered_User(registryID),
    FOREIGN KEY (shipInfoID) REFERENCES Shipping_Info(shipInfoID)
);

CREATE TABLE IF NOT EXISTS Shipping_Company (
    shippingID int NOT NULL,
    companyName varchar(255) NOT NULL,
    priority varchar(255) NOT NULL,
    destination varchar(255) NOT NULL,
    currentLocation varchar(255) NOT NULL,
    departureDate varchar(255) NOT NULL,
    expectedArrival varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Orders (
    orderID int NOT NULL UNIQUE,
    status varchar(20) NOT NULL,
    registryID int NOT NULL,
    shippingID int NOT NULL UNIQUE,
    shipInfoID int NOT NULL,
    bankInfoID int NOT NULL,

    PRIMARY KEY (orderID),
    FOREIGN KEY (registryID) REFERENCES Registered_User(registryID),
    FOREIGN KEY (shippingID) REFERENCES Shipping_Company(shippingID),
    FOREIGN KEY (shipInfoID) REFERENCES Shipping_Info(shipInfoID),
    FOREIGN KEY (bankInfoID) REFERENCES Banking_Info(bankInfoID)
);

CREATE TABLE IF NOT EXISTS CheckoutBasket (
    ISBN int NOT NULL,
    orderID int NOT NULL,
    CONSTRAINT PK_CheckoutBasket PRIMARY KEY (ISBN,orderID),
    FOREIGN KEY (orderID) REFERENCES Orders(orderID)
);

CREATE TABLE IF NOT EXISTS SelectedBooks (
    ISBN int NOT NULL,
    userID int NOT NULL,
    CONSTRAINT PK_SelectedBooks PRIMARY KEY (ISBN,userID),
    FOREIGN KEY (userID) REFERENCES Users(userID)
);
