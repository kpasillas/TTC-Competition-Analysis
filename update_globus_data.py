#!/usr/bin/env python3

from selenium import webdriver
import requests
import bs4
import re
import csv
from datetime import date
from tqdm import tqdm

def main():

    today = date.today()
    file_name = 'globus_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','Departure Date','field','value']
        csv_writer.writerow(field_names)

        linksUS = (
            'https://www.globusjourneys.com/tour/alaskas-iditarod-with-fairbanks/aiq/?nextyear=true&content=price',     # Alaska's Iditarod With Fairbanks
            'https://www.globusjourneys.com/tour/alaskas-iditarod/ai/?nextyear=true&content=price',     # Alaska's Iditarod
            'https://www.globusjourneys.com/tour/americas-historic-east/ah/?nextyear=true&content=price',       # America's Historic East
            'https://www.globusjourneys.com/tour/americas-musical-heritage/as/?nextyear=true&content=price',        # America's Musical Heritage
            'https://www.globusjourneys.com/tour/americas-national-parks/an/?nextyear=true&content=price',      # America's National Parks
            'https://www.globusjourneys.com/tour/best-of-the-hawaiian-islands/ew/?nextyear=true&content=price',     # Best Of The Hawaiian Islands
            'https://www.globusjourneys.com/tour/brazil-argentina-escape-with-santiago/k4e/?nextyear=true&content=price',       # Brazil & Argentina Escape With Santiago
            'https://www.globusjourneys.com/tour/calgary-stampede/cx/?nextyear=true&content=price',     # Calgary Stampede
            'https://www.globusjourneys.com/tour/california-classics/aa/?nextyear=true&content=price',      # California Classics
            'https://www.globusjourneys.com/tour/canadian-rockies-winter-adventure/cl/?nextyear=true&content=price',        # Canadian Rockies Winter Adventure
            'https://www.globusjourneys.com/tour/canyon-country-adventure/av/?nextyear=true&content=price',     # Canyon Country Adventure
            'https://www.globusjourneys.com/tour/cape-cod-the-islands-400th-mayflower-anniversary/ao1/?content=price',      # Cape Cod & The Islands 400Th Mayflower Anniversary
            'https://www.globusjourneys.com/tour/cape-cod-the-islands/ao/?nextyear=true&content=price',     # Cape Cod & The Islands
            'https://www.globusjourneys.com/tour/classic-fall-foliage/ab/?nextyear=true&content=price',     # Classic Fall Foliage
            'https://www.globusjourneys.com/tour/colorful-newfoundland/cn/?nextyear=true&content=price',        # Colorful Newfoundland
            'https://www.globusjourneys.com/tour/costa-rica-escape/k3/?nextyear=true&content=price',        # Costa Rica Escape
            'https://www.globusjourneys.com/tour/cruising-hawaiis-paradise-with-outrigger-waikiki-beach-resort/eno/?nextyear=true&content=price',       # Cruising Hawaii's Paradise With Outrigger Waikiki Beach Resort
            'https://www.globusjourneys.com/tour/cruising-hawaiis-paradise-with-sheraton-princess-kaiulani/en/?nextyear=true&content=price',        # Cruising Hawaii's Paradise With Sheraton Princess Kaiulani
            'https://www.globusjourneys.com/tour/cubas-charming-colonial-cities-havana/yv/?nextyear=true&content=price',        # Cuba's Charming Colonial Cities & Havana
            'https://www.globusjourneys.com/tour/discover-glacier-national-park-hells-canyon-washington-wine-country-with-alaska-cruise/nsi/?nextyear=true&content=price',      # Discover Glacier National Park, Hells Canyon & Washington Wine Country With Alaska Cruise
            'https://www.globusjourneys.com/tour/discover-glacier-national-park-hells-canyon-washington-wine-country/ns/?nextyear=true&content=price',      # Discover Glacier National Park, Hells Canyon & Washington Wine Country
            'https://www.globusjourneys.com/tour/eastern-canada-winter-adventure/co/?content=price',        # Eastern Canada Winter Adventure
            'https://www.globusjourneys.com/tour/eastern-us-canada-discovery/cu/?nextyear=true&content=price',      # Eastern Us & Canada Discovery
            'https://www.globusjourneys.com/tour/enchanted-new-mexico-with-albuquerque-balloon-fiesta/af/?nextyear=true&content=price',     # Enchanted New Mexico With Albuquerque Balloon Fiesta
            'https://www.globusjourneys.com/tour/enchanting-canyonlands/am/?nextyear=true&content=price',       # Enchanting Canyonlands
            'https://www.globusjourneys.com/tour/exploring-americas-great-parks/ar/?nextyear=true&content=price',       # Exploring America's Great Parks
            'https://www.globusjourneys.com/tour/glacier-national-park-the-canadian-rockies/cs/?nextyear=true&content=price',       # Glacier National Park & The Canadian Rockies
            'https://www.globusjourneys.com/tour/grand-hawaii-vacation/ek/?nextyear=true&content=price',        # Grand Hawaii Vacation
            'https://www.globusjourneys.com/tour/grand-western-canada-vacation-with-alaska-cruise/cgi/?nextyear=true&content=price',        # Grand Western Canada Vacation With Alaska Cruise
            'https://www.globusjourneys.com/tour/grand-western-canada-vacation/cg/?nextyear=true&content=price',        # Grand Western Canada Vacation
            'https://www.globusjourneys.com/tour/great-canadian-rail-journey-with-alaska-cruise/czi/?nextyear=true&content=price',      # Great Canadian Rail Journey With Alaska Cruise
            'https://www.globusjourneys.com/tour/great-canadian-rail-journey/cz/?nextyear=true&content=price',      # Great Canadian Rail Journey
            'https://www.globusjourneys.com/tour/great-resorts-of-the-canadian-rockies/cd/?nextyear=true&content=price',        # Great Resorts Of The Canadian Rockies
            'https://www.globusjourneys.com/tour/historic-cities-of-eastern-canada-with-canada-new-england-discovery-cruise/cci/?nextyear=true&content=price',      # Historic Cities Of Eastern Canada With Canada & New England Discovery Cruise
            'https://www.globusjourneys.com/tour/historic-cities-of-eastern-canada/cc/?nextyear=true&content=price',        # Historic Cities Of Eastern Canada
            'https://www.globusjourneys.com/tour/historic-trains-of-the-old-west-with-albuquerque-balloon-fiesta/ncs/?nextyear=true&content=price',     # Historic Trains Of The Old West With Albuquerque Balloon Fiesta
            'https://www.globusjourneys.com/tour/historic-trains-of-the-old-west/nc/?nextyear=true&content=price',      # Historic Trains Of The Old West
            # 'https://www.globusjourneys.com/tour/jasper-dark-sky-festival-canadian-rockies-adventure/ce/?content=price',      # Jasper Dark Sky Festival Canadian Rockies Adventure
            'https://www.globusjourneys.com/tour/legacy-of-the-incas/sp/?nextyear=true&content=price',      # Legacy Of The Incas
            'https://www.globusjourneys.com/tour/mackinac-island-the-great-lakes/nm/?nextyear=true&content=price',      # Mackinac Island & The Great Lakes
            'https://www.globusjourneys.com/tour/majestic-rockies/cv/?nextyear=true&content=price',     # Majestic Rockies
            'https://www.globusjourneys.com/tour/maritimes-adventure/ct/?nextyear=true&content=price',      # Maritimes Adventure
            'https://www.globusjourneys.com/tour/music-cities-nashville-memphis/nf/?nextyear=true&content=price',       # Music Cities: Nashville & Memphis
            'https://www.globusjourneys.com/tour/natural-wonders-of-costa-rica/sr/?nextyear=true&content=price',        # Natural Wonders Of Costa Rica
            'https://www.globusjourneys.com/tour/natures-best-alaska-with-alaska-cruise/cki/?nextyear=true&content=price',      # Nature's Best: Alaska With Alaska Cruise
            'https://www.globusjourneys.com/tour/natures-best-alaska/ck/?nextyear=true&content=price',      # Nature's Best: Alaska
            'https://www.globusjourneys.com/tour/new-england-and-the-hudson-valley/ae/?nextyear=true&content=price',        # New England And The Hudson Valley
            'https://www.globusjourneys.com/tour/newfoundland-labrador/cf/?nextyear=true&content=price',        # Newfoundland & Labrador
            'https://www.globusjourneys.com/tour/northern-californias-finest/al/?nextyear=true&content=price',      # Northern California'S Finest
            'https://www.globusjourneys.com/tour/oregons-coast-cascades-craft-beers/nb/?nextyear=true&content=price',       # Oregon's Coast, Cascades & Craft Beers
            'https://www.globusjourneys.com/tour/pacific-coast-adventure-with-portland-rose-festival/aq1/?nextyear=true&content=price',     # Pacific Coast Adventure With Portland Rose Festival
            'https://www.globusjourneys.com/tour/pacific-coast-adventure/aq/?nextyear=true&content=price',      # Pacific Coast Adventure
            'https://www.globusjourneys.com/tour/parks-canyons-spectacular/ap/?nextyear=true&content=price',        # Parks & Canyons Spectacular
            'https://www.globusjourneys.com/tour/passage-through-new-england-eastern-canada/ca/?nextyear=true&content=price',       # Passage Through New England & Eastern Canada
            'https://www.globusjourneys.com/tour/patagonia-journey-to-the-end-of-the-world/sf/?nextyear=true&content=price',        # Patagonia: Journey To The End Of The World
            'https://www.globusjourneys.com/tour/peru-escape/k2/?nextyear=true&content=price',      # Peru Escape
            'https://www.globusjourneys.com/tour/peru-splendors/so/?nextyear=true&content=price',       # Peru Splendors
            'https://www.globusjourneys.com/tour/quebec-in-depth-with-the-gaspe-peninsula-and-canada-new-england-discovery-cruise/cqi/?content=price',      # Quebec In Depth With The Gaspe Peninsula And Canada & New England Discovery Cruise
            'https://www.globusjourneys.com/tour/quebec-in-depth-with-the-gaspe-peninsula/cq/?content=price',       # Quebec In Depth With The Gaspe Peninsula
            'https://www.globusjourneys.com/tour/quebec-winter-carnival/ci/?nextyear=true&content=price',       # Québec Winter Carnival
            'https://www.globusjourneys.com/tour/south-america-getaway/sb/?nextyear=true&content=price',        # South America Getaway
            'https://www.globusjourneys.com/tour/south-american-odyssey/sg/?nextyear=true&content=price',       # South American Odyssey
            'https://www.globusjourneys.com/tour/southern-california-with-death-valley-joshua-tree-national-parks/nd/?nextyear=true&content=price',     # Southern California With Death Valley & Joshua Tree National Parks
            'https://www.globusjourneys.com/tour/southern-charms/ng/?nextyear=true&content=price',      # Southern Charms
            'https://www.globusjourneys.com/tour/spectacular-alaska!-with-alaska-cruise/aji/?nextyear=true&content=price',      # Spectacular Alaska! With Alaska Cruise
            'https://www.globusjourneys.com/tour/spectacular-alaska!/aj/?nextyear=true&content=price',      # Spectacular Alaska!
            'https://www.globusjourneys.com/tour/spirit-of-south-america/sa/?nextyear=true&content=price',      # Spirit Of South America
            'https://www.globusjourneys.com/tour/spirit-of-the-american-wild-west/au/?nextyear=true&content=price',     # Spirit Of The American Wild West
            'https://www.globusjourneys.com/tour/spirit-of-the-rockies-with-alaska-cruise/cri/?nextyear=true&content=price',        # Spirit Of The Rockies With Alaska Cruise
            'https://www.globusjourneys.com/tour/spirit-of-the-rockies/cr/?nextyear=true&content=price',        # Spirit Of The Rockies
            'https://www.globusjourneys.com/tour/the-classic-lodges-parks-of-the-west/ay/?nextyear=true&content=price',     # The Classic Lodges & Parks Of The West
            'https://www.globusjourneys.com/tour/the-wonders-of-mexicos-yucatan/yy/?content=price',     # The Wonders Of Mexico's Yucatan
            'https://www.globusjourneys.com/tour/tournament-of-roses/ax/?nextyear=true&content=price',      # Tournament Of Roses
            'https://www.globusjourneys.com/tour/ultimate-alaska-the-yukon-with-alaska-cruise/cbi/?nextyear=true&content=price',        # Ultimate Alaska & The Yukon With Alaska Cruise
            'https://www.globusjourneys.com/tour/ultimate-alaska-the-yukon/cb/?nextyear=true&content=price',        # Ultimate Alaska & The Yukon
            'https://www.globusjourneys.com/tour/wonders-of-the-maritimes-scenic-cape-breton/ch/?nextyear=true&content=price',      # Wonders Of The Maritimes & Scenic Cape Breton
            'https://www.globusjourneys.com/tour/yellowstone-winter-wonderland/aw/?nextyear=true&content=price'     # Yellowstone Winter Wonderland
        )

        print()

        for link in tqdm(linksUS):

            res = requests.get(link)
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            trip_name = soup.find("h1").contents[0].text
            code = soup.find("h1").contents[2].text
            code = code.strip("()")
            # print('{} - {}'.format(trip_name, code))
            
            for departure in soup.find_all('div', class_='listing'):

                date_numbers = departure.find('p', class_='date-numbers').text.split()
                departure_date = '{}-{}-{}'.format(date_numbers[0], date_numbers[1], date_numbers[2])
                # print(departure_date)
                
                actual_price = departure.find('p', class_='price-actual').text.strip()
                string_to_write = [trip_name,departure_date,'Actual Price USD',actual_price]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                if departure.find('p', class_='price-strike'):
                    original_price = departure.find('p', class_='price-strike').text
                else:
                    original_price = actual_price
                string_to_write = [trip_name,departure_date,'Original Price USD',original_price]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                if departure.find('div', class_='popular-message'):
                    popular_departure = True
                else:
                    popular_departure = False
                string_to_write = [trip_name,departure_date,'Popular Departure',popular_departure]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                listing_status = departure.find('div', class_='listing-status').text.strip()
                string_to_write = [trip_name,departure_date,'Listing Status',listing_status]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                if re.search( "Not Available", departure.find('div', class_='listing-buttons-contain').text):
                    available = False
                else:
                    available = True
                string_to_write = [trip_name,departure_date,'Available',available]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)

            linkAU = "https://www.globus.com.au/booking?tour={}&season=2020".format(code)
            driver = webdriver.Chrome()
            driver.get(linkAU)
            html = driver.execute_script("return document.documentElement.outerHTML")
            soup = bs4.BeautifulSoup(html, 'lxml')

            for departure in soup.findAll('div', class_='booking-departures__wrapper'):

                date_numbers = departure.find('span', class_='booking-departures__date').text.split()
                departure_date = "{}-{}-{}".format(date_numbers[0], (date_numbers[1])[0:3], (date_numbers[2])[2:4])
                # print(departure_date)

                actual_price = departure.find('span', class_='booking-departures__price--amount').text
                string_to_write = [trip_name,departure_date,'Actual Price AUD',actual_price]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                if departure.find('span', class_='booking-departures__price--strike-through'):
                    original_price = departure.find('span', class_='booking-departures__price--strike-through').text
                else:
                    original_price = actual_price
                string_to_write = [trip_name,departure_date,'Original Price AUD',original_price]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)

        print("\nDone!\n")

if __name__ == '__main__': main()