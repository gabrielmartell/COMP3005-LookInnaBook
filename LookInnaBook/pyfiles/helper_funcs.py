# USEFUL QUERIES/GLOBAL
sortBy = 0
printTitle = '''
    ██╗░░░░░░█████╗░░█████╗░██╗░░██╗  ██╗███╗░░██╗░█████╗░  ██████╗░░█████╗░░█████╗░██╗░░██╗
    ██║░░░░░██╔══██╗██╔══██╗██║░██╔╝  ██║████╗░██║██╔══██╗  ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝
    ██║░░░░░██║░░██║██║░░██║█████═╝░  ██║██╔██╗██║███████║  ██████╦╝██║░░██║██║░░██║█████═╝░
    ██║░░░░░██║░░██║██║░░██║██╔═██╗░  ██║██║╚████║██╔══██║  ██╔══██╗██║░░██║██║░░██║██╔═██╗░
    ███████╗╚█████╔╝╚█████╔╝██║░╚██╗  ██║██║░╚███║██║░░██║  ██████╦╝╚█████╔╝╚█████╔╝██║░╚██╗
╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝  ╚═╝╚═╝░░╚══╝╚═╝░░╚═╝  ╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝
    '''

def build_column_names(c):
    column_name_row = ""
    for name in c:
        column_name_row += ("| %-20s" % name[0])
    column_name_row += "|"

    print(column_name_row)
    return (len(column_name_row)-2)
    
def build_line(length):
    column_line = "|"

    for i in range(length):
        column_line += "_"
    column_line+="|"

    print(column_line)

def build_row(row):
    row_string = ""
    for value in row:
        row_string += ("| %-20s" % value)
    row_string += "|"
    print(row_string)

def print_menu(user):

    print(printTitle)

    if (user.loggedIn == True):
        print(f"    [1] Logout")
    else:
        print(f"    [1] Login")
    
    if (user.loggedIn == False):
        print(f"    [2] Create Account")
    else:
        print(f"    [2] View Books")

    if (user.loggedIn):
        print(f"    [3] Registry")

    if (user.owner):
        print(f"    [4] Admin Menu")

    print(f"    [0] Exit\n")
    
    if (user.owner == True):
        print(f"    Logged In: {user.fname} (OWNER)")
    else:
        print(f"    Logged In: {user.fname}")

def print_book_searches_options(user):
    print(f"    \nHello {user.fname},\n__________________________________________\n")
    print(f"    [1] View By Title (A-Z)")
    print(f"    [2] View By Title (Z-A)")
    print(f"    [3] View By Author (A-Z)")
    print(f"    [4] View By Author (Z-A)\n__________________________________________\n")
    print(f"    [5] Search by Title")
    print(f"    [6] Search by Author")
    print(f"    [7] Search by Genre")
    print(f"    [8] Search by Publisher")
    print(f"    [9] Search by ISBN\n__________________________________________\n")
    print(f"    [10] View Basket")
    print(f"    [11] Select Books")
    print(f"    [12] Unselect Books\n__________________________________________\n")
    print(f"    [13] Checkout")
    print(f"    [14] Check Orders\n")
    print(f"    [0] Return\n")

def print_register_menu():
    print(f"    [1] Register")
    print(f"    [2] View Information")
    print(f"    [0] Return\n")

def print_admin_menu():
    print(f"    [1] Create Tables")
    print(f"    [2] Delete Tables")
    print(f"    [3] Fill Tables\n")
    print(f"    [4] Add Book")
    print(f"    [5] Remove Book")
    print(f"    [6] Delete Book")
    print(f"    [7] Add Publisher\n")

    print(f"    [8] Accounting Statistics")
    print(f"    [9] Email Automation Checker (EAC)")
    print(f"    [10] Free Query")
    print(f"    [11] View Publishers\n")
    print(f"    [0] Return\n")

def passwords_match(p1, pc):
    return (p1 == pc)

def empty_result(result):
    return (len(result) == 0)