#Title: FLIGHT BOOKING APPLICATION FOR ASSESSMENT VERSION 3:
#Author: Kishan Harry
#Purpose: Create a program allowing a user to book a flight ticket from Auckland Airport
#DISCLAIMER BEFORE RUNNIG PROGRAM:
#Please create an account with your valid email address so the receipt email can be sent to you.

#-------------------------------------------------------------------------------------------------------------------------|
#---------------------------------------------------------IMPORTS---------------------------------------------------------|
#-------------------------------------------------------------------------------------------------------------------------|

#Allows efficient reading and writing of csv files
import csv

#Other relevant imports

import re
from datetime import datetime
#Imports for graphical user interface (GUI)
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

#Module used to manipulate images
#from PIL import Image, ImageTk, ImageOps


#-------------------------------------------------------------------------------------------------------------------------|
#--------------------------------------------------ARRAYS & CONSTANTS-----------------------------------------------------|
#-------------------------------------------------------------------------------------------------------------------------|

#lists of international and domestic flights (objects)
international_flights = []
domestic_flights = []

#Account consideration
user_details = [] #Stores account details in dictionary
#List that will hold the current user object once logged in
#and will be cleared when the user logs out
logged_user=[]


#Table format to help with display
MENU_HEADER = "----------------------------"
FLIGHT_DISPLAY_HEADERS = ["-------------------------------------------------------------------------------------------------------------------------------------------------------------------",
                          "|Flight #:| Travel Type:  | Airline Name:        | Airport:                               | Destination:              | Duration:| Date:               | Price($):|",
                          "-------------------------------------------------------------------------------------------------------------------------------------------------------------------"]

#Constants that help with login and account creation
ATTEMPTS = 5
MIN_PW_LENGTH = 8

#Age boundaries for account creation
MIN_AGE = 16
MAX_AGE = 100

#Age boudnaries for ticket creation
ADULT = 18
SENIOR = 65
MAX_AGE = 150

#Accepted charachters in first & lastname
SPECIALS = [" ", "-", ".", "'"] 

#Constants for discounts
DEFAULT_CHILD_DISCOUNT = float(0.80)
DEFAULT_SENIOR_DISCOUNT=float(0.85)
DEFAULT_MULTIPLIER= float(1.00)  #For both age and cabin class
DEFAULT_FIRST_CLASS_MULTIPLIER = float(3.10)
DEFAULT_BUSINESS_CLASS_MULTIPLIER = float(2.10)
#Difference in pricing multipliers between domestic and international classes
CABIN_CLASS_DIFFERENCE = float(0.25)
AGE_DIFFERENCE = float(0.05)

#Front end constants
BG_COLOUR ="#E0D8A7"
MAROON = "#5f0137"
LIGHT_BLUE = "#89c9ec"
DEFAULT = "#f9f9f9"
BUTTON_FONT = ("Public Sans", 12, "bold")
BUTTON_FONT2 = ("Public Sans", 11, "bold")
LARGE_FONT = ("Verdana", 13, "bold", "underline")
SMALL_FONT = ("Times",12,"underline")

#Treeview flight headers
COLUMNS = ("Flight#:", "Travel Type:", "Arline Name:", "Airport:", "Destination:", "Duration:", "Date:", "Price($):")
TICKET_HEADERS =("Name:", "Age Type:", "Cabin Class:" , "Flight#:", "Travel Type:", "Arline Name:", "Airport:", "Destination:", "Duration:", "Date:", "Price($):")

#___________________CUSTOM TYPE CLASSES_____________________

class Flight:
    def __init__(self, travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name):
        '''Constructor method to set attributes of flight'''
        #Set relevant attributes for each flight object 
        self.travel_type = travel_type
        self.flight_number = flight_number
        self.airport = airport
        self.destination = destination
        self.country = country
        self.stopovers = stopovers
        self.airline_name = airline_name
        self.date = date                              
        self.duration = int(duration)                          #Converts string to integer for later operations          
        self.ticket_price = round(float(ticket_price), 2)      #Rounds ticket price to 2 decimal places       

class Domestic(Flight):
    def __init__(self,travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name):
        '''Constructor method to set new attributes of domestic flight'''
        super().__init__(travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name)
        #Set attributes native to domestic class
        self.cabin_class_types = ["First Class", "Economy"]
        self.child_discount = DEFAULT_CHILD_DISCOUNT
        self.adult_discount = DEFAULT_MULTIPLIER
        self.senior_discount = DEFAULT_SENIOR_DISCOUNT
        self.first_class_multiplier = DEFAULT_FIRST_CLASS_MULTIPLIER
        self.economy_class_multiplier = DEFAULT_MULTIPLIER

class International(Domestic, Flight):
    def __init__(self,travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name):
        '''Constructor method to set new attributes of international flight'''
        super().__init__(travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name)
        #Set attributes native to international class
        self.cabin_class_types.append("Business")
        self.child_discount += AGE_DIFFERENCE 
        self.senior_discount += AGE_DIFFERENCE
        self.first_class_multiplier += CABIN_CLASS_DIFFERENCE
        self.business_class_multiplier = DEFAULT_BUSINESS_CLASS_MULTIPLIER
        self.duration = round(float(duration)/60, 1)                        #Converts minutes to hours and rounds ticket price to 2 decimal places

class Ticket(Flight):
    def __init__(self, travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name, cabin_class, ticket_holder_age, ticket_holder_name):
        '''Constructor method to inherit attributes of flight'''
        super().__init__(travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name)
        #Set ticket attributes
        self.cabin_class = cabin_class
        self.ticket_holder_age = ticket_holder_age
        self.ticket_holder_name = ticket_holder_name
    
    def apply_discounts(self, flight):
        '''Applies discounts and multipliers depending on travel type
            and returns the price'''
        
        #Multiplies ticket price property with the respective discount (dependent on travel type)
        if self.ticket_holder_age == "Child":
            self.ticket_price *= flight.child_discount
        elif self.ticket_holder_age == "Adult":
            self.ticket_price *= flight.adult_discount
        elif self.ticket_holder_age == "Senior":
            self.ticket_price *= flight.senior_discount

        if self.cabin_class == "First":
            self.ticket_price *= flight.first_class_multiplier
        elif self.cabin_class == "Business":
            self.ticket_price *= flight.business_class_multiplier
        elif self.cabin_class == "Economy":
            self.ticket_price *= flight.economy_class_multiplier
        #Return appropriate ticket price (discounted)
        return self.ticket_price
          
class Current_User:
    def __init__(self, username, email, password):
        '''Constructor method to define attributes'''
        #Set attributes of user
        self.username = username
        self.password = password
        self.email = email

        #lists to hold domestic and international ticket objects
        self.international_tickets = []
        self.domestic_tickets =[]

        #Dictionary that holds the user's saved data (cart and order history)
        self.saved_data = {}

    def set_current_user(self):
        '''Add the current user to the logged_user list 
            and add their ordered tickets'''
        logged_user.append(self)

    def remove_current_user(self):
        '''Remove the current user from the logged_user list 
            and remove their ordered tickets'''
        logged_user.remove(self)

    def add_ticket(self, ticket_list, ticket):
        '''Add a ticket that the user has ordered'''
        ticket_list.append(ticket)

    def remove_ticket(self, ticket_list, ticket_num):
        '''Remove the ticket the user has selected from their cart'''
        ticket_list.pop(ticket_num)
    
    def append_tickets(self):
        '''Appends all the user's tickets into one list'''
        ticket_list = []
        #Append all tickets to the list as individual tickets (not 2D list)
        for ticket in self.domestic_tickets:
            ticket_list.append(ticket)
        for ticket in self.international_tickets:
            ticket_list.append(ticket)
        
        #Return the ticket list
        return ticket_list
        
    def calculate_total_price(self):
        '''Calculate the total price of the user's tickets'''
        #Total is 0 which increments as program iterates through tickets
        total = 0

        for ticket in self.domestic_tickets:
            total += ticket.ticket_price
        
        for ticket in self.international_tickets:
            total += ticket.ticket_price
        
        #returns the total price
        return total
   
#_____________GENERAL FUNCTIONS_______________

def read_flights_from_csv(filename, flights_list, Travel_Type):
    '''Read list of flights from their respective csv files and instantiate 
        each flight into an object then load them into a list.'''
    
    #Opens file then creates a flight object for each row with
    #attributes matching the fieldnames
    with open(filename, mode="r") as file:
        csvreader = csv.DictReader(file)
        for row in csvreader:
            #Instantiate each flight object based on domestic or international
            flight_object = Travel_Type(row["travel_type"], row["flight_number"], row["airport"], row["destination"], row["country"], row["stopovers"], row["duration"], row["date"], row["price"], row["airline"])
            #Adds flight object to flights list
            flights_list.append(flight_object) 
   
#_____________Screen Classes_____________ (for main screen and different screens)

