from pyfiles.init import *
from pyfiles.helper_funcs import *

def main():
    connection = create_connection()

    menu(connection)

def menu(c):
    user = currentUser("","None","","")
    print_menu(user)

    option = str(input("\n    Option: "))
    while (option != "0"):

        if (option == "1" and user.loggedIn == False):      #LOGIN
            user = login(c, user)
            os.system('cls')
        elif (option == "1" and user.loggedIn):             #LOGOUT
            user = currentUser("","None","","")
            user.loggedIn = False
            user.owner = False
            os.system('cls')
            
        elif (option == "2" and user.loggedIn == False):    #CREATE ACCOUNT
            create_account(c)
        elif (option == "2" and user.loggedIn == True):     #VIEW BOOKS
            books_menu(c, user)
        
        elif (option == "3" and user.loggedIn == True):     #REGISTRY MENU
            register_menu(c, user)

        elif ((option == "4" and user.owner == True) or option == "failsafe"):
            admin_menu(c, user)

        else:
            print("[INVALID INPUT]")
        print_menu(user)
        option = str(input("\n    Option: "))

    sys.exit

##_____________________________________________________________
# LOGGED OUT FUNCTIONS
##_____________________________________________________________

def login(c, user):
    os.system('cls')
    username = str(input("Username: "))
    password = str(input("Password: "))

    findUser = executeSQLFromLocal(f'''SELECT * 
                                    FROM Users
                                    WHERE '{username}' = Users.username AND '{password}' = Users.password
                                        ''', c)

    if (len(findUser) == 0):
        print("\nIncorrect Login")
        time.sleep(5)
        return user
    else:
        user.userID = findUser[0][0]
        user.fname = findUser[0][1]
        user.lname = findUser[0][2]
        user.username = findUser[0][3]
        user.loggedIn = True

        if (findUser[0][0] == 1):
            user.owner = True
    
    checkRegistry = executeSQLFromLocal(f'''SELECT * 
                                        FROM Registered_User
                                        WHERE {findUser[0][0]} = Registered_User.userID
                                        ''', c)
    
    if (len(checkRegistry) == 0):
        print("\nLogging in...\n[NOTICE] You are not registered.")
        time.sleep(2)

    return user

def create_account(c):
    accountMade = False
    os.system('cls')

    ##_____________________________________________________________
    # ACCOUNT CREATION INPUTS
    ##_____________________________________________________________
    while (accountMade == False):
        print("\n- No Spaces\n- Username must be more than 3 letters\n- Password must be more than 5 letters\n\nType 'exit' to exit.\n\n")
        account_valid = True

        firstName = str(input("First Name (optional): "))
        if (" " in firstName):
            account_valid = False
        if (firstName.lower() == "exit"):
            break

        lastName = str(input("Last Name (optional): "))
        if (account_valid == False or (" ") in lastName):
            account_valid = False
        if (lastName.lower() == "exit"):
            break

        username = str(input("Username: "))
        if (account_valid == False or (" " in username) or len(username) <= 3):
            account_valid = False
        if (username.lower() == "exit"):
            break

        password = str(input("Password: "))
        if (account_valid == False or (" " in password) or len(password) <= 5):
            account_valid = False
        if (password.lower() == "exit"):
            break

        passwordConfirm = str(input("Re-Enter Password: "))
        if (passwordConfirm.lower() == "exit"):
            break

        ##_____________________________________________________________
        # CHECK IF PASSWORDS MATCH
        ##_____________________________________________________________
        if (passwords_match(password, passwordConfirm) and account_valid):
            result = executeSQLFromLocal(f'''SELECT * 
                                        FROM Users
                                        WHERE '{username}' = Users.username;
                                            ''', c)
        ##_____________________________________________________________
        # IF USERNAME IS NOT TAKEN
        ##_____________________________________________________________
            if (empty_result(result)):
                print(f"\nDoes the following look correct?\nFirst Name: {firstName:10}\nLast Name: {lastName:10}\nUsername: {username:10}\nPassword: {password:10}")
                
                accountInfoValid = False
                while (accountInfoValid == False):
                    confirmInfo = str(input("\n[Y/N]: "))
                    if (confirmInfo.lower() == "y"):
                        result = executeSQLFromLocal(f'''SELECT max(userID) 
                                                        FROM Users;
                                                        ''', c)
                        userID = result[0][0]

                        if (userID == None):
                            userID = 0
                        else:
                            userID = int(userID)

                        executeSQLFromLocal(f'''INSERT INTO Users 
                                                VALUES({userID+1}, '{firstName}', '{lastName}', '{username}', '{password}' )
                                                    ;''', c)
                        accountInfoValid = True
                        accountMade = True

                    elif (confirmInfo.lower() == "n"):
                        os.system('cls')
                        break

                    else:
                        print("Invalid Input.")

                time.sleep(2)
            else:
                os.system('cls')
                print("Username was taken, please try again.\n")
        else:
            print("There was an error, with your attempted information, please try again.\n")
            time.sleep(5)
            os.system('cls')

    os.system('cls')

##_____________________________________________________________
# LOGGED IN FUNCTIONS
##_____________________________________________________________

