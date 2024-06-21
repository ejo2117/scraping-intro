import mechanicalsoup
import pandas as pd
import sqlite3

browser = mechanicalsoup.StatefulBrowser()
browser.open("https://kworb.net/spotify/country/global_weekly_totals.html")

# extract table data
td = browser.page.find_all("td")
columns = [value.text for value in td]


split_columns = []
for idx, value in enumerate(columns):
    if idx % 7 == 0:
        [artist, title] = [x.strip() for x in value.split("-", 1)]
        split_columns.append(artist)
        split_columns.append(title)
    else:
        split_columns.append(value)


column_names = ["Artist",
                "Title", 
                "Weeks", 
                "Weeks_In_T10",
                "Peak_Position",
                "Weeks_At_Peak", 
                "Peak_Streams", 
                "Total_Streams"]

dictionary = {}
columns = split_columns

# select every 8th item
for idx, key in enumerate(column_names):
    value = columns[idx:][::len(column_names)]
    dictionary[key] = columns[idx:][::len(column_names)]

df = pd.DataFrame(data = dictionary)

# print(df.head())

# insert data into a database
connection = sqlite3.connect("spotify_weekly.db")
cursor = connection.cursor()

cursor.execute("create table spotify ( " + ",".join(column_names) + ")")
for i in range(len(df)):
    cursor.execute("insert into spotify values (?,?,?,?,?,?,?,?)", df.iloc[i])

connection.commit()

connection.close()