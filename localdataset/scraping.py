
import requests
from bs4 import BeautifulSoup
import pandas as pd


def getRelationships(url): 
    # Get the page

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    try: 

        # Get the table div 
        table_div = soup.find('div', id='ff-dating-history-table')

        # Get the table
        table = table_div.find('table')

        # Get the table data
        table_data = table.find_all('tr')


        all_info = []

        for tag in table_data: 
            info = []
            for this_tag in tag: 
                word = this_tag.text.strip()
                filter = ''.join([chr(i) for i in range(1, 32)])
                x = word.translate(str.maketrans('', '', filter))
                info.append(x)
            all_info.append(info)


        length = len(all_info[0])

        relationships = []

        for row in all_info[1:]:
            name = row[1]
            relationship_type = row[2] # ENcounter, Relationship, Unknown, Married
            is_rumor = (row[3] == 'R') # Yes, No
            began = row[4]
            ended = row[5]
            length = row[6]

            dic = {"name" : name, "relationship_type" : relationship_type, "is_rumor" : is_rumor, "began" : began, "ended" : ended, "length" : length}
            relationships.append(dic)

        return relationships
    
    except: 
        return None

   

    

#table_div = soup.find('div' , {'id': 'ff-dating-history-table', 'name': 'ff-dating-history-table' })