# BOOKS________________________________________________________
def books_menu(c, user):
    os.system('cls')
    print_book_searches_options(user)

    option = str(input("\n    Option: "))
    while (option != "0"):
        ##_____________________________________________________________
        # VIEW TABLE FROM SORTING ROW
        ##_____________________________________________________________
        if (int(option) >= 1 and int(option) <= 4):
            print_table(c, int(option), "")
            print_book_searches_options(user)

        ##_____________________________________________________________
        # SEARCH IN TABLE
        ##_____________________________________________________________
        elif (int(option) >= 5 and int(option) <= 9):
            search_input = str(input("\n    Search For: "))
            print_table(c, int(option), search_input)
            print_book_searches_options(user)

        ##_____________________________________________________________
        # CHECK SELECTED BOOKS
        ##_____________________________________________________________
        elif (option == "10"):
            print_selected_books(c, user)
            print_book_searches_options(user)

        ##_____________________________________________________________
        # SELECT BOOK
        ##_____________________________________________________________
        elif (option == "11"):
            book_selection = str(input("\n    Selection (By ISBN): "))
            select_book(c, user, book_selection)
            print_book_searches_options(user)

        elif (option == "12"):
            book_selection = str(input("\n    Selection (By ISBN): "))
            deselect_book(c, user, book_selection)
            print_book_searches_options(user)

        elif (option == "13"):
            checkout(c, user)

        elif (option == "14"):
            
            os.system('cls')

            user_orders = executeSQLFromLocal(f'''SELECT Shipping_Company.*, Orders.orderID, Orders.status, GROUP_CONCAT(Book.title) AS Package
                                                        FROM Shipping_Company, Orders, CheckoutBasket, Book, Registered_User
                                                        WHERE {user.userID}=Registered_User.userID
                                                        AND Registered_User.registryID=Orders.registryID
                                                        AND Orders.shippingID = Shipping_Company.shippingID
                                                        AND Orders.orderID = CheckoutBasket.orderID
                                                        AND CheckoutBasket.ISBN = Book.ISBN
                                                        GROUP BY Orders.orderID''',c)
                                                        
            for order in user_orders:
                books = order[9].replace(",",", ")
                print("\n______________________________________________\n")
                print(f"BEING SHIPPED TO (ADDRESS ID: {order[3]}) BY: {order[1]}\n")
                print(f"ORDER ID: {order[7]}\nSHIPPING ID: {order[0]}")
                print(f"ORDERED: {books}")
                print(f"\nPACKAGE STATUS: {order[8]}\nPACKAGE LOCATION: {order[4]}\n\nDEPARTURE DATE: {order[5]}\nEXPECTED DELIVERY DATE: {order[6]}\nPRIORITY: {order[2]}")
            
            while (True):
                exit_option = input("\nExit (Enter): ")
                break
        
        else:
            print("[INVALID INPUT]")
            
        os.system('cls')
        print_book_searches_options(user)
        option = str(input("\n    Option: "))

    os.system('cls')

