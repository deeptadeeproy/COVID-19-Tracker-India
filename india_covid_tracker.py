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
        count+= 1
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
        #print(err)
        print("\nError: No or bad internet connection.")
        reruns()

def arrange_address():
    # print(jsonDataOne)
    if jsonData[0]["PostOffice"]:
        print("Data received.")
        address = jsonData[0]["PostOffice"][0]["Block"] + ", " + jsonData[0]["PostOffice"][0]["District"] + ", " + \
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
        print("\nPlease wait, requesting data...")
        get_data("https://api.postalpincode.in/pincode/"+postCode)
        if success:
            arrange_address()
            get_data("https://api.covid19india.org/state_district_wise.json")
            confirmed = jsonData[state]["districtData"][district]["confirmed"]
            del jsonData
            print("Confirmed positive COVID-19 cases in your area: " + str(confirmed))
        else:
            print("\nError: Invalid pincode.")
            reruns()
    else:
        print("\nError: Invalid pincode.")
        reruns()

def status_ind():
    global jsonData
    get_data("https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise")
    if success:
        lastRefreshed = jsonData["data"]["lastRefreshed"]
        confirmed = jsonData["data"]["total"]["confirmed"]
        recovered = jsonData["data"]["total"]["recovered"]
        deaths = jsonData["data"]["total"]["deaths"]
        active = jsonData["data"]["total"]["active"]
        print(f"\nCOVID-19 status report (India) as of {lastRefreshed}\n----------\nConfirmed: {confirmed}\nRecovered: {recovered}\nDeaths: {deaths}\nActive: {active}\n----------")

def status_wor():
    global jsonData
    get_data("https://covidapi.info/api/v1/global")
    if success:
        lastRefreshed = jsonData["date"]
        confirmed = jsonData["result"]["confirmed"]
        recovered = jsonData["result"]["recovered"]
        deaths = jsonData["result"]["deaths"]
        active = confirmed -(recovered + deaths)
        print(f"\nCOVID-19 status report (World) as of {lastRefreshed}\n----------\nConfirmed: {confirmed}\nRecovered: {recovered}\nDeaths: {deaths}\nActive: {active}\n----------")

def statewise():
    global jsonData
    key = input("\nEnter state name to find report: ")
    key = key.title()
    get_data("https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise")
    if success:
        boolFound = False
        for i in range(36):
            if jsonData["data"]["statewise"][i]["state"] == key:
                boolFound = True
                confirmed = jsonData["data"]["statewise"][i]["confirmed"]
                recovered = jsonData["data"]["statewise"][i]["recovered"]
                deaths = jsonData["data"]["statewise"][i]["deaths"]
                active = jsonData["data"]["statewise"][i]["active"]
                print(f"\nCOVID-19 status report ({key}, India)")
                print(f"----------\nConfirmed: {confirmed}")
                print(f"Recovered: {recovered}")
                print(f"Deaths: {deaths}")
                print(f"Active: {active}\n----------")
        if i == 35 and boolFound == False:
            print("\nError: Wrong spelling.")

def patdataopen():
    webbrowser.open("https://docs.google.com/spreadsheets/d/e/2PACX-1vSc_2y5N0I67wDU38DjDh35IZSIS30rQf7_NYZhtYYGU1jJYT6_kDx4YpF-qw0LSlGsBYP8pqM_a1Pd/pubhtml")
    print("Redirected to web browser.")
def user_menu():
    choice = input("\nEnter an option number:-\n1. View number of cases by PIN code\n2. View India's status report\n3. View World's status report\n4. View statewise report\n5. View COVID-19 patients database- Open in browser\n\nWaiting for user input: ")
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
        else:
            print("Error: Invalid input")
            reruns()
    else:
        print("\nError: Invalid input.")
    reruns()

def clear_screen():
    if os.name == "nt":
        os.system('cls')
    elif os.name == "mac" or os.name == "mac":
        os.system('clear')

def reruns():
    trial = input("\n\nRun program again? Enter Y to continue or N to exit: ")
    if trial == "Y" or trial == "y":
        clear_screen()
        print("----------Program Start----------\nThis piece of software is developed by SUSH1C4T.\n")
        user_menu()
    elif trial == "N" or trial == "n":
        exit(0)
    else:
        print("\nError: Wrong input")
        reruns()

#Execution starts here
print("----------Program Start----------\nThis piece of software is developed by SUSH1C4T.")
user_menu()

