import json
import os
import webbrowser
import urllib.request
import urllib.error

# Globals
success = False
jsonData = ""
state = ""
district = ""


def countDigit(n):
    count = 0
    while n != 0:
        n //= 10
        count += 1
    return count


# Function Definitions
def get_data(url):
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            global success
            global jsonData
            success = True
            jsonData = json.loads(response.read())
        else:
            print("\nError: Data not received, unknown failure occurred.")
            reruns()
    except urllib.error.URLError as err:
        print(err)
        print("\nError: Could not connect to internet.")
        reruns()


def arrange_address():
    # print(jsonDataOne)
    if jsonData[0]["PostOffice"]:
        print("Data received.")
        address = jsonData[0]["PostOffice"][0]["Block"] + ", " + jsonData[0]["PostOffice"][0][
            "District"] + ", " +\
                  jsonData[0]["PostOffice"][0]["State"]
        print(f"\nYou searched for {address}.")
        del address
        global state
        global district
        state = jsonData[0]["PostOffice"][0]["State"]
        district = jsonData[0]["PostOffice"][0]["District"]
    else:
        print("\nError: Invalid pincode.")
        reruns()


def for_area():
    global jsonData
    postCode = input("\nEnter PIN code: ")
    if type(postCode) == int:
        postCode = str(postCode)
    if postCode.isnumeric() and len(postCode) == 6:
        print("\nPlease wait... Requesting data...")
        get_data("https://api.postalpincode.in/pincode/" + postCode)
        if success:
            arrange_address()
            get_data("https://api.covid19india.org/state_district_wise.json")
            confirmed = jsonData[state]["districtData"][district]["confirmed"]
            del jsonData
            print(f"CONFIRMED POSITIVE COVID-19 CASES IN THE SEARCHED AREA: {confirmed}")
        else:
            print("\nError: Invalid pincode.")
            reruns()
    else:
        print("\nError: Invalid pincode.")
        reruns()


def status_ind():
    global jsonData
    print("\nPlease wait... Requesting data...")
    get_data("https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise")
    if success:
        lastRefreshed = jsonData["data"]["lastRefreshed"]
        confirmed = jsonData["data"]["total"]["confirmed"]
        recovered = jsonData["data"]["total"]["recovered"]
        deaths = jsonData["data"]["total"]["deaths"]
        active = jsonData["data"]["total"]["active"]
        print(f'''
COVID-19 STATUS REPORT (INDIA) AS OF {lastRefreshed}
----------
Confirmed: {confirmed}
Recovered: {recovered}
Deaths: {deaths}
Active: {active}
----------''')


def status_wor():
    global jsonData
    print("\nPlease wait... Requesting data...")
    get_data("https:covidapi.info/api/v1/global")
    if success:
        lastRefreshed = jsonData["date"]
        confirmed = jsonData["result"]["confirmed"]
        recovered = jsonData["result"]["recovered"]
        deaths = jsonData["result"]["deaths"]
        active = confirmed - (recovered + deaths)
        print(f'''
COVID-19 STATUS (WORLD) AS OF {lastRefreshed}
----------
Confirmed: {confirmed}
Recovered: {recovered}
Deaths: {deaths}
Active: {active}
----------''')


def statewise():
    global jsonData
    key = input("\nEnter name of state or union territory: ")
    print("\nPlease wait... Requesting data...")
    get_data("https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise")
    if success:
        boolFound = False
        for i in range(len(jsonData["data"]["statewise"])):
            if jsonData["data"]["statewise"][i]["state"].title() == key.title():
                key = jsonData["data"]["statewise"][i]["state"]
                boolFound = True
                confirmed = jsonData["data"]["statewise"][i]["confirmed"]
                recovered = jsonData["data"]["statewise"][i]["recovered"]
                deaths = jsonData["data"]["statewise"][i]["deaths"]
                active = jsonData["data"]["statewise"][i]["active"]
                print(f"\nCOVID-19 STATUS REPORT ({key.upper()}, INDIA)")
                print(f"----------\nConfirmed: {confirmed}")
                print(f"Recovered: {recovered}")
                print(f"Deaths: {deaths}")
                print(f"Active: {active}\n----------")
        if i == 35 and boolFound == False:
            print("\nError: Wrong spelling.")


