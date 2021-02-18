from tkinter import Tk, messagebox
import tkinter, random, sqlite3


loginpg = tkinter.Tk()
loginpg.title("Welcom to GuessWhat!!!!!")
loginpg.geometry("450x400+400+200")


############ Creating a database to store players details in it
# playersDB = sqlite3.connect("PlayersDetails.db")
# c = playersDB.cursor()
# c.execute("""CREATE TABLE PlayersDetails(
#     firstname TEXT,
#     lastname TEXT,
#     email TEXT,
#     username TEXT,
#     password TEXT,
#     phonenumber INTEGER,
#     coin INTEGER
# )""")
# playersDB.commit()
# c.close()

#i define variables here as global so each function can use it easily
#loginpage username, password
usernameV = tkinter.StringVar()
passwordV = tkinter.StringVar()
#Sign Up details
Sname = tkinter.StringVar()
Slastname = tkinter.StringVar()
Semail = tkinter.StringVar()
Susername = tkinter.StringVar()
Spassword = tkinter.StringVar()
Sphone = tkinter.StringVar()
#forgot password page to get name and password we get the email
ForgottenEmailV = tkinter.StringVar()
#choosepg
GameModeName = tkinter.StringVar()
GuessListName = tkinter.StringVar()
#playmodes
GuessLetterV = tkinter.StringVar()
#helpmode
LettersCount = tkinter.IntVar()
Letter = GuessLetterV.get()
#moneypage
AddedCoins = tkinter.StringVar()

#this is a class of a human to get each player's details
class Human:
    def __init__(self, name, lastname, email, username, paswd, phone, coin=100):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = paswd
        self.phone = phone
        self.coin = coin
#this is a global player so we can call the Player who (loged in) in the hole game
Player = Human("Esmaeil","FaakheriAlamdaari","EsmaeilFaakheriAlamdaari@gmail.com","E.F.A","12345","123456789",100)


#this counter is defined here so each time we open a new game , counter starts a new counting ftom zero
Counter = 0
#this function creates a random word of the choosen topic
def createARandWord():
    global Counter
    Counter=0
    #We add name's files in to a dictionary (with dB_To_Dictionary & get_MainDic)
    def dB_To_Dictionary(name,MDic):
        go=[]
        with open("lists/"+name+".txt","r+") as namelist:
            NameL = namelist.readlines()
            for nlist in NameL:
                index = nlist.find("\n")
                if index != -1:
                    go.append(((nlist[:index]).lower()).replace(" ",""))
                else:
                    go.append(nlist.lower())
            MDic.update({f"{name}" : go})
        return MDic


    def get_MainDic():
        MainDic={}
        for name in ["animals","boys","girls","fruits","countries","musics","colors"]:
            MainDic = dB_To_Dictionary(name, MainDic)
        return MainDic


    NamesDic=get_MainDic()
    nnlist = NamesDic.get(GuessListName.get())
    RandomName = str(random.choice(nnlist))
    Nameslen = len(RandomName)
    print(RandomName)
    temp_1 = f"The Word is one of the {GuessListName.get()} names and it has {Nameslen} letters"
    playPage([RandomName,temp_1,"$" * Nameslen])


#this function gets results of the playguess and choose we won or lost
def ResultGenerator(result):
    ResulPage = tkinter.Toplevel()
    ResulPage.title("GAME OVER")
    ResulPage.geometry("450x400+400+200")
    
    f_1 = tkinter.Frame(ResulPage)
    f_1.grid(row=0, column=0)
    f_2 = tkinter.Frame(ResulPage)
    f_2.grid(row=1, column=0)
    
    ShownText = ""
    if result:
        Player.coin += 50
        playersDB = sqlite3.connect("PlayersDetails.db")
        c = playersDB.cursor()
        c.execute("""UPDATE PlayersDetails SET coin=:coin WHERE firstname=:firstname""",
        {'coin':Player.coin,'firstname':Player.name})
        playersDB.commit()
        c.close()
        ShownText = "Congratulation,You Won and Got 50 coins"
    else:
        ShownText = "Sorry,You Lost"
        
    ResultLabel = tkinter.Label(f_1, text = ShownText) 
    ResultLabel.grid(row=0, column=0)    
    cancelSP = tkinter.Button(f_2, text="Exit", command=ResulPage.quit, width=24)
    cancelSP.grid(row=0, column=0)
    confirmSP = tkinter.Button(f_2, text="Play a new Game", command= lambda:choosePage(), width=24)
    confirmSP.grid(row=0, column=1) 
    ResulPage.mainloop()   


