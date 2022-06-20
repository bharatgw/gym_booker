import datetime as dt
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from html_parsing_functions import find_all_forms, get_form_details

def main():
    # Data used to fill up the form
    inputs = {
        "eaa$TextboxName": "[your name]",
        "eaa$TextboxEmail": "[your email]",
        "eaa$el0$custom54801": "[last 4 digits of your student ID]",
        "eaa$el0$custom54388": "[your ph number]"
    }

    # Read the booking timings I'd like
    with open("timings.txt") as f:
        timings_list = f.readlines()

    print("Your gym timings are:\n")
    for i in timings_list:
        print(i)

    choice = input("(y/n): ")
    if choice == "n":
        return

    timings_dict = dict()

    for i in timings_list:
        day, timing = re.split("-", i)
        timing = re.sub("[ \n]", "", timing)
        timing = timing.split(":")[0]
        timings_dict[day] = timing

    # Find the links to the slot booking pages
    gym_url = requests.get("https://www.trumba.com/calendars/SMU_OSL_Gym.rss")
    soup = BeautifulSoup(gym_url.text, "html.parser")
    slots = soup.find_all("item")

    # Find the date for next Friday
    today = dt.date.today()
    friday = 5 - today.isoweekday()
    if friday <= 0:
        friday = today + dt.timedelta(7)
    else:
        friday = today + dt.timedelta(friday)

    # Go through the relevant slot timings to book the desired ones
    driver = webdriver.Edge()

    # Initialize dates and timing for while loop
    date = today.strftime("%B %#d %Y")
    friday = friday.strftime("%B %#d %Y")
    timing = "8"
    today = today.strftime("%B %#d %Y")

    for slot in slots:
        des = slot.description.text.split(",")
        day = des[0]
        timing = des[-1].split('-')[0].strip()
        date = (des[1] + des[2]).strip()
        if timings_dict[day] == timing and date != today:
            url = slot.find("x-trumba:ealink").text
            # Go to the relevant link for the slot and book it
            driver.get(url)

            forms = find_all_forms(url)
            form_details = get_form_details(forms[0])
            
            # Propagate the data dictionary
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "text" and re.match("eaa.*", input_tag["name"]):
                    data[input_tag["name"]] = inputs[input_tag["name"].split("_")[0]] # One of the tag names changes on every page
    
            
            # Fill out the form fields
            for name, value in data.items():
                input_field = driver.find_element(By.NAME, value = name)
                input_field.send_keys(value)

            submit = driver.find_element(By.ID, value = "eaa_ButtonOK")
            submit.click()

        if date == friday and timing == "6":
            break

    # Quit the webdriver
    driver.quit()

if __name__ == "__main__":
    main()