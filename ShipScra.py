#---------------------------------------------PortScraper1.0--------------------------------------------------------
#Webscaping tool that iterates over the website assuming increments of 1, but can easily be adapted to any requirements

#Packages required
import bs4
import csv
import re
import time
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen


#File Operations
filename = "ships.csv"       #make a new file called ports.csv
f = open(filename,"a")          #open file, "a" means append (add the data to the end of this file if it already exists)
headers = "Ship_name, AIS_Vessel_type, MMSI, Current Area, Latitude, Longitude, Call sign, Flag, Ship Origin Country, Status  \n"       #the col headers in csv
f.write(headers)         #write them ol' headers
#Target Website ('http:www.target.com/')
base_url = 'http://www.marinetraffic.com/en/ais/details/ships/shipid:' #this is a website about ports

w = csv.writer(open("shipper.csv","w"))
w.writerow(["Ship_name","AIS_Vessel_type","MMSI","Current Area","Latitude","Longitude","Call sign","Ship Origin Country","Status"])         #write them ol' headers


#Scaping operation
for x in range(395030,700050,783):          #iterate over as many websites as needed by changing page number
    try:
        real_url = base_url + str(x)

        req = Request(real_url, headers={'User-Agent': 'Mozilla/5.0'})        #get around the 403 "access forbidden" error

        webpage = urlopen(req).read()
        page_soup=soup(webpage,"html.parser")

        #port names
        ship = page_soup.findAll("h1",{"class":"font-200 no-margin"})
        Ship_name = ship[0].text.strip()


        rest = page_soup.findAll("div",{"class":"vertical-offset-10 group-ib"})
        Area = rest[1].text.strip().split('\n')[1]
        Latitude = (rest[2].text.split(':')[1].split('°')[0]).split('\n')[1]
        Longitude = (rest[2].text.split(':')[1].split('/ ')[1]).split('°')[0]

        rest = page_soup.findAll("div",{"class":"group-ib short-line vertical-offset-5"})
        MMSI = rest[0].text.strip().split('\n')[1]
        call_sign = rest[1].text.strip().split('\n')[1]
        flag = rest[2].text.strip().split(':')[1].split('\n')[1]
        ship_origin_country = rest[2].text.strip().split(':')[1].split('\n')[1].split(' [')[1].split(']')[0]
        AIS_Vessel_type = rest[3].text.strip().split(':')[1].split('\n')[1]
        ship_status = rest[-1].text.strip().split('\n')[1]

    except Exception:       #on occasion there is nothing at a particular webpage
        print ("didnt work")
        pass        #pass means the code continues in this instance

    print ("Ship name: " + Ship_name)
    print ("AIS Vessel type: " + AIS_Vessel_type)
    print ("Current Area: " + Area)
    print("Latitude: " + Latitude)
    print ("Longitude: " + Longitude)
    print ("MMSI: " + MMSI)
    print("Call sign: " + call_sign)
    print("Flag: " + flag)
    print ("Ship origin country: " + ship_origin_country)
    print("Status: " + ship_status)
    print("\n --------------------- \n ")

    w.writerow([Ship_name,AIS_Vessel_type,MMSI,Area,Latitude,Longitude,call_sign,flag,ship_origin_country,ship_status])
    #f.write(Ship_name + ',' + AIS_Vessel_type + ',' + MMSI + ',' + Area + ',' + Latitude + ',' + Longitude + ',' + call_sign + ',' + flag + ',' + ship_origin_country + ',' + ship_status + "\n")
    time.sleep(1)
f.close