def checkout(c, user):

    ##_____________________________________________________________
    # CHECKING SELECTED BOOKS AND IF USER IS REGISTERED
    ##_____________________________________________________________

    check_selected = executeSQLFromLocal(f'''SELECT * 
                                            FROM SelectedBooks
                                            WHERE {user.userID} = SelectedBooks.userID''', c)

    if (len(check_selected) == 0):
        print("[ERROR] You haven't selected any books to checkout.")
        return None

    registry_check = executeSQLFromLocal(f'''SELECT registryID 
                                            FROM Registered_User
                                            WHERE {user.userID} = Registered_User.userID''', c)
    if (len(registry_check) == 0):
        print("[ERROR] You are not registered.")
        return None

    ##_____________________________________________________________
    # DECLARING VARIABLES
    ##_____________________________________________________________

    registryID = registry_check[0][0]
    shippingInfo = ""
    bankInfoID = ""
    shipInfoID = ""

    bankingInfo = []
    shippingInfo = []

    ##_____________________________________________________________
    # PROMPTING USER FOR BANKING FORMATION
    ##_____________________________________________________________

    print_information(c, user)
    print("_______________________________\nYOUR INFORMATION:\n")

    print("PAYMENT SELECT:\n    [1] Existing Banking\n    [2] New Banking\n    [3] Cancel Order\n")

    banking_loop = str(input("    Option: "))
    while ( True ):
        if (banking_loop == "1"):
            banking_choice = str(input("    Select (Banking Info ID): "))

            banking_check = executeSQLFromLocal(f'''SELECT * 
                                                    FROM User_BankInfo
                                                    WHERE {registryID}=User_BankInfo.registryID
                                                    AND {banking_choice}=User_BankInfo.bankInfoID''', c)
            if (len(banking_check) != 0):
                bankInfoID = banking_choice
                break
            else:
                print("[ERROR] Account Not Found.")

        elif (banking_loop == "2"):
            while ( True ):
                name = str(input("Name on Card: "))
                bankNum = str(input("Card Number (XXXXXXXXXXXXXXXX): "))
                expiryDate = str(input("Expiry Date (MM/YY): "))
                if (name != "" and bankNum != "" and expiryDate != ""):
                    break
                else:
                    print("[ERROR] Invalid Input")
            bankingInfo.append((name, bankNum, expiryDate))
            break
        elif (banking_loop == "3"):
            return None
        else:
            print("[ERROR] Invalid Input")

    ##_____________________________________________________________
    # PROMPTING USER FOR SHIPPING FORMATION
    ##_____________________________________________________________

    print("\nADDRESS SELECT:\n    [1] Existing Address\n    [2] New Address\n    [0] Cancel Order\n")

    shipping_choice = ""
    shipping_loop = str(input("    Option: "))
    while ( True ):
        if (shipping_loop == "1"):
            shipping_choice = str(input("    Select (Shipping Info ID): "))

            shipping_check = executeSQLFromLocal(f'''SELECT * 
                                                    FROM User_ShipInfo
                                                    WHERE {registryID}=User_ShipInfo.registryID
                                                    AND {shipping_choice}=User_ShipInfo.shipInfoID''', c)
            if (len(shipping_check) != 0):
                shipInfoID = shipping_choice
                break
            else:
                print("[ERROR] Account Not Found.")

        elif (shipping_loop == "2"):
            while ( True ):
                address = str(input("Address ('stop' to stop input): "))
                province = str(input("Province: "))
                city = str(input("City: "))
                postal = str(input("Postal Code (XXX XXX): "))
                if (address != "" and province != "" and city != "" and postal != ""):
                    break
                else:
                    print("[ERROR] Invalid Input")
            shippingInfo.append((address, province, city, postal))
            break
        elif (shipping_loop == "3"):
            return None
        else:
            print("[ERROR] Invalid Input")

    if (len(bankingInfo) > 0): # IF THEY CREATED NEW BANKING INFO
        getBankID = executeSQLFromLocal(f'''SELECT max(bankInfoID) 
                                            FROM Banking_Info;
                                            ''', c)
        bankInfoID = getBankID[0][0]
        if (bankInfoID == None):
            bankInfoID = 0
        else:
            bankInfoID = int(bankInfoID)
            bankInfoID+=1
        
        for info in bankingInfo:
            executeSQLFromLocal(f'''INSERT INTO Banking_Info 
                                    VALUES({bankInfoID}, '{info[0]}', {info[1]}, '{info[2]}')
                                    ;''', c)
            executeSQLFromLocal(f'''INSERT INTO User_BankInfo 
                            VALUES({registryID}, {bankInfoID})
                            ;''', c)

    if (len(shippingInfo) > 0): # IF THEY CREATED NEW SHIPPING INFO
        getShipID = executeSQLFromLocal(f'''SELECT max(shipInfoID) 
                                            FROM Shipping_Info;
                                            ''', c)
        shipInfoID = getShipID[0][0]
        if (shipInfoID == None):
            shipInfoID = 0
        else:
            shipInfoID = int(shipInfoID)
            shipInfoID+=1
        
        for info in shippingInfo:
            executeSQLFromLocal(f'''INSERT INTO Shipping_Info 
                                    VALUES({shipInfoID}, '{info[0]}', '{info[1]}', '{info[2]}', '{info[3]}')
                                    ;''', c)
            executeSQLFromLocal(f'''INSERT INTO User_ShipInfo 
                            VALUES({registryID}, {shipInfoID})
                            ;''', c)
    
    getShippingID = executeSQLFromLocal(f'''SELECT max(shippingID)
                                    FROM Shipping_Company;
                                    ''',c)
    shippingID = getShippingID[0][0]
    if (shippingID == None):
            shippingID = 0
    else:
        shippingID = int(shippingID)
        shippingID+=1

    ##_____________________________________________________________
    # HOW DO THEY WANT THEIR PACKAGE DELIVERED
    ##_____________________________________________________________

    print("\nDELIVERY SELECT:\n    [1] Express (+$3.99)\n    [2] Standard (Free)\n    [3] Cancel Order\n")
    option = str(input("    Option: "))

    today = datetime.date.today() 
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    d1 = today.strftime("%d/%m/%Y")
    d2 = tomorrow.strftime("%d/%m/%Y")

    ##_____________________________________________________________
    # SHIPPING COMPANY CREATION
    ##_____________________________________________________________

    while ( True ):
        if (option == "1"):
            executeSQLFromLocal(f'''INSERT INTO Shipping_Company 
                                    VALUES({shippingID}, 'Super Fast Delivery Company (SFDC)', 'Express', {shipInfoID}, 'Warehouse', '{d1}', '{d1}')
                                    ;''', c)
            break
        elif (option == "2"):
            executeSQLFromLocal(f'''INSERT INTO Shipping_Company 
                                    VALUES({shippingID}, 'Suprisingly Standard Shipping (SSS)', 'Standard', {shipInfoID}, 'Warehouse', '{d1}', '{d2}')
                                    ;''', c)
            break
        elif (option == "3"):
            return None
        else:
            print("[ERROR] Invalid Input")

    getOrderID = executeSQLFromLocal(f'''SELECT max(orderID) 
                                        FROM Orders;
                                        ''', c)
    
    orderID = getOrderID[0][0]
    if (orderID == None):
            orderID = 0
    else:
        orderID = int(getOrderID[0][0])
        orderID+=1
    
    #print(f"Creating Order: {orderID}, {registryID}, {shippingID}, {shipInfoID}, {bankInfoID}")
    ##_____________________________________________________________
    # ORDER CREATION
    ##_____________________________________________________________

    time.sleep(2)
    executeSQLFromLocal(f'''INSERT INTO Orders 
                            VALUES({orderID}, '{"Processed"}', {registryID}, {shippingID}, {shipInfoID}, {bankInfoID})
                            ;''', c)
    time.sleep(2)
    for book in check_selected:
        executeSQLFromLocal(f'''INSERT INTO CheckoutBasket 
                                VALUES({book[0]},{orderID})
                                ;''', c)
        time.sleep(2)
        executeSQLFromLocal(f'''DELETE FROM SelectedBooks 
                                WHERE {book[0]} = SelectedBooks.ISBN AND
                                {user.userID} = SelectedBooks.userID
                                ;''', c)
        time.sleep(2)
        remove_book(c, user, book[0])

def select_book(c, user, selection):
    os.system('cls')
    #___________________________________________________________
    # CHECKING IF BOOK ALREADY EXISTS
    #___________________________________________________________
    check_book = executeSQLFromLocal(f'''SELECT * 
                                        FROM Book
                                        WHERE {selection} = Book.ISBN''', c)
    if (len(check_book) == 0):
        print("[ERROR] Book does not exist.")
        time.sleep(1)
        return None
    
    if (check_book[0][6] == 0):
        print("[ERROR] Book is out of stock.")
        time.sleep(1)
        return None
    #___________________________________________________________
    # CHECKING IF BOOK IS ALREADY SELECTED BY USER
    #___________________________________________________________
    check_book = executeSQLFromLocal(f'''SELECT * 
                                        FROM SelectedBooks
                                        WHERE {selection} = SelectedBooks.ISBN
                                        AND {user.userID} = SelectedBooks.userID''', c)
    if (len(check_book) != 0):
        print("[ERROR] Book is already selected.")
        return None
    #___________________________________________________________
    # SELECTING BOOK
    #___________________________________________________________
    executeSQLFromLocal(f'''INSERT INTO SelectedBooks
                            VALUES ({selection},{user.userID})''', c)
    os.system('cls')

