#Title: FLIGHT BOOKING APPLICATION FOR ASSESSMENT VERSION 1:
#Author: Kishan Harry
#Purpose: Create a program allowing a user to book a flight ticket from Auckland Airport

#-------------------------------------------------------------------------------------------------------------------------|
#---------------------------------------------------------IMPORTS---------------------------------------------------------|
#-------------------------------------------------------------------------------------------------------------------------|

import time
import re
from datetime import datetime

#-------------------------------------------------------------------------------------------------------------------------|
#--------------------------------------------------ARRAYS & CONSTANTS-----------------------------------------------------|
#-------------------------------------------------------------------------------------------------------------------------|

#List of all possible flights. Each flight is a dictionary with relevant attributes such as flight#, airline name etc
FLIGHTS = [
    {'travel_type': 'International', 'flight_number': 'ANZ1347', 'airport': 'Los Angeles International Airport', 'destination': 'Los Angeles, USA', 'country': 'USA', 'stopovers': 0, 'duration': 780, 'date': datetime(2024, 8, 15, 14, 30), 'price': 1500.50, 'airline': 'Air New Zealand'},
    {'travel_type': 'International', 'flight_number': 'QF2653', 'airport': 'Sydney Kingsford Smith Airport', 'destination': 'Sydney, Australia', 'country': 'Australia', 'stopovers': 0, 'duration': 210, 'date': datetime(2024, 9, 10, 10, 15), 'price': 500.00, 'airline': 'Qantas'},
    {'travel_type': 'International', 'flight_number': 'JAL4592', 'airport': 'Haneda Airport', 'destination': 'Tokyo, Japan', 'country': 'Japan', 'stopovers': 1, 'duration': 900, 'date': datetime(2024, 10, 5, 22, 45), 'price': 1200.75, 'airline': 'Japan Airlines'},
    {'travel_type': 'International', 'flight_number': 'SIA1839', 'airport': 'Changi Airport', 'destination': 'Singapore, Singapore', 'country': 'Singapore', 'stopovers': 0, 'duration': 600, 'date': datetime(2024, 11, 20, 18, 0), 'price': 950.25, 'airline': 'Singapore Airlines'},
    {'travel_type': 'International', 'flight_number': 'EMR3842', 'airport': 'Dubai International Airport', 'destination': 'Dubai, UAE', 'country': 'UAE', 'stopovers': 1, 'duration': 1020, 'date': datetime(2024, 12, 1, 7, 20), 'price': 1750.40, 'airline': 'Emirates'},
    {'travel_type': 'International', 'flight_number': 'BA2857', 'airport': 'Heathrow Airport', 'destination': 'London, UK', 'country': 'UK', 'stopovers': 1, 'duration': 1280, 'date': datetime(2024, 8, 25, 16, 55), 'price': 1900.85, 'airline': 'British Airways'},
    {'travel_type': 'International', 'flight_number': 'AA4921', 'airport': 'John F. Kennedy International Airport', 'destination': 'New York, USA', 'country': 'USA', 'stopovers': 0, 'duration': 1020, 'date': datetime(2024, 9, 15, 6, 10), 'price': 1600.35, 'airline': 'American Airlines'},
    {'travel_type': 'International', 'flight_number': 'JAL1398', 'airport': 'Narita International Airport', 'destination': 'Tokyo, Japan', 'country': 'Japan', 'stopovers': 0, 'duration': 870, 'date': datetime(2024, 10, 20, 12, 25), 'price': 1100.50, 'airline': 'Japan Airlines'},
    {'travel_type': 'International', 'flight_number': 'CPA1934', 'airport': 'Hong Kong International Airport', 'destination': 'Hong Kong, China', 'country': 'China', 'stopovers': 0, 'duration': 660, 'date': datetime(2024, 11, 5, 21, 40), 'price': 1300.60, 'airline': 'Cathay Pacific'},
    {'travel_type': 'International', 'flight_number': 'KAL2721', 'airport': 'Incheon International Airport', 'destination': 'Seoul, South Korea', 'country': 'South Korea', 'stopovers': 0, 'duration': 780, 'date': datetime(2024, 12, 15, 9, 0), 'price': 1400.70, 'airline': 'Korean Air'},
    {'travel_type': 'International', 'flight_number': 'ANZ2437', 'airport': 'Los Angeles International Airport', 'destination': 'Los Angeles, USA', 'country': 'USA', 'stopovers': 1, 'duration': 820, 'date': datetime(2024, 8, 20, 15, 45), 'price': 1550.80, 'airline': 'Air New Zealand'},
    {'travel_type': 'International', 'flight_number': 'QF3342', 'airport': 'Sydney Kingsford Smith Airport', 'destination': 'Sydney, Australia', 'country': 'Australia', 'stopovers': 0, 'duration': 210, 'date': datetime(2024, 9, 30, 13, 10), 'price': 510.00, 'airline': 'Qantas'},
    {'travel_type': 'International', 'flight_number': 'JAL9823', 'airport': 'Haneda Airport', 'destination': 'Tokyo, Japan', 'country': 'Japan', 'stopovers': 1, 'duration': 950, 'date': datetime(2024, 10, 14, 17, 50), 'price': 1210.75, 'airline': 'Japan Airlines'},
    {'travel_type': 'International', 'flight_number': 'SIA4598', 'airport': 'Changi Airport', 'destination': 'Singapore, Singapore', 'country': 'Singapore', 'stopovers': 0, 'duration': 610, 'date': datetime(2024, 11, 22, 20, 10), 'price': 960.25, 'airline': 'Singapore Airlines'},
    {'travel_type': 'International', 'flight_number': 'EMR7624', 'airport': 'Dubai International Airport', 'destination': 'Dubai, UAE', 'country': 'UAE', 'stopovers': 1, 'duration': 1030, 'date': datetime(2024, 12, 5, 8, 25), 'price': 1760.40, 'airline': 'Emirates'},
    {'travel_type': 'International', 'flight_number': 'BA5628', 'airport': 'Heathrow Airport', 'destination': 'London, UK', 'country': 'UK', 'stopovers': 1, 'duration': 1290, 'date': datetime(2024, 8, 30, 18, 0), 'price': 1910.85, 'airline': 'British Airways'},
    {'travel_type': 'International', 'flight_number': 'AA8712', 'airport': 'John F. Kennedy International Airport', 'destination': 'New York, USA', 'country': 'USA', 'stopovers': 0, 'duration': 1030, 'date': datetime(2024, 9, 18, 11, 20), 'price': 1610.35, 'airline': 'American Airlines'},
    {'travel_type': 'International', 'flight_number': 'JAL4753', 'airport': 'Narita International Airport', 'destination': 'Tokyo, Japan', 'country': 'Japan', 'stopovers': 0, 'duration': 880, 'date': datetime(2024, 10, 25, 14, 35), 'price': 1110.50, 'airline': 'Japan Airlines'},
    {'travel_type': 'International', 'flight_number': 'CPA9483', 'airport': 'Hong Kong International Airport', 'destination': 'Hong Kong, China', 'country': 'China', 'stopovers': 0, 'duration': 670, 'date': datetime(2024, 11, 8, 23, 50), 'price': 1310.60, 'airline': 'Cathay Pacific'},
    {'travel_type': 'International', 'flight_number': 'KAL6521', 'airport': 'Incheon International Airport', 'destination': 'Seoul, South Korea', 'country': 'South Korea', 'stopovers': 0, 'duration': 790, 'date': datetime(2024, 12, 18, 7, 10), 'price': 1410.70, 'airline': 'Korean Air'},
    {'travel_type': 'International', 'flight_number': 'ANZ1784', 'airport': 'Los Angeles International Airport', 'destination': 'Los Angeles, USA', 'country': 'USA', 'stopovers': 1, 'duration': 830, 'date': datetime(2024, 8, 22, 16, 55), 'price': 1560.80, 'airline': 'Air New Zealand'},
    {'travel_type': 'International', 'flight_number': 'QF9843', 'airport': 'Sydney Kingsford Smith Airport', 'destination': 'Sydney, Australia', 'country': 'Australia', 'stopovers': 0, 'duration': 220, 'date': datetime(2024, 9, 22, 12, 20), 'price': 520.00, 'airline': 'Qantas'},
    {'travel_type': 'International', 'flight_number': 'JAL5321', 'airport': 'Haneda Airport', 'destination': 'Tokyo, Japan', 'country': 'Japan', 'stopovers': 1, 'duration': 960, 'date': datetime(2024, 10, 17, 18, 55), 'price': 1220.75, 'airline': 'Japan Airlines'},
    {'travel_type': 'International', 'flight_number': 'SIA3948', 'airport': 'Changi Airport', 'destination': 'Singapore, Singapore', 'country': 'Singapore', 'stopovers': 0, 'duration': 620, 'date': datetime(2024, 11, 24, 21, 20), 'price': 970.25, 'airline': 'Singapore Airlines'},
    {'travel_type': 'International', 'flight_number': 'EMR4982', 'airport': 'Dubai International Airport', 'destination': 'Dubai, UAE', 'country': 'UAE', 'stopovers': 1, 'duration': 1040, 'date': datetime(2024, 12, 7, 10, 30), 'price': 1770.40, 'airline': 'Emirates'},
    {'travel_type': 'International', 'flight_number': 'BA7628', 'airport': 'Heathrow Airport', 'destination': 'London, UK', 'country': 'UK', 'stopovers': 1, 'duration': 1300, 'date': datetime(2024, 9, 1, 19, 5), 'price': 1920.85, 'airline': 'British Airways'},
    {'travel_type': 'International', 'flight_number': 'AA4723', 'airport': 'John F. Kennedy International Airport', 'destination': 'New York, USA', 'country': 'USA', 'stopovers': 0, 'duration': 1040, 'date': datetime(2024, 9, 21, 12, 25), 'price': 1620.35, 'airline': 'American Airlines'},
    {'travel_type': 'International', 'flight_number': 'JAL9238', 'airport': 'Narita International Airport', 'destination': 'Tokyo, Japan', 'country': 'Japan', 'stopovers': 0, 'duration': 890, 'date': datetime(2024, 10, 28, 15, 40), 'price': 1120.50, 'airline': 'Japan Airlines'},
    {'travel_type': 'International', 'flight_number': 'CPA4932', 'airport': 'Hong Kong International Airport', 'destination': 'Hong Kong, China', 'country': 'China', 'stopovers': 0, 'duration': 680, 'date': datetime(2024, 11, 11, 1, 0), 'price': 1320.60, 'airline': 'Cathay Pacific'},
    {'travel_type': 'International', 'flight_number': 'KAL9432', 'airport': 'Incheon International Airport', 'destination': 'Seoul, South Korea', 'country': 'South Korea', 'stopovers': 0, 'duration': 800, 'date': datetime(2024, 12, 21, 8, 15), 'price': 1420.70, 'airline': 'Korean Air'},
    {'travel_type': 'International', 'flight_number': 'ANZ5938', 'airport': 'Los Angeles International Airport', 'destination': 'Los Angeles, USA', 'country': 'USA', 'stopovers': 1, 'duration': 840, 'date': datetime(2024, 8, 24, 18, 0), 'price': 1570.80, 'airline': 'Air New Zealand'},
    {'travel_type': 'International', 'flight_number': 'QF5639', 'airport': 'Sydney Kingsford Smith Airport', 'destination': 'Sydney, Australia', 'country': 'Australia', 'stopovers': 0, 'duration': 230, 'date': datetime(2024, 9, 25, 14, 30), 'price': 530.00, 'airline': 'Qantas'},
    {'travel_type': 'International', 'flight_number': 'JAL8639', 'airport': 'Haneda Airport', 'destination': 'Tokyo, Japan', 'country': 'Japan', 'stopovers': 1, 'duration': 970, 'date': datetime(2024, 10, 30, 20, 45), 'price': 1230.75, 'airline': 'Japan Airlines'},
    {'travel_type': 'International', 'flight_number': 'SIA4837', 'airport': 'Changi Airport', 'destination': 'Singapore, Singapore', 'country': 'Singapore', 'stopovers': 0, 'duration': 630, 'date': datetime(2024, 11, 27, 22, 30), 'price': 980.25, 'airline': 'Singapore Airlines'},
    {'travel_type': 'International', 'flight_number': 'EMR4329', 'airport': 'Dubai International Airport', 'destination': 'Dubai, UAE', 'country': 'UAE', 'stopovers': 1, 'duration': 1050, 'date': datetime(2024, 12, 10, 11, 35), 'price': 1780.40, 'airline': 'Emirates'},
    {'travel_type': 'International', 'flight_number': 'BA2837', 'airport': 'Heathrow Airport', 'destination': 'London, UK', 'country': 'UK', 'stopovers': 1, 'duration': 1310, 'date': datetime(2024, 9, 3, 20, 10), 'price': 1930.85, 'airline': 'British Airways'},
    {'travel_type': 'International', 'flight_number': 'AA4929', 'airport': 'John F. Kennedy International Airport', 'destination': 'New York, USA', 'country': 'USA', 'stopovers': 0, 'duration': 1050, 'date': datetime(2024, 9, 23, 13, 35), 'price': 1630.35, 'airline': 'American Airlines'},
    {'travel_type': 'International', 'flight_number': 'JAL9348', 'airport': 'Narita International Airport', 'destination': 'Tokyo, Japan', 'country': 'Japan', 'stopovers': 0, 'duration': 900, 'date': datetime(2024, 11, 1, 16, 45), 'price': 1130.50, 'airline': 'Japan Airlines'},
    {'travel_type': 'International', 'flight_number': 'CPA4239', 'airport': 'Hong Kong International Airport', 'destination': 'Hong Kong, China', 'country': 'China', 'stopovers': 0, 'duration': 690, 'date': datetime(2024, 11, 14, 2, 10), 'price': 1330.60, 'airline': 'Cathay Pacific'},
    {'travel_type': 'International', 'flight_number': 'KAL8327', 'airport': 'Incheon International Airport', 'destination': 'Seoul, South Korea', 'country': 'South Korea', 'stopovers': 0, 'duration': 810, 'date': datetime(2024, 12, 23, 9, 20), 'price': 1430.70, 'airline': 'Korean Air'},
    {'travel_type': 'International', 'flight_number': 'ANZ1938', 'airport': 'Los Angeles International Airport', 'destination': 'Los Angeles, USA', 'country': 'USA', 'stopovers': 1, 'duration': 850, 'date': datetime(2024, 8, 26, 19, 10), 'price': 1580.80, 'airline': 'Air New Zealand'},
    {'travel_type': 'International', 'flight_number': 'QF8943', 'airport': 'Sydney Kingsford Smith Airport', 'destination': 'Sydney, Australia', 'country': 'Australia', 'stopovers': 0, 'duration': 240, 'date': datetime(2024, 9, 28, 15, 40), 'price': 540.00, 'airline': 'Qantas'},
    {'travel_type': 'International', 'flight_number': 'JAL3482', 'airport': 'Haneda Airport', 'destination': 'Tokyo, Japan', 'country': 'Japan', 'stopovers': 1, 'duration': 980, 'date': datetime(2024, 11, 3, 21, 55), 'price': 1240.75, 'airline': 'Japan Airlines'},
    {'travel_type': 'International', 'flight_number': 'SIA2374', 'airport': 'Changi Airport', 'destination': 'Singapore, Singapore', 'country': 'Singapore', 'stopovers': 0, 'duration': 640, 'date': datetime(2024, 11, 30, 23, 40), 'price': 990.25, 'airline': 'Singapore Airlines'},
    {'travel_type': 'International', 'flight_number': 'EMR4987', 'airport': 'Dubai International Airport', 'destination': 'Dubai, UAE', 'country': 'UAE', 'stopovers': 1, 'duration': 1060, 'date': datetime(2024, 12, 13, 12, 40), 'price': 1790.40, 'airline': 'Emirates'},
    {'travel_type': 'International', 'flight_number': 'BA3948', 'airport': 'Heathrow Airport', 'destination': 'London, UK', 'country': 'UK', 'stopovers': 1, 'duration': 1320, 'date': datetime(2024, 9, 5, 21, 20), 'price': 1940.85, 'airline': 'British Airways'},
    {'travel_type': 'International', 'flight_number': 'AA5839', 'airport': 'John F. Kennedy International Airport', 'destination': 'New York, USA', 'country': 'USA', 'stopovers': 0, 'duration': 1060, 'date': datetime(2024, 9, 25, 14, 45), 'price': 1640.35, 'airline': 'American Airlines'},
    {'travel_type': 'International', 'flight_number': 'SIA2841', 'airport': 'Changi Airport', 'destination': 'Singapore, Singapore', 'country': 'Singapore', 'stopovers': 0, 'duration': 620, 'date': datetime(2024, 12, 10, 20, 30), 'price': 1000.00, 'airline': 'Singapore Airlines'},
    {'travel_type': 'International', 'flight_number': 'QF2235', 'airport': 'Sydney Kingsford Smith Airport', 'destination': 'Sydney, Australia', 'country': 'Australia', 'stopovers': 0, 'duration': 210, 'date': datetime(2024, 12, 15, 11, 45), 'price': 520.00, 'airline': 'Qantas'}
]

