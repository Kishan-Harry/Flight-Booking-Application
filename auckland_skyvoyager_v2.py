#Title: FLIGHT BOOKING APPLICATION FOR ASSESSMENT VERSION 2:
#Author: Kishan Harry
#Purpose: Create a program allowing a user to book a flight ticket from Auckland Airport


#-------------------------------------------------------------------------------------------------------------------------|
#---------------------------------------------------------IMPORTS---------------------------------------------------------|
#-------------------------------------------------------------------------------------------------------------------------|

#Allows efficient reading and writing of csv files
import csv

#Relevant imports
import time
import re
from datetime import datetime


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

#___________________CUSTOM TYPE CLASSES_____________________

class Flight:
    def __init__(self, travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name):
        '''Constructor method to set attributes of flight'''  
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
        
    
    def display_flight(self, unit):
        '''Print the list of flights'''
        #Print formatted table of flights (^&< aligns the string among n characters)
        print(f"| {self.flight_number:<7} | {self.travel_type:<13} | {self.airline_name:<20} | {self.airport:<38} | {self.destination:<25} | {self.duration:>4} {unit} | {self.date:<19} | ${self.ticket_price:<7.2f} |")

    def create_ticket(self, flight, user):
        '''Instantiates a Ticket object once user's flight has been selected, 
            and calculates price of the ticket then adds to user's ticket_list'''
        while True:
            try:
                #Prints age discounts in a nice table format and asks for age of ticket recipient
                print("\n"+MENU_HEADER+f"\n| Child:  | {1-flight.child_discount:.2f}% discount |"+f"\n| Adult:  | {1-flight.adult_discount:.2f}% discount |"+f"\n| Senior: | {1-flight.senior_discount:.2f}% discount |"+"\n"+MENU_HEADER)
                recipient_age = int(input("\nEnter age of recipient ticket holder: > "))
            except ValueError:
                print("\nPlease enter a valid age.")
            else:
                #Asigns the age type to the ticket holder based on the user's inputted age
                if recipient_age < ADULT and recipient_age > 0:
                    ticket_holder_age = "Child"
                    print(f"\n{ticket_holder_age} discount applied to ticket")
                elif recipient_age >= ADULT and recipient_age < SENIOR:
                    ticket_holder_age = "Adult"
                    print(f"\n{ticket_holder_age} discount applied to ticket")
                elif recipient_age >= SENIOR and recipient_age < MAX_AGE:
                    ticket_holder_age = "Senior"
                    print(f"\n{ticket_holder_age} discount applied to ticket")
                else:
                    print("\nPlease enter a valid age.")
                    continue
                break

        while True:
            try:
                #Asks user to choose a cabin class
                print("\nPlease select a cabin class")
                #If the length of the cabin_class_types attribute (type is list) from the domestic and international flight classes (further below)
                #is 2 then this means the flight is domestic with only Economy and First Class so those multipliers will show whereas international has 
                #Business class as well
                if len(flight.cabin_class_types) == 2:
                    cabin_class_type = mode(f"1.) - First Class ${self.ticket_price*flight.first_class_multiplier:.2f}\n2.) - Economy Class ${self.ticket_price*flight.economy_class_multiplier:.2f}")
                elif len(flight.cabin_class_types) == 3:
                    cabin_class_type = mode(f"1.) - First Class ${self.ticket_price*flight.first_class_multiplier:.2f}\n2.) - Economy Class ${self.ticket_price*flight.economy_class_multiplier:.2f}\n3.) - Business Class ${self.ticket_price*flight.business_class_multiplier:.2f}")
            except:
                print("\nPlease enter the number corresponding to your choice.")
            else:
                #Assigns the cabin class type to the ticket holder based on their choice
                if cabin_class_type == 1:
                    cabin_class = "First Class"
                    print(f"{cabin_class} cabin applied to ticket")
                elif cabin_class_type == 2:
                    cabin_class = "Economy Class"
                    print(f"{cabin_class} cabin applied to ticket")
                elif cabin_class_type == 3 and cabin_class_type == len(flight.cabin_class_types):
                    cabin_class = "Business Class"
                    print(f"{cabin_class} cabin applied to ticket")
                else:
                    print("\nPlease enter the number corresponding to your choice.") 
                    continue
                break
        
        #Instantiates a ticket object with age type and cabin class type attributes
        user_ticket = Ticket(self.travel_type, self.flight_number, self.airport, self.destination, self.country, self.stopovers, self.duration, self.date, self.ticket_price, self.airline_name, cabin_class, ticket_holder_age)
        #Calculates the new price of the ticket based on their choices
        user_ticket.ticket_price = user_ticket.apply_discounts(flight)

        #Adds the ticket to the users respective ticket list
        if type(flight)==Domestic: #could also use if type(flight) == Domestic/International
            user.add_ticket(user.domestic_tickets, user_ticket)
        elif type(flight) == International:
            user.add_ticket(user.international_tickets, user_ticket)

        #Display order status
        print("\nAdding ticket to order...")
        time.sleep(0.5)
        print("\n\033[1;32;40mTicket added to order successfully\033[0;37;40m.")

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
    def __init__(self, travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name, cabin_class, ticket_holder_age):
        '''Constructor method to inherit attributes of flight'''
        super().__init__(travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name)
        self.cabin_class = cabin_class
        self.ticket_holder_age = ticket_holder_age

    def display_flight(self, unit):
        '''Inherits and overrides display flight function from Flight class'''
        #Prints the desired table format
        print_list(FLIGHT_DISPLAY_HEADERS)
        super().display_flight(unit) #Inherit method from parent class (this method will override it)
        print(FLIGHT_DISPLAY_HEADERS[0])
        print(f"| Ticket Age Type: {self.ticket_holder_age}")
        print(f"| Cabin Class Type: {self.cabin_class}")
        print(FLIGHT_DISPLAY_HEADERS[0])
    
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

        if self.cabin_class == "First Class":
            self.ticket_price *= flight.first_class_multiplier
        elif self.cabin_class == "Business Class":
            self.ticket_price *= flight.business_class_multiplier
        elif self.cabin_class == "Economy Class":
            self.ticket_price *= flight.economy_class_multiplier

        #Return ticket price
        return self.ticket_price
          
