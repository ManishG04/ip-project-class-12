import pandas as pd
import mysql.connector as my

a = []
dtf = pd.DataFrame(a)
try:
    con = my.connect(host='localhost', user='root',
                     passwd='admin1234', database='bank')
    cur = con.cursor()
    q2 = "select * from amount;"
    dtf = pd.read_sql(q2, con)
except my.errors.DatabaseError:
    print('Server Connection Failed')


def values():
    for val in dtf:
        return val


start = 'mainmenu'


def mainmenu():
    d = ['New User Registration',
         'LogIn']
    global df
    df = pd.DataFrame(d, index=[1, 2])
    print(df)
    new = 'new_user_registration'
    return new


def new_user_registration():
    global acno, cifno, brcd, regno
    acno = int(input('Account Number:'))
    cifno = int(input('CIF Number:'))
    brcd = input('Branch Code:')
    regno = int(input('Registered Mobile No.:'))
    new = 'login'
    return new


def login():
    global usrnm, pswd, new
    usrnm = input('Username:')
    pswd = input('Password:')
    while values() != dtf[login(usrnm)].amount:
        global ndtf
        ndtf = pd.read_sql(q2, con)
    new = 'personalbanking'
    return new


def personalbanking():
    nd = ['Balance Details',
          'Deposit Amount',
          'Withdraw Amount',
          'ATM Card details',
          'All account Holders',
          'Delete Account']
    global ndf
    ndf = pd.DataFrame(nd, index=[1, 2, 3, 4, 5, 6])
    print(ndf)
    new = 'dep_amnt'
    return new


def dep_amnt():
    global dpam
    dpam = int(input('Enter Amount to be deposited:'))
    if ndtf[login(usrnm)].amount > dtf[login(usrnm)].amount:
        print('Amount has been deposited.')
    new = 'wit_amnt'
    return new


def wit_amnt():
    global wtam
    wtam = int(input('Enter Amount to be withdrawl:'))
    if ndtf[login(usrnm)].amount < dtf[login(usrnm)].amount:
        print('Amount has been deposited.')
    new = 'atmcard'
    return new


def atmcard():
    print()
    print('Account Number:', new_user_registration(acno))
    print('CIF Number:', new_user_registration(cifno))
    new = 'acc_holders'
    return new


def del_acc():
    global acc
    acc = input('Account to be deleted:')
    if acc == new_user_registration(acno):
        dtf.drop(new_user_registration(acno), axis=1)
    else:
        print('Your Account cannot be found or it has already been deleted!')
    new = 'exit'
    return new


while True:
    if start == 'mainmenu':
        start = mainmenu()
    elif start == 'exit':
        break
    global choice1
    choice1 = int(input('Enter your choice:'))
    if choice1 == 1:
        start = new_user_registration()
    else:
        start = login()
        global choice2
        choice2 = int(input('Enter your choice:'))
        if choice2 == 1:
            print()
        elif choice2 == 2:
            start = dep_amnt()
        elif choice2 == 3:
            start = wit_amnt()
        elif choice2 == 4:
            start = atmcard()
# elif choice2 == 5:
# print(acc_holders())
        elif choice2 == 6:
            start = del_acc()
