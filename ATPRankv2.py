#!/usr/bin/python3.8

#This script will send me the Top50 ATP Tennis player rankings to my inbox every Tuesday.
#It will send as an HTML table embedded in the body of an email.
#The email provider of choice is MailJet and its API

import urllib3

urllib3.disable_warnings()

import requests, bs4
from datetime import date
import pandas as pd

if (date.today().weekday()) == 1:
    res = requests.get('https://www.espn.com/tennis/rankings')
    res.raise_for_status()
    playerSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    table = playerSoup.find("table")
    columns = table.find_all('th')
    column_names = [c.string for c in columns]

    table_rows = table.find_all('tr')
    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.get_text() for tr in td]
        l.append(row)

    df = pd.DataFrame(l, columns=column_names)
    df = df.drop([0]).head(50)
    df = df.to_html()
    print("An email will be sent.")
else:
    print("Today is not a Tuesday.")

from mailjet_rest import Client

if (date.today().weekday()) == 1:
    api_key = 'INSERT MAILJET CLIENT KEYS'
    api_secret = 'INSERT MAILJET CLIENT KEYS'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "INSERT YOUR EMAIL",
                    "Name": "ATP Rankings"
                },
                "To": [
                    {
                        "Email": "INSERT YOUR EMAIL",
                        "Name": "YOUR NAME"
                    }
                ],
                "Subject": "ATP Top50 Ranking Update",
                "HTMLPart": "{}".format(df)
            }
        ]
    }
    result = mailjet.send.create(data=data)

else:
    print("Today is not a Tuesday, no email will be sent.")