#this page is called when user needs some cheet
def game_help(Randomdata):
    Randomdata = list(Randomdata)
    Ghelp = tkinter.Toplevel(loginpg)
    Ghelp.title("Help page!!!!!")

    f_1 = tkinter.Frame(Ghelp)
    f_1.grid(row=0, column=0)
    f_2 = tkinter.Frame(Ghelp)
    f_2.grid(row=1, column=0)
    f_3 = tkinter.Frame(Ghelp)
    f_3.grid(row=2, column=0, columnspan=2)

    l_1 = tkinter.Label(f_1, text="""Each letter costs 10$, write how many letters you want to know:""")
    l_1.grid(row=0, column=0)
    E_1 = tkinter.Entry(f_2, textvariable=LettersCount)
    E_1.grid(row=0,column=0)
    E_1.delete(0,tkinter.END)

    
    #this function gives the letters between the letters the we haven't guessed it yet
    def showHelp():
        Needed_Letters = LettersCount.get()
        ChoosenLabel = Randomdata[2]
        Selectedname = Randomdata[0]
        if ChoosenLabel.count("$") == len(ChoosenLabel):
            ChoosenLabel = []
        else:
            for i in ChoosenLabel:
                if i == "$":
                    ChoosenLabel.remove("$")
                try:
                    ChoosenLabel.remove("$")
                except ValueError:
                    print("EFA_Error")                

        if ChoosenLabel !=[]:
            print(ChoosenLabel)
            for i in ChoosenLabel:
                try:
                    Selectedname.remove(i)
                except ValueError:
                    print(i,"is not in the Name so it must be an Error")

        T=""
        if Needed_Letters <= len(Selectedname):
            for i in range(Needed_Letters):
                RLetters = random.choice(Selectedname)
                Selectedname.remove(RLetters)
                T += f"{RLetters}, "
            Player.coin -= Needed_Letters*10
            print(Player.coin)
            HelpAnswer = messagebox.showinfo("Letter Guess Game's Help",T)
        else:
            G = "Please give a number of letters you need to know not more(please don't mention how many letters you have got write) and  remmember that you can only write the letters until you have got at least one guess"
            HelpAnswer = messagebox.showwarning("Letter Guess Game's Help",G)

    
    cancelPB = tkinter.Button(f_3, text="Cancel", command=Ghelp.quit, width=18)
    cancelPB.grid(row=0, column=0)
    confirmB = tkinter.Button(f_3, text="Confirm", command=showHelp, width=18)
    confirmB.grid(row=0, column=1)
    Ghelp.mainloop()


#this function gets data from the playpage_1 and chooses if we won or lost or we have choise or not
def pLayGuessWhat_1(RData):
    Letter=GuessLetterV.get()
    Faultscount = choiseCounter(False)
    ChoosenName = list(RData[2])
    if Faultscount < len(RData[0])-1 :
        if RData[2] == RData[0]:
            ResultGenerator(True)
        else:    
            try:
                exists = RData[0].index(Letter)
            except ValueError:
                exists = -1

            first=-1
            if Letter not in RData[2] and exists !=-1:
                Count = RData[0].count(Letter)
                while Count>0:
                    exists = RData[0].index(Letter,first+1)
                    first = exists
                    Count -= 1
                    ChoosenName[exists] = Letter
            else:
                Panswer_1 = messagebox.showinfo("Notice",f"You Lost a Choise, You have {len(RData[0])-Faultscount-1} guess left")
                choiseCounter(True)

            RData[2] = "".join(ChoosenName)

    else:
        Panswer_2 = messagebox.showinfo("Sorry","You cant't have another guess")
        ResultGenerator(False)

    return RData


#this function gets data from the playpage_2 and chooses if we won or lost or we have choise or not
def pLayGuessWhat_2(RData):
    word = GuessLetterV.get()
    if RData[0] == word:
        RData[2] = RData[0]
        ResultGenerator(True)
    else:
        ResultGenerator(False)
    return RData