#Main (default) screen
class Flight_booker_app(tk.Tk):

    def __init__(self, *args, **kwargs):
        '''Constrcutor method to intialise attributes of the main app'''
        tk.Tk.__init__(self, *args, **kwargs)

        #Sets window title to name of application
        tk.Tk.wm_title(self, "Auckland SkyVoyager") 

        #Disable maximise and minimise
        self.resizable(False,False)
        
        #Creates a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #___________________TOP_______________________
        #Keeps the header constant throughout each screen of the app for consistency
        #Labels for Heading and Subheading of login_menu  #H1 remains on every screen for consistency and standards heuristic
        heading = tk.Label(self,text = "AUCKLAND SKY VOYAGER", font=("Helvetica",20, "bold"), fg ="black", bg=BG_COLOUR, justify="center", wraplength=460)        
        heading.place(relx=0.5,rely=0.1, anchor="center")
       
        #Creates a dictionary of frames to use the 'controller' as the key to access each frame.
        self.frames = {}

        #Tuple of classes for the different screens. For each screen, a container will be intialised.
        for F in (LoginMenu, CreateAccount, Exit, Login, MainMenu, TravelType, BookFlight, Personalisation, CartMenu, DisplayCart, EditOrder, ConfirmOrder, Logout): 
            
            #Instantiates a frame
            frame = F(container, self)
            #Set the frame as the value for the screen in the self.frames dict
            #(so that the controller can jump between instantiated screens)
            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew")
            frame.config(bg =BG_COLOUR)

        self.show_frame(LoginMenu)

    def show_frame(self, key, flight_type=None): 
        '''Creating show_frame method to be used throughout the program'''
        frame = self.frames[key]

        #For handling flight type choice
        if flight_type:
            frame.load_flights(flight_type)

        #In charge of raising the frames to the top of the window
        frame.tkraise() 

    def get_screen(self, screen_class):
        '''Retrieve a screen instance from the controller'''
        return self.frames.get(screen_class)

    #___________________________General Methods_____________________________
    def clear_entries(self, entries):
        """Deletes text inside entry boxes (all of the ones per each page)"""
        for entry in entries:
            entry.delete(0, tk.END)
    
    def kill(self): 
        """Closes the application (terminates the window)"""
        app.destroy()
    
    #______________________CONFIGURATIONS FOR ENTRYBOXES___________________________
    def config_entry_bg(self, entry, colour):
        '''Change bg colour of entry to green or red or whatever colour'''
        entry.config(bg=colour)
        #Return the modified entry box
    
    def validate_empty(self, entry_names, boxes):
        '''Configure entry widgets if empty'''
        #Highlight a red background colour for all empty boxes
        #Find out which ones are empty
        empty_boxes = []
        filled_boxes = []
        for box in boxes:
            if len(box[0])==0:
                empty_boxes.append(box)
            elif len(box[0])!=0:
                filled_boxes.append(box)
        
        #Get the widget name and run the decorator turning bg red
        for box in empty_boxes:
            entry = entry_names.get(box[1])
            self.config_entry_bg(entry, '#FFCCCC')
            
        #Get the widget name and run the decorator turning bg white (default)
        for box in filled_boxes:
            entry = entry_names.get(box[1])
            self.config_entry_bg(entry, 'white')

    def back_config(self,entries):
        '''Clears the entry box widgets and converts bg colours back to white'''
        for entry in entries:
            self.config_entry_bg(entry, "white")
        self.clear_entries(entries)

    #_____________________________TREEVIEW METHODS_____________________________________
    def create_headings(self, tree, headings):
        '''Set the headings of the treeview'''
        #For each heading in the headers tuple, the heading will be set
        for header in headings:
            tree.heading(header, text=header)

#_______________________________LOGIN COMPONENT SCREENS_________________________________

class LoginMenu(tk.Frame):

    def __init__(self, parent, controller):
        '''Constructor Method to define attributes and widgets'''
        super().__init__(parent)
        #Buttons for login, create account and exit
        login_menu_btn_login = tk.Button(self, width=16, text = "LOGIN", font=BUTTON_FONT,command=lambda: controller.show_frame(Login))
        login_menu_btn_ca = tk.Button(self,width=16, text = "CREATE ACCOUNT", font=BUTTON_FONT, command=lambda: controller.show_frame(CreateAccount))
        login_menu_btn_exit = tk.Button(self,width=16, text = "EXIT APP", font=BUTTON_FONT, command=lambda: controller.show_frame(Exit))
        login_menu_options = tk.Label(self, text="Options:", font=SMALL_FONT, fg="black", bg=BG_COLOUR)

        #Placing widgets on screen
        login_menu_options.place(relx=0.5, rely=0.4, anchor="center")
        login_menu_btn_login.place(relx=0.5, rely=0.5, anchor = "center")
        login_menu_btn_ca.place(relx=0.5, rely=0.6, anchor = "center")
        login_menu_btn_exit.place(relx=0.5, rely=0.7, anchor = "center") 

        #Description
        login_menu_description = tk.Label(self, text="Welcome to Auckland SkyVoyager.\nBook flight tickets from Auckland Domestic and International Airport to suit your travel needs!",justify = "center",  font=("Times", 12),fg="black", bg=BG_COLOUR, wraplength=350)
        
        #Placing widgets on screen
        login_menu_description.place(relx=0.5,rely=0.25, anchor="center", width=320, height =110)
     