class Current_User:
    def __init__(self, username, email, password):
        '''Constructor method to define attributes'''
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

        #Access domestic and international tickets from saved_ticket dictionary

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


    def select_flight(self, flights_list):
        '''Add chosen flight to the user's order'''
        user_selecting_flight = False
        while user_selecting_flight == False:
            try:
                #Ask user to select a flight via flight number
                chosen_flight_num = input("\nEnter the flight number of the flight you wish to book: > ").strip()
            except:
                print("\nPlease try again\n")
            else:
                #Check if the flight_code is real
                for flight in flights_list:
                    if flight.flight_number == chosen_flight_num:

                        #Set the loop repeat variable to True
                        user_selecting_flight == True
                        #Creates a ticket
                        flight.create_ticket(flight, self)    
                        
                        #Asks whether they would like to continue ordering
                        continue_ordering = confirm("Would you like to order another flight (Y/N): > ")
                        return continue_ordering
                        
                #At this stage, the flight number doesn't exist therefore loop must repeat
                if user_selecting_flight == False:
                    print("\nEnter a flight number from the list please.")
                    continue
        
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

def mode(options): 
    """displays numbered mode options"""   
    #Displays options in predtermined format
    #Saves space when writing menus
    print("")
    print(MENU_HEADER)
    print(options)
    print(MENU_HEADER)
    mode = int(input("\n> "))
    return mode