#lists of flight objects
flight_objects = []

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
DEFAULT_MULTIPLIER= float(1.00)

class Flight:
    def __init__(self, travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name):
        '''Constructor method to set attributes of flight''' 
        #Define attributes of each flight 
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
        self.child_discount = DEFAULT_CHILD_DISCOUNT
        self.adult_discount = DEFAULT_MULTIPLIER
        self.senior_discount = DEFAULT_SENIOR_DISCOUNT

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
                #If input is invalid (ie; inputs string instead of integer), case is handled
                print("\nPlease enter a valid age.")
            
            else:
                #Asigns the age type to the ticket holder based on the user's inputted age and prints notification
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

        #Instantiates a ticket object with age type and cabin class type attributes
        user_ticket = Ticket(self.travel_type, self.flight_number, self.airport, self.destination, self.country, self.stopovers, self.duration, self.date, self.ticket_price, self.airline_name, ticket_holder_age)
        #Calculates the new price of the ticket based on their choices
        user_ticket.ticket_price = user_ticket.apply_discounts(flight)
        #Adds ticket to the user's order list
        user.add_ticket(user.tickets, user_ticket)

        #Display order status
        print("\nAdding ticket to order...")
        time.sleep(0.5)
        print("\n\033[1;32;40mTicket added to order successfully\033[0;37;40m.")