class CreateAccount(tk.Frame, Flight_booker_app):

    def __init__(self, parent, controller):
        '''Constrcutor method to define attributes and widgets'''
        super().__init__(parent)

        #Attributes
        self.controller = controller

        #Labels
        create_account_description =tk.Label(self, text = "Create an account! - Password must be at least 8 characters, contain a number, a special character and a capital letter. ", justify = "left", wraplength=460, font=("Times", 11),fg="black", bg=BG_COLOUR)
        create_account_lb_first_name = tk.Label(self,text= "Enter First Name :", font = ('Arial', 12, "bold"), fg="darkgreen", bg=BG_COLOUR )
        create_account_lb_last_name = tk.Label(self,text= "Enter Last Name :", font = ('Arial', 12, "bold"), fg="darkgreen", bg=BG_COLOUR )
        create_account_lb_email = tk.Label(self,text= "Enter Email :", font = ('Arial', 12, "bold"), fg="darkgreen", bg=BG_COLOUR )
        create_account_lb_pass = tk.Label(self,text= "Create Password :", font = ('Arial', 12, "bold"), fg="darkgreen", bg=BG_COLOUR )
        create_account_lb_age = tk.Label(self, text= "Enter Age :", font = ('Arial', 12, "bold"), fg="darkgreen", bg=BG_COLOUR )
        #Entries
        self.create_account_e_first = tk.Entry(self, width=15)
        self.create_account_e_last = tk.Entry(self, width=15)
        self.create_account_e_email = tk.Entry(self, width=25)
        self.create_account_e_pass = tk.Entry(self, width=25, show="*")
        self.create_account_e_age = tk.Entry(self, width=25)
        #Append entries to a list
        entries =[self.create_account_e_first, self.create_account_e_last, self.create_account_e_email, self.create_account_e_pass, self.create_account_e_age]
        
        #Buttons and commands
        create_account_btn_CA = tk.Button(self, width = 16, text = "CREATE ACCOUNT", font=BUTTON_FONT ,command=lambda: self.create_account(self.create_account_e_first.get(), self.create_account_e_last.get(), self.create_account_e_email.get(), self.create_account_e_pass.get(), self.create_account_e_age.get(), entries)) #'entries' paramater included so the boxes can be cleared
        create_account_btn_back = tk.Button(self, width = 16, text = "BACK", font=BUTTON_FONT, command=lambda:  [controller.back_config(entries), controller.show_frame(LoginMenu)])

        #Placing widgets on screen
        #Labels
        create_account_description.place(relx=0.5,rely=0.25, anchor="center")
        create_account_lb_first_name.place(relx=0.35,rely=0.35, anchor="center")
        create_account_lb_last_name.place(relx=0.65,rely=0.35, anchor="center")
        create_account_lb_email.place(relx=0.5,rely=0.46, anchor="center")
        create_account_lb_pass.place(relx=0.5,rely=0.55, anchor="center")
        create_account_lb_age.place(relx=0.5,rely=0.65, anchor="center")
        #Entries
        self.create_account_e_first.place(relx=0.35,rely=0.4, anchor="center")
        self.create_account_e_last.place(relx=0.65,rely=0.4, anchor="center")
        self.create_account_e_email.place(relx=0.5,rely=0.5, anchor="center")
        self.create_account_e_pass.place(relx=0.5,rely=0.6, anchor="center")
        self.create_account_e_age.place(relx=0.5,rely=0.7, anchor="center")
        #Buttons
        create_account_btn_back.place(relx=0.32,rely=0.84, anchor="center")
        create_account_btn_CA.place(relx=0.68,rely=0.84, anchor="center")

    def create_account(self, first_name, last_name, email, password, age, entries):
        '''Creates account and updates csv file'''
        
        #Stores the entries in a tuple
        fn = (first_name, "fn")
        ln = (last_name, "ln")
        em = (email, "em")
        p = (password, "p")
        a = (age, "a")

        boxes = [fn, ln, em, p, a]

        #Creates dictionary with tuple as the key and name of entry box as the value
        entry_names = {
            "fn": self.create_account_e_first, 
            "a": self.create_account_e_age, 
            "ln": self.create_account_e_last, 
            "em": self.create_account_e_email, 
            "p": self.create_account_e_pass}
        
        #Set all box backgrounds to white
        for box in boxes:
            entry = entry_names.get(box[1])
            super().config_entry_bg(entry, 'white')

        #Handles case validation
        msg = ""
        #Checks if entry boxes are empty
        if len(fn[0])==0 or len(ln[0])==0 or len(em[0])==0 or len(p[0])==0 or len(a[0])==0:
            msg = "Names, email, password or age cannot be empty"

            #Highlight a red background colour for all empty boxes
            #Find out which ones are empty
            super().validate_empty(entry_names, boxes)
        
        else:
            try:
                validation = True
                while validation == True:

                    #Combine names into one username
                    username = f"{first_name} {last_name}"                   
                    ##Checks for any invalid characters in the username then creates a message if invalid
                    for ch in username:
                        if ch in SPECIALS or ch.isalpha():
                            continue
                        else:
                            msg = ("Your name contains invalid characters. Please" 
                            " try again and enter a valid name.")
                            #Configure first and last name widgets to bg = red and break out of loop
                            super().config_entry_bg(entry_names["fn"], '#FFCCCC')
                            super().config_entry_bg(entry_names["ln"], '#FFCCCC')
                            validation = False
                            break
                    
                    #Breaks out of the loop if name is invalid
                    if validation == False:
                        break
                    
                    #Runs the email validator function
                    valid_email = self.validate_email(email)
                    
                    #If the email is invalid, prompt again.
                    if not valid_email:
                        msg ="That email is not a valid email address, please try again."
                        super().config_entry_bg(entry_names["em"], '#FFCCCC')
                        break
                    
                    #Initialize flag to check if the email already exists in account dict.
                    for account in user_details:
                        if account["email"]==email:
                            msg = "This email has already been taken. Please enter another email address."
                            super().config_entry_bg(entry_names["em"], '#FFCCCC')
                            validation = False
                            break
                    
                    #Breaks out of loop if email already exists
                    if validation == False:
                        break
                    
                    #Password is then validated using a series of regex expressions
                    if len(p[0]) < MIN_PW_LENGTH:
                        msg = "Make sure your password is at least 8 characters in length."
                        super().config_entry_bg(entry_names["p"], '#FFCCCC')
                    elif re.search('[0-9]',password) is None:
                        msg = "\nMake sure your password has a number in it.\n"
                        super().config_entry_bg(entry_names["p"], '#FFCCCC')
                    elif re.search('[A-Z]',password) is None: 
                        msg = "\nMake sure your password has a capital letter in it.\n"
                        super().config_entry_bg(entry_names["p"], '#FFCCCC') 
                    elif re.search('[!@#$%^&*]',password) is None:
                        super().config_entry_bg(entry_names["p"], '#FFCCCC') 
                        msg = "\nMake sure your password has a special character in it.\n"
                        super().config_entry_bg(entry_names["p"], '#FFCCCC')
                    
                    #Checks if age is a number
                    elif any(ch.isdigit() for ch in a) == False:
                        msg = "age must be a NUMBER!"
                        super().config_entry_bg(entry_names["a"], '#FFCCCC')
                    
                    #Asks the user for their age then compares with boundary case
                    elif int(age) < MIN_AGE or int(age) > MAX_AGE:
                        msg = "You are not eligibile to create an account. You must be at least 16 years old"
                        
                        #Clear entry box widgets and driect user back to main screen
                        self.controller.show_frame(LoginMenu)
                        self.controller.clear_entries(entries) #Could also do controller.clear_entries if you don't want to use inheritance

                    else:
                        #Append a dictionary with account information to user_details list
                        account = {}
                        account["username"]=username
                        account["email"]=email
                        account["password"] = password
                        account["data"] = {} #Empty dictionary that will have the user's saved data after logging out
                        user_details.append(account)
                        msg = "Account created successfully"

                        #Instantiates a user object with the logged user's attributes
                        user = Current_User(username, email, password)

                        #Extract saved data (since new account it will be an empty dict)
                        saved_data = account["data"]
                        #Adjust the saved_data attribute
                        user.saved_data = saved_data

                        #Sets the current user
                        user.set_current_user()

                        #Configure the mainmenu label widget
                        main_menu = self.controller.get_screen(MainMenu)
                        if main_menu:
                            main_menu.configure_label()
                        
                        #Clear entry box widgets and direct user to main menu
                        self.controller.clear_entries(entries)
                        self.controller.show_frame(MainMenu)

                    #Breaks out of loop after validation steps
                    break
    
            except Exception as ep:
                messagebox.showerror('error', ep)

        if msg!="":
            #If message does not equal nothing (a.k.a if it is not one of the 4 prompts above)- ensures the popup doesn't still show after the calculation is successful. 
            #otherwsie if msg is still "" as defined before the if/else statements, then no popup will show whcih is good.
            messagebox.showinfo('message', msg)
   
    def validate_email(self, email):
        '''Validates user's email via a regex expression'''
        #Compares email to the regex expression then returns true or false
        return bool(re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email))
        
class Exit(tk.Frame):
    def __init__(self, parent, controller):
        '''Constructor Method to define attributes and widgets'''
        super().__init__(parent)
        exit_sub_heading = tk.Label(self, text="Exiting the program will delete all stored data for all accounts.\nAre you sure you want to continue?", justify = "center", wraplength=460, font=("Times", 12, "bold"),fg="black", bg=BG_COLOUR)
        #Confirmation buttons for yes and no 
        exit_btn_yes = tk.Button(self, width=16, text = "YES", font=BUTTON_FONT, fg = "black", bg=DEFAULT, command=lambda: controller.kill())
        exit_btn_no = tk.Button(self, text = "NO", width=16, font=BUTTON_FONT, fg = "black", bg=DEFAULT, command=lambda: controller.show_frame(LoginMenu))
        
        #Placing widgets on screen
        exit_sub_heading.place(relx=0.5,rely=0.2, anchor="center")
        exit_btn_yes.place(relx=0.7,rely=0.7, anchor="center")
        exit_btn_no.place(relx=0.3,rely=0.7, anchor="center")

class Login(tk.Frame, Flight_booker_app):
    def __init__(self, parent, controller):
        '''Constructor method to define attributes and widgets'''
        super().__init__(parent)

        #Controller
        self.controller = controller
        
        #Create description
        self.login_text = "Login to your account!"
        self.txt=tk.StringVar()
        self.txt.set(self.login_text)
        self.login_description =tk.Label(self, textvariable=self.txt, justify = "center", wraplength=370, font=("Times", 12), fg="black", bg=BG_COLOUR)
        
        #Labels
        login_lb_user = tk.Label(self,text= "Enter Email :", font = ('Arial', 12, "bold"), fg="darkgreen", bg=BG_COLOUR )
        login_lb_pass = tk.Label(self,text= "Enter Password :", font = ('Arial', 12, "bold"), fg="darkgreen", bg=BG_COLOUR )
        
        #Entries
        self.login_e_email = tk.Entry(self, width=25)
        self.login_e_pass = tk.Entry(self, width=25, show="*")
        entries = [self.login_e_email, self.login_e_pass]
        
        #Buttons
        login_btn_login = tk.Button(self, text = "SIGN IN", fg="black", bg=DEFAULT, width=16, font=BUTTON_FONT, command=lambda: self.login(self.login_e_email.get(), self.login_e_pass.get(), entries)) 
        login_btn_back = tk.Button(self, text = "BACK", fg="black", bg=DEFAULT, font=BUTTON_FONT, width=16, command=lambda: [controller.back_config(entries), self.txt.set(self.login_text), self.login_description.config(textvariable = self.txt, fg="black"), controller.show_frame(LoginMenu)])
        
        #Placing widgets on screen
        self.login_description.place(relx=0.5,rely=0.25,anchor="center")
        login_lb_user.place(relx=0.4,rely=0.4,anchor="center")
        login_lb_pass.place(relx=0.4,rely=0.6,anchor="center")
        self.login_e_email.place(relx=0.6,rely=0.4,anchor="center")
        self.login_e_pass.place(relx=0.6,rely=0.6,anchor="center")
        login_btn_login.place(relx=0.68,rely=0.84,anchor="center")
        login_btn_back.place(relx=0.32,rely=0.84,anchor="center")

    def login(self, email, password, entries):
        '''Function and validation for the login button'''

        #Stores the entries in a tuple
        em = (email, "em")
        p = (password, "p")

        #Creates dictionary with tuple as the key and name of entry box as the value
        entry_names = {
            "em": self.login_e_email, 
            "p": self.login_e_pass}
        
        boxes = [em, p]

        #Set all box backgrounds to white
        for box in boxes:
            entry = entry_names.get(box[1])
            super().config_entry_bg(entry, 'white')

        #sets number of tries left from the string (textvariable in the label) so that it can be used for later.
        if self.txt.get().find("1") > -1: 
            attempts = 1
        elif self.txt.get().find("2") > -1:
            attempts = 2
        elif self.txt.get().find("3") > -1:
            attempts = 3
        elif self.txt.get().find("4") > -1:
            attempts = 4
        else:
            attempts = ATTEMPTS

        #Handles case validation
        msg = ""
        if len(em[0])==0 or len(p[0])==0:
            msg = "username and password can't be empty"

            #Highlight a red background colour for all empty boxes
            #Find out which ones are empty
            super().validate_empty(entry_names, boxes)

        else:
            try:
                #Checks if email exists in dictionary  
                email_exists = False
                for account in user_details:
                    if email == account["email"]:
                        email_exists = True
                        #Sets correct password to that in the account dictionary
                        correct_password = account["password"]
                        break

                if email_exists == True and password == correct_password:
                    #Instantiates a user object with the logged user's attributes
                    user = Current_User(account["username"], account["email"], account["password"])
                    
                    #Extract saved data (if new account it will be an empty dict)
                    saved_data = account["data"]
                    #Adjust the saved_data attribute
                    user.saved_data = saved_data

                    if len(user.saved_data)!=0:
                        #Restore tickets and orders
                        user.domestic_tickets=user.saved_data["domestic"]  #list of dictionaries
                        user.international_tickets=user.saved_data["international"] #list of dictionaries

                    #Sets the current user
                    user.set_current_user()

                    #Configure the mainmenu label widget
                    main_menu = self.controller.get_screen(MainMenu)
                    if main_menu:
                        main_menu.configure_label()

                    #Navigates to main menu
                    msg = "Login Successful!"
                    self.txt.set(self.login_text)
                    self.login_description.config(textvariable=self.txt, fg ="black")
                    self.controller.show_frame(MainMenu)
                    #Sink the frame and configure widgets back to default
                    self.controller.clear_entries(entries)
                
                else:
                    attempts = attempts-1
                    #Highlight entry boxes red
                    super().config_entry_bg(entry_names["p"], '#FFCCCC')
                    super().config_entry_bg(entry_names["em"], '#FFCCCC')

                    if attempts == 0:
                        #Navigate back to login menu and configure widgets back to normal
                        msg = "Too many failed login attempts." + " LOGIN DENIED!"
                        self.controller.show_frame(LoginMenu)
                        self.txt.set(self.login_text)
                        self.login_description.config(textvariable=self.txt, fg ="black")
                        self.controller.clear_entries(entries)
                        super().config_entry_bg(entry_names["p"], 'white')
                        super().config_entry_bg(entry_names["em"], 'white')
                    
                    else:
                        #Configure the label with the number of attempts left
                        self.controller.clear_entries(entries)
                        newtext = f"Incorrect email or password! {attempts} attempts left."
                        self.txt.set(newtext)
                        self.login_description.config(textvariable=self.txt, fg ="darkred")

         
            except Exception as ep:
                messagebox.showerror('error', ep)
        
        if msg!= "": #If message does not equal nothing (a.k.a if it is not one of the 4 prompts above)- ensures the popup doesn't still show after the calculation is successful. 
            #otherwsie if msg is still "" as defined before the if/else statements, then no popup will show which is good.
            messagebox.showinfo('message', msg)