def read_flights_from_csv(filename, flights_list, Travel_Type):
    '''Read list of flights from their respective csv files and instantiate 
        each flight into an object then load them into a list.'''
    
    #Opens file then creates a flight object for each row with
    #attributes matching the fieldnames
    with open(filename, mode="r") as file:
        csvreader = csv.DictReader(file)
        for row in csvreader:
            #Instantiate flight based on domestic or international
            flight_object = Travel_Type(row["travel_type"], row["flight_number"], row["airport"], row["destination"], row["country"], row["stopovers"], row["duration"], row["date"], row["price"], row["airline"])
            #Adds flight object to flights list
            flights_list.append(flight_object) 

def print_list(list):
    '''Prints list with a for loop'''
    for element in list:
        print(element)
        
def confirm(confirmation_text):
    '''Gets user to confirm with yes or no then returns True or False'''
    #Displays confirmation text then returns True for yes and False for no
    while True:
        confirmation = input(f"\n{confirmation_text}").capitalize().strip()
        if confirmation == "Y":
            return True
        elif confirmation == "N":
            return False
        else:
            print("\n\033[1;33mFailed to read confirmation\033[0;37;40m.")
            continue
    
#_________________MAIN ________________
def main():
    '''Runs the main loop of the program'''
    
    #Greet the user when they open the app
    print("\nWelcome to Auckland SkyVoyager! \nBook upcoming domestic or " 
            "international flights from Auckland Airport to suit your travel " 
            "needs.")
    
    user_exists = True
    while user_exists == True:

        #Display the login menu options
        user_logging_in = True
        while user_logging_in == True:
            user_logging_in=login_menu()

        #Pull out the current user object from the list
        current_user = logged_user[0]
    
        #Once the user has logged on, display the main menu
        user_logged_on = True
        while user_logged_on == True:
            user_logged_on=main_menu(current_user)

#------------------------------MENUS---------------------------

def login_menu():
    '''Displays login menu options and logs the user in'''

    #Menu options are displayed
    while True:
        try:
            option = mode("1.) - log in\n2.) - Create Account\n3.) - Exit")
        except ValueError:
            print("\nPlease enter either 1, 2, or 3:")
        else:
            if option == 1:
                #Run the the login function. If returned false, 
                #then function returns false back to main 
                attempted_login_result = login()
                return attempted_login_result

            elif option ==2:
                #Run the create account function which will always return false
                attempted_account_creation = create_account()
                return attempted_account_creation

            elif option ==3:
                #Asks the user to confirm whether they would like to exit the program
                #If yes, the program will quit and if no, the loop will continue and menu 
                #options will display again. A failed confirmation will redisplay menu options
                confirmation = confirm("Are you sure you want to exit? (Y/N): > ")
                if confirmation == True:
                    print("\nThank you for using Auckland SkyVoyager!")
                    quit()
                elif confirmation == False:
                    continue
            else:
                print("\nPlease enter either 1, 2, or 3:")     

def main_menu(user):
    '''Runs the 'main menu' loop of the application where user orders 
        tickets and manages their cart etc'''

    #Main menu options are displayed
    main_menu_repeat = True
    while main_menu_repeat == True:
        try:
            option = mode("1.) - Book Flight\n2.) - View Cart\n3.) - Logout(Save) ")
        except ValueError:
            print("\nPlease enter either 1, 2, or 3:")
        else:
            #Runs the book_flight function where the user can book tickets
            if option ==1:
                main_menu_repeat = book_flight(user)
            
            #Runs the view flight function where the user can view and confirm 
            #their order
            elif option ==2:
                main_menu_repeat = view_cart(user)

            elif option ==3:
                main_menu_repeat = logout(user)

            else:
                print("\nPlease enter either 1, 2, or 3:")  
    
    #Returns False
    return False 

#--------------------------BOOK FLIGHT ACTIONS----------------------

