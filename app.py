import mechanicalsoup
import pandas as pd
import sqlite3

browser = mechanicalsoup.StatefulBrowser()
browser.open("https://en.wikipedia.org/wiki/Comparison_of_Linux_distributions")

# extract table headers
th = browser.page.find_all("th", attrs={"class": "table-rh"})
distribution = [value.text.replace("\n", "") for value in th]
distribution = distribution[:98]

# extract table data
td = browser.page.find_all("td")
columns = [value.text.replace("\n", "") for value in td]
columns = columns[6:1084]

column_names = ["Founder", 
                "Maintainer", 
                "Initial_Release_Year", 
                "Current_Stable_Version", 
                "Security_Updates", 
                "Release_Date", 
                "System_Distribution_Commitment", 
                "Forked_From", 
                "Target_Audience", 
                "Cost", 
                "Status"]

dictionary = {"Distribution": distribution}

#select every 11th item
for idx, key in enumerate(column_names):
    dictionary[key] = columns[idx:][::len(column_names)]

df = pd.DataFrame(data = dictionary)
print(df.tail())