#this function is used in the PlayGuess functions to count how many choise we have left(it is until to the Randomwords letters count)
def choiseCounter(Tl):
    global Counter
    if Tl==True:
        Counter += 1
    return Counter


# #this page gets the letter/words and sends it to pLayGuessWhat_1/2 and if it needs some help with the letters it goes to Gamehelp
def playPage(Randomdata):            
    PPG = tkinter.Toplevel(loginpg)
    PPG.title(f"EFA_Guess{GameModeName.get()}!!")

    f_1 = tkinter.Frame(PPG)
    f_1.grid(row=0, column=0)
    f_2 = tkinter.Frame(PPG)
    f_2.grid(row=1, column=0)
    f_3 = tkinter.Frame(PPG)
    f_3.grid(row=2, column=0, columnspan=3)

    l_1 = tkinter.Label(f_1,text=Randomdata[1])
    l_1.grid(row=0, column=0)
    l_2 = tkinter.Label(f_2, text=Randomdata[2])
    l_2.grid(row=0, column=0)
    E_1_1 = tkinter.Entry(f_2, textvariable=GuessLetterV)
    E_1_1.grid(row=0, column=1)
    E_1_1.delete(0,tkinter.END)


    def playGame():
        if GameModeName.get() == "Letters":
            GottenData = pLayGuessWhat_1(Randomdata)
        elif GameModeName.get() == "Words":
            GottenData = pLayGuessWhat_2(Randomdata)
        else:
            print("there is an Error") 
        
        l_1 = tkinter.Label(f_1,text=GottenData[1])
        l_1.grid(row=0, column=0)
        l_2 = tkinter.Label(f_2, text=GottenData[2])
        l_2.grid(row=0, column=0) 
        E_1_1.delete(0,tkinter.END)                 

    cancelPB = tkinter.Button(f_3, text="Cancel", command=PPG.quit, width=18)
    cancelPB.grid(row=0, column=0)
    cancelPB = tkinter.Button(f_3, text="HELP", command=lambda:game_help(Randomdata), width=18)
    cancelPB.grid(row=0, column=1)
    confirmB = tkinter.Button(f_3, text="Confirm", command=playGame, width=18)
    confirmB.grid(row=0, column=2)
    PPG.mainloop()


#this page we choose game mode and lists topic or get some coins and sends it to the play function
def choosePage():
    choosepg = tkinter.Toplevel()
    choosepg.title("EFA_GuessWhat!!")
    choosepg.geometry("450x400+400+200")

    f_1 = tkinter.Frame(choosepg)
    f_1.grid(row=0, column=0)
    f_2 = tkinter.Frame(choosepg)
    f_2.grid(row=1, column=0)
    f_3 = tkinter.Frame(choosepg)
    f_3.grid(row=2, column=0, columnspan=2)
    f_4 = tkinter.Frame(choosepg)
    f_4.grid(row=3, column=0)
    f_5 = tkinter.Frame(choosepg)
    f_5.grid(row=4, column=0, columnspan=7)
    f_6 = tkinter.Frame(choosepg)
    f_6.grid(row=5, column=0, columnspan=3)

    l_1 = tkinter.Label(f_1,height=5,text=" "*10+f"Hello {(Player.name).upper()} {(Player.lastname).upper()} WELCOM TO THE GUESS WHAT!!!!! ")
    l_1.grid(row = 0, column=0)
    l_2 = tkinter.Label(f_2, height=5, text=" "*30+"Choose Your Game Mode: ")
    l_2.grid(row=0, column=0)
    l_3 = tkinter.Label(f_4, height=5, text=" "*25+"Choose Your Favorite Topic ")
    l_3.grid(row=0, column=0)

    GameMode = [("Guess Letters Game","Letters"),("Guess Words Game","Words")]
    i=0
    for Mode, ModeV in GameMode:
        tkinter.Radiobutton(f_3, text=Mode, value=ModeV, variable=GameModeName).grid(row=0,column=i)
        i +=1

    Topics=[("Animals","animals"),("Boys","boys"),("Girls","girls"),("Colors","colors"),
            ("Countries","countries"),("Fruits","fruits"),("Musics","musics")]
    j=0
    for Topic,T in Topics:
        tkinter.Radiobutton(f_5, text=Topic, value=T, variable=GuessListName).grid(row = 0, column=j)
        j +=1


    cancelPB = tkinter.Button(f_6, text="Cancel", command=choosepg.quit, width=18)
    cancelPB.grid(row=0, column=0)
    cancelPB = tkinter.Button(f_6, text="Buy Coins", command= lambda : moneypage(choosepg), width=18)
    cancelPB.grid(row=0, column=1)
    confirmB = tkinter.Button(f_6, text="Enter Game", command=createARandWord, width=18)
    confirmB.grid(row=0, column=2)
    choosepg.mainloop()


