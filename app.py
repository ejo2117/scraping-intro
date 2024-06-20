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
print(columns)