#______________________________BOOK FLIGHT COMPONENET SCREENS_____________________________

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        '''Constructor method to define attributes and widgets'''
        super().__init__(parent)

        #Attributes
        self.controller = controller
        self.default_text = '"Welcome name! You can now view and book current flights!'
        self.txt = tk.StringVar()
        self.txt.set(self.default_text)

        #Description
        self.mainmenu_decription = tk.Label(self, textvariable = self.txt, justify = "center",  font=("Times", 12),fg="black", bg=BG_COLOUR)

        #Buttons
        mainmenu_btn_book_flight = tk.Button(self, width=16, text = "BOOK FLIGHT", font=BUTTON_FONT,command=lambda: controller.show_frame(TravelType))
        mainmenu_btn_view_cart = tk.Button(self, width=16, text = "VIEWCART", font=BUTTON_FONT,command=lambda: [self.label_summary(), controller.show_frame(CartMenu)])
        mainmenu_btn_logout = tk.Button(self, width=16, text = "LOGOUT(SAVE)", font=BUTTON_FONT,command=lambda: controller.show_frame(Logout))
        mainmenu_btn_options = tk.Label(self, text="Options:", font=SMALL_FONT, fg="black", bg=BG_COLOUR)

        #Placing widgets on screen
        mainmenu_btn_book_flight.place(relx=0.5, rely=0.5, anchor = "center")
        mainmenu_btn_view_cart.place(relx=0.5, rely=0.6, anchor = "center")
        mainmenu_btn_logout.place(relx=0.5, rely=0.7, anchor = "center")
        mainmenu_btn_options.place(relx=0.5, rely=0.4, anchor="center")
        self.mainmenu_decription.place(relx=0.5,rely=0.25, anchor="center")

    def configure_label(self):
        '''Configures description label to the name of user'''
        #Retrieve current user object
        user = logged_user[0]
        username = user.username
        newtext = f"Welcome {username}!  You can now view and book current flights!"
        self.txt.set(newtext)
        self.mainmenu_decription.config(textvariable = self.txt)
    
    def label_summary(self):
        '''Communicates label summary to cartmenu screen'''
        #Get the screen
        cart_screen= self.controller.get_screen(CartMenu)
        #Retrieve the current user
        user = logged_user[0]
        #Get the list of all tickets
        ticket_list = user.append_tickets()
        length = len(ticket_list)
        #Calculate total price
        total_price = user.calculate_total_price()
        #Configure label widget with summary on CartMenu window (instance)
        newtext = f"There are {length} Flight Tickets in cart of {user.username} ({user.email}). This comes to a total price of ${total_price:.2f}."
        cart_screen.configure_label(newtext)

class TravelType(tk.Frame):
    def __init__(self, parent, controller):
        '''Constructor method to define attributes and widgets'''
        super().__init__(parent)

        #Attributes
        self.controller = controller

        #Buttons
        traveltype_options_lbl = tk.Label(self, text="Choose Travel Type:", font=SMALL_FONT, fg="black", bg=BG_COLOUR)
        traveltype_btn_domestic = tk.Button(self, width=16, text = "DOMESTIC", font=BUTTON_FONT,command=lambda: controller.show_frame(BookFlight, "domestic"))
        traveltpe_btn_btn_international = tk.Button(self, width=16, text = "INTERNATIONAL", font=BUTTON_FONT,command=lambda: controller.show_frame(BookFlight, "international"))
        back_button = tk.Button(self, width=16, text="BACK", font = BUTTON_FONT, command=lambda: controller.show_frame(MainMenu))
        #Placing Widgets on Screen
        traveltype_options_lbl.place(relx=0.5, rely=0.4, anchor="center")
        traveltype_btn_domestic.place(relx = 0.5, rely=0.5, anchor="center")
        traveltpe_btn_btn_international.place(relx = 0.5, rely = 0.6, anchor="center")
        back_button.place(relx=0.5, rely=0.7, anchor="center")

class BookFlight(tk.Frame):
    def __init__(self, parent, controller):
        '''Constructor method to define attributes and widgets'''
        super().__init__(parent)

        #Attributes
        self.controller=controller
        self.flight_type = [] #Will store the flights (D or I)

        #Treeview Frame and Widget
        bookflight_tv_frame = tk.Frame(self, borderwidth=3, relief="sunken", padx=10, pady=10)
        self.bookflight_treeview = ttk.Treeview(bookflight_tv_frame, columns=COLUMNS, show='headings', height = 17, selectmode="browse")
        
        #Headings and columns
        self.controller.create_headings(self.bookflight_treeview, COLUMNS)
        self.bookflight_treeview.column("Flight#:", width=100, anchor="w", minwidth=100)
        self.bookflight_treeview.column("Travel Type:", width=115, anchor="w", minwidth=115)
        self.bookflight_treeview.column("Arline Name:", width=150, anchor="w", minwidth=150)
        self.bookflight_treeview.column("Airport:", width=210, anchor="w", minwidth=210)
        self.bookflight_treeview.column("Destination:", width=190, anchor="w", minwidth=190)
        self.bookflight_treeview.column("Duration:", width=100, anchor="w", minwidth=100)
        self.bookflight_treeview.column("Date:", width=145, anchor="w", minwidth=145)
        self.bookflight_treeview.column("Price($):", width=95, anchor="w", minwidth=95)
        
        #Scrollbars
        bookflight_scrollbar = tk.Scrollbar(bookflight_tv_frame, orient = "vertical", command=self.bookflight_treeview.yview)
        self.bookflight_treeview.configure(yscroll = bookflight_scrollbar.set)
        bookflight_scrollbar.pack(side="right", fill="y")

        #Buttons
        select_button = tk.Button(self, text = "SELECT", width=16,font=BUTTON_FONT,command=lambda: self.select_flight())
        back_button = tk.Button(self, text="BACK", width =16, font=BUTTON_FONT, command=lambda:self.back())
        
        #Placing widgets on screen
        bookflight_tv_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.bookflight_treeview.pack(fill="both", expand=True)
        select_button.place(relx=0.6, rely = 0.875, anchor="center")
        back_button.place(relx=0.4, rely=0.875, anchor="center")

        # Bind click event to clear selection
        self.bind("<Button-1>", self.clear_selection)

    def load_flights(self, flight_type):
        '''Loads respective flights (International or Domestic) into the treeview'''
        self.bookflight_treeview.delete(*self.bookflight_treeview.get_children()) #Clear existing data
        if flight_type == "domestic":
            self.flight_type = domestic_flights
            flights_list = domestic_flights
            unit = "min"
        else:
            flights_list = international_flights
            self.flight_type = international_flights
            unit = "hrs"
        
        #Load the flights list into the treeview
        for flight in flights_list:
            self.bookflight_treeview.insert("", "end", values=(f" {flight.flight_number}", f" {flight.travel_type}", f" {flight.airline_name}", f" {flight.airport}", f" {flight.destination}", f" {flight.duration} {unit}",f" {flight.date}", f" ${flight.ticket_price:.2f}" ))

    def select_flight(self):
        '''Gets the user's selection'''
        selected_item=self.bookflight_treeview.selection()

        if not selected_item:
            #No item is selected
            messagebox.showinfo("No Selection", "Please select a flight!")
        else:
            # Get selected flight details and transfer to personalisation screen
            flight = self.bookflight_treeview.item(selected_item)["values"]
            
            #Get the selected flight number and retrieve the flight object
            flight_num = flight[0].strip()
            for flight_object in self.flight_type:
                if flight_object.flight_number == flight_num:
                    desired_flight_obj = flight_object
                    break
            personalisation_screen = self.controller.get_screen(Personalisation)
            personalisation_screen.load_flight(flight, desired_flight_obj)
            self.controller.show_frame(Personalisation)

    def clear_selection(self, event):
        # Clear the selection in the Treeview
        self.bookflight_treeview.selection_remove(self.bookflight_treeview.selection())

    def back(self):
        '''Clears treeview and goes back'''
        self.bookflight_treeview.delete(*self.bookflight_treeview.get_children())
        self.controller.show_frame(TravelType)