#this function chooses if it is loginpage or signuppage or passwordforgotpage and sends data to the choosepage
def gamechooser(Pn):
    global Player
    if Pn == 1:
        playersDB = sqlite3.connect("PlayersDetails.db")
        c = playersDB.cursor()
        UserName = usernameV.get()
        PassWord = passwordV.get()
        if UserName == "" or PassWord == "":
            alert_1 = messagebox.showwarning("Notice","Please Fill All Boxes To Pass")
        else:
            c.execute("SELECT * FROM PlayersDetails WHERE username = :username AND password = :password",{"username":UserName,"password":PassWord})
            DBdetails=c.fetchall()
            c.close()

            if DBdetails == []:
                alert_2 = messagebox.showerror("Error","Username or password is not defined")
            else:
                PlayerD=DBdetails[0]
                Player=Human(PlayerD[0],PlayerD[1],PlayerD[2],PlayerD[3],PlayerD[4],PlayerD[5],PlayerD[6])
                choosePage()

    elif Pn == 2:
        playersDB = sqlite3.connect("PlayersDetails.db")
        c = playersDB.cursor()
        Flag=True
        SName = Sname.get().lower()
        SLast = Slastname.get().lower()
        SUser = Susername.get().lower()
        SPass = Spassword.get().lower()
        SEmail = Semail.get().lower()
        SPhone = Sphone.get()

        try:
            SPhone = int(SPhone)
        except ValueError:
            alert_1_2 = messagebox.showwarning("Error","Please Fill PhoneNumber Boxes with only numbers")

        if SName == "" or SLast == "" or SEmail == "" or SUser == "" or SPass == "" or SPhone==0:
            alert_3 = messagebox.showwarning("Notice","Please Fill All Boxes To Pass")
        else:
            Player = Human(SName, SLast, SEmail, SUser, SPass, SPhone, 100)

            c.execute("SELECT * FROM PlayersDetails WHERE firstname=:firstname",{"firstname":SName})
            if len(c.fetchall()) !=0:
                selected_text=f"Sorry!! This firstname, has already been used in the game's DB "
                select_1 = messagebox.showwarning("Warning",selected_text)
                Flag=False

            c.execute("SELECT * FROM PlayersDetails WHERE lastname = :lastname",{"lastname":SLast})
            if len(c.fetchall()) !=0:
                selected_text=f"Sorry!! This lastname, has already been used in the game's DB "
                select_1 = messagebox.showwarning("Warning",selected_text)
                Flag=False

            c.execute("SELECT * FROM PlayersDetails WHERE email=:email",{"email":SEmail})
            if len(c.fetchall()) !=0:
                selected_text=f"Sorry!! This email, has already been used in the game's DB "
                select_1 = messagebox.showwarning("Warning",selected_text)
                Flag=False

            c.execute("SELECT * FROM PlayersDetails WHERE username=:username",{"username":SUser})
            if len(c.fetchall()) !=0:
                selected_text=f"Sorry!! This username, has already been used in the game's DB "
                select_1 = messagebox.showwarning("Warning",selected_text)
                Flag=False
            if Flag==True:
                c.execute("INSERT INTO PlayersDetails VALUES (:firstname,:lastname,:email,:username,:password,:phonenumber,:coin)",
                {
                    "firstname":Player.name,
                    "lastname":Player.lastname,
                    "email":Player.email,
                    "username":Player.username,
                    "password":Player.password,
                    "phonenumber":Player.phone,
                    "coin":Player.coin
                })

                c.execute("SELECT oid,* FROM PlayersDetails")
                print(c.fetchall())
                playersDB.commit()
                c.close()
                choosePage()
            else:
                playersDB.commit()
                c.close()
                signUpPage()

    elif Pn == 3:
        playersDB = sqlite3.connect("PlayersDetails.db")
        c = playersDB.cursor()
        Extracoins=0
        try:
            Extracoins = int(AddedCoins.get())
        except ValueError:
            alert_4 = messagebox.showwarning("Error","Please Fill the Box with only integer numbers")

        Player.coin += Extracoins
        c.execute("""UPDATE PlayersDetails SET coin=:coin WHERE firstname=:firstname""",
        {'coin':Player.coin,'firstname':Player.name})
        playersDB.commit()
        c.close()
        choosePage()

    elif Pn==4:
        playersDB = sqlite3.connect("PlayersDetails.db")
        c = playersDB.cursor()
        Em = ForgottenEmailV.get()
        if Em == "":
            alert_1 = messagebox.showwarning("Notice","Please Fill The Box To Send The Details")
        else:
            c.execute("SELECT * FROM PlayersDetails WHERE email =:email",{"email":Em})
            Details = c.fetchall()
            if Details == []:
                av = messagebox.showwarning("Warning",f"{Em} doesn't exists in the DataBase,make sure it is correct")
            else:
                Manswer = messagebox.showinfo("congradulation",f"your username and password is sent to {Em}")
    else:
        print("there is an Unknown Error")