def deselect_book(c, user, selection):
    os.system('cls')
    #___________________________________________________________
    # CHECKING IF BOOK ALREADY EXISTS
    #___________________________________________________________
    check_book = executeSQLFromLocal(f'''SELECT * 
                                        FROM Book
                                        WHERE {selection} = Book.ISBN''', c)
    if (len(check_book) == 0):
        print("[ERROR] Book does not exist.")
        return None

    #___________________________________________________________
    # CHECKING IF BOOK IS ALREADY SELECTED BY USER
    #___________________________________________________________
    check_book = executeSQLFromLocal(f'''SELECT * 
                                        FROM SelectedBooks
                                        WHERE {selection} = SelectedBooks.ISBN
                                        AND {user.userID} = SelectedBooks.userID''', c)
    if (len(check_book) == 0):
        print("[ERROR] Book is not selected by you.")
        return None
    #___________________________________________________________
    # SELECTING BOOK
    #___________________________________________________________
    executeSQLFromLocal(f'''DELETE FROM SelectedBooks
                            WHERE {selection} = SelectedBooks.ISBN
                            AND {user.userID} = SelectedBooks.userID''', c)
    os.system('cls')
    
def print_selected_books(c, user):
    os.system('cls')
    selected_books = executeSQLFromLocal(f'''SELECT Book.ISBN, Book.title, BookAuthors.author, BookGenres.genre, Book.price, Book.pageNum, Publisher.name, Book.quantity
                                            FROM Book, SelectedBooks
                                            INNER JOIN BookAuthors ON BookAuthors.ISBN=Book.ISBN
                                            INNER JOIN BookGenres ON BookGenres.ISBN=Book.ISBN
                                            INNER JOIN Publisher ON Publisher.pID=Book.publisher
                                            WHERE {user.userID} = SelectedBooks.userID 
                                            AND SelectedBooks.ISBN = Book.ISBN''', c)
    if (len(selected_books) == 0):
        print("[EMPTY]")
        while (True):
            exit_option = input("\nExit (Enter): ")
            break
    else:
        for book in selected_books:
            print(f"    (IBSN: {book[0]}) {book[1]} by {book[2]} [{book[3]}] (${book[4]})\n     Pages: {book[5]}\n     Published By: {book[6]}\n     In Stock: {book[7]}")
        while (True):
            exit_option = input("\nExit (Enter): ")
            break
    os.system('cls')

def print_table(c, option, search_input):
    os.system('cls')
    os.system('color 70')
    columns = [('ISBN',), ('Title',), ('Author(s)',), ('Genre(s)',), ('(CDN$) Price',), ('No. of Pages',), ('Publisher',), ('Quantity',)]

    sort_queries = ["title ASC","title DESC","author ASC","author DESC"]
    search_queries = ["=title","=author","=genre","=Publisher.name","=Book.ISBN"]

    if (option >= 1 and option <= 4):
        rows = executeSQLFromLocal(f'''SELECT Book.ISBN, title, author, genre, price, pageNum, Publisher.name, quantity
                                        FROM Book
                                        INNER JOIN BookAuthors ON BookAuthors.ISBN=Book.ISBN
                                        INNER JOIN BookGenres ON BookGenres.ISBN=Book.ISBN
                                        INNER JOIN Publisher ON Publisher.pID=Book.publisher
                                        ORDER BY {sort_queries[option-1]}''', c)
    else:
        rows = executeSQLFromLocal(f'''SELECT Book.ISBN, title, author, genre, price, pageNum, Publisher.name, quantity
                                        FROM Book
                                        INNER JOIN BookAuthors ON BookAuthors.ISBN=Book.ISBN
                                        INNER JOIN BookGenres ON BookGenres.ISBN=Book.ISBN
                                        INNER JOIN Publisher ON Publisher.pID=Book.publisher
                                        WHERE '{search_input}'{search_queries[option-5]}
                                        ORDER BY Book.ISBN ASC''', c)
    length = build_column_names(columns)
    build_line(length)

    try:
        for row in rows:
            build_row(row)
            build_line(length)
    except:
        pass

    while (True):
        exit_option = input("\nExit (Enter): ")
        break
        
    os.system('color 07')
    os.system('cls')

# REGISTRY_____________________________________________________
def register(c, user, bankInfo, shipInfo):

    ##_____________________________________________________________
    # ADD TO REGISTRY
    ##_____________________________________________________________
    result = executeSQLFromLocal(f'''SELECT registryID 
                                    FROM Registered_User
                                    WHERE {user.userID}=Registered_User.userID;''', c)
    if (len(result) == 0):
        result = executeSQLFromLocal(f'''SELECT max(registryID) 
                                        FROM Registered_User;
                                        ''', c)
        registryID = result[0][0]
        if (registryID == None):
            registryID = 0
        else:
            registryID = int(registryID)
            registryID+=1

        executeSQLFromLocal(f'''INSERT INTO Registered_User 
                                VALUES({registryID}, {user.userID})
                                ;''', c)
    else:
        registryID = result[0][0]
    ##_____________________________________________________________
    # ADD BANKING INFO
    ##_____________________________________________________________
    result = executeSQLFromLocal(f'''SELECT max(bankInfoID) 
                                    FROM Banking_Info;
                                    ''', c)
    bankID = result[0][0]
    if (bankID == None):
        bankID = 0
    else:
        bankID = int(bankID)
        bankID+=1
    
    for info in bankInfo:
        executeSQLFromLocal(f'''INSERT INTO Banking_Info 
                                VALUES({bankID}, '{info[0]}', {info[1]}, '{info[2]}')
                                ;''', c)
        executeSQLFromLocal(f'''INSERT INTO User_BankInfo 
                        VALUES({registryID}, {bankID})
                        ;''', c)
        bankID+=1

    ##_____________________________________________________________
    # ADD SHIPPING INFO
    ##_____________________________________________________________
    result = executeSQLFromLocal(f'''SELECT max(shipInfoID) 
                                    FROM Shipping_Info;
                                    ''', c)
    shipID = result[0][0]
    if (shipID == None):
        shipID = 0
    else:
        shipID = int(shipID)
        shipID+=1
    
    for info in shipInfo:
        executeSQLFromLocal(f'''INSERT INTO Shipping_Info 
                                VALUES({shipID}, '{info[0]}', '{info[1]}', '{info[2]}', '{info[3]}')
                                ;''', c)
        executeSQLFromLocal(f'''INSERT INTO User_ShipInfo 
                                VALUES({registryID}, {shipID})
                                ;''', c)
        shipID+=1