class Personalisation(tk.Frame):
    def __init__(self, parent, controller):
        '''Constructor method to define attributes and widgets'''
        super().__init__(parent)

        #Attributes
        self.controller = controller
        self.flight_obj = None
        
        #Labels
        flight_details = tk.Label(self, text="Flight Information:", justify = "center",  font=("Times", 12),fg="black", bg=BG_COLOUR)
        cabin_class = tk.Label(self, text ="Select Cabin Class:", justify = "center",  font=("Times", 12),fg="black", bg=BG_COLOUR)
        age=tk.Label(self, text="Age of Ticket Holder:", justify = "center",  font=("Times", 12),fg="black", bg=BG_COLOUR)
        price = tk.Label(self, text="Price:", justify = "center",  font=("Times", 12),fg="black", bg=BG_COLOUR)
        name = tk.Label(self, text="Name of Ticket Holder", justify = "center",  font=("Times", 12),fg="black", bg=BG_COLOUR)

        #Treeview
        tree_frame = tk.Frame(self, borderwidth=3, relief="sunken", padx=10, pady=10)
        self.treeview = ttk.Treeview(tree_frame, columns=COLUMNS, show='headings', height = 1)

        #Headings and columns
        self.controller.create_headings(self.treeview, COLUMNS)
        self.treeview.heading("Price($):", text="Price($):")
        self.treeview.column("Flight#:", width=100, anchor="w", minwidth=100)
        self.treeview.column("Travel Type:", width=115, anchor="w", minwidth=115)
        self.treeview.column("Arline Name:", width=150, anchor="w", minwidth=150)
        self.treeview.column("Airport:", width=210, anchor="w", minwidth=210)
        self.treeview.column("Destination:", width=190, anchor="w", minwidth=190)
        self.treeview.column("Duration:", width=100, anchor="w", minwidth=100)
        self.treeview.column("Date:", width=145, anchor="w", minwidth=145)
        self.treeview.column("Price($):", width=95, anchor="w", minwidth=95)

        self.treeview.pack(fill="both", expand=True)

        self.disable_treeview()

        #Dropdowns
        self.cc_options = []
        self.option_add('*TCombobox*Listbox.font', ("consolas",9))
        self.cabinclass=ttk.Combobox(self, values=self.cc_options, width = 40, font=("consolas",9))
        self.cabinclass['state'] = 'readonly'
        self.cabinclass.bind("<<ComboboxSelected>>", self.display_ticket_price)
        
        self.a_options =[]
        self.ageclass = ttk.Combobox(self, values = self.a_options, width = 41, font=("consolas",9))
        self.ageclass['state'] = 'readonly'
        self.ageclass.bind("<<ComboboxSelected>>", self.display_ticket_price)

        
        #Entries
        self.name_th = tk.Entry(self, width=25)
        
        #Text box
        self.price_box = tk.Text(self, width = 10, height=0, state='disabled', font=("Arial", 24, "bold"), bg="lightgreen")
        
        #Buttons
        back = tk.Button(self, text="BACK", width =16, font=BUTTON_FONT, command=lambda:[self.back(), self.controller.show_frame(BookFlight)])
        create_ticket = tk.Button(self, text="CREATE TICKET", width=16, font=BUTTON_FONT, command=lambda: self.create_ticket())

        #Placing Widgets on Screen
        flight_details.place(relx = 0.5, rely=0.20, anchor="center")
        cabin_class.place(relx=0.19, rely=0.45, anchor="center")
        age.place(relx=0.5, rely = 0.45, anchor="center")
        name.place(relx = 0.81, rely = 0.45, anchor="center")
        price.place(relx = 0.5, rely=0.65, anchor="center")

        tree_frame.place(relx=0.5, rely=0.3, anchor="center")
        self.cabinclass.place(relx=0.19, rely=0.5, anchor="center")
        self.ageclass.place(relx = 0.5, rely = 0.5, anchor="center")

        self.name_th.place(relx=0.81, rely=0.5, anchor="center")
        self.price_box.place(relx= 0.5, rely= 0.7, anchor="center")
        back.place(relx=0.3, rely=0.82, anchor="center")
        create_ticket.place(relx=0.7, rely=0.82, anchor="center")
    
    def display_ticket_price(self, event):
        '''Configures the text box and applies discounts when combobox value is selected'''
        age_selection = self.ageclass.get()
        ageindex = self.ageclass.current()

        cc_selection = self.cabinclass.get()
        ccindex = self.cabinclass.current()

        price = self.flight_obj.ticket_price

        #Does not configure anything if age selected is title or nothing
        if age_selection != "|---Age of Ticket Holder--| Discount(%) |" or ageindex !=-1:
            #Selected child
            if ageindex == 1:
                price = price*self.flight_obj.child_discount
            #Selected adult
            elif ageindex == 2:
                price = price*self.flight_obj.adult_discount
            #Selected sneior
            elif ageindex ==3:
                price = price*self.flight_obj.senior_discount
        
        #Does not configure anything if cc selected is title or nothing
        if cc_selection != "|----Select a Cabin Class---| Price($) |" or ageindex !=-1:
            #Selected First class
            if ccindex == 1:
                price = price*self.flight_obj.first_class_multiplier
            #Selected  Economy class
            elif ccindex == 2:
                price = price*self.flight_obj.economy_class_multiplier
            #Selected Business class
            elif ccindex ==3:
                price = price*self.flight_obj.business_class_multiplier

        #Display price in textbox
        self.price_box.config(state="normal")
        self.price_box.delete('1.0', tk.END)
        self.price_box.insert(tk.END, f"${price:.2f}")
        self.price_box.config(state="disabled")
    
    def create_ticket(self):
        '''Creates a ticket and performs validation'''

        #Configure background of entry to white
        self.controller.config_entry_bg(self.name_th, 'white')

        #Show error if invalid combobox selections are selected
        ageindex = self.ageclass.current()
        ccindex = self.cabinclass.current()
        name = self.name_th.get().strip()

        #Check for invalid characters in name
        validation = True
        for ch in name:
            if ch in SPECIALS or ch.isalpha():
                continue
            else:
                self.controller.config_entry_bg(self.name_th, '#FFCCCC')
                validation = False
                messagebox.showinfo('Error', "Name contains invalid characters. Please enter a valid name!")
                break

        if validation == True:
            try:
                #Handles invalid index
                if ageindex == -1 or ageindex == 0 or ccindex ==-1 or ccindex ==0:
                    messagebox.showinfo('Selection Error', "Please select a valid age or cabin class!")
                
                #Handles invalid entry
                elif len(name) ==0:
                    self.controller.config_entry_bg(self.name_th, '#FFCCCC')
                    messagebox.showinfo('Error', "Please enter a name!")
                    
                elif ccindex >=1 and ageindex >=1:
                    #We do the following
                    if ageindex ==1:
                        ticket_holder_age = "Child"
                    elif ageindex ==2:
                        ticket_holder_age = "Adult"
                    elif ageindex ==3:
                        ticket_holder_age = "Senior"
                    
                    if ccindex ==1:
                        cabin_class = "First"
                    elif ccindex ==2:
                        cabin_class = "Economy"
                    elif ccindex ==3:
                        cabin_class = "Business"
                                        
                    #Instantiates a ticket object with age type and cabin class type attributes
                    user_ticket = Ticket(self.flight_obj.travel_type, self.flight_obj.flight_number, self.flight_obj.airport, self.flight_obj.destination, self.flight_obj.country, self.flight_obj.stopovers, self.flight_obj.duration, self.flight_obj.date, self.flight_obj.ticket_price, self.flight_obj.airline_name, cabin_class, ticket_holder_age, name)
                    #Calculates the new price of the ticket based on their choices
                    user_ticket.ticket_price = user_ticket.apply_discounts(self.flight_obj)
                
                    #Adds the ticket to the users respective ticket list
                    user = logged_user[0]
                    if type(self.flight_obj)==Domestic:
                        user.add_ticket(user.domestic_tickets, user_ticket)
                    elif type(self.flight_obj)==International:
                        user.add_ticket(user.international_tickets, user_ticket)
                                                          
                    #Empty necessary widgets
                    self.back()
                    #Navigate to mainmenu
                    self.controller.show_frame(MainMenu)
                    messagebox.showinfo('Information', "Ticket has been added to your order successfully")
            
            except Exception as ep:
                messagebox.showerror('error', ep)

    def load_flight(self, flight_data, flight_obj):
        '''Loads flight from selection on previous screen'''
        #Set the attribute to the flight object and configure text box
        self.flight_obj = flight_obj
        self.price_box.config(state="normal")
        self.price_box.delete('1.0', tk.END)
        self.price_box.insert(tk.END, f"${flight_obj.ticket_price:.2f}")
        self.price_box.config(state="disabled")

        self.treeview.delete(*self.treeview.get_children()) #Clear existing data
        self.treeview.insert("", "end", values=flight_data) #Insert the data
        
        #Set the flight attribute as the necessary flight object and retrieve the cabin class types
        #If the length of the cabin_class_types attribute (type is list) from the domestic and international flight classes (further below)
        #is 2 then this means the flight is domestic with only Economy and First Class so those multipliers will show whereas international has 
        #Business class as well

        #Clear any existing options
        self.cc_options.clear()
        self.cabinclass.config(self.cc_options)
        self.a_options.clear()
        self.ageclass.config(self.a_options)

        #Append required options
        self.cc_options.append("|----Select a Cabin Class---| Price($) |")
        
        if len(flight_obj.cabin_class_types) == 2:
            self.cc_options.append(f"|First Class                | ${flight_obj.ticket_price*flight_obj.first_class_multiplier:<7.2f} |")
            self.cc_options.append(f"|Economy Class              | ${flight_obj.ticket_price*flight_obj.economy_class_multiplier:<7.2f} |")       
        elif len(flight_obj.cabin_class_types) ==3:
            self.cc_options.append(f"|First Class                | ${flight_obj.ticket_price*flight_obj.first_class_multiplier:<7.2f} |")
            self.cc_options.append(f"|Economy Class              | ${flight_obj.ticket_price*flight_obj.economy_class_multiplier:<7.2f} |")
            self.cc_options.append(f"|Business Class             | ${flight_obj.ticket_price*flight_obj.business_class_multiplier:<7.2f} |")
            
        
        self.cabinclass.config(values = self.cc_options)
        self.cabinclass.current(0)

        #Display the age options and prices in the dropdown box
        self.a_options.append("|---Age of Ticket Holder--| Discount(%) |")
        self.a_options.append(f"|Child: (0-17yrs)         | {(1-flight_obj.child_discount)*100:>11.1f}% |")
        self.a_options.append(f"|Adult: (18-64yrs)        | {(1-flight_obj.adult_discount)*100:>11.1f}% |")
        self.a_options.append(f"|Senior: (65+yrs)         | {(1-flight_obj.senior_discount)*100:>11.1f}% |")

        self.ageclass.config(values=self.a_options)
        self.ageclass.current(0)
        
    def disable_treeview(self):
        # Override the selection and clicking events
        def disable_event(*args):
            return "break"
        
        # Disable selecting items
        self.treeview.bind("<Button-1>", disable_event)
        self.treeview.bind("<Double-1>", disable_event)
        self.treeview.bind("<B1-Motion>", disable_event)

        # Disable keyboard selection
        self.treeview.bind("<Key>", disable_event)

    def back(self):
        '''Go back to previous screen and configure all widgets'''
        self.treeview.delete(*self.treeview.get_children()) #Clear treeview data
        #Clear any existing options
        self.cc_options.clear()
        self.cabinclass.config(self.cc_options)
        self.a_options.clear()
        self.ageclass.config(self.a_options)
        #Clear price box
        self.price_box.config(state='normal')
        self.price_box.delete('1.0', tk.END)
        self.price_box.config(state="disabled")
        #Clear entries
        self.name_th.delete(0, tk.END)
      