#this function adds coin to the players class
def moneypage(master):
    MPG = tkinter.Toplevel(master)
    MPG.title("Coin Shop")
    MPG.geometry("480x150+400+350")

    f_1 = tkinter.Frame(MPG)
    f_1.grid(row=0,column=0)
    f_2 = tkinter.Frame(MPG)
    f_2.grid(row=1, column=0,columnspan=2)
    f_3 = tkinter.Frame(MPG)
    f_3.grid(row=2, column=0,columnspan=2)

    l_1 = tkinter.Label(f_1, text="20 coins costs only 0.98 $")
    l_1.grid(row=0,column=0)
    l_2 = tkinter.Label(f_2, text="how much coin you want?")
    l_2.grid(row=0, column=0)

    e = tkinter.Entry(f_2, textvariable=AddedCoins)
    e.grid(row=0,column=1)

    cancelSP = tkinter.Button(f_3, text="Cancel", command=MPG.quit, width=24)
    cancelSP.grid(row=0, column=0)
    confirmSP = tkinter.Button(f_3, text="Confirm", command= lambda:gamechooser(3), width=24)
    confirmSP.grid(row=0, column=1)
    MPG.mainloop()


#passwordForgotPage is opened after loginpage then sends player's email to the gamechooser to decide what to do
def passwordForgotPage():
    PFP = tkinter.Toplevel(loginpg)
    PFP.title("Forgot Password")
    PFP.geometry("480x150+400+350")

    f_1 = tkinter.Frame(PFP)
    f_1.grid(row=0, column=0, rowspan=2)
    f_2 = tkinter.Frame(PFP)
    f_2.grid(row=1, column=0, columnspan=2)

    l_1 = tkinter.Label(f_1, height=10, text="""Please write Your Email ,
    to send Username and password for you:""")
    l_1.grid(row=0, column=0)
    ForgottenEmailE = tkinter.Entry(f_1, textvariable=ForgottenEmailV)
    ForgottenEmailE.grid(row=0, column=1)

    cancelPB = tkinter.Button(f_2, text="Cancel", command=PFP.quit, width=24)
    cancelPB.grid(row=0, column=0)
    confirmB = tkinter.Button(f_2, text="Confirm", command=lambda:gamechooser(4), width=24)
    confirmB.grid(row=0, column=1)
    PFP.mainloop()


