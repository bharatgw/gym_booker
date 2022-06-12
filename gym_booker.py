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
        "eaa$TextboxName": "Bharat",
        "eaa$TextboxEmail": "bharatg.2020@economics.smu.edu.sg",
        "eaa$el0$custom54801": "4660",
        "eaa$el0$custom54388": "88732752"
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

    # Find the number of slot booking links to go through to find the relevant ones
    nslotsday = 6
    nslots = max(5 - dt.date.weekday(dt.date.today()) * nslotsday, 5*nslotsday)

    # Go through the relevant slot timings to book the desired ones
    driver = webdriver.Edge()

    for slot in slots[0:nslots]:
        des = slot.description.text.split(",")
        day = des[0]
        timing = des[-1].split('-')[0].strip()
        if timings_dict[day] == timing:
            url = slot.find("x-trumba:ealink").text
            print(url)

            # Go to the relevant link for the slot and book it
            driver.get(url)

            forms = find_all_forms(url)
            form_details = get_form_details(forms[0])
            
            # Propagate the data dictionary
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "text" and re.match("eaa.*", input_tag["name"]):
                    data[input_tag["name"]] = inputs[input_tag["name"].split("_")[0]] # One of the tag names changes on every page
                
                # Ignore hidden tags
            
            # Fill out the form fields
            for name, value in data.items():
                input_field = driver.find_element(By.NAME, value = name)
                input_field.send_keys(value)

            submit = driver.find_element(By.ID, value = "eaa_ButtonOK")
            submit.click()

    # Quit the webdriver
    driver.quit()

if __name__ == "__main__":
    main()