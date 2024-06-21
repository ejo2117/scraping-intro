import mechanicalsoup
import pandas as pd
import sqlite3

browser = mechanicalsoup.StatefulBrowser()
browser.open("https://kworb.net/spotify/country/global_weekly_totals.html")


# thing = "Artist name - song name - remix"
# nospace = [x.strip() for x in thing.split("-", 1)]
# print(nospace)

# extract table headers
# th = browser.page.find_all("td", attrs={"class": "text mp"})
# artistAndTitle = [value.text for value in th]
# artistAndTitle = artistAndTitle[:98]
# print(artistAndTitle)

# # extract table data
td = browser.page.find_all("td")
columns = [value.text for value in td]
# columns = columns[6:1084]

# f = open("test.txt", "a")
# f.write(str(columns))
# f.close()


column_names = ["Artist_And_Title", 
                "Weeks", 
                "Weeks_In_T10",
                "Peak_Position",
                "Weeks_At_Peak", 
                "Peak_Streams", 
                "Total_Streams"]

# dictionary = {"Distribution": distribution} 
dictionary = {}

# # select every 11th item
for idx, key in enumerate(column_names):
    dictionary[key] = columns[idx:][::len(column_names)]
    # dictionary["Position"] = idx

df = pd.DataFrame(data = dictionary)

# print(df.head())

# # insert data into a database
connection = sqlite3.connect("spotify_weekly.db")
cursor = connection.cursor()

cursor.execute("create table spotify ( " + ",".join(column_names) + ")")
for i in range(len(df)):
    cursor.execute("insert into spotify values (?,?,?,?,?,?,?)", df.iloc[i])

connection.commit()

connection.close()