class Ticket(Flight):
    def __init__(self, travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name, ticket_holder_age):
        '''Constructor method to inherit attributes of flight'''
        super().__init__(travel_type, flight_number, airport, destination, country, stopovers, duration, date, ticket_price, airline_name)
        #Set a ticket_holder name attribute
        self.ticket_holder_age = ticket_holder_age

    def display_flight(self, unit):
        '''Inherits and overrides display flight function from Flight class'''
        #Prints the desired table format
        print_list(FLIGHT_DISPLAY_HEADERS)
        super().display_flight(unit) #Inherit method from parent class (this method will override it)
        print(FLIGHT_DISPLAY_HEADERS[0])
        print(f"| Ticket Age Type: {self.ticket_holder_age}")
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
        
        #Retruns ticket price
        return self.ticket_price
        
class Current_User:
    def __init__(self, username, email, password):
        '''Constructor method to define attributes'''
        #Set the username, password and email attributes
        self.username = username
        self.password = password
        self.email = email

        #lists to hold domestic and international ticket objects
        self.tickets = []
        
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
        #Append all tickets to the list as individual tickets
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

        #Increment the price to the total price
        for ticket in self.tickets:
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

def instantiate_flights(flights_list):
    '''Instantie each flight from dictionary then instantiate them into flight objects 
        then load them into a list.'''
    
    #Convert flight dictionary into a list of flight objects
    for flight in FLIGHTS:
        # Convert datetime object to string
        date = flight['date'].strftime('%Y-%m-%d %H:%M:%S')
        flight_object = Flight(flight["travel_type"], flight["flight_number"], flight["airport"], flight["destination"], flight["country"], flight["stopovers"], flight["duration"], date, flight["price"], flight["airline"])
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
            option = mode("1.) - Book Flight\n2.) - View Cart\n3.) - Logout")
        except ValueError:
            print("\nPlease enter either 1, 2, or 3:")
        else:
            #Runs the book_flight function where the user can book tickets
            if option ==1:
                main_menu_repeat = book_flight(user)
            
            #Runs the view flight function where the user can view and confirm 
            # their order
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
    '''Allows user to choose from flights then carries out 
        subsequent operations'''
    while True:
        #Displays the domestic flights in min
        print(f"\nHere is a list of current  flights from Auckland Airport\n")
        display_all_flights(flight_objects, "hrs")
        #Run the select flight method where they will 
        #be able to create a ticket
        user_order_ticket = user.select_flight(flight_objects)

        if user_order_ticket == True:
            continue
        elif user_order_ticket == False:
            #Will return True when user_booking_flight is false
            return True
            
