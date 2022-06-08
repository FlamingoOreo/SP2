from tkinter import  *
import mysql.connector as mysql
import winsound
from DataBaseConfig import dbconfig
from Functions import *  # Importing the functions from the module created to support the application's features
import tkinter.messagebox as mbox



window = Tk()
window.iconbitmap("LockIcon.ico")  # The icon top left of the application
window.title("Password Vault")
window.geometry("800x500")
window.configure(bg="#008b8b")
window.resizable(False,False)  # Prevents resizable windows as GUI can glitch
""" FUNCTIONS """
def twofactor():
    """
    As security is important, 2FA is an expected service for any online authentication in 2022
    WIP.......................................................................................
    """
    pass

def FORGET_WINDOW():
    """
    After the User has authenticated, the root login window is forgotten and cannot be accessed again
    """
    Root_Password_Entry.destroy()
    Root_Username_Entry.destroy()
    Welcome_Message.forget()
    Root_2FA_Entry.destroy()
    Root_2FA.forget()
    Root_Username.forget()
    Root_Password.forget()
    window.unbind("<Return>") # Unbinds the <enter> on keyboard for the login to prevent any bugs later

def NEW_Search(): # Allows user to search again
    Decrypt_Password.place_forget()
    New_Search.place_forget()
    Add_Update.place_forget()
    Search_By_Name.place(y=280, x=220)
    Search_By_Details.place(y=350, x=220)
    Search_By_Name_Update.place(y=280, x=220)
    Search_By_Details_Update.place(y=350, x=220)
    Search_Output.place_forget()
    Search_Field_Entry.place(y=210, x=220)
    Search_Output_Update.place_forget()
    Search_Field_Entry_Update.place(y=210, x=220)
    Submit_New_Password.place_forget()

def add(): # Displays the Add page
    Add_Page.place(x=0,y=0)
    Back_Arrow.place(x=0,y=0)
    Main_Page.place_forget()
def update(): # Displays the Update page
    Update_Page.place(x=0,y=0)
    Back_Arrow.place(x=0,y=0)
    Main_Page.place_forget()
def search(): # Displays the Search page
    Search_Page.place(x=0,y=0)
    Back_Arrow.place(x=0, y=0)
    Main_Page.place_forget()

def Back(): # The back arrow
    Add_Page.place_forget()
    Search_Page.place_forget()
    Update_Page.place_forget()
    Back_Arrow.place_forget()
    Submit_New_Password.place_forget()
    main()

def login():
    """
    The initial attempt to authenticate the user.
    If the user_input is that of the DBconfig, then they will be Authenticated.
    Being Authenticated is a global variable which allows
    the user to continuously browse and add/remove entries to the database.
    The functions will check often if the AUTHENTICATED is True.Should it be false at any point,then there will be
    limited functionality inside the application
    """
    try:
        conn = mysql.connect(user='{}'.format(Root_Username_Entry.get()),
                             password='{}'.format(Root_Password_Entry.get()),
                             host='127.0.0.1')   # Takes the user_input to attempt login to the SQL database
        cursor = conn.cursor() # This will be whatever your SQL root username + PW currently is. Check DB config file
        cursor.execute("use vault;")
        window.after(200, lambda: Lock_Image.config(file="Lock_Success.png"))
        winsound.PlaySound("Windows Notify Calendar.wav", winsound.SND_ALIAS | winsound.SND_ASYNC)
        window.after(1000,FORGET_WINDOW)  # This is executed to unpack the different widgets for the initial login
        window.after(1500,main)
        WarningLabel.destroy()
        global AUTHENTICATED  # Used throughout the application to confirm authentication. Only set to True here
        AUTHENTICATED = True
        Login.configure(state=DISABLED)
    except mysql.Error as msg:  # If user types wrong details for root, error_counter is increased. At 3 = termination
        global ERRORCOUNTER
        WarningLabel.place(y=400, x=525)  # It lets the user know how many attempts they have left
        ERRORCOUNTER += 1
        ERRORCOUNTER_TEXT.set( "-- INCORRECT -- \n YOU HAVE USED {}/3 ATTEMPTS".format(ERRORCOUNTER)) # ^^^^ text_var
        print(ERRORCOUNTER)
        print("Error",msg)
        window.after(200, lambda: Lock_Image.config(file="Lock_Fail.png"))  # Flicks the lock images to red 1/5th of sec
        winsound.PlaySound("Windows Critical Stop.wav", winsound.SND_ALIAS | winsound.SND_ASYNC)
        window.after(500, lambda: Lock_Image.config(file="Lock.png"))   # Changes it to the regular image
        if ERRORCOUNTER == 3:
            window.destroy()  # 3 unsuccessful attempts and it will terminate the window. In a real-life scenario
        # the user would also not be allowed to re-enter the application. Sake of the prototype, they can re-enter