def book_flight(user):
    '''Allows user to choose from Domestic or International then carries out 
        subsequent operations'''
    user_booking_flight = True
    while user_booking_flight == True:
        try:
            #Display options
            option = mode("1.) - Domestic\n2.) - International\n3.) - Back")
        except ValueError:
            print("\nPlease enter either 1, 2, or 3:")
        else:
            if option ==1:
                #Displays the domestic flights in min
                print(f"\nHere is a list of current domestic flights from Auckland domestic Airport\n")
                display_all_flights(domestic_flights, "min")
                user_booking_flight = order_ticket(user, domestic_flights)
            
            elif option ==2:
                #Displays the international flights in hrs
                print(f"\nHere is a list of current international flights from Auckland International Airport\n")
                display_all_flights(international_flights, "hrs")
                user_booking_flight = order_ticket(user, international_flights)

            #Returning true so that main_menu loop can repeat
            elif option ==3:
                return True

            else:
                print("\nPlease enter either 1, 2, or 3:")  
    
    #Will return True when user_booking_flight is false
    return True

def display_all_flights(flights_list, duration_unit):
    '''Display the list of flights according to travel_type'''
    #Print out the headings for each column
    print_list(FLIGHT_DISPLAY_HEADERS)
    #Print out each flight
    for flight in flights_list:
        flight.display_flight(duration_unit)
    #Print out bottom line
    print(FLIGHT_DISPLAY_HEADERS[0])

def order_ticket(user, flights_list):
    '''Gets user to order a ticket and adds it to their order'''
    user_order_ticket = True
    while user_order_ticket == True:
        try:
            option = mode("1.) - Select a flight\n2.) - Back")
        except ValueError:
            print("\nPlease enter either 1, or 2:")
        else:
            if option ==1:
                #If the user has selected 1, they will run the select flight method where they will 
                #be able to create a ticket
                user_order_ticket = user.select_flight(flights_list)
            elif option ==2:
                return True
            else:
                print("\nPlease enter either 1, or 2:")
    
    #Will return false when user_order_ticket is false
    return False

#--------------------------VIEW CART ACTIONS-----------------------

def view_cart(user):
    '''Allows user to display thier tickets, edit their order or confirm their order
        returns true or false to run the main menu loop'''
    user_viewing_cart = True
    while user_viewing_cart == True:
        try:
            #Display options
            option = mode("1.) - Display Cart\n2.) - Edit Order\n3.) - Confirm Order\n4.) - Back ")
        except ValueError:
            print("\nPlease enter either 1, 2, 3 or 4:")
        else:
            if option == 1:
                user_viewing_cart = display_users_tickets(user)
            elif option ==2:
                user_viewing_cart = edit_order(user)
            elif option ==3:
                user_viewing_cart = confirm_order(user)
            elif option ==4:
                return True
            else:
                print("\nPlease enter either 1, 2, 3 or 4:")
    
    #Returns true if confirm order is false and loop has been broken
    return True

def display_users_tickets(user):
    '''Displays the users tickets form their cart'''
    #Checks if the user has any tickets at all
    if len(user.domestic_tickets) ==0 and len(user.international_tickets) ==0:
        print("\nNo pending items in your cart Please order a flight.")
        #Returns True back to loop
        return True
    else: 
        print(f"\nSummary of tickets in cart of {user.username} ({user.email}):")
        
        #Handle domestic tickets
        print_ticket(user.domestic_tickets, "min", "Domestic")
        
        #Handle international tickets
        print_ticket(user.international_tickets, "hrs", "International")
        
        #Display the total price
        total_price = user.calculate_total_price()
        print("\n"+FLIGHT_DISPLAY_HEADERS[0])
        print(f"|\033[1;32;40mTotal($)\033[0;37;40m |                                                                                                                                            | ${total_price:<7.2f} |")
        print(FLIGHT_DISPLAY_HEADERS[0])
        
        #Returns True back to loop
        return True
            