#________________________________VIEW CART AND LOGOUT COMPONENET SCREENS _____________________

class CartMenu(tk.Frame):
    def __init__(self, parent, controller):
        '''Constructor method to define attributes and widgets'''
        super().__init__(parent)

        #Attributes
        self.controller = controller
        self.default_text = f"There are no pending tickets in cart of user:"
        self.txt = tk.StringVar()
        self.txt.set(self.default_text)
        
        #Labels
        self.display_details = tk.Label(self, textvariable=self.txt, justify = "center",  font=("Times", 12),fg="black", wraplength=480, bg=BG_COLOUR)
        options = tk.Label(self, text="Options:", font=SMALL_FONT, fg="black", bg=BG_COLOUR)

        #Buttons
        btn_back = tk.Button(self, width=16, text = "BACK", font=BUTTON_FONT,command=lambda: controller.show_frame(MainMenu))
        btn_display_cart = tk.Button(self, width=16, text = "DISPLAY CART", font=BUTTON_FONT,command=lambda: self.display_cart())
        btn_edit_order = tk.Button(self, width=16, text = "EDIT ORDER", font=BUTTON_FONT,command=lambda: self.edit_order())
        btn_confirm_order = tk.Button(self, width = 16, text = "CONFIRM ORDER", font=BUTTON_FONT,command=lambda: self.confirm_order())
       
        #Placing widgets on the screen
        self.display_details.place(relx=0.5, rely=0.25, anchor="center")
        options.place(relx = 0.5, rely=0.33, anchor="center")
        btn_back.place(relx = 0.5, rely= 0.7, anchor="center")
        btn_display_cart.place(relx = 0.5, rely=0.4, anchor="center")
        btn_edit_order.place(relx = 0.5, rely=0.5, anchor="center")
        btn_confirm_order.place(relx = 0.5, rely = 0.6, anchor="center")
    
    def check_cart_length(self):
        '''Check's cart length before proceeding'''
        #Handle cart length of 0
        user = logged_user[0]
        if len(user.domestic_tickets) ==0 and len(user.international_tickets) ==0:
            messagebox.showinfo('Information', "You have no pending items in your cart. Please order a flight ticket!")
            return True
        else:
            return False
        
    def display_cart(self):
        '''Navigates to screen if cart length not 0'''
        not_zero = self.check_cart_length()
        if not_zero == False:
            cart_screen = self.controller.get_screen(DisplayCart)
            d_list = logged_user[0].domestic_tickets
            i_list = logged_user[0].international_tickets
            total_price = logged_user[0].calculate_total_price()
            cart_screen.load_data(d_list, i_list, total_price)
            self.controller.show_frame(DisplayCart)
        
    def edit_order(self):
        '''Navigates to screen if cart length not 0'''
        not_zero = self.check_cart_length()
        if not_zero == False:
            cart_screen = self.controller.get_screen(EditOrder)
            cart_screen.load_data()
            self.controller.show_frame(EditOrder)

    def confirm_order(self):
        '''Navigates to screen if cart length not 0'''
        not_zero = self.check_cart_length()
        if not_zero == False:
            self.controller.show_frame(ConfirmOrder)

    def configure_label(self, newtext):
        '''Configures display_details widget with cart summary'''
        self.txt.set(newtext)
        self.display_details.config(textvariable=self.txt)

