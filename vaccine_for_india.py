'''
========================================================================================================================================
Program Name	: vaccine_for_india.py
Description	    : This process gets the details for Vaccination information from co-win portal.
Input		    : N/A
Ouput           : N/A
Author		    : Pratik Saxena
======================================================================================
============================== MODIFICATION HISTORY============================
  DATE(MM-DD-YYYY)      PROGRAMMER                       MODIFICATION
======================================================================================
  04-05-2021            Pratik Saxena        Initial Version
======================================================================================
'''

import requests,json
import smtplib, ssl
import csv
from datetime import timedelta, date, datetime

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
from_address  = "xyz@gmail.com"  # Enter your address
password = "xyz"
now = datetime.now()


EndDate = (date.today() + timedelta(days=1)).strftime("%d-%m-%Y")

print("process started at {}".format(now))
#URL to get from co-win Public API , update the URL based on location
url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=363&date={}".format(EndDate)

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)
pretty_json = json.loads(response.text)
mail_flag = 0
for func in pretty_json["sessions"]:
    # This will filter for centre which are allowing 18+ 
    if func["min_age_limit"] < 45:
        mail_flag = 1

        print("Center name:{}".format(func["name"]))
        print("Center address:{}".format(func["address"]))
        print("district:{}".format(func["district_name"]))
        print("block:{}".format(func["block_name"]))
        print("pincode:{}".format(func["pincode"]))
        print("date of availability:{}".format(func["date"]))
        print("available:{}".format(func["available_capacity"]))
        print("Min age:{}".format(func["min_age_limit"]))
        print("End of details \n")

        name = ("Center name:{}".format(func["name"]))
        address = ("Center address:{}".format(func["address"]))
        district = ("district:{}".format(func["district_name"]))
        block = ("block:{}".format(func["block_name"]))
        pincode = ("pincode:{}".format(func["pincode"]))
        date = ("date of availability:{}".format(func["date"]))
        availability = ("available:{}".format(func["available_capacity"]))
        age = ("Min age:{}".format(func["min_age_limit"]))
        end  = ("End of details \n")


        message = """\
            Subject: Covid Vaccine Pune detail 18+

            {0},
            {1},
            {2},
            {3},
            {4},
            {5},
            {6},
            {7},""".format(name,address,district,block,pincode,date,availability,age,end)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(from_address, password)
            with open("email_list.csv") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for name, email, grade in reader:
                    server.sendmail(
                        from_address,
                        email,
                        message.format(name=name, grade=grade),
                    )

then = datetime.now()

print("process ended at {}".format(then))