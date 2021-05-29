import requests
from bs4 import BeautifulSoup
import pandas

def list_per_page(soup) : 
    all = soup.find_all("div",{"class":"propertyRow"})
    l = []
    for item in all :
        d = {}
        #find address in span
        d["Address"]=item.find_all("span",{"class":"propAddressCollapse"})[0].text 
        d["Locality"]=item.find_all("span",{"class":"propAddressCollapse"})[1].text
        d["Price"]=item.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")
        try:
            d["Beds"]=item.find("span",{"class":"infoBed"}).find("b").text
        except:
            d["Beds"]=None
        try:
            d["Area"]=item.find("span",{"class":"infoSqFt"}).find("b").text
        except:
            d["Area"]=None
        try:
            d["Full Baths"]=item.find("span",{"class":"infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"]=None
        try:
            d["Half Baths"]=item.find("span",{"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"]=None
        for column_group in item.find_all("div",{"class":"columnGroup"}):
            feature_groups = column_group.find_all("span",{"class":"featureGroup"})
            feature_names = column_group.find_all("span",{"class":"featureName"})
            for feature_group, feature_name in zip(feature_groups,feature_names):
                if "Lot Size:" in feature_group.text :
                    d["Lot Size"]=feature_name.text
        l.append(d)
    return l

link = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/"
link_header = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
result = []
r = requests.get(link, headers=link_header)
c = r.content
soup = BeautifulSoup(c, "html.parser")
page_number = soup.find_all("a",{"class":"Page"})[-1].text
for page in range(0,int(page_number)) :
    url = base_url+"%s.html"%(page*10)
    print(url)
    r = requests.get(url, headers=link_header)
    c = r.content

    soup = BeautifulSoup(c, "html.parser")
    result.extend(list_per_page(soup))
    print(len(result))
len(result)

df = pandas.DataFrame(result)
df.to_csv("output.csv")