def display_all_flights(flights_list, duration_unit):
    '''Display the list of flights'''
    #Print out the headings for each column
    print_list(FLIGHT_DISPLAY_HEADERS)
    #Print out each flight
    for flight in flights_list:
        flight.display_flight(duration_unit)
    #Print out bottom line
    print(FLIGHT_DISPLAY_HEADERS[0]) #display

#--------------------------VIEW CART ACTIONS-----------------------

def view_cart(user):
    '''Displays the users tickets form their cart'''
    #Checks if the user has any tickets at all
    if len(user.tickets) ==0:
        print("\nNo pending items in your cart Please order a flight.")
        #Returns True back to loop
        return True
    else: 
        print(f"\nSummary of tickets in cart of {user.username} ({user.email}):")
        
        #Handle tickets
        print_ticket(user.tickets, "hrs", "International")
        
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

#--------------------------LOGOUT-----------------------------

def logout(user):
    '''Remove logged user from logged_user list and saves their cart'''
    confirmation = confirm("Logging out will exit you from the program. Do you want to continue (Y/N): >")
    if confirmation ==False:
        return True 
    elif confirmation == True:
        #Remove current user from logged user list and quit the program
        user.remove_current_user()
        print("\nThank you for using Auckland SkyVoyager!\nEnjoy your trip!")
        print("\nQuitting the program...")
        time.sleep(1.0)
        quit()

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
  password = input("Create a password: > ")       
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
    """matches password to username in accounts dictionary"""
    while  True:
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
            
            #Sets the current user
            user.set_current_user()
            print("\nLogging in...\n")
            time.sleep(0.6)
            print("\033[1;32;40mLogin Successful\033[0;37;40m.")
            #Returns false indicating user can process to main menu
            return False
        
        else:
            print(f"Incorrect username or password. \nPlease try again.")
        
            
#Print out a loading icon to notify user that the app is working 
#and loading flights from the csv file
print("Loading....")

#Read flights from dictionaryd load them as a list of Flight objects.
instantiate_flights(flight_objects)
       
#Call the main function for the program
main()