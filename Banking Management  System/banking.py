
from tkinter import *
from tkinter import messagebox
import sqlite3
import time

from tkinter.scrolledtext import ScrolledText
from PIL import Image



try:
    con = sqlite3.connect(database = "bank_database.sqlite")
    cur = con.cursor()
    cur.execute("create table customers(account integer primary key autoincrement, name text, password text, mobile text, email text, balance float, date text)")
    con.commit()
    con.close()
except:
    print("Table alredy exists in bank_database.")
    
try:
    con = sqlite3.connect(database = "bank_database.sqlite")
    cur = con.cursor()
    cur.execute("create table transactions(account int, type text, amount float, balance float, date text)")
    con.commit()
    con.close()
except:
    print("Table alredy exists in bank_database.")

bg = 'white'
try:
    bg_file = r"C:\Users\Lenovo\Downloads\wp01.png"
    bg_image = Image.open(bg_file)
    re_image = bg_image.resize((1920,1080))
    bgimg = re_image.save('bgimg.png')
except:
    bg_file = 'bgimg.png'
    
try:
    icon_file = r"D:\pyhon logo.png"
    image = Image.open(icon_file)
    icon = image.save('icon.ico')
except:
    icon_file = 'icon.ico'


bg_img = 'bgimg.png'




win = Tk()
win.title('My Account')
win.iconbitmap('icon.ico')
win.state("zoomed")
#win.configure(bg=bg)
win.minsize(950,500)



#background
bimg = PhotoImage(file = bg_img)
bglbl = Label(win, image = bimg)
bglbl.place(x=0, y=0)


#main heading.
heading_label = Label(win, text = 'ONLINE BANKING', font = ('', 42, 'bold'), bg = bg, fg = '#33ccff')
heading_label.place(relx = .32, rely = .03)