#signuppage is opened after loginpage then saves and sends player's data to the gamechooser to decide what to do
def signUpPage():
    SP = tkinter.Toplevel(loginpg)
    SP.title("Sign Up Page")
    SP.geometry("460x650+300+10")

    f_1 = tkinter.Frame(SP)
    f_1.grid(row=0, column=0, columnspan = 2)
    f_2 = tkinter.Frame(SP)
    f_2.grid(row=1, column=0, columnspan = 2)
    f_3 = tkinter.Frame(SP)
    f_3.grid(row=2, column=0, columnspan = 2)
    f_4 = tkinter.Frame(SP)
    f_4.grid(row=3, column=0, columnspan = 2)
    f_5 = tkinter.Frame(SP)
    f_5.grid(row=4, column=0, columnspan = 2)
    f_6 = tkinter.Frame(SP)
    f_6.grid(row=5, column=0, columnspan = 2)
    f_7 = tkinter.Frame(SP)
    f_7.grid(row=6, column=0, columnspan = 2)
    f_8 = tkinter.Frame(SP)
    f_8.grid(row=7, column=0, columnspan = 2)

    l_1 = tkinter.Label(f_1, height=5, text="Name: " + 50*" ")
    l_1.grid(row = 0, column=0)
    l_2 = tkinter.Label(f_2, height=5, text="Last Name: " + 39 * " ")
    l_2.grid(row=0, column=0)
    l_3 = tkinter.Label(f_3, height=5, text="Email: " + 48 * " ")
    l_3.grid(row=0, column=0)
    l_4 = tkinter.Label(f_4, height=5, text="User name: " + 38 * " ")
    l_4.grid(row = 0, column=0)
    l_5 = tkinter.Label(f_5, height=5, text="Password: " + 39 * " ")
    l_5.grid(row = 0, column=0)
    l_6 = tkinter.Label(f_6, height=5, text="Phone: " + 44 * " ")
    l_6.grid(row=0, column=0)

    e_1 = tkinter.Entry(f_1, textvariable = Sname)
    e_1.grid(row = 0, column=1)
    e_2 = tkinter.Entry(f_2, textvariable = Slastname)
    e_2.grid(row = 0, column=1)
    e_3 = tkinter.Entry(f_3, textvariable = Semail)
    e_3.grid(row = 0, column=1)
    e_4 = tkinter.Entry(f_4, textvariable = Susername)
    e_4.grid(row = 0, column=1)
    e_5 = tkinter.Entry(f_5, textvariable = Spassword)
    e_5.grid(row = 0, column=1)
    e_6 = tkinter.Entry(f_6, textvariable = Sphone)
    e_6.grid(row = 0, column=1)

    cancelSP = tkinter.Button(f_8, text="Cancel", command=SP.quit, width=24)
    cancelSP.grid(row=0, column=0)
    confirmSP = tkinter.Button(f_8, text="Confirm", command= lambda:gamechooser(2), width=24)
    confirmSP.grid(row=0, column=1)
    SP.mainloop()


#loginpage is opened at first then sends player's data to the gamechooser to decide what to do
def loginPage():
    f_1 = tkinter.Frame(loginpg)
    f_1.grid(row = 0, column = 0, columnspan = 2)
    f_2 = tkinter.Frame(loginpg)
    f_2.grid(row = 1, column = 0, columnspan = 2)
    f_3 = tkinter.Frame(loginpg)
    f_3.grid(row = 2, column = 0, columnspan = 2)
    f_4 = tkinter.Frame(loginpg)
    f_4.grid(row = 3, column = 0, columnspan = 2)
    f_5 = tkinter.Frame(loginpg)
    f_5.grid(row = 4, column = 0, columnspan = 2)

    l_1 = tkinter.Label(f_1,height=5, text = "UserName:"+" "*17)
    l_1.grid(row = 0, column=0)
    l_2 = tkinter.Label(f_2,height=5, text="Password:" + " " * 18)
    l_2.grid(row=0, column=0)
    l_3 = tkinter.Label(f_3,height=5, text="Not a Member?            ")
    l_3.grid(row=0, column=0)
    l_4 = tkinter.Label(f_4,height=5, text = "Forgot Password (and) Username?")
    l_4.grid(row=0, column=0)

    e_1 = tkinter.Entry(f_1, textvariable = usernameV)
    e_1.grid(row = 0, column=1)
    e_2 = tkinter.Entry(f_2, textvariable = passwordV)
    e_2.grid(row=0, column=1)

    signupB = tkinter.Button(f_3, text = "Sign Up", command=signUpPage, width=20)
    signupB.grid(row = 0, column=1)
    PassFB = tkinter.Button(f_4, text="Help", command=passwordForgotPage, width=20)
    PassFB.grid(row=0, column =1)
    exitB = tkinter.Button(f_5, text="Exit", command=loginpg.quit, width=24)
    exitB.grid(row=0, column=0)
    confirmB = tkinter.Button(f_5, text="Enter", command=lambda:gamechooser(1), width=24)
    confirmB.grid(row=0, column=1)
    loginpg.mainloop()


#This Game is created by ESMAEIL FAAKHERI ALAMDAARI   975367018
loginPage()