def main():
    """
    The function that runs after the user has authenticated.
    This will further display on the screen that the user is logged into root
    """
    Main_Page.place(x=0, y=0)
    if AUTHENTICATED == True: # If the user is authenticated, this occurs
        conn = mysql.connect(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("select user();")
        Confirmation = Label(window, text="AUTHENTICATED: {}".format(cursor.fetchall()), # A confirmation message
                             font="Futura 14 bold ", bg="#008b8b", fg="#080808")
        Confirmation.place(y=470, x=0)

def submit():
    """
     Submits a new entry to the SQL database.
     First by checking if the user_input is valid E.G length and password requirements, Then salting the password by
     using the last 4 characters of the password and adding it to the end. This salt is then encrypted and when it is
     decrypted, the salt_remover function will remove the initial salt placed onto the password
    """
    SUBMITABLE = True  # Used to check throughout the adding sequence if the credentials are appropriate to the standard
    if len(Add_Username_Entry.get()) == 0:  # A simple way to check that the field is not empty
        mbox.showerror(title= "Error", message="The username can't be empty")
        SUBMITABLE = False
    elif len(Add_Username_Entry.get()) < 3:  # A simple way to check that a username is not too short
        mbox.showerror(title="Error", message="The username can't be less than 3 characters")
        SUBMITABLE = False
    if passwordrequisite(str(Add_Password_Entry.get())) != True:
        mbox.showerror(title="Error", message='Password Error: ' + str(passwordrequisite(str(Add_Password_Entry.get()))))
        SUBMITABLE = False  # Using the function to check if the password is strong enough, check functions for detail.
    try:
        if AUTHENTICATED and SUBMITABLE == True: # If the user is authenticated and the requirements are met
            conn = mysql.connect(**dbconfig)
            cursor = conn.cursor()
            cursor.execute("use vault;")
            cursor.execute(query, (
            str(Add_Username_Entry.get()), salt_generator(str(Add_Password_Entry.get())), "123123",
            Add_Details_Entry.get()))  # Emphasis on the salt_generator function that changes the password to be salted
            conn.commit()  # Adds the user_input to the database
            Add_Username_Entry.delete(0, 'end')  # Removes the entries
            Add_Password_Entry.delete(0, 'end')
            Add_Details_Entry.delete(0, 'end')
            mbox.showinfo(title="SUCCESS", message="New user added successfully ")
            winsound.PlaySound("Add_Success.wav", winsound.SND_ALIAS | winsound.SND_ASYNC)
    except mysql.Error as msg:
        print(msg)  # This error most likely will be a duplicate entry, as the password column needs to be UNIQUE
        mbox.showerror(title="Error", message="Passwords have to be UNIQUE. This password already exists")


def SEARCH_By_Details(decider):  # Decider is used as both the search and update page uses this function.
    if decider == 0:  # We know that this is from the search page button - Helps with variable control
        decider_entry = Search_Field_Entry
        decider_output = Search_Output
    else:  # Else means that we know that this is from the update page button - Helps with variable control
        decider_entry = Search_Field_Entry_Update
        decider_output = Search_Output_Update
    """
    Searches the SQL database by the entry_input from the user. Returning all the entries with the correct details match
    """
    try:
        if AUTHENTICATED == True: # If the user is authenticated, this occurs
            conn = mysql.connect(**dbconfig)
            cursor = conn.cursor()
            if len(decider_entry.get()) == 0:
                return mbox.showerror(title="ERROR", message="Search must include input")  # If user searches without
            cursor.execute("use vault;")  # typing anything in the input field, it raises this error
            cursor.execute("select username,password,details from Passwordvault where details like '%{}%'".format(
                str(decider_entry.get()))) # Here the query uses "like", this is the same as using IN
            decider_entry.place_forget()
            Update_Password_Entry.place_forget()
            Data = cursor.fetchall()
            if len(Data) == 0:  # If there is no entry matching, this informs the user
                mbox.showerror(title="Entry Not Found",
                               message=f"No entry for '{str(decider_entry.get())}' as Details")
                decider_entry.place(y=210, x=220)
                return None
            ENTRY = []
            ENTRY_COUNTER = 1  # This counter is compared to the COUNT counter to find out which exact entry we are at
            for i in range(len(Data)):
                ENTRY.append(i)
            if len(ENTRY) > 1:  # If there is only one entry in search
                ENTRY_COUNTER = ENTRY[1]
            decider_output.place(y=150, x=220)
            global COUNT # needed to keep track of how many iterations to be able to decrypt the correct iteration
            COUNT = 1
            for x in Data:
                OUTPUT.set(f"Username = {x[0]}\n Password = {x[1]}\n Details = {x[2]}")
                if ENTRY_COUNTER == len(Data): # The last entry, the loop ends here
                    if decider != 0:  # If decider == 0 then it is the search page, or else the update page
                        Search_By_Details_Update.place_forget()
                        Search_By_Name_Update.place_forget()
                        New_Search_Update.place(y=350, x=220)
                        Add_Update.place(y=280, x=220)
                        global entry_to_be_updated
                        entry_to_be_updated = x
                    Search_By_Details.place_forget()
                    Search_By_Name.place_forget()
                    if decider == 0:  # If decider == 0 then it is the search page, or else the update page
                        Decrypt_Password.place(y=280, x=220)
                    New_Search.place(y=350, x=220)
                    global FETCHER # Fetcher tracks the pick by the user. This is then used to decrypt later
                    global USERNAME_CLICKED
                    FETCHER = x[2]
                    USERNAME_CLICKED = False  # Implies if this is a search by username or details, used to decrypt
                    break
                answer = mbox.askyesno(title="VAULT", message=f"Entry: {ENTRY_COUNTER}/{len(Data)} Continue?")
                ENTRY_COUNTER = ENTRY[ENTRY.index(ENTRY_COUNTER)] + 1
                if not answer:  # The entry that the user picks by clicking "no", the loop ends here
                    if decider != 0:  # If decider == 0 then it is the search page, or else the update page
                        Search_By_Details_Update.place_forget()
                        Search_By_Name_Update.place_forget()
                        New_Search_Update.place(y=350, x=220)
                        Add_Update.place(y=280, x=220)
                        entry_to_be_updated = x
                    Search_By_Details.place_forget()
                    Search_By_Name.place_forget()
                    if decider == 0:  # If decider == 0 then it is the search page, or else the update page
                        Decrypt_Password.place(y=280, x=220)
                    New_Search.place(y=350, x=220)
                    FETCHER = x[2]  # Fetcher tracks the pick by the user. This is then used to decrypt later
                    USERNAME_CLICKED = False  # Useful now we know that it is a detail search - For the decrypter
                    break
                COUNT += 1
    except mysql.Error and IndexError as msg:
            mbox.showerror(title="Entry Not Found",
                           message=f"No entry for '{str(decider_entry.get())}' as Details")
            decider_entry.place(y=210, x=220)
            print(msg)


def SEARCH_By_Name(decider=0):  # Decider is used as both the search and update page uses this function.
    if decider == 0:  # We know that this is from the search page button - Helps with variable control
        decider_entry = Search_Field_Entry
        decider_output = Search_Output

    else:
        decider_entry = Search_Field_Entry_Update
        decider_output = Search_Output_Update
        pass  # Else means that we know that this is from the update page button - Helps with variable control

    """
    Searches the SQL database by the entry_input from the user. Returning all the entries with the correct username match
    """
    try:
        if AUTHENTICATED == True:
            conn = mysql.connect(**dbconfig)
            cursor = conn.cursor()
            if len(decider_entry.get()) == 0:
                return mbox.showerror(title="ERROR", message="Search must include input")  # If user searches without
            cursor.execute("use vault;")  # typing anything in the input field, it raises this error
            cursor.execute("select username,password,details from Passwordvault where username like '%{}%'".format(
                str(decider_entry.get())))  # Here the query uses "like", this is the same as using IN
            decider_entry.place_forget()
            Update_Password_Entry.place_forget()
            Data = cursor.fetchall()
            if len(Data) == 0:
                mbox.showerror(title="Entry Not Found",
                               message=f"No entry for '{str(decider_entry.get())}' as Username")
                decider_entry.place(y=210, x=220)
                return None
            ENTRY = []
            ENTRY_COUNTER = 1
            for i in range(len(Data)):
                ENTRY.append(i)
            if len(ENTRY) > 1: # If there is only one entry in search
                ENTRY_COUNTER = ENTRY[1]
            decider_output.place(y=150, x=220)
            global COUNT
            COUNT = 1  # needed to keep track of how many iterations to be able to decrypt the correct iteration
            for x in Data:
                OUTPUT.set(f"Username = {x[0]}\n Password = {x[1]}\n Details = {x[2]}")
                if ENTRY_COUNTER == len(Data):
                    if decider != 0:  # If decider == 0 then it is the search page, or else the update page
                        Search_By_Details_Update.place_forget()
                        Search_By_Name_Update.place_forget()
                        New_Search_Update.place(y=350, x=220)
                        Add_Update.place(y=280, x=220)
                        global entry_to_be_updated
                        entry_to_be_updated = x
                    Search_By_Details.place_forget()
                    Search_By_Name.place_forget()
                    if decider == 0:  # If decider == 0 then it is the search page, or else the update page
                        Decrypt_Password.place(y=280, x=220)
                    New_Search.place(y=350, x=220)
                    global FETCHER
                    global USERNAME_CLICKED
                    FETCHER = x[0] # Fetcher tracks the pick by the user. This is then used to decrypt later
                    USERNAME_CLICKED = True # Implies if this is a search by username or details, used to decrypt
                    break
                answer = mbox.askyesno(title="VAULT", message=f"Entry: {ENTRY_COUNTER}/{len(Data)} Continue?")
                ENTRY_COUNTER = ENTRY[ENTRY.index(ENTRY_COUNTER)] + 1
                if not answer:  # The entry that the user picks by clicking "no", the loop ends here
                    if decider != 0:  # If decider == 0 then it is the search page, or else the update page
                        print("True")
                        Search_By_Details_Update.place_forget()
                        Search_By_Name_Update.place_forget()
                        New_Search_Update.place(y=350, x=220)
                        Add_Update.place(y=280, x=220)
                        entry_to_be_updated = x
                    Search_By_Details.place_forget()
                    Search_By_Name.place_forget()
                    if decider == 0:  # If decider == 0 then it is the search page, or else the update page
                        Decrypt_Password.place(y=280, x=220)
                    New_Search.place(y=350, x=220)
                    FETCHER = x[0] # Fetcher tracks the pick by the user. This is then used to decrypt later
                    USERNAME_CLICKED = True
                    break
                COUNT += 1
    except mysql.Error and IndexError as msg:
        mbox.showerror(title="Entry Not Found", message=f"No entry for '{str(decider_entry.get())}' as Username")
        decider_entry.place(y=210, x=220)
        print(msg)

def DECRYPT_Password():
    """
    A function used to display the decrypted password to the user. This function takes use of another function know as
    the "salt_remover" as the password was stored not only encrypted, but also salted in the SQL database.
    """
    try:
        if USERNAME_CLICKED == True:  # To check if it was a search by Username, if false then the "else" is executed
            counter = 1
            if AUTHENTICATED == True:
                conn = mysql.connect(**dbconfig)
                cursor = conn.cursor()
                cursor.execute("use vault;")
                cursor.execute("select username,cast(aes_decrypt(password,'123123') as char(100)),details from Passwordvault where username = '{}'".format(str(FETCHER)))
                Data = cursor.fetchall() # The encryption key is 123123, of course in a real life scenario, this would
                for x in Data:  # be more advanced and hidden. This key is used to encrypt/decrypt PW stored in SQL
                    if int(counter) == int(COUNT):  # This will find the exact entry that the user has selected using
                        break  # the count variable. As it will equal to the one used during the search for it break
                    else:
                        counter += 1
                y = list(x)  # The data retrieved is a tuple ( not mutable ) thus we convert it to a list, append entry
                y[1] = str(salt_remover(x[1])) # then we turn it back into a tuple with the correct unsalted PW
                desalted = tuple(y)  # As the passwords are salted, this uses a function to un-salt the PW
                OUTPUT.set(f"Username = {desalted[0]}\n Password = {desalted[1]}\n Details = {desalted[2]}")
        else:  # This is executed if the search was by DETAILS. Preforms the same kind of code but different SQL query
            counter = 1
            if AUTHENTICATED == True:
                conn = mysql.connect(**dbconfig)
                cursor = conn.cursor()
                cursor.execute("use vault;")
                cursor.execute("select username,cast(aes_decrypt(password,'123123') as char(100)),details from Passwordvault where details = '{}'".format(str(FETCHER)))
                Data = cursor.fetchall()
                for x in Data:
                    if int(counter) == int(COUNT):  # This will find the exact entry that the user has selected using
                        break  # the count variable. As it will equal to the one used during the search for it break
                    else:
                        counter += 1
                y = list(x) # The data retrieved is a tuple ( not mutable ) thus we convert it to a list, append entry
                y[1] = str(salt_remover(x[1]))  # then we turn it back into a tuple with the correct unsalted PW
                desalted = tuple(y)  # As the passwords are salted, this uses a function to un-salt the PW
                OUTPUT.set(f"Username = {desalted[0]}\n Password = {desalted[1]}\n Details = {desalted[2]}")
    except mysql.Error and NameError as msg:
        print(msg)  # For debugging


def update_password():
    """
    This places the update password entry and the corresponding button
    """
    Update_Password_Entry.place(y=210, x=220)
    Search_Output_Update.place_forget()
    Add_Update.place_forget()
    Submit_New_Password.place(y=280, x=220)




def SUBMIT_Password():
    """
    Submits a new password for the selected Entry, salting it first then lastly storing it in the SQL database using AES
    encryption
    """
    SUBMITABLE = True
    try:
        if passwordrequisite(str(Update_Password_Entry.get())) != True:
            mbox.showerror(title="Error",
                           message='Password Error: ' + str(passwordrequisite(str(Update_Password_Entry.get()))))
            SUBMITABLE = False  # Using the function to check if the password is strong enough, check functions for detail.

        if AUTHENTICATED and SUBMITABLE == True:  # Only executes if both conditions are met
            conn = mysql.connect(**dbconfig)
            cursor = conn.cursor()
            cursor.execute("use vault;")
            cursor.execute(query2, (str(salt_generator(Update_Password_Entry.get())), "123123", str(entry_to_be_updated[0]),str(entry_to_be_updated[2])))
            conn.commit()
            mbox.showinfo(title="SUCCESS", message="Password updated successfully ")
            winsound.PlaySound("Add_Success.wav", winsound.SND_ALIAS | winsound.SND_ASYNC)

    except mysql.Error and TypeError as msg:
        mbox.showerror(title="Error", message="Passwords have to be UNIQUE. This password already exists")
        print(msg)  # This error most likely will be a duplicate entry, as the password column needs to be UNIQUE

    finally:
        if SUBMITABLE == True:
            Update_Password_Entry.place_forget()
            Submit_New_Password.place_forget()
            Update_Password_Entry.delete(0,END)
            Update_Password_Entry.insert(0, "New password")

"""
Tkinter Frames, images, labels, buttons and packs/places  
"""
########## VARIABLES
ERRORCOUNTER = 0
ERRORCOUNTER_TEXT = StringVar()
OUTPUT = StringVar()
AUTHENTICATED = False
query = "insert into passwordvault (username,password,details) values (%s, aes_encrypt(%s, %s), %s)"
query2 = "update passwordvault set password = AES_ENCRYPT(%s,%s) where username = %s and details = %s"
########### FRAMES
Main_Page = Frame(window,width=800,height=500,bg="#008b8b")
Add_Page = Frame(window,width=800,height=500,bg="#008b8b")
Update_Page = Frame(window,width=800,height=500,bg="#008b8b")
Search_Page = Frame(window,width=800,height=500,bg="#008b8b")
########### Images
Lock_Image = PhotoImage(file="Lock.png")
Arrow_Image = PhotoImage(file="Arrow.png")
Submit_Image = PhotoImage(file="Submit.png")
########## LABELS
Welcome_Message = Label(window,text="Welcome to the Password Vault\n Please login to gain access to the vault"
                        ,font="Futura 28 bold ",bg="#008b8b",fg="#080808")
Root_Username = Label(window,text="Root Username:",font="Futura 24 bold",bg="#008b8b",fg="#383838")
Root_Password = Label(window,text="Root Password:",font="Futura 24 bold",bg="#008b8b",fg="#383838")
Root_2FA = Label(window,text="2FA:",font="Futura 24 bold",bg="#008b8b",fg="#383838")
WarningLabel = Label(window, textvariable=ERRORCOUNTER_TEXT,
                     bg="#008b8b", fg="red", font="Arial 13 bold ")
Add_Username = Label(Add_Page,text="Username:",font="Futura 24 bold",bg="#008b8b",fg="#383838")
Add_Password = Label(Add_Page,text="Password:",font="Futura 24 bold",bg="#008b8b",fg="#383838")
Add_Details = Label(Add_Page,text="Details:",font="Futura 24 bold",bg="#008b8b",fg="#383838")
Search_Output = Label(Search_Page, textvariable=OUTPUT, font="Futura 20 bold", bg="#008b8b", fg="#383838")
Search_Output_Update = Label(Update_Page, textvariable=OUTPUT, font="Futura 20 bold", bg="#008b8b", fg="#383838")
####### Entries
Root_Username_Entry = Entry(window,font="Arial 16 bold")
Root_Password_Entry = Entry(window,font="Arial 16 bold",show="*")
Root_2FA_Entry = Entry(window,font="Arial 16 bold")
Root_2FA_Entry.insert(0,"WORK IN PROGRESS")
Root_2FA_Entry.configure(state="disabled")
Add_Username_Entry = Entry(Add_Page,font="Arial 16 bold")
Add_Password_Entry = Entry(Add_Page,font="Arial 16 bold",show="*")
Add_Details_Entry = Entry(Add_Page,font="Arial 16 bold")
Search_Field_Entry = Entry(Search_Page,font="Arial 26 bold")
Search_Field_Entry_Update = Entry(Update_Page,font="Arial 26 bold")
Update_Password_Entry = Entry(Update_Page,font="Arial 24 bold")
Update_Password_Entry.insert(0,"New password")


####### Buttons
Login = Button(height=100,width=100,borderwidth=0,image=Lock_Image,bg="#008b8b",command=login)
Search = Button(Main_Page,text="Search",font="Arial 24 bold",bg="#008b8b",fg="#383838",command=search)
Update = Button(Main_Page,text="Update",font="Arial 24 bold",bg="#008b8b",fg="#383838",command=update)
Add = Button(Main_Page,text="Add",font="Arial 24 bold",bg="#008b8b",fg="#383838",command=add)
Back_Arrow = Button(height=100,width=100,borderwidth=0,image=Arrow_Image,bg="#008b8b",command=Back)
Add_Submit = Button(Add_Page,height=100,width=100,borderwidth=0,image=Submit_Image,bg="#008b8b",command=submit)
window.bind("<Return>", lambda event:login())
Search_By_Name = Button(Search_Page,text="Search by Username",font="Futura 24 bold",bg="#008b8b"
                        ,fg="#383838",command=lambda: SEARCH_By_Name(0))
Search_By_Details = Button(Search_Page,text="Search by Details",font="Futura 24 bold",bg="#008b8b"
                           ,fg="#383838",command=lambda: SEARCH_By_Details(0))
Decrypt_Password = Button(Search_Page,text="Decrypt Password",font="Futura 24 bold",bg="#008b8b"
                          ,fg="#383838",command=DECRYPT_Password)
New_Search = Button(Search_Page,text="New Search",font="Futura 24 bold",bg="#008b8b",fg="#383838",command=NEW_Search)
New_Search_Update = Button(Update_Page,text="New Search",font="Futura 24 bold",bg="#008b8b",fg="#383838",command=NEW_Search)

Search_By_Name_Update = Button(Update_Page,text="Search by Username",font="Futura 24 bold",bg="#008b8b"
                        ,fg="#383838",command=lambda: SEARCH_By_Name(1))
Search_By_Details_Update = Button(Update_Page,text="Search by Details",font="Futura 24 bold",bg="#008b8b"
                           ,fg="#383838",command=lambda: SEARCH_By_Details(1))
Add_Update = Button(Update_Page,text="Update Password",font="Futura 24 bold",bg="#008b8b"
                           ,fg="#383838",command=update_password)
Submit_New_Password = Button(Update_Page,text="Submit New Password",font="Futura 24 bold",bg="#008b8b"
                           ,fg="#383838",command=SUBMIT_Password)
####### PACKS & PLACES
Welcome_Message.pack(anchor=N,pady=(40.20))
Root_Username_Entry.place(y=180,x=250)
Root_Username.pack(anchor=W,pady=(0,40))
Root_Password_Entry.place(y=265,x=250)
Root_Password.pack(anchor=W,padx=(0,3.5))
Root_2FA_Entry.place(y=345,x=250)
Root_2FA.pack(anchor=W,pady=(40.20),padx=(150,175))
Login.pack()
Search.place(y=200,x=200)
Update.place(y=200,x=350)
Add.place(y=200,x=500)
Add_Username.place(y=150,x=300)
Add_Username_Entry.place(y=190,x=270)
Add_Password.place(y=220,x=300)
Add_Password_Entry.place(y=260,x=270)
Add_Details.place(y=290,x=300)
Add_Details_Entry.place(y=330,x=270)
Add_Submit.place(y=365,x=330)
Search_Field_Entry.place(y=210,x=220)
Search_Field_Entry_Update.place(y=210,x=220)
Search_By_Name.place(y=280,x=220)
Search_By_Details.place(y=350,x=220)
Search_By_Name_Update.place(y=280,x=220)
Search_By_Details_Update.place(y=350,x=220)

window.mainloop()