def remove_shipping():
    pass

def remove_banking():
    pass

def register_menu(c, user):
    os.system('cls')
    print_register_menu()

    option = str(input("    Option: "))
    while (option != "0"):
    #___________________________________________________________
    # USER REGISTER
    #___________________________________________________________
        if (option == "1"):
            os.system('cls')
            additionComplete = False
            while (additionComplete == False):
                register_valid = True
                shipping_valid = True

                bankInfo = []
                shippingInfo = []

                print("\n- No Spaces\n- No Hyphens\n\nType 'exit' to exit.\n\n")
                print("[NOTICE] Type 'stop' to stop input.\n")
                broke = False
                while (True):
                    name = str(input("Name on Card: "))
                    if (name == "stop"): break
                    if (name == "exit"): 
                        broke = True
                        break

                    bankNum = str(input("Card Number (XXXXXXXXXXXXXXXX): "))
                    if (bankNum == "stop"): break
                    if (bankNum == "exit"): 
                        broke = True
                        break

                    expiryDate = str(input("Expiry Date (MM/YY): "))
                    if (expiryDate == "stop"): break
                    if (expiryDate == "exit"): 
                        broke = True
                        break
                    
                    if (empty_result(name) or empty_result(bankNum) or empty_result(expiryDate)):
                        register_valid = False
                    elif (name == "exit" or bankNum == "exit" or expiryDate == "exit"):
                        broke = True
                        break
                    else:
                        bankInfo.append((name, bankNum, expiryDate))

                if (broke):
                    break

                print("[NOTICE] Type 'stop' to stop input.\n")
                while (True):
                    address = str(input("Address ('stop' to stop input): "))
                    if (address == "stop"): break
                    if (address == "exit"): 
                        broke = True
                        break

                    province = str(input("Province: "))
                    if (province == "stop"): break
                    if (province == "exit"): 
                        broke = True
                        break

                    city = str(input("City: "))
                    if (city == "stop"): break
                    if (city == "exit"): 
                        broke = True
                        break

                    postal = str(input("Postal Code (XXX XXX): "))
                    if (postal == "stop"): break
                    if (postal == "exit"): 
                        broke = True
                        break
                    if (empty_result(address) or empty_result(province) or empty_result(city) or empty_result(postal)):
                        shipping_valid = False
                    elif (address == "stop" or province == "stop" or city == "stop" or postal == "stop"):
                        break
                    elif (address == "exit" or province == "exit" or city == "exit" or postal == "exit"):
                        broke = True
                        break
                    else:
                        shippingInfo.append((address, province, city, postal))
                if (broke):
                    break
                    
                print(bankInfo)
                print(shippingInfo)

                if (register_valid and shipping_valid and len(bankInfo) != 0):
                    register(c, user, bankInfo, shippingInfo)
                else:
                    break
            os.system('cls')
            print_register_menu()
    
    #___________________________________________________________
    # VIEW INFORMATION
    #___________________________________________________________
        elif (option == "2"):
            print_information(c, user)
            while (True):
                exit_option = input("\nExit (Enter): ")
                break
        else:
            print("[ERROR] Invalid Input.")

        os.system('cls')
        print_register_menu()
        option = str(input("    Option: "))

    os.system('cls')

def print_information(c, user):
        shipping_results = executeSQLFromLocal(f'''SELECT Shipping_Info.shipInfoID, Shipping_Info.address, Shipping_Info.province, Shipping_Info.city, Shipping_Info.postal
                                                    FROM Shipping_Info, User_ShipInfo, Registered_User 
                                                    WHERE {user.userID}=Registered_User.userID 
                                                    AND Registered_User.registryID=User_ShipInfo.registryID
                                                    AND User_ShipInfo.shipInfoID=Shipping_Info.shipInfoID''',c)

        banking_results = executeSQLFromLocal(f'''SELECT Banking_Info.bankInfoID, Banking_Info.name, Banking_Info.cardNum, Banking_Info.expiryDate
                                                    FROM Banking_Info, User_BankInfo, Registered_User 
                                                    WHERE {user.userID}=Registered_User.userID 
                                                    AND Registered_User.registryID=User_BankInfo.registryID
                                                    AND User_BankInfo.bankInfoID=Banking_Info.bankInfoID''',c)
        os.system('cls')
        print(f"SHIPPING:\n")
        for address in shipping_results:
            print(f"Shipping Information ID: {address[0]}\nAddress: {address[1]}\nProvince: {address[2]}\nCity: {address[3]}\nPostal Code: {address[4]}\n")
        print(f"BANKING:\n")
        for banking in banking_results:
            print(f"Banking Information ID: {banking[0]}\nName on Card: {banking[1]}\nCard Number: {address[2]}\nExpiry Date:: {address[3]}\n")

##_____________________________________________________________
# OWNER FUNCTIONS
##_____________________________________________________________

