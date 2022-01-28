import mysql.connector as mysql
from random import randint # CREATE ACCOUNT NO

# GLOBAL VARIABLES
result: str = None
Loginid: str = None

# CREATE CONNECTION
def create_connection():
    connection = mysql.connect(host="localhost", user="root", passwd="root", database="bank")
    return connection

def Logincheck(Loginid, Password):
    sq1 = "SELECT * FROM account WHERE user_id=%s AND Password=%s"
    data =(Loginid, Password,)
    con = create_connection()
    c = con.cursor() #' cursor' method give you the cursor to work with your code, point to the particular location
    c.execute(sq1, data) # 'execute' method for execute anything
    myresult = c.fetchone()
    return bool(myresult)

def get_Login(Loginid):
    sq1 = "SELECT * FROM account WHERE user_id=%s"
    data = (Loginid,)
    con = create_connection()
    c = con.cursor()
    c.execute(sq1, data)
    result = c.fetchone()
    print(result)
    return result

def get_result(Loginid, Password):
    #GLOBAL RESULT
    sq1 = "SELECT * FROM account WHERE user_id=%s AND Password=%s"
    data = (Loginid, Password, )
    con = create_connection()
    c = con.cursor()
    c.execute(sq1, data)
    result = c.fetchone()
    # print(myresult)
    return result

def Login():
    global Loginid
    Loginid = input("Enter Login Id ::")
    Password = input("Enter Password ::")
    if Logincheck(Loginid, Password) is True:
        myresult = get_result(Loginid, Password)

        if Loginid == myresult[6] and Password == myresult[7]:
            print("\tLogin Successfull !\n")
            print("\tWelcome To Your Profile\n")
            
    else:
        print("Your details are not matched with our system\nPlease Register Yourself or Enter correct USERID and PASSWORD")
        main1() 
        

def user_db():
    sq1 = "SELECT user_id FROM account"
    con = create_connection()
    c = con.cursor()
    c.execute(sq1)
    return c.fetchall()

# CREATE user_Id
def create_ID(name, dob):  
    name = name.split()
    dob = dob.split("/")

    user_id = (name[0]+dob[1]+name[-1])
    user_DB = (each[0] for each in user_db())

    # WHEN SAME 'user_id' IS AVAILABLE THEN (add 4 digit random no) Create UNIQUE 'user_id'
    if user_id in user_DB:
       
        while True:

            temp_id = user_id + str(randint(1000, 9999))
            print("temp_id", temp_id)

            if temp_id not in user_DB:

                return temp_id

    print("Returing the user ID", user_id)
    return user_id

# OPEN ACCOUNT
def OpenAc():

    n = input("Enter Your Name: ")

    #ac=input("Enter Your Account No: ")

    ac = randint(1111111111, 9999999999)

    #print("Your Account Number is : ", ac)

    db = input("Enter D.O.B in This Format(DD/MM/YY): ")

    p = input("Enter Phone: ")

    ad = input("Enter Address: ")

    balance = int(input("Enter Opening Balance :"))

    # CREATE login id
    ID = create_ID(n, db)
    print("Your unique user ID is ", ID)
    password = input('Enter Password(Must be unique) :')

    data1 = (n, ac, db, ad, p, balance, ID, password)

    sql1 = 'insert into account values(%s,%s,%s,%s,%s,%s,%s,%s)'

    con = create_connection()
    c = con.cursor()

    c.execute(sql1, data1)

    con.commit()

    print("Account Creation is Successfull!")
    main1()

# DEPOSIT
def DepoAm():

    result = get_Login(Loginid)
    am = int(input("Enter Amount to Deposit : "))
    ac = result[1]
    tam = result[5]+am
    sql = "update account set balance=%s where acno=%s"
    d = (tam, ac)
    con = create_connection()
    c = con.cursor()
    c.execute(sql, d)
    con.commit()
    print("Your Current Account Balance : ", tam)
    main2()

# WITHDRAWAL
def WdrawAm():
    result = get_Login(Loginid)
    am = int(input("Enter Amount to Withdraw: "))
    ac = result[1]

    if (am <= result[5]):
        tam = result[5]-am
        sql = "update account set balance=%s where acno=%s"
        d = (tam, ac)
        con = create_connection()
        c = con.cursor()
        c.execute(sql, d)
        con.commit()
        print(am, " Deducted Sucessfully ! ")
        print("Your Current Account Balance :", tam)
       
    else:
        print("You've not enough balance to withdraw ! ")
        print("Your Account Balance : ", result[5])
    main2()


def Balance():
    result = get_Login(Loginid)
    print("Your Account Balance :", result[1], " is :: ", result[5])
    main2()


def DisAcc():
    result = get_Login(Loginid)
    print("Profile Name is :: \t", result[0])
    print("Account number is :: \t", result[1])
    print("Date of Birth is :: \t", result[2])
    print("Address is :: \t\t", result[3])
    print("Phone Number is :: \t", result[4])
    print("User id is :: \t\t", result[6])
    print("User password is \t\t*****")
    main2()

# CLOSE ACCOUNT
def CloseAc():
    result = get_Login(Loginid)
    ac = result[1]
    con = create_connection()
    c = con.cursor()
    sql = "delete from account where acno=%s"
    d = (ac,)
    c.execute(sql, d)
    con.commit()
    print(f"{result[0]} Your Account is Closed!")

# CHANGE PASSWORD
def ChangePassword():
    result = get_Login(Loginid)
    am = input("Enter New Password : ")
    if(am != result[7]):

        con = create_connection()
        c = con.cursor()
        ac = result[1]
        sql = "update account set Password=%s where acno=%s"
        d = (am, ac)
        c.execute(sql, d)
        con.commit()
        print(f"Your old password is :: {result[7]} Changed to :: {am}")
    else:
        print("Your new password is same with Old password. \n \tPlease retry again! ")
    main2()

def main1():

    print("========WELCOME TO THE BANKING SYSTEM========")
    print("""
        => If you want to 'LOGIN' type '1'
        => If you want to 'REGISTER' type '2'
            """)
    choice = input("Enter Your choice :: ")
    if(choice == '1'):
        Login()
    elif(choice == '2'):
        OpenAc()
    else:
        print("Wrong Input")
        print("You have to choose between the given options")
        main1()


main1()


def main2():
    print("Welcome to the Dashboard")
    print("""
        1.Deposit Amount

        2.Withdraw Amount

        3.Balance Enquiry

        4.Display Coustomer Details            

        5.Change Password

        6.Close My AC

        7.Logout
            """)

    choice = input("Choose between the given options :: ")

   
    if(choice == '1'):

        DepoAm()

    elif(choice == '2'):

        WdrawAm()

    elif(choice == '3'):

        Balance()

    elif(choice == '4'):

        DisAcc()

    elif(choice == '5'):

        ChangePassword()

    elif(choice == '6'):

        CloseAc()

    elif(choice == '7'):
        print("You've been sucessfully Logout, from the system.")
        exit()

    else:
        print("Wrong Input")
        main2()
  
main2()