def print_ticket(ticket_list, unit, travel_type):
    '''Prints users tickets to save code repetition'''       
    
    #Checks the length of list of tickets
    if len(ticket_list)==0:
        print(f"\n\033[1;31;40mNo {travel_type} tickets to show.\033[0;37;40m")
    else:
        #Outputs the number (amount) of each type of ticket
        print(f"\n\033[1;32;40m{travel_type} Tickets:\033[0;37;40m [{len(ticket_list)}]")
        for ticket in ticket_list:
            #Outputs the index+1 of the ticket in the list to number the tickets
            print(f"\n({ticket_list.index(ticket)+1}):")
            ticket.display_flight(unit)

def edit_order(user):
    '''Allows user to edit order (remove tickets etc)'''
    #Checks if the user has any tickets at all
    if len(user.domestic_tickets) ==0 and len(user.international_tickets) ==0:
        print("\nNo pending items in your cart Please order a flight.")
        #Returns True back to loop
        return True
    
    editing_order = True
    while editing_order == True:
        try:
            #Create a list with domestic and international tickets user has ordered
            #This will also reset the list each time loop repeats
            all_tickets = user.append_tickets()

            #Display each ticket object in  table format with ticket class 
            #(overrided) display_flight method
            for ticket in all_tickets:
                print(f"\n({all_tickets.index(ticket)+1}):")
                if ticket.travel_type == "Domestic":
                    ticket.display_flight("min")
                elif ticket.travel_type == "International":
                    ticket.display_flight("hrs")
            
            #Display the total price
            total_price = user.calculate_total_price()
            print("\n"+FLIGHT_DISPLAY_HEADERS[0])
            print(f"|\033[1;32;40mTotal($)\033[0;37;40m |                                                                                                                                            | ${total_price:<7.2f} |")
            print(FLIGHT_DISPLAY_HEADERS[0])

            if len(all_tickets) ==0:
                #Redirect user to the previous menu
                print("\nCart has been emptied\nRedirecting....")
                time.sleep(1.5)
                return True
            
            #Display options
            option = mode("1.) - Remove Ticket\n2.) - Back")
            
        except ValueError:
            print("\nPlease enter either 1 or 2:")
        else:
            #Checks length of list to see if there are tickets to remove first
            if len(all_tickets)==0:
                print("\nNo tickets to remove. Please order a flight.")
                return True
            
            elif option ==1:
                #Find the length of the ticket list
                list_length = len(all_tickets)
                editing_order = remove_tickets(user, all_tickets, list_length)

            elif option ==2:
                return True
            else:
                print("\nPlease enter either 1 or 2:")
            
def remove_tickets(user, all_ticket_list, list_length):
    '''Remove the desired ticket from the user's order'''
    user_removing_ticket = True
    while user_removing_ticket == True:
        try:
            number = int(input(f"\nSelect the number of the ticket you would like to remove. (select a number from 1-{list_length}): > "))
        except ValueError:
            print(f"\nPlease enter a valid number (1-{list_length})")
        else:
            #Checks if the number inputted is 
            #greater than the boundaries (0 and length of list)
            if number <=0 or number > len(all_ticket_list):
                print(f"\nPlease enter a valid number (1-{list_length})")
            else:
                #Convert the number to the appropriate index
                ticket_list_index = number-1
                
                #Check if the ticket selected is domestic or international
                #to remove from appropriate list
                if all_ticket_list[ticket_list_index].travel_type == "Domestic":
                    user.remove_ticket(user.domestic_tickets, ticket_list_index)
                    return True
                elif all_ticket_list[ticket_list_index].travel_type == "International":
                    #In case user removes an international ticket
                    international_index = ticket_list_index - len(user.domestic_tickets)
                    user.remove_ticket(user.international_tickets, international_index)
                    return True
                else:
                    print(f"\nPlease enter a valid number (1-{list_length})")
                