def add_book(title, authors, genres, price, pageNum, publisher, publisherCut, ISBN, c):
    os.system('cls')
    #___________________________________________________________
    # CHECK IF PUBLISHER IS VALID
    #___________________________________________________________
    check_publisher = executeSQLFromLocal(f'''SELECT * 
                                            FROM Publisher
                                            WHERE {publisher} = Publisher.pID''', c)
    
    if (len(check_publisher) == 0):
        print("[ERROR] Publisher does not exist.")
        return None
        
    publisherID = check_publisher[0][0]
    if (publisherID == None):
        print("[ERROR] Publisher ID is wrong or does not exist.")
        return None

    #___________________________________________________________
    # CHECK IF ISBN IS VALID
    #___________________________________________________________
    check_ISBN = executeSQLFromLocal(f'''SELECT Book.quantity 
                                            FROM Book
                                            WHERE {ISBN} = Book.ISBN''', c)
    
    ISBN_exists = False
    if (len(check_ISBN) != 0):
        print("[ERROR] ISBN Exists.")
        ISBN_exists = True

    #___________________________________________________________
    # IF ALREADY EXISTS, ADD TO QUANTITY
    #___________________________________________________________
    if (ISBN_exists):
            executeSQLFromLocal(f'''UPDATE Book 
                                    SET quantity = {check_ISBN[0][0]+1}
                                    WHERE {ISBN} = Book.ISBN''', c)
    #___________________________________________________________
    # OTHERWISE, ADD TO BOOK TABLE
    #___________________________________________________________
    else:
        executeSQLFromLocal(f'''INSERT INTO Book 
                                VALUES({ISBN}, '{title}', {price}, {pageNum}, {publisher}, {publisherCut}, {1})
                                ;''', c)

    #___________________________________________________________
    # ADD TO AUTHORS AND GENRES
    #___________________________________________________________
        for author in authors:
            print(author)
            executeSQLFromLocal(f'''INSERT INTO BookAuthors (ISBN, author)
                                VALUES ({ISBN}, '{author}')''', c)
        for genre in genres:
            executeSQLFromLocal(f'''INSERT INTO BookGenres (ISBN, genre)
                                VALUES ({ISBN}, '{genre}')''', c)
    os.system('cls')

def remove_book(c, user, selection):
    os.system('cls')

    #___________________________________________________________
    # CHECKING IF BOOK ALREADY EXISTS
    #___________________________________________________________
    check_book = executeSQLFromLocal(f'''SELECT * 
                                        FROM Book
                                        WHERE {selection} = Book.ISBN''', c)
    if (len(check_book) == 0):
        print("[ERROR] Book does not exist.")
        return None

    #___________________________________________________________
    # REMOVING BOOK
    #___________________________________________________________

    if (check_book[0][6] == 0):
        print("[ERROR] Book quantity is already at 0.")


        return None

    quantity = int(check_book[0][6])-1
    executeSQLFromLocal(f'''UPDATE Book
                        SET quantity = {quantity}
                        WHERE {selection} = Book.ISBN''', c)

    if (quantity == 5):
        send_email(c, user, check_book) 

    if (quantity == 0):
        executeSQLFromLocal(f'''DELETE FROM SelectedBooks
                            WHERE {selection} = SelectedBooks.ISBN''', c)
    os.system('cls')

def delete_book(c, user, selection):
    os.system('cls')

    #___________________________________________________________
    # CHECKING IF BOOK ALREADY EXISTS
    #___________________________________________________________
    check_book = executeSQLFromLocal(f'''SELECT * 
                                        FROM Book
                                        WHERE {selection} = Book.ISBN''', c)
    if (len(check_book) == 0):
        print("[ERROR] Book does not exist.")
        return None

    #___________________________________________________________
    # REMOVING BOOK
    #___________________________________________________________

    executeSQLFromLocal(f'''DELETE FROM Book
                            WHERE {selection} = Book.ISBN''', c)
    executeSQLFromLocal(f'''DELETE FROM BookGenres
                        WHERE {selection} = BookGenres.ISBN''', c)
    executeSQLFromLocal(f'''DELETE FROM BookAuthors
                        WHERE {selection} = BookAuthors.ISBN''', c)
    executeSQLFromLocal(f'''DELETE FROM CheckoutBasket
                        WHERE {selection} = CheckoutBasket.ISBN''', c)
    executeSQLFromLocal(f'''DELETE FROM SelectedBooks
                        WHERE {selection} = SelectedBooks.ISBN''', c)


    os.system('cls')

def add_publisher(name, address, contactEmail, numbers, accountNum, transitNum, institutionNum, c):
        #___________________________________________________________
        # CHECKING IF PUBLISHER ALREADY EXISTS
        #___________________________________________________________
        check_publisher = executeSQLFromLocal(f'''SELECT * 
                                                FROM Publisher
                                                WHERE {name} = Publisher.name''', c)
        #___________________________________________________________
        # GETTING NEXT Publisher ID
        #___________________________________________________________

        result = executeSQLFromLocal(f'''SELECT max(pID) 
                                            FROM Publisher;
                                            ''', c)
        pID = result[0][0]
        if (pID == None):
            pID = 0
        elif (check_publisher != None):
            pID = check_publisher[0][0]
        else:
            pID = int(pID)
            pID+=1
        #___________________________________________________________
        # ADDING PUBLISHER TO TABLE
        #___________________________________________________________

        executeSQLFromLocal(f'''INSERT INTO Publisher 
                                    VALUES({pID}, '{name}', '{address}', '{contactEmail}', '{accountNum}', '{transitNum}', '{institutionNum}')
                                        ;''', c)

        #___________________________________________________________
        # ADDING PHONE NUMBERS TO TABLE
        #___________________________________________________________

        for number in numbers:
            executeSQLFromLocal(f'''INSERT INTO PublisherPhones 
                                        VALUES({pID}, '{number}')
                                            ;''', c)

def send_email(c, user, bookInfo):
    print(f"\n[NOTICE] We've noticed that {bookInfo[0][1]} is almost out of stock! Expect more soon!\n")
        
    check_publisher = executeSQLFromLocal(f'''SELECT Publisher.name
                                            FROM Publisher
                                            WHERE {bookInfo[0][4]} = Publisher.pID''', c)
    print(check_publisher)
    valuesLastMonth = []

    today = datetime.date.today()
    first = today.replace(day=1)
    second = first - datetime.timedelta(days=1)
    last_month = second.replace(day=1)

    for i in range(31):
        date = last_month.strftime("%d/%m/%Y")

        print(date)
        results = executeSQLFromLocal(f'''SELECT Shipping_Company.shippingID, Shipping_Company.departureDate
                                            FROM Shipping_Company, Orders, CheckoutBasket 
                                            WHERE '{bookInfo[0][0]}'=CheckoutBasket.ISBN
                                            AND '{date}'=Shipping_Company.departureDate
                                            AND Shipping_Company.shippingID=Orders.shippingID
                                            AND Orders.orderID=CheckoutBasket.orderID''', c)
        
        print(results)
        time.sleep(1)
        if (len(results) != 0):
            for result in results:
                valuesLastMonth.append(result)
        last_month += datetime.timedelta(days=1)
    
    if (len(valuesLastMonth) != 0):
        email_log = (f"To whom this may concern at {check_publisher[0][0]},\n\nI am emailing from LookInnaBook hoping to order more of '{bookInfo[0][1]}'\nLast month, we've sold {len(valuesLastMonth)} copies, and we hope to recieve as much as we sold.\nCan't wait to hear back.\n\n- LookInnaBook Owner\n{today}\n\n")
        (user.emails).append(email_log)
    time.sleep(2)

