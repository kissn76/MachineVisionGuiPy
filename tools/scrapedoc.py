import requests
from bs4 import BeautifulSoup
import json

URL = "https://docs.opencv.org/4.7.0/d8/d6a/group__imgcodecs__flags.html#ga61d9b0126a3e57d9277ac48327799c80"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

job_elements = soup.find_all("div", class_="memitem")

js_content = {}

for job_element in job_elements:
    title_element = None

    try:
        title_element = job_element.find("td", class_="memname")
        title_element = title_element.text.strip()
        title_element = title_element[title_element.rfind(":") + 1:]
    except:
        pass

    desc = ""
    try:
        desc = job_element.select("div.memdoc > p:nth-child(2)")[0]
        desc = desc.text.strip()
    except:
        pass

    enum_elements = job_element.find_all("tr")
    enums = {}
    for enum_element in enum_elements:
        enum_title = None
        description_element = None

        try:
            enum_title = enum_element.find("td", class_="fieldname")
            enum_title = enum_title.text.strip()
            enum_title = enum_title[:enum_title.rfind("Python: cv.") - 1]
        except:
            pass

        try:
            description_element = enum_element.find("td", class_="fielddoc").text.strip()
        except:
            pass

        if bool(enum_title):
            enums.update({enum_title: description_element})

    if bool(title_element):
        enumerator = {"description": desc, "enumerator": enums}
        js_content.update({title_element: enumerator})

with open("imgcodecs_flags.json", "w") as fp:
    json.dump(js_content, fp, indent=4)