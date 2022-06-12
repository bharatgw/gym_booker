from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def find_all_forms(url):
    with requests.session() as s:
        res = s.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        forms = soup.find_all("form")

    return forms

def get_form_details(form):
    details = {}

    action = form.attrs.get("action").lower()

    method = form.attrs.get("method", "get").lower()

    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")

        input_name = input_tag.attrs.get("name")

        input_value = input_tag.attrs.get("value", "")

        inputs.append({"type": input_type, "name": input_name, "value":input_value})

    for select in form.find_all("select"):
        select_name = select.attrs.get("name")

        select_type = "select"

        select_options = []

        select_default_value = ""

        for select_option in select.find_all("option"):

            option_value = select_option.attrs.get("value")

            if option_value:
                select_options.append(option_value)

                if select_option.attrs.get("selected"):
                    select_default_value = option_value
        if not select_default_value and select_options:
            select_default_value = select_options[0]
        
        inputs.append({"type" : select_type, "name": select_name, "values": select_options, "value": select_default_value})

    for textarea in form.find_all("textarea"):
        textarea_name = textarea.attrs.get("name")

        textarea_type = "textarea"

        textarea_value = textarea.attrs.get("value", "")

        inputs.append({"type": textarea_type, "name": textarea_name, "value": textarea_value})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs

    return details

def collect_inputs(form_details):
    data = {}
    
    for input_tag in form_details["inputs"]:

        if input_tag["type"] == "hidden":
            data[input_tag["name"]] = input_tag["value"]

        elif input_tag["type"] == "select":
            for i, option in enumerate(input_tag["values"], start = 1):
                if option == input_tag["value"]:
                    print(f"{i} # {option} (default)")
                else:
                    print(f"{i} # {option}")
                
                choice = input(f"Enter the option for the select field '{input_tag['name']}' (1 - {i}): ")
                
                try:
                    choice = int(choice)
                except:
                    value = input_tag["value"]
                else:
                    value = input_tag["values"][choice - 1]

            data[input_tag["name"]] = value
            
        elif input_tag["type"] != "submit":
            value = input(f"Eneter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
            data[input_tag["name"]] = value
    
    return data

def submit_form(form_details, data, url, session):
    url = urljoin(url, form_details["action"])

    if form_details["method"] == "post":
        res = session.post(url, data = data)
    elif form_details["method"] == "get":
        res = session.get(url, params = data)

    return res

def view_afterpage(res, url):
    soup = BeautifulSoup(res.content, "html.parser")
    for link in soup.find_all("link"):
        try:
            link.attrs["href"] = urljoin(url, link.attrs["href"])
        except:
            pass
    for script in soup.find_all("script"):
        try:
            script.attrs["src"] = urljoin(url, script.attrs["src"])
        except:
            pass
    for img in soup.find_all("img"):
        try:
            img.attrs["src"] = urljoin(url, img.attrs["src"])
        except:
            pass
    for a in soup.find_all("a"):
        try:
            a.attrs["href"] = urljoin(url, a.attrs["href"])
        except:
            pass

    # write the page content to a file
    with open("page.html", "w", encoding = "utf-8") as f:
        f.write(str(soup))

    return soup