class DisplayCart(tk.Frame):
    def __init__(self, parent, controller):
        '''Constructor method to define attributes and widgets'''
        super().__init__(parent)

        #Attributes
        self.controller = controller
        self.default_text = ""
        self.txtd = tk.StringVar()
        self.txtd.set(self.default_text)
        self.txti = tk.StringVar()
        self.txti.set(self.default_text)

        #Labels
        self.domestic = tk.Label(self, textvariable=self.txtd, justify = "center",  font=("Times", 12),fg="black", bg=BG_COLOUR)
        self.international = tk.Label(self, textvariable=self.txti, justify = "center",  font=("Times", 12),fg="black", bg=BG_COLOUR)
        total_price = tk.Label(self, text="Total price:",justify = "center",  font=("Times", 12),fg="black", bg=BG_COLOUR)
        
        #Treeviews
        tree_d_frame = tk.Frame(self, borderwidth=3, relief="sunken", padx=10, pady=10)
        tree_i_frame = tk.Frame(self, borderwidth=3, relief="sunken", padx=10, pady=10)
        self.treeview_d = ttk.Treeview(tree_d_frame, columns=TICKET_HEADERS, show='headings', height = 3)
        self.treeview_i = ttk.Treeview(tree_i_frame, columns=TICKET_HEADERS, show='headings', height = 3)
        
        #Headings and columns
        self.controller.create_headings(self.treeview_d, TICKET_HEADERS)
        self.treeview_d.column("Name:", width = 70, anchor="w", minwidth=70)
        self.treeview_d.column("Age Type:", width = 70, anchor="w", minwidth=70)
        self.treeview_d.column("Cabin Class:", width = 70, anchor="w", minwidth=70)
        self.treeview_d.column("Flight#:", width=80, anchor="w", minwidth=80)
        self.treeview_d.column("Travel Type:", width=95, anchor="w", minwidth=95)
        self.treeview_d.column("Arline Name:", width=130, anchor="w", minwidth=130)
        self.treeview_d.column("Airport:", width=190, anchor="w", minwidth=190)
        self.treeview_d.column("Destination:", width=170, anchor="w", minwidth=170)
        self.treeview_d.column("Duration:", width=80, anchor="w", minwidth=80)
        self.treeview_d.column("Date:", width=125, anchor="w", minwidth=125)
        self.treeview_d.column("Price($):", width=75, anchor="w", minwidth=75)

        #Headings and columns
        self.controller.create_headings(self.treeview_i, TICKET_HEADERS)
        self.treeview_i.column("Name:", width = 70, anchor="w", minwidth=70)
        self.treeview_i.column("Age Type:", width = 70, anchor="w", minwidth=70)
        self.treeview_i.column("Cabin Class:", width = 70, anchor="w", minwidth=70)
        self.treeview_i.column("Flight#:", width=80, anchor="w", minwidth=80)
        self.treeview_i.column("Travel Type:", width=95, anchor="w", minwidth=95)
        self.treeview_i.column("Arline Name:", width=130, anchor="w", minwidth=130)
        self.treeview_i.column("Airport:", width=190, anchor="w", minwidth=190)
        self.treeview_i.column("Destination:", width=170, anchor="w", minwidth=170)
        self.treeview_i.column("Duration:", width=80, anchor="w", minwidth=80)
        self.treeview_i.column("Date:", width=125, anchor="w", minwidth=125)
        self.treeview_i.column("Price($):", width=75, anchor="w", minwidth=75)

        
        #Scrollbars
        d_scrollbar = tk.Scrollbar(tree_d_frame, orient = "vertical", command=self.treeview_d.yview)
        self.treeview_d.configure(yscroll = d_scrollbar.set)
        d_scrollbar.pack(side="right", fill="y")

        i_scrollbar = tk.Scrollbar(tree_i_frame, orient = "vertical", command=self.treeview_i.yview)
        self.treeview_i.configure(yscroll = i_scrollbar.set)
        i_scrollbar.pack(side="right", fill="y")
        
        
        #Buttons
        back = tk.Button(self, text="BACK", width =16, font=BUTTON_FONT, command=lambda:[self.back(), self.controller.show_frame(CartMenu)])

        #Textbox
        self.price_box = tk.Text(self, width = 8, height=0, state='disabled', font=("Arial", 24, "bold"), bg="white")

        #Placing widgets on screen
        self.domestic.place(relx=0.5, rely=0.25, anchor="center")
        tree_d_frame.place(relx=0.5, rely=0.38, anchor="center")
        self.international.place(relx=0.5, rely=0.54, anchor="center")
        tree_i_frame.place(relx=0.5, rely=0.67, anchor="center")
        total_price.place(relx = 0.55, rely = 0.85, anchor="center")
        self.price_box.place(relx=0.65, rely=0.85, anchor="center")
        back.place(relx=0.4, rely=0.85, anchor="center")
        self.treeview_d.pack(fill="both", expand=True)
        self.treeview_i.pack(fill="both", expand=True)
        
        self.disable_treeview(self.treeview_d)
        self.disable_treeview(self.treeview_i)

    def load_data(self, d_list, i_list, price):
        '''Load tickets into treeviews'''
        user = logged_user[0]
        #Get length of ticket lists
        domestic_length = len(user.domestic_tickets)
        international_length = len(user.international_tickets)
        dtext = f"Domestic Tickets: ({domestic_length})"
        itext = f"International Tickets: ({international_length})"

        #Configure labels
        self.txtd.set(dtext)
        self.domestic.config(textvariable=self.txtd)
        self.txti.set(itext)
        self.international.config(textvariable=self.txti)

        #Insert domestic and international tickets
        self.treeview_d.delete(*self.treeview_d.get_children()) #Clear existing data
        for ticket in d_list:
            self.treeview_d.insert("", "end", values=(f" {ticket.ticket_holder_name}", f" {ticket.ticket_holder_age}", f" {ticket.cabin_class}",f" {ticket.flight_number}", f" {ticket.travel_type}", f" {ticket.airline_name}", f" {ticket.airport}", f" {ticket.destination}", f" {ticket.duration} min",f" {ticket.date}", f" ${ticket.ticket_price:.2f}")) #Insert the data

        self.treeview_i.delete(*self.treeview_i.get_children()) #Clear existing data    
        for ticket in i_list:
            self.treeview_i.insert("", "end", values=(f" {ticket.ticket_holder_name}", f" {ticket.ticket_holder_age}", f" {ticket.cabin_class}",f" {ticket.flight_number}", f" {ticket.travel_type}", f" {ticket.airline_name}", f" {ticket.airport}", f" {ticket.destination}", f" {ticket.duration} hrs",f" {ticket.date}", f" ${ticket.ticket_price:2f}")) #Insert the data

        #Configure total price box
        self.price_box.config(state='normal')
        self.price_box.delete('1.0', tk.END)
        self.price_box.insert(tk.END, f"${price:.2f}")
        self.price_box.config(state="disabled")


    def back(self):
        '''Clear treeviews'''
        self.treeview_d.delete(*self.treeview_d.get_children()) #Clear treeview data
        self.treeview_i.delete(*self.treeview_i.get_children()) #Clear treeview data
        #Clear price box
        self.price_box.config(state='normal')
        self.price_box.delete('1.0', tk.END)
        self.price_box.config(state="disabled")


    def disable_treeview(self, tree):
        # Override the selection and clicking events
        def disable_event(*args):
            return "break"
        
        # Disable selecting items
        tree.bind("<Button-1>", disable_event)
        tree.bind("<Double-1>", disable_event)
        tree.bind("<B1-Motion>", disable_event)

        # Disable keyboard selection
        tree.bind("<Key>", disable_event)

