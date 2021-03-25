# import pandas as pd
# import PyPDF2
import tabula
from pathlib import Path
import datetime
import requests
import csv
import yagmail

import credentials

# get current directory
cwd = Path.cwd()

# get timestamp for log
day_timestamp = datetime.datetime.today().date()
print(str(day_timestamp))
day = str(day_timestamp)


# declare the path of your file
filename = Path.cwd() / "resources" / "covid_data.pdf"

# supply link for aquiring pdf
url = "https://www.healthvermont.gov/sites/default/files/documents/pdf/COVID19-Transmission-Schools.pdf"

# get PDF
response = requests.get(url)

# write pdf to machine
filename.write_bytes(response.content)

output = Path.cwd() / "resources" / "output.csv"
covid_csv = Path.cwd() / "resources" / "vdh_covid_update.csv"

# convert PDF into CSV file
tabula.convert_into(filename, str(output), output_format="csv", pages="all")
# read csv, and split on "," the line
csv_file = csv.reader(open(output, "r"), delimiter=",")

schools = [
    "FRANKLIN ELEMENTARY SCHOOL",
    "HIGHGATE ELEMENTARY SCHOOL",
    "SWANTON SCHOOLS",
    "MISSISQUOI VALLEY UHS #7",
]


def get_schools(schools):

    school_data = []

    # loop through the csv list
    for row in csv_file:
        for school in schools:

            # if current rows 2nd value is equal to input, print that row
            if school in row[0]:
                school_data.append(row)
                break
    print(school_data)
    return school_data


school_covid_numbers = get_schools(schools)

for school in school_covid_numbers:
    if school[0] == "MISSISQUOI VALLEY UHS #7":
        school[0] = "Missisquoi Vally Union"
    school[0] = school[0].title()


headers = ["School", "Cases Reported in the Past 7 Days", "Total Cases"]

with open(covid_csv, "w") as f:
    write = csv.writer(f)
    write.writerow(headers)
    write.writerows(school_covid_numbers)

print("done")


# setup gmail link
gmail_user = credentials.gmail_user
gmail_password = credentials.gmail_password
yag = yagmail.SMTP(gmail_user, gmail_password)

yag.send(
    "russell.gregory@mvsdschools.org",
    "data acquired " + day,
    attachments=str(covid_csv),
)