def confirm_order(user):
    '''Confirms the user's order and writes the tickets to a file
        and saves them to the user's data storage and sends emailed receipt'''
    
     #Checks if the user has any tickets at all
    if len(user.domestic_tickets) ==0 and len(user.international_tickets) ==0:
        print("\nNo pending items in your cart Please order a flight.")
        #Returns True back to loop
        return True
    
    #Ask user to confirm if they want to continue
    confirm_order = confirm("Confirming order will save your receipt to a file and quit the program - are you sure you would like to continue? (Y/N): > ")
    if confirm_order == False:
        return True
    elif confirm_order == True:
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
                #Get file pointer position
                position = file.tell()
                # Print the display headers for each ticket and write each ticket
                for header in FLIGHT_DISPLAY_HEADERS:
                    file.write("\n" + header)
                if ticket.travel_type == "Domestic":
                    file.write(f"\n| {ticket.flight_number:<7} | {ticket.travel_type:<13} | {ticket.airline_name:<20} | {ticket.airport:<38} | {ticket.destination:<25} | {ticket.duration:>4} {'min'} | {ticket.date:<19} | ${ticket.ticket_price:<7.2f} |")
                elif ticket.travel_type == "International":
                    file.write(f"\n| {ticket.flight_number:<7} | {ticket.travel_type:<13} | {ticket.airline_name:<20} | {ticket.airport:<38} | {ticket.destination:<25} | {ticket.duration:>4} {'hrs'} | {ticket.date:<19} | ${ticket.ticket_price:<7.2f} |")
                
                # Add additional personalized details to each ticket and write it to the file
                file.write("\n" + FLIGHT_DISPLAY_HEADERS[0])
                file.write(f"\n| Ticket Age Type: {ticket.ticket_holder_age}")
                file.write(f"\n| Cabin Class Type: {ticket.cabin_class}")
                file.write("\n" + FLIGHT_DISPLAY_HEADERS[0] + "\n")

            #Write the total price
            file.write("\n" + FLIGHT_DISPLAY_HEADERS[0])
            file.write(f"\n|Total($) |                                                                                                                                            | ${total_price:<7.2f} |")
            file.write("\n"+FLIGHT_DISPLAY_HEADERS[0])

        #Print confirmation statement
        print(f"\n\033[1;32;40mOrder has been confirmed\033[0;37;40m and receipt has been saved to a file.\nThank you for your order.\nHave a nice trip!")
        
        #Exit the program.
        quit()
            
#--------------------------LOGOUT-----------------------------

def logout(user):
    '''Remove logged user from logged_user list and saves their cart'''
    confirmation = confirm("Logging out will save your cart so you can restore cart when logging back in. Do you want to continue (Y/N): >")
    if confirmation ==False:
        return True 
    elif confirmation == True:
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
    #Return false back to the loop
    return False

#-------------------------CREATE ACCOUNT & LOGIN------------------------------
def create_account(): 
    '''Creates account and updates csv file'''
    
    #Ask user for their information by running the following functions
    username = create_names()
    user_email = check_email()
    user_password = create_password()
    age = check_age()

    if age == True:
        #Append a dictionary with account information to user_details list
        account = {}
        account["username"]=username
        account["email"]=user_email
        account["password"] = user_password
        account["data"] = {} #Empty dictionary that will have the user's saved data after logging out
        user_details.append(account)
        print(user_details)          
        print("\n\033[1;32;40mAccount created successfully\033[0;37;40m.")
    
    return True

