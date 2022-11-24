import pandas as pd
import mysql.connector as my
import os

try:
    con = my.connect(host='localhost', user='root',
                     passwd='', database='bank')
    cur = con.cursor()
except my.errors.DatabaseError:
    print('Server Connection Failed')

LENGTH = 30

loggeduserdata = pd.DataFrame([])
start = 'mainmenu'


def heading_print(name):
    """
    Displays a good looking heading. 
    """
    os.system('cls' if os.name == 'nt' else 'clear')    # clearing screen
    print("#", "-"*LENGTH, "#")     # decorative purpose
    n = name.title().center(LENGTH, "-")    # centers the text for a given LENGTH
    print("#", n, "#")
    # If the user is logged in then display the name
    if not loggeduserdata.empty:
        loggedmsg = f"Logged in as : {loggeduserdata['name'][0]}"
        print("#", f"{loggedmsg}".center(LENGTH, "-"), "#")


def input_choice(msg="Enter your choice: "):
    """
    Take choice as integer from the user.
    Returns an int.
    """
    print("#", "-"*LENGTH, "#")     # decorative purpose
    choice = int(input(msg))
    return choice


def enter_to_continue():
    """
    Just stops the program for readability.
    Returns None.
    """
    c = input("Press Enter to continue: ")
    return


def mainmenu():
    heading_print("main menu")
    d = ['New User Registration',
         'LogIn',
         'Personal Banking',
         'Exit Program']
    codes = [
        'new_user_registration',
        'login',
        'personalbanking',
        'exit'
    ]
    df = pd.DataFrame([], index=range(1, len(codes)+1))
    df["Choices"] = d
    df["Codes"] = codes
    print(df.Choices)
    choice = input_choice()
    new = df['Codes'][choice]
    return new


def new_user_registration():
    heading_print("New User Registration")
    accno = int(input('Account Number: '))
    name = input("Full name: ")
    branch = input("Enter Branch code (PAT): ") or "PAT"
    passwd = input("Create Password: ")
    q = f"""
    INSERT INTO 
        users (accno, name, passwd, branch)
    VALUES
        ({accno}, '{name}', '{passwd}', "{branch}")
    """
    try:
        cur.execute(q)
        con.commit()
    except Exception as e:
        print(e)
        print("Invalid details please try again.")
        enter_to_continue()
        return 'new_user_registration'
    print("New user created. Login to continue.")
    enter_to_continue()
    new = 'login'
    return new


def login():
    heading_print("LogIn")
    global loggeduserdata
    accno = input('Account Number: ')
    passwd = input('Password: ')
    q = f"SELECT * FROM users WHERE accno='{accno}' and passwd='{passwd}';"
    loggeduserdata = pd.read_sql(q, con)
    if loggeduserdata.empty:
        print("No user with that Acc no. and password exists.")
    else:
        print("Logged In as", loggeduserdata["name"][0] + ".")
    enter_to_continue()
    new = 'mainmenu'
    return new


def personalbanking():
    # Is avalaible only if user is logged in.
    if not loggeduserdata.empty:
        heading_print("Personal Banking")
        d = {
            "Choices": [
                'Balance Details',
                'Deposit Amount',
                'Withdraw Amount',
                'Atm Card Details',
                'Delete Account',
                'Back to Main Menu'],
            "Codes": [
                'show_balance',
                'dep_amnt',
                'wit_amnt',
                'atmcard',
                'del_acc',
                'mainmenu']
        }
        ndf = pd.DataFrame(d, index=range(1, 7))
        print(ndf['Choices'])
        choice = input_choice()
        return ndf['Codes'][choice]
    else:
        print("Please Login first.")
        enter_to_continue()
        return "login"


def show_balance():
    heading_print("your balance")
    bal = loggeduserdata.loc[0, 'balance']
    print("Your Balance is:", bal)
    enter_to_continue()
    return "personalbanking"


def add_amnt(amt):
    """
    "Adds" a given amount to the balance of the logged in user.
    Can also be negative.
    """
    global loggeduserdata
    newamt = loggeduserdata['balance'][0] + amt
    accno = loggeduserdata['accno'][0]
    # update sql
    q = f"UPDATE users SET balance={newamt} WHERE accno={accno};"
    # update df
    loggeduserdata.loc[0, 'balance'] = newamt
    cur.execute(q)
    con.commit()
    return newamt


def dep_amnt():
    heading_print("Deposit Amount")
    dpam = float(input('Enter Amount to be deposited:'))
    newamt = add_amnt(dpam)
    print(f"Amount of INR {dpam} successfully deposited.")
    print(f"New Balance: {newamt}")
    enter_to_continue()
    new = 'personalbanking'
    return new


def wit_amnt():
    heading_print("Withdraw Amount")
    wtam = float(input('Enter Amount to be withdrawl:'))
    newamt = loggeduserdata['balance'][0] - wtam
    # cannot withdraw if low balance
    if newamt < 0:
        print("Not enough balance. try again.")
        enter_to_continue()
        return 'wit_amnt'
    else:
        add_amnt(-wtam)
        print(f"Amount of INR {wtam} successfully deposited.")
        print(f"New Balance: {newamt}")
        enter_to_continue()
        new = 'personalbanking'
        return new


def logout():
    global loggeduserdata
    loggeduserdata = pd.DataFrame([])   # clearing dataframe
    print("Logged out successfully.")
    enter_to_continue()
    return "mainmenu"


def del_acc():
    global loggeduserdata
    heading_print("Delete Account")
    confirm = input('Are you sure you want to delete this account? (y/n) ')
    confirm = confirm.lower()
    if confirm == 'y' or confirm == 'yes':
        # update sql
        accno = loggeduserdata['accno'][0]
        q = f"DELETE FROM users WHERE accno={accno};"
        cur.execute(q)
        con.commit()
        # update df
        loggeduserdata = pd.DataFrame([])
        print("Account successfully deleted.")
        enter_to_continue()
        return 'mainmenu'
    else:
        return 'personalbanking'


while True:
    if start == 'mainmenu':
        start = mainmenu()
    elif start == 'new_user_registration':
        start = new_user_registration()
    elif start == 'login':
        start = login()
    elif start == 'personalbanking':
        start = personalbanking()
    elif start == 'show_balance':
        start = show_balance()
    elif start == 'dep_amnt':
        start = dep_amnt()
    elif start == 'wit_amnt':
        start = wit_amnt()
    elif start == 'logout':
        start = logout()
    elif start == 'del_acc':
        start = del_acc()
    elif start == 'exit':
        break