class EditOrder(tk.Frame):
    def __init__(self, parent, controller):
        '''Constructor method to define attributes and widgets'''
        super().__init__(parent)

        #Attributes
        self.controller = controller

        #Dictionary to map the rows of the treeview by index
        self.row_map = {}

        #Buttons
        remove_btn = tk.Button(self, text = "REMOVE", width=16,font=BUTTON_FONT,command=lambda: self.remove_tickets())
        back_btn = tk.Button(self, text ="BACK", width=16, font=BUTTON_FONT, command=lambda: [self.back(), controller.show_frame(CartMenu)])
        
        #Labels
        remove = tk.Label(self, text="Select a ticket to remove from your order.", justify = "center",  font=("Times", 12, "bold"),fg="black", bg=BG_COLOUR)
        price = tk.Label(self, text="Total price:", font=("Times", 12, "bold"),fg="black", bg=BG_COLOUR)

        #Text box
        self.price_box = tk.Text(self, width = 10, height=0, state='disabled', font=("Arial", 24, "bold"), bg="white")
          
        #Treeview
        #Create column headers
        column_headers = ["#:"]
        for header in TICKET_HEADERS:
            column_headers.append(header)
        column_headers = tuple(column_headers)
        
        frame = tk.Frame(self, borderwidth=3, relief="sunken", padx=10, pady=10)
        self.treeview = ttk.Treeview(frame, columns=column_headers, show='headings', height = 14, selectmode="extended")
        #Headings and columns
        self.controller.create_headings(self.treeview, column_headers)
        self.treeview.column("#:", width = 22, anchor="w", minwidth=22)
        self.treeview.column("Name:", width = 68, anchor="w", minwidth=68)
        self.treeview.column("Age Type:", width = 68, anchor="w", minwidth=68)
        self.treeview.column("Cabin Class:", width = 68, anchor="w", minwidth=68)
        self.treeview.column("Flight#:", width=78, anchor="w", minwidth=78)
        self.treeview.column("Travel Type:", width=93, anchor="w", minwidth=93)
        self.treeview.column("Arline Name:", width=128, anchor="w", minwidth=128)
        self.treeview.column("Airport:", width=188, anchor="w", minwidth=188)
        self.treeview.column("Destination:", width=168, anchor="w", minwidth=168)
        self.treeview.column("Duration:", width=78, anchor="w", minwidth=78)
        self.treeview.column("Date:", width=123, anchor="w", minwidth=123)
        self.treeview.column("Price($):", width=73, anchor="w", minwidth=73)

        #Scrollbars
        scrollbar = tk.Scrollbar(frame, orient = "vertical", command=self.treeview.yview)
        self.treeview.configure(yscroll = scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        #Placing widgets on screen
        self.treeview.pack(fill="both", expand=True)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        price.place(relx=0.725, rely=0.85, anchor="center")
        self.price_box.place(relx= 0.85, rely= 0.85, anchor="center")
        remove.place(relx=0.5, rely=0.18, anchor="center")
        remove_btn.place(relx=0.5, rely = 0.85, anchor="center")
        back_btn.place(relx=0.25, rely=0.85, anchor="center")

        #Bind click event to clear selection
        self.bind("<Button-1>", self.clear_selection)

    def load_data(self):
        '''Loads tickets into treeview'''
        #Retrieve current user
        user = logged_user[0]
        #Create a list with domestic and international tickets user has ordered
        #This will also reset the list each time loop repeats
        all_tickets = user.append_tickets()

        #Insert all tickets
        self.treeview.delete(*self.treeview.get_children())#Clear existing data
        for ticket in all_tickets:
            if ticket.travel_type == "Domestic":
                id = self.treeview.insert("", "end", values=(f"{all_tickets.index(ticket)+1}", f" {ticket.ticket_holder_name}", f" {ticket.ticket_holder_age}", f" {ticket.cabin_class}",f" {ticket.flight_number}", f" {ticket.travel_type}", f" {ticket.airline_name}", f" {ticket.airport}", f" {ticket.destination}", f" {ticket.duration} min",f" {ticket.date}", f" ${ticket.ticket_price:.2f}" ))
                index = all_tickets.index(ticket)
                #Map the id to the index
                self.row_map[id] = index

            elif ticket.travel_type == "International":
                id = self.treeview.insert("", "end", values=(f"{all_tickets.index(ticket)+1}", f" {ticket.ticket_holder_name}", f" {ticket.ticket_holder_age}", f" {ticket.cabin_class}",f" {ticket.flight_number}", f" {ticket.travel_type}", f" {ticket.airline_name}", f" {ticket.airport}", f" {ticket.destination}", f" {ticket.duration} hrs",f" {ticket.date}", f" ${ticket.ticket_price:.2f}" ))
                index = all_tickets.index(ticket)
                #Map the id to the index
                self.row_map[id] = index      
        
        #Display total price
        price=user.calculate_total_price()
        self.price_box.config(state="normal")
        self.price_box.delete('1.0', tk.END)
        self.price_box.insert(tk.END, f"${price:.2f}")
        self.price_box.config(state="disabled")
    
    def remove_tickets(self):
        '''Removes selected tickets'''
        #Retrieve current user
        user = logged_user[0]
        all_tickets = user.append_tickets()

        #Get the tuple of selected items
        selected_items=self.treeview.selection()      

        if not selected_items:
            #No item is selected
            messagebox.showinfo("No Selections", "Please select a ticket to remove!")
        else:
            #retrieve IDs and remove the items
            #Store indices in a list
            indices = []
            for id in selected_items:
                index = self.row_map[id]
                indices.append(index)              

            #Check if the ticket selected is domestic or international
            #to remove from appropriate list
            #Reverse the indices so that iterating through the list has no errors
            for index in sorted(indices, reverse=True):
                if all_tickets[index].travel_type == "Domestic":                    
                    user.remove_ticket(user.domestic_tickets, index)               
                elif all_tickets[index].travel_type == "International":
                    #In case user removes an international ticket
                    international_index = index - len(user.domestic_tickets)                  
                    user.remove_ticket(user.international_tickets, international_index)               
            
            #Get the new ticket list
            updated_list = user.append_tickets()
            
            if len(updated_list) ==0:
                self.back() #clears treeview
                #load updated data
                self.load_data()
                #Redirect user to the previous menu
                messagebox.showinfo("Emptied Cart", "Cart has been emptied.")
                self.controller.show_frame(CartMenu)
            else:
                self.back() #clears treeview
                #load updated data
                self.load_data()

    def clear_selection(self, event):
        # Clear the selection in the Treeview
        self.treeview.selection_remove(self.treeview.selection())
    
    def back(self):
        '''Clears treeview and price box'''
        self.treeview.delete(*self.treeview.get_children()) #Clear treeview data
        #Clear price box
        self.price_box.config(state='normal')
        self.price_box.delete('1.0', tk.END)
        self.price_box.config(state="disabled")

        #Clear dictionary
        self.row_map.clear()       

        #Configure cartmenu label
        cart_screen = self.controller.get_screen(CartMenu)
        user=logged_user[0]
        ticket_list = user.append_tickets()
        newtext = f"There are {len(ticket_list)} Flight Tickets in cart of {user.username} ({user.email}). This comes to a total price of ${user.calculate_total_price():.2f}."
        cart_screen.configure_label(newtext)
      
class ConfirmOrder(tk.Frame):
    def __init__(self, parent, controller):
        '''Constructor method to define attributes and widgets'''
        super().__init__(parent)
        #Attributes
        self.controller = controller
        sub_heading = tk.Label(self, text="Confirming order will save your receipt to a file and quit the program.\nAre you sure you want to continue?", justify = "center", wraplength=460, font=("Times", 12, "bold"),fg="black", bg=BG_COLOUR)
        #Confirmation buttons for yes and no 
        btn_yes = tk.Button(self, width=16, text = "YES", font=BUTTON_FONT, fg = "black", bg=DEFAULT, command=lambda: self.yes())
        btn_no = tk.Button(self, text = "NO", width=16, font=BUTTON_FONT, fg = "black", bg=DEFAULT, command=lambda: controller.show_frame(CartMenu))
        
        #Placing widgets on screen
        sub_heading.place(relx=0.5,rely=0.2, anchor="center")
        btn_yes.place(relx=0.7,rely=0.7, anchor="center")
        btn_no.place(relx=0.3,rely=0.7, anchor="center")

    def yes(self):
        '''Writes order to reciept file and quits program'''
        #Retrieve user
        user = logged_user[0]
        #Write recipet to a file and save tickets (and date of order)
        date_of_order = datetime.now()
        date_of_order = date_of_order.date()
        date_string = date_of_order.strftime('%Y-%m-%d')

        #Get total price
        total_price = user.calculate_total_price()

        #Create a current_order list and append user's cart 
        ordered_tickets = user.append_tickets()

        #Write receipt to a text file
        with open("order_receipt.txt", mode="w+") as file:
            #Write the header
            file.write(f"A summary of tickets ordered on {date_string} by {user.username} ({user.email}) is below:")
            
            # Write each ticket in their order to the file in a table format
            for ticket in ordered_tickets:
                # Print the display headers for each ticket and write each ticket
                for header in FLIGHT_DISPLAY_HEADERS:
                    file.write("\n" + header)
                if ticket.travel_type == "Domestic":
                    file.write(f"\n| {ticket.flight_number:<7} | {ticket.travel_type:<13} | {ticket.airline_name:<20} | {ticket.airport:<38} | {ticket.destination:<25} | {ticket.duration:>4} {'min'} | {ticket.date:<19} | ${ticket.ticket_price:<7.2f} |")
                elif ticket.travel_type == "International":
                    file.write(f"\n| {ticket.flight_number:<7} | {ticket.travel_type:<13} | {ticket.airline_name:<20} | {ticket.airport:<38} | {ticket.destination:<25} | {ticket.duration:>4} {'hrs'} | {ticket.date:<19} | ${ticket.ticket_price:<7.2f} |")
                
                # Add additional personalized details to each ticket and write it to the file
                file.write("\n" + FLIGHT_DISPLAY_HEADERS[0])
                file.write(f"\n| Name: {ticket.ticket_holder_name}")
                file.write(f"\n| Ticket Age Type: {ticket.ticket_holder_age}")
                file.write(f"\n| Cabin Class Type: {ticket.cabin_class}")
                file.write("\n" + FLIGHT_DISPLAY_HEADERS[0] + "\n")

            #Write the total price
            file.write("\n" + FLIGHT_DISPLAY_HEADERS[0])
            file.write(f"\n|Total($) |                                                                                                                                            | ${total_price:<7.2f} |")
            file.write("\n"+FLIGHT_DISPLAY_HEADERS[0])

        #Display message
        messagebox.showinfo('Information', "Order has been successfully confirmed and receipt has been saved to a file. Thank you for your order. Enjoy your flight!")
        
        #Exit the program
        self.controller.kill()

class Logout (tk.Frame):
    def __init__(self, parent, controller):
        '''Constructor method to define attributes and widgets'''
        super().__init__(parent)
        #Attributes
        self.controller = controller
        sub_heading = tk.Label(self, text="Logging out will save your cart so you can restore your cart when logging back in.\nDo you want to continue?", justify = "center", wraplength=460, font=("Times", 12, "bold"),fg="black", bg=BG_COLOUR)
        #Confirmation buttons for yes and no 
        btn_yes = tk.Button(self, width=16, text = "YES", font=BUTTON_FONT, fg = "black", bg=DEFAULT, command=lambda: self.yes())
        btn_no = tk.Button(self, text = "NO", width=16, font=BUTTON_FONT, fg = "black", bg=DEFAULT, command=lambda: controller.show_frame(MainMenu))
        
        #Placing widgets on screen
        sub_heading.place(relx=0.5,rely=0.2, anchor="center")
        btn_yes.place(relx=0.7,rely=0.7, anchor="center")
        btn_no.place(relx=0.3,rely=0.7, anchor="center")

    def yes(self):
        '''Logs user out of program and saves their cart details'''
        user = logged_user[0]

        #Append all user's data to saved_data dictionary by changing the keys
        user.saved_data["domestic"] = user.domestic_tickets
        user.saved_data["international"] = user.international_tickets

        #Pull the current account and add saved data
        for account in user_details:
            if account["email"]==user.email:
                #Add saved data
                account["data"]=user.saved_data
                break

        #Remove current user from logged user list
        user.remove_current_user()

        #Display message
        messagebox.showinfo('Information', 'Your cart has been saved. Log back in to view it.')
        
        #Direct user to login menu
        self.controller.show_frame(LoginMenu)


#Read flights from csv file and load them as a list of Flight objects.
read_flights_from_csv('international_flights.csv', international_flights, International)
read_flights_from_csv('domestic_flights.csv', domestic_flights, Domestic)          

#Run the app
app = Flight_booker_app()
app.geometry("1250x620")
app.resizable(width=False,height=False) #Ensures window dimensions can't change and the window is not resizeable
app.mainloop()