#Frame or screen.
def login_screen():
    frm = Frame(win)
    #frm.configure(bg='green')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    
    #background.
    bimg = PhotoImage(file = bg_img)
    bglbl = Label(frm, image = bimg)
    bglbl.image = bimg
    bglbl.place(x=0, y=0)
    
    #clock.
    
    
    
    #login button funtion.
    def login_button():
        try:
            account_no = int(entryaccount.get())
        except:
            messagebox.showerror("Error","Invalid Account number or Password.\nPlease check and try again.")
            return
        password = entrypass.get()
        
        con = sqlite3.connect(database = "bank_database.sqlite")
        cur = con.cursor()
        cur.execute("select * from customers where account=(?) and password=(?)",(account_no, password))
        con.commit()
        detail = cur.fetchone()
        
        if detail==None:
            messagebox.showerror("Error","Invalid Account number or Password.\nPlease check and try again.")
            return
        
        else:
            account_detail = detail[0]
            name_detail = detail[1]
            password_detail = detail[2]
            mobile_detail = detail[3]
            email_detail = detail[4]
            balance_detail = detail[5]
            date_detail = detail[6]
        
            login_frame = Frame(win)
            login_frame.place(relx=0,rely=.15,relwidth=1,relheight=.85)
            
            #background.
            bimg = PhotoImage(file = bg_img)
            bglbl = Label(login_frame, image = bimg)
            bglbl.image = bimg
            bglbl.place(x=0, y=0)
            
            #labels.
            heading = Label(login_frame, text = f"WELCOME {detail[1].upper()}", font = 'arial 20')
            heading.pack()
            
        
            #withdraw_button funs in login frame.
            def withdraw_button():
                #withdraw_frame.destroy()
                withdraw_frame = Frame(login_frame)
                withdraw_frame.place(relx = .25, rely = .15, relheight = .7, relwidth = .5)
                
                #frame baackground.
                bimg = PhotoImage(file = bg_img)
                bglbl = Label(withdraw_frame, image = bimg)
                bglbl.image = bimg
                bglbl.place(x=0, y=0)
                
                def submit():
                    try:
                        amount = float(entryamount.get())
                    except:
                        messagebox.showerror("Error","Please enter amounts.")
                        return
                    if amount<=0:
                        messagebox.showinfo("Validation", 'Invalid Amount.')
                        return
                    elif amount>balance_detail:
                        messagebox.showinfo("Validation", 'Insufficient Balance.')
                        return
                    elif amount>25000:
                        messagebox.showerror("Limitation","You can withdraw only 25000 at a time. ")
                        return
                    else:    
                        con = sqlite3.connect(database = "bank_database.sqlite")
                        cur = con.cursor()
                        cur.execute("update customers set balance = balance-? where account=?",(amount, account_detail))
                        con.commit()
                        con.close()
                        
                        con = sqlite3.connect(database = "bank_database.sqlite")
                        cur = con.cursor()
                        cur.execute("select balance from customers where account=?",(account_detail,))
                        con.commit()
                        updatedbalance = cur.fetchone()
                        
                        con = sqlite3.connect(database = "bank_database.sqlite")
                        cur = con.cursor()
                        cur.execute("insert into transactions values(?,?,?,?,?)",(account_detail, 'Dr', amount, updatedbalance[0], time.ctime()))
                        con.commit()
                        con.close()
                        
                        messagebox.showinfo("Withdraw","Amount succefully withdraw")
                        login_frame.destroy()
                        
                        
                def cancel():
                    withdraw_frame.destroy()
                    
                #labels in withdraw farme.
                withdraw_frame_heading = Label(withdraw_frame, text = 'WITHDRAW OPERATION',font = ('', 15, 'bold', 'underline'), bg = bg, fg = "#33ccff")
                withdraw_frame_heading.place(relx = .41, rely = .01)
                
                enter_amount = Label(withdraw_frame, text = "Enter Amount :",  bg = bg, font = ('', 11, 'bold'))
                enter_amount.place(relx=.2, rely=.3)
                
                #button in withdraw.
                submit_button = Button(withdraw_frame, text = 'Submit', font = "arial 19", width = 15, bg = "#898990", fg = "#ffffff", command = submit)
                submit_button.place(relx = 0, rely = .63)
                submit_button.bind("<Enter>", lambda event : submit_button.configure(bg = '#80e5ff'))
                submit_button.bind("<Leave>",lambda event : submit_button.configure(bg = '#898990'))
                
                
                cancel_button = Button(withdraw_frame, text = 'Cancel', font = "arial 19", width = 15, bg = "#898990", fg = "#ffffff", command = cancel)
                cancel_button.place(relx = 0, rely = .8)
                cancel_button.bind("<Enter>", lambda event : cancel_button.configure(bg = 'red'))
                cancel_button.bind("<Leave>",lambda event : cancel_button.configure(bg = '#898990'))
                
                #entry .
                entryamount = Entry(withdraw_frame, font = 'arial 11', width = '15', bg = "#e6faff",bd = "0")
                entryamount.place(relx = .43, rely = .3)
                #entryaccount.configure(bg = "#e6faff")
                entryamount.focus()
                
            def withdraw_enter(event):
                withdraw_button.configure(bg = '#80e5ff')
            def withdraw_leave(event):
                withdraw_button.configure(bg = "#898990")
            
            
            #deposit_button funs in login frame.
            def deposit_button():
                #withdraw_frame.destroy()
                deposit_frame = Frame(login_frame)
                deposit_frame.place(relx = .25, rely = .15, relheight = .7, relwidth = .5)
                
                #frame baackground.
                bimg = PhotoImage(file = bg_img)
                bglbl = Label(deposit_frame, image = bimg)
                bglbl.image = bimg
                bglbl.place(x=0, y=0)
                
                
                def submit():
                    try:
                        amount = float(entryamount.get())
                    except:
                        messagebox.showerror("Error","Please enter amounts.")
                        return
                    if amount<=0:
                        messagebox.showinfo("Validation", 'Invalid Amount.')
                        return
                    elif amount>50000:
                        messagebox.showerror("Limitation","You can deposit only 50000 maximum amount at a time")
                        return
                    else:    
                        con = sqlite3.connect(database = "bank_database.sqlite")
                        cur = con.cursor()
                        cur.execute("update customers set balance = balance+? where account=?",(amount, account_detail))
                        con.commit()
                        
                        
                        con = sqlite3.connect(database = "bank_database.sqlite")
                        cur = con.cursor()
                        cur.execute("select balance from customers where account=?",(account_detail,))
                        con.commit()
                        updatedbalance = cur.fetchone()
                        
                        updatedbalance = updatedbalance[0]
                        
                        con = sqlite3.connect(database = "bank_database.sqlite")
                        cur = con.cursor()
                        cur.execute("insert into transactions values(?,?,?,?,?)",(account_detail, 'Cr', amount, updatedbalance, time.ctime()))
                        con.commit()
                        con.close()
                        
                        messagebox.showinfo("Deposit","Amount succefully Deposit.")
                        login_frame.destroy()
                        
                        
                def cancel():
                    deposit_frame.destroy()
                
                #labels in deposit farme.
                deposit_frame_heading = Label(deposit_frame, text = 'DEPOSIT OPERATION',font = ('', 15, 'bold', 'underline'), bg = bg, fg = "#33ccff")
                deposit_frame_heading.place(relx = .41, rely = .01)
                
                enter_amount = Label(deposit_frame, text = "Enter Amount :",  bg = bg, font = ('', 11, 'bold'))
                enter_amount.place(relx=.2, rely=.3)
                
                #buttons in deposit.
                submit_button = Button(deposit_frame, text = 'Submit', font = "arial 19", width = 15, bg = "#898990", fg = "#ffffff", command = submit)
                submit_button.place(relx = 0, rely = .63) 
                
                cancel_button = Button(deposit_frame, text = 'Cancel', font = "arial 19", width = 15, bg = "#898990", fg = "#ffffff", command = cancel)
                cancel_button.place(relx = 0, rely = .8)
                
                submit_button.bind("<Enter>", lambda event : submit_button.configure(bg = '#80e5ff'))
                submit_button.bind("<Leave>",lambda event : submit_button.configure(bg = '#898990'))
                
                cancel_button.bind("<Enter>", lambda event : cancel_button.configure(bg = 'red'))
                cancel_button.bind("<Leave>",lambda event : cancel_button.configure(bg = '#898990'))
                
                
                #entry.
                entryamount = Entry(deposit_frame, font = 'arial 11', width = '15', bg = "#e6faff",bd = "0")
                entryamount.place(relx = .43, rely = .3)
                #entryaccount.configure(bg = "#e6faff")
                entryamount.focus()
                
            def deposit_enter(event):
                deposit_button.configure(bg = '#80e5ff')
            def deposit_leave(event):
                deposit_button.configure(bg = "#898990")
            
            
            #balance_button funs in login frame.
            def balance_button():
                balance_frame = Frame(login_frame)
                balance_frame.place(relx = .25, rely = .15, relheight = .7, relwidth = .5)
                
                #frame baackground.
                bimg = PhotoImage(file = bg_img)
                bglbl = Label(balance_frame, image = bimg)
                bglbl.image = bimg
                bglbl.place(x=0, y=0)
                
                def back():
                    balance_frame.destroy()
                
                #labels in balance farme.
                balance_frame_heading = Label(balance_frame, text = 'YOUR BALANCE',font = ('', 15, 'bold', 'underline'), bg = bg, fg = "#33ccff")
                balance_frame_heading.place(relx = .41, rely = .01)
                
                balance = Label(balance_frame, text = f"Available Balance is {balance_detail}", font = 'arial 18')
                balance.place(relx = .33, rely = .4)
                
                #button.
                
                back_button = Button(balance_frame, text = 'Back', font = "arial 19", width = 15, bg = "#898990", fg = "#ffffff",command = back)
                back_button.place(relx = 0, rely = .8)
                
                back_button.bind("<Enter>", lambda event : back_button.configure(bg = 'red'))
                back_button.bind("<Leave>",lambda event : back_button.configure(bg = '#898990'))
                
                
            def balance_enter(event):
                balance_button.configure(bg = '#80e5ff')
            def balance_leave(event):
                balance_button.configure(bg = "#898990")
            
            
            #update_button funs in login frame.
            def update_button():
                update_frame = Frame(login_frame)
                update_frame.place(relx = .25, rely = .15, relheight = .7, relwidth = .5)
                
                #frame baackground.
                bimg = PhotoImage(file = bg_img)
                bglbl = Label(update_frame, image = bimg)
                bglbl.image = bimg
                bglbl.place(x=0, y=0)
                
                
                def submit():
                    update_name = entry_name.get()
                    update_pass = entry_pass.get()
                    update_mob = entry_mob.get()
                    update_email = entry_email.get()
                    
                    if len(update_name)<=0:
                        messagebox.showinfo("Validation","Please enter your name.")
                        return
                    elif len(update_pass)<6:
                        messagebox.showwring("Warning","Password has been greater than 6 characters.")
                        return
                    elif len(update_mob)<10 or len(update_mob)>10:
                        messagebox.showerror("Error","Invalid Mobile Number.")
                        return
                    elif '@gmail.com' not in update_email:
                        messagebox.showerror("Error","Invalid email.")
                        return
                    
                    else:
                        con = sqlite3.connect (database = "bank_database.sqlite")
                        cur = con.cursor()
                        cur.execute("update customers set name=?, password=?, mobile=?, email=? ",(update_name, update_pass, update_mob, update_email))
                        con.commit()
                        con.close()
                        
                        messagebox.showinfo("Updated","Account has been updated")
                        login_frame.destroy()
                        
                        
                    
                def cancel():
                    update_frame.destroy()
                    
                    
                #labels in update farme.
                update_frame_heading = Label(update_frame, text = 'UPDATE YOUR ACCOUNT',font = ('', 15, 'bold', 'underline'), bg = bg, fg = "#33ccff")
                update_frame_heading.place(relx = .41, rely = .01)
                
                name_label = Label(update_frame, text = "Name :", bg = bg, font = ('', 11, 'bold'))
                name_label.place(relx=.3, rely=.1+.2)

                password_label = Label(update_frame, text = "Password :", bg = bg, font = ('', 11, 'bold'))
                password_label.place(relx=.3, rely=.18+.2)

                mobile_label = Label(update_frame, text = "Mobile :", bg = bg, font = ('', 11, 'bold'))
                mobile_label.place(relx=.3, rely=.26+.2)

                email_label = Label(update_frame, text = "Email :", bg = bg, font = ('', 11, 'bold'))
                email_label.place(relx=.3, rely=.34+.2)
                
                #entry.
                entry_name = Entry(update_frame, font = 'arial 11', width = '17', bg = "#e6faff",bd = "0")
                entry_name.place(relx = .49, rely = .3)
                entry_name.focus()
                entry_name.insert(0,name_detail)
                
                entry_pass = Entry(update_frame, font = 'arial 11', width = '17', bg = "#e6faff",bd = "0", show = '*')
                entry_pass.place(relx = .49, rely = .18+.2)
                entry_pass.insert(0,password_detail)
                
                entry_mob = Entry(update_frame, font = 'arial 11', width = '17', bg = "#e6faff",bd = "0")
                entry_mob.place(relx = .49, rely =.26+.2)
                entry_mob.insert(0,mobile_detail)
                
                entry_email = Entry(update_frame, font = 'arial 11', width = '17', bg = "#e6faff",bd = "0")
                entry_email.place(relx = .49, rely = .34+.2)
                entry_email.insert(0,email_detail)
                
                #buttons.
                submit_button = Button(update_frame, text = 'Submit', font = "arial 19", width = 15, bg = "#898990", fg = "#ffffff", command = submit)
                submit_button.place(relx = 0, rely = .63) 
                
                cancel_button = Button(update_frame, text = 'Cancel', font = "arial 19", width = 15, bg = "#898990", fg = "#ffffff", command = cancel)
                cancel_button.place(relx = 0, rely = .8)
                
                submit_button.bind("<Enter>", lambda event : submit_button.configure(bg = '#80e5ff'))
                submit_button.bind("<Leave>",lambda event : submit_button.configure(bg = '#898990'))
                
                cancel_button.bind("<Enter>", lambda event : cancel_button.configure(bg = 'red'))
                cancel_button.bind("<Leave>",lambda event : cancel_button.configure(bg = '#898990'))
                
                
            def update_enter(event):
                update_button.configure(bg = '#80e5ff')
            def update_leave(event):
                update_button.configure(bg = "#898990")
            
            
            #history_button funs in login frame.
            def history_button():
                history_frame = Frame(login_frame)
                history_frame.place(relx = .25, rely = .15, relheight = .7, relwidth = .5)
                
                #frame baackground.
                bimg = PhotoImage(file = bg_img)
                bglbl = Label(history_frame, image = bimg)
                bglbl.image = bimg
                bglbl.place(x=0, y=0)
                
                def back():
                    history_frame.destroy()
                    
                #labels in history farme.
                history_frame_heading = Label(history_frame, text = 'YOUR HISTORY',font = ('', 15, 'bold', 'underline'), bg = bg, fg = "#33ccff")
                history_frame_heading.place(relx = .41, rely = .01)
                
                #scrollbar.
                st = ScrolledText(history_frame, width = 92, height =23)
                st.place(relx = 0.01, rely = .07)
                st.delete(1.0,END)
                
                msg="Type\tAmount\t\tDate\t\t\t\tUpdated bal\n\n"
                
                con = sqlite3.connect(database = "bank_database.sqlite")
                cur = con.cursor()
                cur.execute("select type, amount, date, balance from transactions where account=?",(account_detail,))
                con.commit()
                transactions = cur.fetchall()
                for tp in transactions:
                    msg=msg+f" {tp[0]}\t{tp[1]}\t\t{tp[2]}\t\t\t\t{tp[3]}\n\n"
                
                st.insert(END,msg)
                    
                
                #button.
                back_button = Button(history_frame, text = "Back", font = "arial 19", width = 20, bg = "#898990", fg = "#ffffff", command = back)
                back_button.place(relx = 0, rely = .87)
                
                back_button.bind("<Enter>", lambda event : back_button.configure(bg = 'red'))
                back_button.bind("<Leave>",lambda event : back_button.configure(bg = '#898990'))
                
            def history_enter(event):
                history_button.configure(bg = '#80e5ff')
            def history_leave(event):
                history_button.configure(bg = "#898990")
            
            
            #logout_button funs in login frame.
            def logout_button():
                logout_button.configure(bg = "#33ccff")
                login_frame.destroy()
                
            def logout_enter(event):
                logout_button.configure(fg = "#ff0000", bg = "#ffffff")
            def logout_leave(event):
                logout_button.configure(fg = "#33ccff", bg = "#ffffff")
            
            
            
            #buttons in login_frame.
            withdraw_button = Button(login_frame, text = 'Withdraw', font = "arial 19", width = 15, bg = "#898990", fg = "#ffffff", command = withdraw_button)
            withdraw_button.place(relx = 0, rely = .23)
            
            deposit_button = Button(login_frame, text = 'deposit', font = "arial 19", width = 9, bg = "#898990", fg = "#ffffff", command = deposit_button)
            deposit_button.place(relx = 0, rely = .35)
            
            balance_button = Button(login_frame, text = 'Balance', font = "arial 19", width = 15, bg = "#898990", fg = "#ffffff", command = balance_button)
            balance_button.place(relx = 0, rely = .47)
            
            update_button = Button(login_frame, text = 'Update', font = "arial 19", width = 9, bg = "#898990", fg = "#ffffff", command = update_button)
            update_button.place(relx = 0, rely = .59)
            
            history_button = Button(login_frame, text = 'History', font = "arial 19", width = 15, bg = "#898990", fg = "#ffffff", command = history_button)
            history_button.place(relx = 0, rely = .71)
            
            logout_button = Button(login_frame, text = 'Logout', font = "arial 19", width = 9, bg = "#ffffff", fg = "#33ccff", bd = 0, command = logout_button)
            logout_button.place(relx = 0, rely = .01)
            
            
            #Events binding in login_frame.
            withdraw_button.bind("<Enter>", withdraw_enter)
            withdraw_button.bind("<Leave>", withdraw_leave)
            
            deposit_button.bind('<Enter>', deposit_enter)
            deposit_button.bind('<Leave>', deposit_leave)
            
            balance_button.bind('<Enter>', balance_enter)
            balance_button.bind('<Leave>', balance_leave)
            
            update_button.bind('<Enter>', update_enter)
            update_button.bind('<Leave>', update_leave)
            
            history_button.bind('<Enter>', history_enter)
            history_button.bind('<Leave>', history_leave)
            
            logout_button.bind('<Enter>', logout_enter)
            logout_button.bind('<Leave>', logout_leave)
            
            # user profile pic and button.
            
    
    def login_enter(event):
        login_button.configure(bg = '#80e5ff')
    def login_leave(event):
        login_button.configure(bg = "#898990")
    
    #reset button function.
    def reset_button():
        entryaccount.delete(0, 'end')
        entrypass.delete(0, 'end')
        entryaccount.focus()
    
    def reset_enter(event):
        reset_button.configure(bg = '#80e5ff')
    def reset_leave(event):
        reset_button.configure(bg = "#898990")
    
    #create an account button functions.
    def create_button():
        create_account_frame = Frame(win)
        create_account_frame.place(relx=0,rely=.15,relwidth=1,relheight=.85)
        
        #background.
        bimg = PhotoImage(file = bg_img)
        bglbl = Label(create_account_frame, image = bimg)
        bglbl.image = bimg
        bglbl.place(x=0, y=0)
        
        
        #create2_button.
        def create2_button():
            name = name_entry.get()
            password = pass_entry.get()
            mobile = mobile_entry.get()
            email = email_entry.get()
            bal = 0.0
            date = time.ctime()
            
            if len(name)<0:
                messagebox.showinfo("Validation","Please give all details.")
                return
            
            if len(password)<6:
                messagebox.showwarning("Not Secure","Password should be greater than 6 characters.")
                return
            if len(mobile)<10 or len(mobile)>10:
                messagebox.showerror("Error","Invalid Mobile Number.")
                return
            if '@gmail.com' not in email:
                messagebox.showerror("Error","Invalid Email.")
                return
            
            
            con = sqlite3.connect(database = "bank_database.sqlite")
            cur = con.cursor()
            cur.execute("insert into customers (name, password, mobile, email, balance, date) values(?,?,?,?,?,?)",(name,password,mobile,email,bal,date))
            con.commit()
            con.close()
            
            con = sqlite3.connect(database = "bank_database.sqlite")
            cur = con.cursor()
            cur.execute("select max(account) from customers")
            max_account = cur.fetchone()
            con.commit()
            messagebox.showinfo('Welcome',f"Your Account has been created.\nYour Account No : {max_account[0]}")
            create_account_frame.destroy()
            
            
        def create2_enter(event):
            create2_button.configure(bg = '#80e5ff')
        def create2_leave(event):
            create2_button.configure(bg = "#898990")
        
        
        #reset2_button.
        def reset2_button():
            email_entry.delete(0,'end')
            mobile_entry.delete(0,'end')
            pass_entry.delete(0,'end')
            name_entry.delete(0,'end')
            name_entry.focus()
            
            
        def reset2_enter(event):
            reset2_button.configure(bg = '#80e5ff')
        def reset2_leave(event):
            reset2_button.configure(bg = "#898990")
        
        
        #cancel_button.
        def cancel_button():
            create_account_frame.destroy()
        def cancel_enter(event):
            cancel_button.configure(bg = 'red')
        def cancel_leave(event):
            cancel_button.configure(bg = "#898990")
        
        
        
        #labels in create accounts.
        name_label = Label(create_account_frame, text = "Name :", bg = bg, font = ('', 14, 'bold'))
        name_label.place(relx=.3, rely=.1)
        
        password_label = Label(create_account_frame, text = "Password :", bg = bg, font = ('', 14, 'bold'))
        password_label.place(relx=.3, rely=.18)
        
        mobile_label = Label(create_account_frame, text = "Mobile :", bg = bg, font = ('', 14, 'bold'))
        mobile_label.place(relx=.3, rely=.26)
        
        email_label = Label(create_account_frame, text = "Email :", bg = bg, font = ('', 14, 'bold'))
        email_label.place(relx=.3, rely=.34)
        
        frame_heading_label = Label(create_account_frame, text = "Form No.001", bg = bg, font = ('', 14, 'bold', 'underline'))
        frame_heading_label.place(relx = .45, rely = .01)
        
        
        #entry in create account frame.
        name_entry = Entry(create_account_frame, font = 'arial 15', width = '16')
        name_entry.place(relx=.45, rely=.1)
        name_entry.configure(bg = "#e6faff")
        name_entry.focus()
        
        pass_entry = Entry(create_account_frame, font = 'arial 15', width = '16',show = '*')
        pass_entry.place(relx=.45, rely=.18)
        pass_entry.configure(bg = "#e6faff")
        
        mobile_entry = Entry(create_account_frame, font = 'arial 15', width = '16')
        mobile_entry.place(relx=.45, rely=.26)
        mobile_entry.configure(bg = "#e6faff")
        
        email_entry = Entry(create_account_frame, font = 'arial 15', width = '16')
        email_entry.place(relx=.45, rely=.34)
        email_entry.configure(bg = "#e6faff")
        
        
        #buttons in create account frame.
        create2_button = Button(create_account_frame, text = "Create Account", font = "arial 19", width = 20, bg = "#898990", fg = "#ffffff", command = create2_button)
        create2_button.place(relx = 0, rely = .56)
        
        reset2_button = Button(create_account_frame, text = "Reset all", font = "arial 19", width = 12, bg = "#898990", fg = "#ffffff", command = reset2_button)
        reset2_button.place(relx = 0, rely = .69)
        
        cancel_button = Button(create_account_frame, text = "Cancel", font = "arial 19", width = 20, bg = "#898990", fg = "#ffffff", command = cancel_button)
        cancel_button.place(relx = 0, rely = .82)
        
        
        #buttons event binding in create account frame.
        create2_button.bind("<Enter>",create2_enter)
        create2_button.bind("<Leave>",create2_leave)
        
        reset2_button.bind("<Enter>",reset2_enter)
        reset2_button.bind("<Leave>",reset2_leave)
        
        cancel_button.bind("<Enter>",cancel_enter)
        cancel_button.bind("<Leave>",cancel_leave)
        
        
        
    
    
    def create_enter(event):
        create_button.configure(bg = '#80e5ff')
    def create_leave(event):
        create_button.configure(bg = "#898990")
    
    #forgot button function.
    def forgot_button():
        forgot_button_frame = Frame(win)
        forgot_button_frame.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    
        #background.
        bimg = PhotoImage(file = bg_img)
        bglbl = Label(forgot_button_frame, image = bimg)
        bglbl.image = bimg
        bglbl.place(x=0, y=0)
        
        # recover button.
        def recover_button():
            try:
                account=int(account_forgot.get())
            except:
                messagebox.showerror("Error","Invalid account number.")
                return
            mobile=mobile_forgot.get()
            email=email_forgot.get()
            
            try:
                con = sqlite3.connect(database="bank_database.sqlite")
                cur = con.cursor()
                cur.execute("select password from customers where account=(?) and mobile=(?) and email=(?)",(account,mobile,email))
                password = cur.fetchone()
                con.commit()

                messagebox.showinfo("Recovered",f"Your Password : {password[0]}")
                forgot_button_frame.destroy()
            
            except:
                messagebox.showerror("Error","Account details are not matched.\nPlease check and try again.")
                return
            
        def recover_enter(event):
            recover_button.configure(bg = '#80e5ff')
        def recover_leave(event):
            recover_button.configure(bg = "#898990")
        
        # reset3 button.
        def reset3_button():
            account_forgot.delete(0,"end")
            mobile_forgot.delete(0,"end")
            email_forgot.delete(0,"end")
            account_forgot.focus()
        def reset3_enter(event):
            reset3_button.configure(bg = '#80e5ff')
        def reset3_leave(event):
            reset3_button.configure(bg = "#898990")
        
        #cancel2 button.
        def cancel2_button():
            forgot_button_frame.destroy()
        def cancel2_enter(event):
            cancel2_button.configure(bg = 'red')
        def cancel2_leave(event):
            cancel2_button.configure(bg = "#898990")
        
        
        #labels in forgot.
        forgot_frame_heading = Label(forgot_button_frame, text ="Recover Your Password",  font = ('', 14, 'bold', 'underline'), bg = bg)
        forgot_frame_heading.place(relx = .40, rely = .01)
        
        forgot_frame_account = Label(forgot_button_frame, text ="Account No :",  font = ('', 14, 'bold'), bg = bg)
        forgot_frame_account.place(relx = .35, rely = .15)
        
        forgot_frame_mobile = Label(forgot_button_frame, text ="Reg. Mob :",  font = ('', 14, 'bold'), bg = bg)
        forgot_frame_mobile.place(relx = .35, rely = .24)
        
        forgot_frame_email = Label(forgot_button_frame, text ="Email :",  font = ('', 14, 'bold'), bg = bg)
        forgot_frame_email.place(relx = .35, rely = .33)
        
        
        #entry in forgot.
        account_forgot = Entry(forgot_button_frame, font = 'arial 15', width = '16', bg = '#e6faff')
        account_forgot.place(relx = .50, rely = .15)
        account_forgot.focus()
        
        mobile_forgot = Entry(forgot_button_frame, font = 'arial 15', width = '16',bg = '#e6faff')
        mobile_forgot.place(relx = .50, rely = .24)
        
        email_forgot = Entry(forgot_button_frame, font = 'arial 15', width = '16', bg = '#e6faff')
        email_forgot.place(relx = .50, rely = .33)
        
        
        #buttons in forgot.
        recover_button = Button(forgot_button_frame, text = "Recover", font = "arial 19", width = 20, bg = "#898990", fg = "#ffffff", command = recover_button)
        recover_button.place(relx = 0, rely = .51)
        
        reset3_button = Button(forgot_button_frame, text = "Reset", font = "arial 19", width = 12, bg = "#898990", fg = "#ffffff", command = reset3_button)
        reset3_button.place(relx = 0, rely = .63)

        cancel2_button = Button(forgot_button_frame, text = "Cancel", font = "arial 19", width = 20, bg = "#898990", fg = "#ffffff", command = cancel2_button)
        cancel2_button.place(relx = 0, rely = .75)
        
        
        #buttons binding in forgot frame.
        recover_button.bind("<Enter>", recover_enter)
        recover_button.bind("<Leave>", recover_leave)
        
        reset3_button.bind("<Enter>", reset3_enter)
        reset3_button.bind("<Leave>", reset3_leave)
        
        cancel2_button.bind("<Enter>", cancel2_enter)
        cancel2_button.bind("<Leave>", cancel2_leave)
        
        
    
    def forgot_enter(event):
        forgot_button.configure(bg = '#80e5ff')
    def forgot_leave(event):
        forgot_button.configure(bg = "#898990")

    
    #labels
    acnlbl = Label(win, text = 'Account No : ', bg = bg, font = ('', 14, 'bold'))
    acnlbl.place(relx = .35, rely = .20)

    passlbl = Label(win, text = 'Password : ', bg = bg, font = ('', 14, 'bold'))
    passlbl.place(relx = .35, rely = .27)


    #entrys.
    entryaccount = Entry(win, font = 'arial 15', width = '16')
    entryaccount.place(relx = .49, rely = .20)
    entryaccount.configure(bg = "#e6faff")
    entryaccount.focus()

    entrypass = Entry(win, font = 'arial 15', width = '16', show = "*")
    entrypass.place(relx = .49, rely = .27)
    entrypass.configure(bg = "#e6faff")


    #Buttons.
    login_button = Button(win, text = "Log In", font = "arial 19", width = 9, bg = "#898990", fg = "#ffffff", command = login_button)
    login_button.place(relx = .35, rely = .36)

    reset_button = Button(win, text = "Reset", font = "arial 19", width = 9, bg = "#898990", fg = "#ffffff", command = reset_button)
    reset_button.place(relx = .52, rely = .36)

    create_button = Button(win, text = "Create an  account", font = "arial 19", width = 20, bg = "#898990", fg = "#ffffff", command = create_button)
    create_button.place(relx = .35, rely = .50)

    forgot_button = Button(win, text = "Forgot Password", font = "arial 19", width = 20, bg = "#898990", fg = "#ffffff", command = forgot_button)
    forgot_button.place(relx = .35, rely = .64)
    
    
    #button event binding.
    login_button.bind('<Enter>', login_enter)
    login_button.bind('<Leave>', login_leave)
    
    reset_button.bind('<Enter>', reset_enter)
    reset_button.bind('<Leave>', reset_leave)
    
    create_button.bind('<Enter>', create_enter)
    create_button.bind('<Leave>', create_leave)
    
    forgot_button.bind('<Enter>', forgot_enter)
    forgot_button.bind('<Leave>', forgot_leave)
    
    
login_screen()
win.mainloop()






