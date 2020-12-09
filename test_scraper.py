import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint

headers = {"Accept-Language": "en-US,en;q=0.5"}

code = []
name = []
group = []
subgroup = []
category = []
subgrouplinks = []
codelinks = []

pages = [
    "/icd9/001-139/"
]

groups = [
    "infectious and parasitic diseases"
]

i = 0
j = 0
k = 0

def extract_links(page):
    #print("HREF: " + str(page))
    site = requests.get("https://dexur.com" + str(page))
    print("Current page link: https://dexur.com" + str(page))
    soup = BeautifulSoup(site.text, 'html.parser')
    table = soup.find('table', class_="table table-bordered table-striped")
    codelinks = table.find_all('a', href=True)
    
    return codelinks

def extract_table(page):
    #print("HREF: " + str(page))
    site = requests.get("https://dexur.com" + str(page))
    print("Current page table: https://dexur.com" + str(page))
    soup = BeautifulSoup(site.text, 'html.parser')
    table = soup.find('table', class_="table table-bordered table-striped")
    rows = table.find_all('td')
    codelinks = table.find_all('a', href=True)
    
    return rows


for page in pages:
  # Get Links to Subgroups
  subgroup_href = []
  subgrouplinks = extract_links(page)
  # Append links to iteratable araray
  for link in subgrouplinks:
    subgroup_href.append(link['href'])
  # Get tables from each page 
  rows_page = extract_table(page)
  # Iterate over table rows
  for row1 in rows_page:
    group_ = row1.text
    if ( i % 2 != 0): 
        print("Group: " + group_)
        group.append(group_)
    i+=1
    # Open Subgroups
    for sub in subgroup_href:
      # Get Codelinks of each Subgroup
      print("Current Subgroup: " + str(sub))
      code_href = []
      codelinks = extract_links(sub)
      # Append codelinks to iteratable array
      for codelink in codelinks:
        code_href.append(codelink['href'])
      # Get table from each page
      rows_sub = extract_table(sub)
      # Iterate over table rows
      for row2 in rows_sub:
        subgroup_ = row2.text
        # Get Links to Codes
        # Iterate over Codes of Subgroup
        for cod in code_href:
            # Get Codelinks of each Subgroup
          print("Current Codepage: " + str(cod))
          ref = []
          links = extract_links(cod)
          # Append codelinks to iteratable array
          for link in links:
            ref.append(link['href'])
          # Get table from each page
          rows_cod= extract_table(cod)



        #   rows_code = extract_table(cod)
        # for row3 in rows_code:
        #   code_ = row3.text
        #   if ( i % 2 == 0): 
        #     #print("Code: " + code_)
        #     code.append(code_)
        #   if ( i % 2 != 0):
        #     name.append(code_) 
        #     #print("Group: " + group_)
        #     #print("Subgroup: " + subgroup_)
        #     group.append(group_)
        #     subgroup.append(subgroup_)
        #       #print("Name: " + code_)
        #     i+=1

print('Subgroup refs: ' + str(subgroup_href))
print('Code refs: ' + str(code_href))

sleep(randint(2,10))  
    # Open subpages
        # # Open codepages
        # for code in codelinks:
        #     rows, links = extract_table(code)

        # for text in rows:
        #     code_ = text.text
        #     category = "test"
        #     if ( j % 2 != 0):
        #         name.append(code_)
        #         subgroup.append(subgroup_)
        #         group.append(group_)
        #         print("Name: " + code_)
        #     if ( k % 2 == 0):
        #         code.append(code_)
        #         print("Code: " + code_)
        #     k+=1
        



print(len(group))
print(len(subgroup))
icd9 = pd.DataFrame({
'sub_group': subgroup,
'group': group,
'name': name,
'code': code
})


# to see your dataframe
print(icd9)

# to see the datatypes of your columns
print(icd9.dtypes)

# to see where you're missing data and how much data is missing 
print(icd9.isnull().sum())

# to move all your scraped data to a CSV file
icd9.to_csv('icd9.csv')