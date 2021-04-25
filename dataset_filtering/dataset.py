from bs4 import BeautifulSoup
import csv
import pandas as pd

file1 = open("MyFile.txt", "w")
def trim(string):
    v1=string.find('/')
    string=string[0:v1]
    return string
with open("d1.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")

links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))



string_set = links
new_set = {x.replace("https://", "") for x in string_set}
new_set = {x.replace("http://", "") for x in string_set}
new_set = list(set(new_set))
for i in range(0,len(new_set)):
    new_set[i]=trim(new_set[i])
new_set = list(set(new_set))
#for i in new_set:
#    print(str(new_set[i])
#for i in new_set:
#    print(new_set[i])
df = pd.DataFrame(new_set)
df.to_csv('videos_sports_music.csv')
file1.write(str(new_set))
file1.close()