def patdataopen():
    webbrowser.open("docs.google.com/spreadsheets/d/e/2PACX-1vSc_2y5N0I67wDU38DjDh35IZSIS30rQf7_NYZhtYYGU1jJYT6_kDx4YpF-qw0LSlGsBYP8pqM_a1Pd/pubhtml")
    print("Redirected to web browser...")


def help_num():
    global jsonData
    jsonData = {
        "Andhra Pradesh" : "08662410978",
        "Arunachal Pradesh" : "9436055743",
        "Assam" : "6913347770",
        "Bihar" : "104",
        "Chhattisgarh" : "104",
        "Goa" : "104",
        "Gujarat" : "104",
        "Haryana" : "8558893911",
        "Himachal Pradesh" : "104",
        "Jharkhand" : "104",
        "Karnataka" : "104",
        "Kerala" : "04712552056",
        "Madhya Pradesh" : "104",
        "Maharashtra" : "02026127394",
        "Manipur" : "3852411668",
        "Meghalaya" : "108",
        "Mizoram" : "102",
        "Nagaland" : "7005539653",
        "Odisha" : "9439994859",
        "Punjab" : "104",
        "Rajasthan" : "01412225624",
        "Sikkim" : "104",
        "Tamil Nadu" : "04429510500",
        "Telangana" : "104",
        "Tripura" : "03812315879",
        "Uttarakhand" : "104",
        "Uttar Pradesh" : "18001805145",
        "West Bengal" : "1800313444222",
        "Andaman And Nicobar Islands" : "03192232102",
        "Chandigarh" : "9779558282",
        "Dadra And Nagar Haveli" : "104",
        "Daman And Diu" : "104",
        "Delhi" : "01122307145",
        "Jammu And Kashmir" : "01912520982",
        "Ladakh" : "01982256462",
        "Lakshadweep" : "104",
        "Puducherry" : "104"
    }
    
    key = input("Enter name of state or union territory: ")
    print("\nPlease wait... Looking up data...")
    if key.title() in jsonData.keys():
        print(f"\n\nHELPLINE NUMBER FOR {key.title().upper()}, INDIA: {jsonData[key.title()]}")
    else:
        print(f"\n\nError: Wrong spelling")
    del jsonData


def user_menu():
    choice = input('''
Enter an option number:-
        
1. View number of cases by PIN code
2. View India's status report
3. View World's status report
4. View statewise report
5. View COVID-19 patients database -Open in browser
6. Search helpline number (statewise)

Waiting for user input: '''
    )

    if choice:
        if type(choice) == int:
            choice = str(choice)

        if choice == "1":
            clear_screen()
            for_area()
        elif choice == "2":
            clear_screen()
            status_ind()
        elif choice == "3":
            clear_screen()
            status_wor()
        elif choice == "4":
            clear_screen()
            statewise()
        elif choice == "5":
            clear_screen()
            patdataopen()
        elif choice == "6":
            clear_screen()
            help_num()
        else:
            print("Error: Invalid input")
            reruns()
    else:
        print("\nError: Invalid input.")
    reruns()


def clear_screen( ):
    if os.name == "nt":
        os.system('cls')
    elif os.name == "posix" or os.name == "linux":
        os.system('clear')


def reruns():
    ans = input("\n\nRun program again? Enter Y to continue or N to exit: ")
    if ans == "Y" or ans == "y":
        clear_screen()
        print("----------Program Start----------\nThis piece of software is developed by deeptadeeproy.\n")
        user_menu()
    elif ans == "N" or ans == "n":
        exit(0)
    else:
        print("\nError: Wrong input")
        reruns()


# Execution starts here
print("----------Program Start----------\nThis piece of software is developed by deeptadeeproy.")
user_menu()
