import requests
from bs4 import BeautifulSoup
import json


works = [
    # [
    #     "https://docs.opencv.org/4.7.0/d2/de8/group__core__array.html",
    #     "tools/scrape/scraped_docs/core_array.json",
    #     "tools/scrape/scraped_docs/enum_core_array.py"
    # ],
    # [
    #     "https://docs.opencv.org/4.7.0/d8/d6a/group__imgcodecs__flags.html",
    #     "tools/scrape/scraped_docs/imgcodecs_flags.json",
    #     "tools/scrape/scraped_docs/enum_imgcodecs_flags.py"
    # ],
    # [
    #     "https://docs.opencv.org/4.7.0/d4/d15/group__videoio__flags__base.html",
    #     "tools/scrape/scraped_docs/videoio_flags.json",
    #     "tools/scrape/scraped_docs/enum_videoio_flags.py"
    # ],
    # [
    #      "https://docs.opencv.org/4.7.0/d7/d1b/group__imgproc__misc.html",
    #      "tools/scrape/scraped_docs/imgproc_misc.json",
    #      "tools/scrape/scraped_docs/enum_imgproc_misc.py"
    # ],
    # [
    #     "https://docs.opencv.org/4.7.0/da/d54/group__imgproc__transform.html",
    #      "tools/scrape/scraped_docs/imgproc_transform.json",
    #      "tools/scrape/scraped_docs/enum_imgproc_transform.py"
    # ],
]

for work in works:
    URL = work[0]
    json_filename = work[1]
    enum_filename = work[2]
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    job_elements = soup.find_all("div", class_="memitem")

    js_content = {}
    enum_content = {}

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
        enums_python = {}
        for enum_element in enum_elements:
            enum_title = None
            description_element = None

            try:
                enum_title = enum_element.find("td", class_="fieldname")
                enum_title = enum_title.text.strip()
                enum_title = enum_title[:enum_title.rfind("Python: cv.") - 1]
                enum_python = f'cv2.{enum_title}'
            except:
                pass

            try:
                description_element = enum_element.find("td", class_="fielddoc").text.strip()
            except:
                pass

            if bool(enum_title):
                enums_python.update({enum_title: enum_python})
                enums.update({enum_title: description_element})

        if bool(title_element) and bool(enums):
            enumerator = {"description": desc, "enumerator": enums}
            js_content.update({title_element: enumerator})
            enum_content.update({title_element: enums_python})

    with open(json_filename, "w") as fp:
        json.dump(js_content, fp, indent=4)

    with open(enum_filename, "w") as file1:
        file1.write("import cv2" + "\n"*3)
        dictItemCount1 = len(enum_content)
        dictPosition1 = 1
        for enum_title, enum in enum_content.items():
            file1.write(f'{enum_title} = ' + '{\n')
            dictItemCount2 = len(enum)
            dictPosition2 = 1
            for en, py in enum.items():
                file1.write(f'    "{en}": {py}')
                if not dictPosition2 == dictItemCount2:
                    file1.write(",")
                file1.write("\n")
                dictPosition2 += 1

            file1.write("}\n")
            if not dictPosition1 == dictItemCount1:
                file1.write("\n")
            dictPosition1 += 1