def create_names():
    '''Asks user for first and last name andchecks if they are valid''' 
    #'repeat_loop' is used to help break out of nested loops
    repeat_loop = True
    while repeat_loop == True:
        try:
            user_first_name = input("\nWhat is your first name?: > ")
            user_last_name = input("What is your last name?: > ")
        except:
            print("\nPlease enter a name.")
        else:
            #Checks if first name is empty or not then 
            #repeats loop if no name is entered
            if len(user_first_name)==0 or len(user_last_name)==0:
                print("\nNames cannot be empty! Please try again.")
                continue

            #Joins the user's names together into one string
            username = f"{user_first_name} {user_last_name}"

            #Checks for any invalid characters in the username 
            #then repeats loop if any invalidities are present
            repeat_loop = False
            for ch in username:
                if ch in SPECIALS or ch.isalpha():
                    continue
                else:
                    print("\nYour name contains invalid characters. Please" 
                          " try again and enter a valid name.")
                    repeat_loop = True
                    break  
    #Breaks out of the loop and Returns the username.                     
    return username

def check_email():
    '''Asks user for email address then validates and checks if 
    existing email is in accounts.csv file'''
   
    repeat_loop = True
    while repeat_loop:
        email = input("\nEnter your email address: > ") 
        # Validates the email address using the validate function.
        valid_email = validate_email(email)

        # If the email is invalid, prompt again.
        if not valid_email:
            print("\nThat email is not a valid email address, please try again.")
            continue

        # Initialize flag to check if the email already exists in account dict.
        email_exists = False
        for account in user_details:
            if account["email"]==email:
                print("\nThis email has already been taken. Please enter another email address.")
                email_exists = True
                break

        # If the email is valid and does not exist, exit the loop
        if email_exists == True:
            continue
        elif email_exists == False:
            break

    return email

def validate_email(email):
    '''Validates user's email via a regex expression'''
    #Compares email to the regex expression then returns true or false
    return bool(re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email))

def create_password():
  """verifies created password"""
  #Asks user to create a password. 
  #Password is then validated using a series of regex expressions
  while True:
    password = input("Create a password: > ")       
    if len(password) < MIN_PW_LENGTH:
        print("\nMake sure your password is at least 8 characters in length.\n")
    elif re.search('[0-9]',password) is None:
        print("\nMake sure your password has a number in it.\n")
    elif re.search('[A-Z]',password) is None: 
        print("\nMake sure your password has a capital letter in it.\n")
    elif re.search('[!@#$%^&*]',password) is None: 
        print("\nMake sure your password has a special character in it.\n")
    else:
        break
  return password

def check_age():
    #Asks the user for their age then compares with boundary case
    #If User is of eligible age then set age to true.
    repeat_loop = True
    while repeat_loop == True:
        try:
            age = int(input("Enter your age: > "))
            if age < MIN_AGE or age > MAX_AGE: 
                print("\nSorry, \033[1;31;40myou are not eligibile " 
                      "\033[0;37;40mto create an account. You must be " 
                      "at least 16 years old.")  
                #Sets age to False so the function returns False
                age = False 
                break
            else:
                #Sets age to True so the function returns True
                age = True
                break
        except ValueError:
            print("\nPlease enter a valid number.\n")
    return age

def login(): 
    """matches password to username in accounts.csv file"""

    #Maximum number of login attempts.
    attempts = ATTEMPTS
    while  attempts > 0:
        email = input("\nEnter your email address: > ")
        password = input("Enter your password: > ")
        
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
            print("\nLogging in...\n")
            time.sleep(0.6)
            print("\033[1;32;40mLogin Successful\033[0;37;40m.")
            #Returns false indicating user can process to main menu
            return False
            
        else:
            attempts = attempts-1
            print(f"Incorrect username or password. \n {attempts} attempts left")
        
        if attempts == 0:
            #Denies the current user from attempting again and redirects to login menu
            print(f"Too many failed login attempts." + "\n \033[1;31;40mLogin denied\033[0;37;40m.")
            return True
            
#Print out a loading icon to notify user that the app is working 
#and loading flights from the csv file
print("Loading....")

#Read flights from csv file and load them as a list of Flight objects.
read_flights_from_csv('international_flights.csv', international_flights, International)
read_flights_from_csv('domestic_flights.csv', domestic_flights, Domestic)          

#Call the main function for the program
main()