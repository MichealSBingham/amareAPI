
import requests
from bs4 import BeautifulSoup
import pandas as pd




def getLink(fromTags):
    for tag in fromTags:
        x = tag.find('a')
        if x is not None:
            return x['href']
    return None  

        
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
            tags = []
            for this_tag in tag:
                
                tags.append(this_tag)
                
                word = this_tag.text.strip()
                filter = ''.join([chr(i) for i in range(1, 32)])
                x = word.translate(str.maketrans('', '', filter))
                info.append(x)
                
            
            info.append(tags)
            #print(f"info: {info}")
            all_info.append(info)


        #length = len(all_info[0])

        relationships = []

        for row in all_info[1:]:
            
            name = row[1]
            relationship_type = row[2] # ENcounter, Relationship, Unknown, Married
            is_rumor = (row[3] == 'R') # Yes, No
            began = row[4]
            ended = row[5]
            length = row[6]
            urlTo = getLink(row[-1])

            dic = {"name" : name, "relationship_type" : relationship_type, "is_rumor" : is_rumor, "began" : began, "ended" : ended, "length" : length, "url": urlTo}
            relationships.append(dic)

        

        
        
        return relationships

    except: 
        return None



def getRelationshipsbroken(url): 
    # Get the page

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    urlToPartner = None

    try: 

        # Get the table div 
        table_div = soup.find('div', id='ff-dating-history-table')

        # Get the table
        table = table_div.find('table')

        # Get the table data
        table_data = table.find_all('tr')

        all_info = []


        for tag in table_data:
            print("\n\n\n\n")
            tags_for_row = tag.find_all('td')
            thisInfo = [] 
            for this_tag in tags_for_row:

                word = this_tag.text.strip()
                filter = ''.join([chr(i) for i in range(1, 32)])
                text = word.translate(str.maketrans('', '', filter))  # text for this tag ..


                thisInfo.append(text)
                
                pass 

        
    
    except: 
        return None

   

    

#table_div = soup.find('div' , {'id': 'ff-dating-history-table', 'name': 'ff-dating-history-table' })