def admin_menu(c, user):
    os.system('cls')
    print_admin_menu()

    option = str(input("    Option: "))
    while (option != "0"):
    #___________________________________________________________
    # CREATE ALL TABLES
    #___________________________________________________________
        if (option == "1"):
            executeSQLFromFile("sql_queries\create_tables.sql",c)
    #___________________________________________________________
    # DESTROY ALL TABLES
    #___________________________________________________________
        elif (option == "2"):
            confirm = str(input("    Are you sure? [Y/N]: "))
            if (confirm == "y"):
                executeSQLFromFile("sql_queries\delete_tables.sql", c)
    #___________________________________________________________
    # TESTING
    #___________________________________________________________
        elif (option == "3"):
            add_publisher("Covici Friede", "500 S State St", "covici@gmail.com", [6131234567], "1111222233334444","12345","123", c)
            add_publisher("ABRAMS", "210 S State St", "abrams@gmail.com", [6132225567], "1111222233334445","12345","123", c)
            for i in range(11):
                add_book("Of Mice and Men", ["John Steinbeck"], ["Drama"], 15.00, 200, 0, 10, 1, c)
            for i in range(15):
                add_book("Diary of a Wimpy Kid", ["Jeff Kinney"], ["Comedy"], 15.00, 200, 1, 10, 2, c)
            for i in range(6):
                add_book("Funny Business", ["Jeff Kinney"], ["Comedy"], 13.00, 200, 1, 10, 3, c)
            executeSQLFromFile("sql_queries/fill_tables.sql",c)
    #___________________________________________________________
    # ADDING BOOK
    #___________________________________________________________
        elif (option == "4"):
            os.system('cls')
            additionComplete = False
            while (additionComplete == False):
                book_valid = True
                print("\n- No Spaces\n\nType 'exit' to exit.\n\n")

                # TITLE
                title = str(input("Book Title: "))
                if (empty_result(title)):
                    book_valid = False
                if (title.lower() == "exit"):
                    break

                # AUTHORS
                broke = False
                authors = []
                while (True):
                    author = str(input("Author ('stop' to stop input): "))
                    author.replace(" ", "")
                    if (empty_result(author)):
                        book_valid = False
                    elif (author == "stop"):
                        break
                    elif (author == "exit"):
                        broke = True
                        break
                    else:
                        authors.append(author)
                if (broke):
                    break

                # GENRES
                genres = []
                while (True):
                    genre = str(input("Genre ('stop' to stop input): "))
                    if (empty_result(genre)):
                        book_valid = False
                    elif (genre == "stop"):
                        break
                    elif (genre == "exit"):
                        broke = True
                        break
                    else:
                        genres.append(genre)
                if (broke):
                    break

                # PRICE
                price = str(input("Price: "))
                if (empty_result(price)):
                    book_valid = False
                if (price.lower() == "exit"):
                    break

                # NUMBER OF PAGES
                pageNum = str(input("No. of Pages: "))
                if (empty_result(pageNum)):
                    book_valid = False
                if (pageNum.lower() == "exit"):
                    break

                # PUBLISHER ID
                publisher = str(input("Publisher (ID): "))
                if (empty_result(publisher)):
                    book_valid = False
                if (publisher.lower() == "exit"):
                    break

                # PUBLISHER SALES CUT
                publisherCut = str(input("Publisher's Cut: "))
                if (empty_result(publisherCut)):
                    book_valid = False
                if (publisherCut.lower() == "exit"):
                    break

                # ISBN 
                ISBN = str(input("ISBN: "))
                if (empty_result(ISBN)):
                    book_valid = False
                if (ISBN.lower() == "exit"):
                    break

                if (book_valid):
                    add_book(title, authors, genres, price, pageNum, publisher, publisherCut, ISBN, c)
                
            #print_menu(user)
    #___________________________________________________________
    # REMOVE BOOK
    #___________________________________________________________
        elif (option == "5"):
            selection = str(input("    Selection (ISBN)\n'exit' to cancel: "))
            if (selection != "exit"):
                remove_book(c, user, selection)

    #___________________________________________________________
    # DELETE BOOK
    #___________________________________________________________
        elif (option == "6"):
            selection = str(input("    THIS WILL DELETE ALL ENTRIES OF THIS BOOK\n     Selection (ISBN)\n'exit' to cancel: "))
            if (selection != "exit"):
                delete_book(c, user, selection)

    #___________________________________________________________
    # ADDING PUBLISHER
    #___________________________________________________________
        elif (option == "7"):
            os.system('cls')
            additionComplete = False
            while (additionComplete == False):
                publisher_valid = True
                print("\n- No Spaces\n\nType 'exit' to exit.\n\n")

                # NAME
                name = str(input("Name: "))
                if (empty_result(name)):
                    publisher_valid = False
                if (name.lower() == "exit"):
                    break

                # ADDRESS
                address = str(input("Address: "))
                if (empty_result(address)):
                    publisher_valid = False
                if (address.lower() == "exit"):
                    break

                # CONTACT EMAIL
                contactEmail = str(input("Contact Email: "))
                if (empty_result(contactEmail)):
                    publisher_valid = False
                if (contactEmail.lower() == "exit"):
                    break

                # CONTACT NUMBERS
                broke = False
                numbers = []
                while (True):
                    number = str(input("Number ('stop' to stop input): "))
                    if (empty_result(number)):
                        publisher_valid = False
                    elif (number == "stop"):
                        break
                    elif (number == "exit"):
                        broke = True
                        break
                    else:
                        numbers.append(number)
                if (broke):
                    break

                # PUBLISHER ID
                accountNum = str(input("Banking Account Number: "))
                if (empty_result(accountNum)):
                    publisher_valid = False
                if (accountNum.lower() == "exit"):
                    accountNum

                # PUBLISHER SALES CUT
                transitNum = str(input("Banking Transit Number: "))
                if (empty_result(transitNum)):
                    publisher_valid = False
                if (transitNum.lower() == "exit"):
                    break

                # ISBN 
                institutionNum = str(input("Banking Institution Number: "))
                if (empty_result(institutionNum)):
                    publisher_valid = False
                if (institutionNum.lower() == "exit"):
                    break
                
                if (publisher_valid):
                    add_publisher(name, address, contactEmail, numbers, accountNum, transitNum, institutionNum, c)
                    additionComplete = True
            
    #___________________________________________________________
    # SEE STATISTICS
    #___________________________________________________________
        elif (option == "8"):
            os.system('cls')
            print("\nACCOUNTING STATISTICS:")
            print("\n   OVERALL GAIN STATISTIC:")

            sales_loss_result = executeSQLFromLocal('''SELECT Book.Price, Book.PublisherCut
                                                        FROM CheckoutBasket, Book
                                                        WHERE CheckoutBasket.ISBN=Book.ISBN''',c)
            
            find_most_occurence_book = executeSQLFromLocal('''SELECT Book.title, CheckoutBasket.ISBN, COUNT(CheckoutBasket.ISBN)*(Book.price) AS Occurence
                                                            FROM CheckoutBasket, Book, BookAuthors
                                                            WHERE CheckoutBasket.ISBN=Book.ISBN
                                                            AND BookAuthors.ISBN=Book.ISBN
                                                            GROUP BY CheckoutBasket.ISBN
                                                            ORDER BY COUNT(CheckoutBasket.ISBN) DESC''',c)
                                                            
            find_most_occurence_author = executeSQLFromLocal('''SELECT BookAuthors.author, SUM(Book.price), COUNT(CheckoutBasket.ISBN)  
                                                                FROM CheckoutBasket, Book, BookAuthors
                                                                WHERE CheckoutBasket.ISBN=Book.ISBN
                                                                AND BookAuthors.ISBN=Book.ISBN
                                                                GROUP BY BookAuthors.author
                                                                ORDER BY SUM(Book.price) DESC''',c)

            find_most_occurence_genre = executeSQLFromLocal('''SELECT BookGenres.genre, SUM(Book.price), COUNT(CheckoutBasket.ISBN)  
                                                                FROM CheckoutBasket, Book, BookGenres
                                                                WHERE CheckoutBasket.ISBN=Book.ISBN
                                                                AND BookGenres.ISBN=Book.ISBN
                                                                GROUP BY BookGenres.genre
                                                                ORDER BY SUM(Book.price) DESC''',c)
            total_gained = 0
            total_lost = 0

            for sale in sales_loss_result:
                money_gained = float(sale[0] - ( (sale[1] / 100) * (sale[0]) ) )
                money_lost = float(sale[0] - money_gained)

                total_gained+=money_gained
                total_lost+=money_lost
            
            print(f"    From sales, the bookstore has gained ${total_gained:.2f} in profits.")
            print(f"    However, the bookstore has lost ${total_lost:.2f} in publisher cuts.")

            print("\n   GROSS GAIN BY BOOK STATISTIC:")
            for sale in find_most_occurence_book:
                print(f"    '{sale[0]}' has brought in a gross total of ${sale[2]:.2f}")

            print("\n   GROSS GAIN BY AUTHOR STATISTIC:")
            for sale in find_most_occurence_author:
                print(f"    '{sale[0]}' has brought in a gross total of ${sale[1]:.2f} among {sale[2]} book(s)")

            print("\n   GROSS GAIN BY GENRE STATISTIC:")
            for sale in find_most_occurence_genre:
                print(f"    Books that are considered '{sale[0]}' has brought in a gross total of ${sale[1]:.2f} among {sale[2]} book(s)")

            while (True):
                exit_option = input("\nExit (Enter): ")
                break
        
    #___________________________________________________________   
    # SEE EMAILS
    #___________________________________________________________
        elif (option == "9"):
            os.system('cls')
            if (len(user.emails) == 0):
                print("[EMPTY] No emails were sent out, meaning we're stocked up!")
            else:
                for email in user.emails:
                    print("______________________________________________________\n")
                    print(email)
                    
            while (True):
                exit_option = input("\nExit (Enter): ")
                break
    #___________________________________________________________   
    # FREE QUERY
    #___________________________________________________________
        elif (option == "10"):
            query = str(input("    Query:\n "))
            result = executeSQLFromLocal(query, c)
            print(result)
    
    #___________________________________________________________   
    # VIEW PUBLISHERS
    #___________________________________________________________
        elif (option == "11"):
            publishers = executeSQLFromLocal('''SELECT *
                                                FROM Publisher''',c)
                                            
            if (len(publishers) == 0):
                print(f"[ERROR] There are no publishers.")
            else:
                for publis in publishers:
                    print("\n______________________________________________________________\n")
                    print(f"Publisher ({publis[0]}): {publis[1]}\nAddress: {publis[2]}\nEmail: {publis[3]}\n\nBANKING:\nAccount Number: {publis[4]}\nTransit Number: {publis[5]}\nInstitution Number: {publis[6]}\n\nPhone Numbers:")
                    publisNum = executeSQLFromLocal(f'''SELECT PublisherPhones.contactNum
                        FROM PublisherPhones
                        WHERE {publis[0]} = PublisherPhones.pid''',c)
                    for number in publisNum:                   
                        print(f"{number[0]}")
                        

            while (True):
                exit_option = input("\nExit (Enter): ")
                break         
        else:
            print("[INVALID INPUT]")

        os.system('cls')
        print_admin_menu()
        option = str(input("    Option: "))

    os.system('cls')

if __name__ == "__main__":
    main()