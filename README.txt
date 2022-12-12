Name: Gabriel Martell
Student #: 101191857

Installation and Execution:
--------------------------------------
This application is ran through a Python Executeable, therefore Python or Python3 will be needed to run this.
You can refer to this "https://realpython.com/run-python-scripts/#:~:text=To%20run%20Python%20scripts%20with,see%20the%20phrase%20Hello%20World!" if need be.
Once that is done, you can run the executeable called "look_inna_book.py", located in the LookInnaBook folder directory. 
Make sure that the "LookInnaBook" folder and all of its elements are contained. There are some directory calls and changing it will cause compile errors. 
TD;LR download the folder not the files within.

This program uses SQLite.

Instructions:
--------------------------------------
From there you can choose to login, create an account, or return. If you wish to see the administration capabilities, you can login with "gabemartell" as the username and "password" as the password.
Otherwise, feel free to create an account and login that way, or you can login with "l_kalife" as the username and "password" as the password.

From there you can Logout, View Books, Register, or view the Admin Menu if registered as an owner. 

From logging out, you will return to the menu on application start up.

From viewing books, you can view the books by sorting or searching. You can also select book, deselect them, and checkout with your selected books.

From the registry, you can register yourself (so you CAN checkout) or view your shipping and banking information.

From the Admin Menu, You can Fill, Remove and Create the database tables. In addition, you can add publishers and add/remove/delete books.
Furthermore, you can view the accounting statistics, view the emails sent out (when an order decreaes past a quantity of five), and view the publishers.
Note that the emails sent out are local to the concurrent application, they are automatically archived (deleted) when the application is closed. It will prioritize moreso like a log of what has been sent out today.

To get the most out of seeing what this program can do, delete the tables, create them, and then fill them again.

Notes:
--------------------------------------
The SQL queries are located in the sql_queries directory.
