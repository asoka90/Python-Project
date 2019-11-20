import sqlite3
import os
import time
import sys
import getpass

#Open db
conn = sqlite3.connect('systemDB.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS customer_records (
    [CUSTOMER NO.] INTEGER PRIMARY KEY AUTOINCREMENT
                           NOT NULL,
    NAME           TEXT    NOT NULL,
    CONTACTS       TEXT    NOT NULL,
    MONTH          INTEGER NOT NULL,
    DATE           INTEGER NOT NULL,
    VENUE          TEXT    NOT NULL,
    PACKAGE        TEXT    NOT NULL,
    BILL           INTEGER NOT NULL,
    BALANCE        INTEGER DEFAULT [0]
                           NOT NULL,
    STATUS         TEXT    NOT NULL,
    ISSUED         TEXT    NOT NULL
)
''')
#Month Names
month_names = ["Jan", "Feb", "March", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]

#loading animation
def loading_bar():
        for i in range(5):
                sys.stdout.write("\rPlease wait. Loading [{0}]".format("." * (i * 1)))
                sys.stdout.flush()
                time.sleep(0.5)
        os.system("cls")

#view record
def read():
        print("Date format - mm/dd")
        cur.execute('''SELECT [CUSTOMER NO.], NAME, CONTACTS, MONTH || '/' ||  DATE, PACKAGE, VENUE, BILL, BALANCE, STATUS, ISSUED FROM customer_records ''')
        rows = cur.fetchall()
        header = ["Customer no.", "Name", "Contact", "Date of Event", "Package", "Venue", "Total Bill", "Balance","Status", "Date Issued"]
        data = list()
        for i in rows:
                data.append(i)
        
        row_format ="{:<15}" * (len(header) + 1)
        print(row_format.format("", *header))
        for team, row in zip(data, data):
            print(row_format.format("", *row))

        input("Press enter key to Exit")
        
def checkData(month, date):
        cur.execute('''SELECT * FROM dateAvailability ''')
        rows = cur.fetchall()
        date = date - 1
        return rows[date][month]

def add_record():
        
        valid = False
        while valid == False:
                print("*To exit just enter '0'")
                valid_name = False
                valid_contact = False
                valid_venue = False
                valid_package = False
                valid_chc = False
                valid_check = False
                
                #Get Name
                while valid_name == False:
                        name = input("Enter name of customer: ")
                        name = name.capitalize()
                        if name == "0":
                                return
                        if name == "" or len(name) <= 4 or name.isspace() == True:
                                print("This field required more than 4 letters.")
                                continue
                        elif all(x.isspace() or x.isalpha() for x in name):
                                valid_name = True
                        else:
                                print("Invalid name.")
                                
                #Get Contact
                while valid_contact == False:
                        contact = input("Enter contact of customer: ")
                        if contact == "0":
                                return
                        if contact =="" or  len(contact) <= 5 or len(contact) >11: 
                                print("This field required more than 5 digits and less than 11 digits.")
                                continue
                        elif all(x.isdigit() for x in contact) and contact.isspace() == False:
                                valid_contact = True
                        else:
                                print("Invalid contact")
                
                #Month with Date availability checker
                while valid_check == False:
                        valid_month = False
                        valid_date = False
                        while valid_month == False:
                                try:
                                        month_of_event = int(input("Enter the month of the event<1-12>: "))
                                        if month_of_event == 0:
                                                return
                                        if month_of_event > 0 and month_of_event <= 12:
                                                valid_month = True
                                        else:
                                                print("You entered an invalid month! Try again.", '\n')
                                                time.sleep(2)
                                                continue
                                except ValueError:
                                        print("error")
                                        
                        #Date with availability checker
                        while valid_date == False:
                                try:
                                        date_of_event = int(input("Enter date of the event<1-31>: "))
                                        if date_of_event == 0:
                                                return
                                        if date_of_event > 0 and date_of_event <= 31:
                                                if month_of_event == 2 and (date_of_event <= 0 or date_of_event > 28 ):
                                                        print("Invalid date for February")
                                                        continue
                                                elif (month_of_event == 4 or month_of_event == 6 or month_of_event == 9 or month_of_event == 11) and (date_of_event <= 0 or date_of_event > 30 ):
                                                        print("Invalid date for this month.")
                                                        continue
                                                else:
                                                        valid_date = True
                                        else:
                                                print("You entered an invalid date! Try again.", '\n')
                                                time.sleep(2)
                                                continue
                                except ValueError:
                                        print("Error")
                        
                        check = checkData(month_of_event, date_of_event)
                        if check >= 2:
                                print("\nDate not available\n")
                                time.sleep(1)
                        else:
                                valid_check = True
                #Venue
                while valid_venue == False:
                        venue = input("Enter venue of customer: ")
                        if venue == "0":
                                return
                        if venue == "" or len(venue) <= 3 or venue.isspace() == True:
                                print("This field required more than 3 letters.")
                                continue
                        elif all(x.isspace() or x.isalpha() for x in venue):
                                valid_venue = True
                        else:
                                print("Invalid venue.")
                #Package
                while valid_package == False:
                        package = input("\nChoose from this package:\nPackage A = ₱1500\nPackage B = ₱4000\nPackage C = ₱7000\nWhat is your choice? ")
                        if package == "0":
                                return
                        package = package.upper()
                        A = "A"
                        B = "B"
                        C = "C"
                        if package.casefold() == A.casefold() or package.casefold() == B.casefold() or package.casefold() == C.casefold():
                                                #Total bill
                                if package.lower() == A.lower():
                                        bill = 1500
                                if package.lower() == B.lower():
                                        bill = 4000
                                if package.lower() == C.lower():
                                        bill = 7000
                                valid_package = True
                        elif package == "":
                                valid_package = False
                                print("\nInvalid choice. Enter again.", "\r")
                        else:
                                print("\nInvalid choice. Enter again.", "\r")
        
                while valid_chc == False:       
                        chc = input("Final? Y/N (0 to exit): ")
                        if chc == 'Y' or chc == 'y':
                                cur.execute('''INSERT INTO customer_records (
                                 NAME,
                                 CONTACTS,
                                 MONTH,
                                 DATE,
                                 VENUE,
                                 PACKAGE,
                                 BILL,
                                 BALANCE,
                                 STATUS,
                                 ISSUED
                             )
                             VALUES (
                                 ?,
                                 ?,
                                 ?,
                                 ?,
                                 ?,
                                 ?,
                                 ?,
                                 ?,
                                 'TENTATIVE',
                                 date('now')
                             ) ''', (name, contact, month_of_event, date_of_event, venue, package, bill, bill))
                                conn.commit()
                                month = month_names[month_of_event - 1]
                                cur.execute('''UPDATE dateAvailability SET '''+month+''' = '''+month+''' + 1 WHERE Date = ?''', (date_of_event,))
                                conn.commit()
                                print("\n\nSuccessful... Thank you.")
                                time.sleep(1)
                                valid_chc = True
                                valid = True
                                os.system('cls')
                        elif chc == 'N' or chc == 'n':
                                print("Reset data...")
                                time.sleep(1.5)
                                os.system("cls")
                                valid_chc = True
                        elif chc == "0":
                                print("Going back to Main Menu...")
                                time.sleep(1.5)
                                os.system("cls")
                                valid_chc = True
                                return
                        else:
                                print("Invalid choice.")
                                time.sleep(1.5)

#Edit Info
def edit_info():
        valid = False
        Y = "Y"
        N = "N"
        
        valid = False
        while valid == False:
                cur.execute("SELECT NAME, CONTACTS, MONTH, DATE, VENUE, PACKAGE, BILL, BALANCE, STATUS, ISSUED FROM customer_records")
                rows = cur.fetchall()

                #Get names
                names = list()
                for data in rows:
                        names.append(data[0].lower())

                searchName = input("Search customer name(0 to exit): ")
                time.sleep(0.75)
                os.system('cls')
                if searchName == "0":
                        print("Thank you.")
                        time.sleep(1)
                        return
                if searchName.lower() in names:
                        print("Searching...")
                        valid_1 = False
                        while valid_1 == False:
                                for k in rows:
                                        if k[0].lower() == searchName.lower():
                                                print("Name: " + k[0])
                                                print("Contacts: " + k[1])
                                                print("Date of event: " + str(k[2]) + "/" + str(k[3]))
                                                print("Venue: "+ k[4])
                                                print("Package: "+ k[5])
                                                print("Bill: ₱"+ str(k[6]))
                                                print("Balance: ₱"+ str(k[7]))
                                                print("Status: "+ k[8])
                                                print("Date Issued: "+ k[9])

                                                chc = input("Edit this customer info? Y/N: ")
                                                if chc.casefold() == Y.casefold():
                                                        valid_chc = False
                                                        while valid_chc == False:
                                                                valid_contact = False
                                                                valid_venue = False
                                                                #Contact
                                                                while valid_contact == False:
                                                                        contact = input("Enter contact of customer: ")
                                                                        if contact == "" or  len(contact) <= 5 or len(contact) > 11:
                                                                                print("This field required more than 5 digits and less than 11 digits.")
                                                                                continue
                                                                        elif all(x.isdigit() for x in contact) and contact.isspace() == False:
                                                                                valid_contact = True
                                                                        else:
                                                                                print("Invalid contact")

                                                                #Venue
                                                                while valid_venue == False:
                                                                        venue = input("Enter venue: ")
                                                                        if venue == "" or len(venue) <= 3 or venue.isspace() == True:
                                                                                print("This field required more than 3 letters.")
                                                                                continue
                                                                        elif all(x.isspace() or x.isalpha() for x in venue):
                                                                                valid_venue = True
                                                                        else:
                                                                                print("Invalid venue.")
                                                                
                                                                chc = input("Is this final? Y/N: ")
                                                                if chc.casefold() == Y.casefold():
                                                                        print("Okay please wait... ")
                                                                        time.sleep(0.5)
                                                                        print("Done")
                                                                        cur.execute('''UPDATE customer_records SET CONTACTS = ?, VENUE = ? WHERE NAME = ?''', (contact, venue, k[0]))
                                                                        conn.commit()
                                                                        os.system("cls")
                                                                        valid_chc = True
                                                                        valid_1 = True
                                                                elif chc.casefold() == N.casefold():
                                                                        print("Okay please wait... \n\nPreparing...")
                                                                        time.sleep(0.5)
                                                                else:
                                                                        print("Incorrect choice")
                                                                        
                                                elif chc.casefold() == N.casefold():
                                                        print("Okay please wait... \n\n")
                                                        time.sleep(0.5)
                                                        os.system('cls')
                                                        valid_1 = True
                                                else:
                                                        print("Incorrect choice")
                elif searchName.lower() not in names:                        
                        print("Customer not found")
                        valid_else = True
                        while valid_else == True:
                                chc = input("Do you want to try again? Y/N ")
                                if chc.casefold() == Y.casefold():
                                        print("Okay please wait... ")
                                        time.sleep(0.5)
                                        valid_else = False
                                        os.system("cls")
                                elif chc.casefold() == N.casefold():
                                        print("Okay please wait... \n\nThank You.")
                                        time.sleep(0.5)
                                        os.system("cls")
                                        return
                                else:
                                        print("\nIncorrect choice")
                else:
                        print("Incorrect choice")
#Payment
def payment():
        Y = "Y"
        N = "N"

        valid = False
        while valid == False:
                cur.execute("SELECT NAME, MONTH, DATE, PACKAGE, BILL, BALANCE, STATUS, ISSUED, [CUSTOMER NO.] FROM customer_records")
                rows = cur.fetchall()
                 #Get names
                names = list()
                for data in rows:
                        names.append(data[0].lower())
                searchName = input("Search customer name(0 to exit): ")
                if searchName == "0":
                        print("Thank you.")
                        time.sleep(1)
                        os.system('cls')
                        return
                if searchName.lower() in names:
                        valid_1 = False
                        while valid_1 == False:
                                os.system("cls")
                                for k in rows:
                                        if k[0].lower() == searchName.lower():
                                                print("Name: " + k[0])
                                                print("Date of event: " + str(k[1]) + "/" + str(k[2]))
                                                print("Package: "+ k[3])
                                                print("Bill: ₱"+ str(k[4]))
                                                print("Balance: ₱"+ str(k[5]))
                                                print("Status: "+ k[6])
                                                print("Date Issued: "+ k[7])
                                                chc = input("Is this the customer? Y/N: ")
                                                if chc.casefold() == Y.casefold():                                                                                                        
                                                        valid_payment = False
                                                        while valid_payment == False:
                                                                try:
                                                                        if k[6] == "TENTATIVE" or k[6] == "RESERVED":
                                                                                payment = float(input("Minimum of ₱700 for the reservation\nEnter amount of payment: "))
                                                                                payment = round(payment, 2)       
                                                                                if payment >= 700 and payment < k[5]:
                                                                                        valid_choice = False
                                                                                        while valid_choice == False:
                                                                                                choice = input("\nAre you sure? Y/N: ")
                                                                                                if choice.lower() == Y.lower():
                                                                                                        print("Wait....")
                                                                                                        time.sleep(0.5)                                                                                                        
                                                                                                        total = k[5] - payment                                                                                                        
                                                                                                        total = max(0, total)
                                                                                                        change = abs(k[5] - payment)
                                                                                                        cur.execute('''UPDATE customer_records SET BALANCE = ? WHERE [CUSTOMER NO.] = ?''', (total, k[8]))
                                                                                                        conn.commit()
                                                                                                        print("Payment successful!.\nYour change is: 0.00")                                                                                                                                                        
                                                                                                        input("\n\nPress any key to return")
                                                                                                        valid_choice = True
                                                                                                        os.system('cls')
                                                                                                elif choice.lower() == N.lower():
                                                                                                        print("Okay please wait...")
                                                                                                        time.sleep(0.5)                                                                                                        
                                                                                                        valid_choice = True
                                                                                                        os.system('cls')
                                                                                                else:
                                                                                                        print("Invalid choice!")
                                                                                        valid_payment = True
                                                                                        valid_1 = True
                                                                                elif payment >= k[5]:
                                                                                        valid_choice = False
                                                                                        while valid_choice == False:
                                                                                                choice = input("\nAre you sure? Y/N: ")
                                                                                                if choice.lower() == Y.lower():
                                                                                                        print("Wait....")
                                                                                                        time.sleep(0.5)                                                                                                        
                                                                                                        total = k[5] - payment                                                                                                        
                                                                                                        total = max(0, total)
                                                                                                        change = abs(k[5] - payment)
                                                                                                        cur.execute('''UPDATE customer_records SET BALANCE = ? WHERE [CUSTOMER NO.] = ?''', (total, k[8]))
                                                                                                        conn.commit()
                                                                                                        print("Payment successful!.\nYour change is: " + str(change))
                                                                                                        input("\n\nPress any key to return")
                                                                                                        valid_choice = True
                                                                                                        os.system('cls')                                                                                                        
                                                                                                elif choice.lower() == N.lower():
                                                                                                        print("Okay please wait...")
                                                                                                        time.sleep(0.5)                                                                                                
                                                                                                        valid_choice = True
                                                                                                        os.system('cls')
                                                                                                else:
                                                                                                        print("Invalid choice!")
                                                                                        valid_payment = True
                                                                                        valid_1 = True
                                                                                else:
                                                                                        print("\nInsufficient amount.")
                                                                                        time.sleep(0.5)                                                                                                                                                              
                                                                        else:
                                                                                print("\nCustomer " + k[0] + " is already paid.")
                                                                                valid_payment = True
                                                                                valid_1 = True
                                                                except ValueError:
                                                                        print("\nMust be an integer!")
                                                                        time.sleep(0.5)
                                                elif chc.casefold() == N.casefold():
                                                                        print("Okay please wait...")
                                                                        time.sleep(0.5)
                                                                        valid_1 = True
                                                                        os.system('cls')
                                                else:
                                                        print("Incorrect choice")
                                                        time.sleep(0.5)                                                        
                elif searchName.lower() not in names:
                        print("Customer not found")
                        valid_else = True
                        while valid_else == True:
                                chc = input("Do you want to try again? Y/N ")
                                if chc.casefold() == Y.casefold():
                                        print("Okay please wait... ")
                                        time.sleep(0.5)
                                        valid_else = False
                                        os.system("cls")
                                elif chc.casefold() == N.casefold():
                                        print("Okay please wait... \n\nThank You.")
                                        time.sleep(0.5)
                                        os.system("cls")
                                        return
                                else:
                                        print("\nIncorrect choice")
                else:
                        print("Incorrect")
## Cancellation
def cancellation():
        Y = "Y"
        N = "N"
        

        valid = False
        while valid == False:
                cur.execute("SELECT NAME, MONTH, DATE, PACKAGE, BILL, BALANCE, STATUS, ISSUED, [CUSTOMER NO.] FROM customer_records")
                rows = cur.fetchall()

                #Get names
                names = list()
                for data in rows:
                        names.append(data[0].lower())
                os.system('cls')
                searchName = input("Search customer name(0 to exit): ")
                if searchName == "0":
                        print("Thank you.")
                        time.sleep(1)
                        return
                if searchName.lower() in names:
                        valid_1 = False
                        while valid_1 == False:
                                for k in rows:
                                        if k[0].lower() == searchName.lower():
                                                print("Name: " + k[0])
                                                print("Date of event: " + str(k[1]) + "/" + str(k[2]))
                                                print("Package: "+ k[3])
                                                print("Bill: ₱"+ str(k[4]))
                                                print("Balance: ₱"+ str(k[5]))
                                                print("Status: "+ k[6])
                                                print("Date Issued: "+ k[7])
                                                chc = input("Is this the customer? Y/N: ")
                                                if chc.casefold() == Y.casefold():                                                                                                        
                                                        valid_payment = False
                                                        while valid_payment == False:
                                                                try:
                                                                        if k[6] == "TENTATIVE" or k[6] == "RESERVED":
                                                                                choice = input("\nDo you want cancel your reservation Y/N: ")                                                                                                                                                                                                                
                                                                                if choice.lower() == Y.lower():
                                                                                        print("Wait....")
                                                                                        time.sleep(0.5)                                                                                                                                                                                
                                                                                        cur.execute('''UPDATE customer_records SET PACKAGE = "VOID" WHERE [CUSTOMER NO.] = ?''', (k[8],))
                                                                                        conn.commit()
                                                                                        month = month_names[k[1] - 1]
                                                                                        cur.execute('''UPDATE dateAvailability SET '''+month+''' = '''+month+''' - 1 WHERE Date = ?''', (k[2],))
                                                                                        conn.commit()
                                                                                        print("Cancellation successful!.\n")
                                                                                        valid_choice = True
                                                                                        valid_1 = True
                                                                                        input("\n\nPress any key to return")
                                                                                        os.system('cls')
                                                                                        valid_payment = True
                                                                                        valid_1 = True
                                                                                elif choice.lower() == N.lower():
                                                                                        print("Okay please wait...")
                                                                                        time.sleep(0.5)
                                                                                        valid_payment = True
                                                                                        valid_1 = True
                                                                                        os.system('cls')
                                                                                else:
                                                                                        print("Invalid choice!")                                                                                        
                                                                                        time.sleep(0.5)
                                                                                        os.system('cls')
                                                                        else:
                                                                                print("\nCustomer " + k[0] + " is already paid or reserved. Must be tentative to be cancelled")
                                                                                valid_payment = True
                                                                                valid_1 = True
                                                                                os.system('cls')
                                                                except ValueError:
                                                                        print("\nMust be an integer!")
                                                                        time.sleep(0.5)
                                                elif chc.casefold() == N.casefold():
                                                                        print("Okay please wait...")
                                                                        time.sleep(0.5)
                                                                        valid_1 = True
                                                                        os.system('cls')
                                                else:
                                                        print("Incorrect choice")
                                                        time.sleep(0.5)                                                        
                elif searchName.lower() not in names:
                        print("Customer not found")
                        valid_else = True
                        while valid_else == True:
                                chc = input("Do you want to try again? Y/N ")
                                if chc.casefold() == Y.casefold():
                                        print("Okay please wait... ")
                                        time.sleep(0.5)
                                        valid_else = False
                                        os.system("cls")
                                elif chc.casefold() == N.casefold():
                                        print("Okay please wait... \n\nThank You.")
                                        time.sleep(0.5)
                                        os.system("cls")
                                        return
                                else:
                                        print("\nIncorrect choice")
                else:
                        print("Incorrect")
                         
#main
if __name__ == "__main__":
        #STARTUP CHECK DATABASE
        #Check if paid
        cur.execute('''UPDATE customer_records
                SET STATUS = 'PAID'
                WHERE BALANCE = 0''')
        conn.commit()
        #Check if reserved
        cur.execute('''UPDATE customer_records
                SET STATUS = 'RESERVED'
                WHERE BALANCE <= (BILL - 700)''')
        conn.commit()
        #Chack if tentative
        cur.execute('''UPDATE customer_records
                SET STATUS = 'TENTATIVE'
                WHERE BALANCE = BILL''')
        conn.commit()

        conn.execute('''UPDATE customer_records SET PACKAGE = "C" WHERE PACKAGE = "c" ''')
        conn.commit()
        valid_main = False
        valid_user = False
        valid_passw = False
        
        while valid_user == False:
                user = getpass.getpass("Enter user: ")
                passw = getpass.getpass("Enter password: ")
                if user == "" or passw == "" or len(user) < 4 or len(passw) < 4:
                        print("User and password required more than 4 characters.")
                elif user == 'admin' and passw == 'admin':
                        print("Access Granted.")
                        valid_user = True
                else:
                        print("Incorrect try again")
                time.sleep(1.5)
                os.system('cls')
                
                
        while valid_main == False:
                try:
                        os.system('cls')
                        chc = int(input("Menu:\n1. Add record\n2. Update Customer Information\n3. Payment and Cancellation\n4. View Records\n0. Exit\n\n*No deletion of date. Cancel the order then add the customer again.\n\nChoice: "))                     
                        time.sleep(0.5)
                        os.system('cls')
                                
                        if chc == 1:
                                loading_bar()
                                add_record()
                        elif chc == 2:
                                loading_bar()
                                edit_info()
                        elif chc == 3:
                                loading_bar()
                                valid = False
                                while valid == False:
                                        try:
                                                chc = int(input("1. Payment\n2. Cancel reservation\n0. Exit\n\nEnter choice: "))
                                                if chc == 0:
                                                        print("Exiting...")
                                                        valid = True
                                                        time.sleep(0.5)
                                                elif chc == 1:
                                                        os.system('cls')
                                                        payment()
                                                elif chc == 2:
                                                        os.system('cls')
                                                        cancellation()
                                                else:
                                                        print("Invalid choice!")
                                        except ValueError:
                                                print("Invalid choice!")
                        elif chc == 4:
                                loading_bar()
                                read()
                        elif chc == 0:
                                print("Thank you")
                                time.sleep(1.5)
                                conn.close()
                                quit()
                        else:
                                print("Incorrect choice!")
                                time.sleep(1)
                except ValueError:
                        print("Incorrect choice!")
                        time.sleep(1)
