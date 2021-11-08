import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

page = requests.get('https://www.basketball-reference.com/leagues/NBA_2022.html')
soup = BeautifulSoup(page.text, 'html.parser')

d = {}

for i in str(soup).split('\n'):
    if '<caption>' in i:

        cat = ""
        head = ""
        
        
        # get headers
        for k in i.split('</th>'):

            #get specific table type
            if "caption" in k:
                
                try:
                    temp1 = k[k.index('id=')+4:]
                    cat = temp1[:temp1.index('"')]
                except:
                    pass
            
        # get stats
        for j in i.split('</td>'):
            
            if j[-1] == '>':
                try:
                    
                    temp = j[j.index('html">')+6:]
                    temp = temp[:temp.index('<')].strip()
                    
                    if temp not in master_dict:
                        master_dict[temp] = {}
                    row.append(temp)
                        
                except:
                    pass
                
            else:
                
                try:
                    stat = j[j.index('t="')+3:]
                    
                    tempstat = stat[:stat.index('>')-1]
                    
                    if tempstat not in d:
                        d[tempstat] = {}
                        
                    if temp not in d[tempstat]:
                        d[tempstat][temp] = -1
                        
                    try:
                        if d[tempstat][temp] == -1:
                            d[tempstat][temp] = float(j[j.index('">')+2:])
                        
                    except:
                        this = j[j.index('">')+2:]
                        try:
                            if d[tempstat][temp] == -1:
                                d[tempstat][temp] = int(re.sub(',','', this))
                        except:
                            if d[tempstat][temp] == -1:
                                d[tempstat][temp] = this
                        
                        
                except:
                    pass
teams = pd.DataFrame(d)
teams = teams.drop(columns=['ranker" scope="row'])

file = open('NBA_teams.csv', 'w')
file.write(NBA_df.to_csv())
file.close()

print(NBA_df.head())