#!/usr/bin/python3.8

#This script will send me the Top 30 Chess player rankings to my inbox on the 3rd day of each month.
#It will send as an HTML table embedded in the body of an email.
#The email provider of choice is MailJet and its API


import urllib3
urllib3.disable_warnings()
import requests, bs4
import pandas as pd
from mailjet_rest import Client


res1 = requests.get('https://www.calendardate.com/todays.htm')
res1.raise_for_status()
daySoup = bs4.BeautifulSoup(res1.text, 'html.parser')
date = daySoup.select('#ttop')
datenum = [el.text for el in date]
daySearch = '03'
test = [i for i in datenum if daySearch in i]
if len(test) > 0:
    res = requests.get('https://chess-rankings.com')
    res.raise_for_status()
    chessSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    table = chessSoup.find("table", attrs={"id": "mainRanks"})
    columns = table.find_all('th')
    column_names = [c.string for c in columns]

    table_rows = table.find_all('tr')
    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.get_text() for tr in td]
        l.append(row)

    df = pd.DataFrame(l, columns=column_names)
    df = df.drop([0]).drop(columns=['  Title   ', '  Fed   ', '  K   ']).head(30)
    df = df.to_html()
    print("An email with the rankings will be sent.")

    api_key = 'INSERT YOUR MAILJET CLIENT KEYS'
    api_secret = 'INSERT YOURMAILJET CLIENT KEYS'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "INSERT YOUR EMAIL",
                    "Name": "Chess Rankings"
                },
                "To": [
                    {
                        "Email": "INSERT YOUR EMAIL",
                        "Name": "INSERT YOUR NAME"
                    }
                ],
                "Subject": "Chess Rankings",
                "HTMLPart": "{}".format(df)
            }
        ]
    }
    result = mailjet.send.create(data=data)
else:
    print("It is not the 3rd of the month, no email will be sent.")


