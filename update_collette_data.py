#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import bs4
import csv
from datetime import date
from datetime import datetime
from tqdm import tqdm

def main():

    today = date.today()
    file_name = 'collette_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','DepartureID','Departure Date','field','value']
        csv_writer.writerow(field_names)
        # print(field_names)
    
        coletteTrips = (
            ('ColletteAY20', 'https://www.gocollette.com/en/tours/north-america/usa/alaska-and-the-yukon/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/alaska-and-the-yukon/booking?b=1#step/1'),        # Alaska and The Yukon featuring the Yukon, Fairbanks and Denali
            ('ColletteADLC20', 'https://www.gocollette.com/en/tours/north-america/usa/alaska-discovery/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/alaska-discovery/booking?b=1#step/1'),        # Alaska Discovery Land & Cruise featuring a 7-night Princess Cruise
            ('ColletteANL20', 'https://www.gocollette.com/en/tours/north-america/usa/alaskas-northern-lights/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/alaskas-northern-lights/booking?b=1#step/1'),     # Alaska's Northern Lights
            ('ColletteANLI20', 'https://www.gocollette.com/en/tours/north-america/usa/alaskas-northern-lights-featuring-iditarod-race/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/alaskas-northern-lights-featuring-iditarod-race/booking?b=1#step/1'),     # Alaska's Northern Lights featuring the Iditarod Race
            ('ColletteABF20', 'https://www.gocollette.com/en/tours/north-america/usa/albuquerque-balloon-fiesta/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/albuquerque-balloon-fiesta/booking?b=1#step/1'),      # Albuquerque Balloon Fiesta
            ('ColletteACC20', 'https://www.gocollette.com/en/tours/north-america/usa/americas-cowboy-country/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/americas-cowboy-country/booking?b=1#step/1'),     # America’s Cowboy Country
            ('ColletteAMC20', 'https://www.gocollette.com/en/tours/north-america/usa/americas-music-cities/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/americas-music-cities/booking?b=1#step/1'),       # America's Music Cities featuring New Orleans, Memphis & Nashville
            ('ColletteAMCJF20', 'https://www.gocollette.com/en/tours/north-america/usa/americas-music-cities-jazz-festival/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/americas-music-cities-jazz-festival/booking?b=1#step/1'),     # America's Music Cities featuring New Orleans Jazz Fest, Memphis & Nashville
            ('ColletteAMCH20', 'https://www.gocollette.com/en/tours/north-america/usa/americas-music-cities-holiday/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/americas-music-cities-holiday/booking?b=1#step/1'),       # America's Music Cities Holiday featuring Nashville, Memphis & New Orleans
            ('ColletteANPD20', 'https://www.gocollette.com/en/tours/north-america/usa/americas-national-parks-and-denver/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/americas-national-parks-and-denver/booking?b=1#step/1'),      # America's National Parks and Denver
            ('ColletteAV20', 'https://www.gocollette.com/en/tours/north-america/usa/autumn-in-vermont/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/autumn-in-vermont/booking?b=1#step/1'),       # Autumn in Vermont featuring Lake Champlain and the Adirondacks
            ('ColletteBCSM20', 'https://www.gocollette.com/en/tours/north-america/usa/bluegrass-smoky-mountains/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/bluegrass-smoky-mountains/booking?b=1#step/1'),       # Bluegrass Country & the Smoky Mountains featuring Louisville, Gatlinburg & Asheville
            ('ColletteCRGNP20', 'https://www.gocollette.com/en/tours/north-america/canada/canadian-rockies--glacier-national-park/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/canada/canadian-rockies--glacier-national-park/booking?b=1#step/1'),      # Canadian Rockies & Glacier National Park
            ('ColletteCRGNPCS20', 'https://www.gocollette.com/en/tours/north-america/canada/canadian-rockies-glacier-national-park-with-calgary-stampede/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/canada/canadian-rockies-glacier-national-park-with-calgary-stampede/booking?b=1#step/1'),     # Canadian Rockies & Glacier National Park featuring the Calgary Stampede
            ('ColletteCRT20', 'https://www.gocollette.com/en/tours/north-america/canada/canadian-rockies-by-train/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/canada/canadian-rockies-by-train/booking?b=1#step/1'),        # Canadian Rockies by Train
            ('ColletteCRTCS20', 'https://www.gocollette.com/en/tours/north-america/canada/canadian-rockies-by-train-with-calgary-stampede/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/canada/canadian-rockies-by-train-with-calgary-stampede/booking?b=1#step/1'),        # Canadian Rockies by Train featuring the Calgary Stampede
            ('ColletteCRRM20', 'https://www.gocollette.com/en/tours/north-america/canada/canadian-rockies-featuring-rocky-mountaineer/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/canada/canadian-rockies-featuring-rocky-mountaineer/booking?b=1#step/1'),     # Canadian Rockies featuring Rocky Mountaineer
            ('ColletteCRRMCS20', 'https://www.gocollette.com/en/tours/north-america/canada/canadian-rockies-featuring-rocky-mountaineer-with-calgary-stampede/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/canada/canadian-rockies-featuring-rocky-mountaineer-with-calgary-stampede/booking?b=1#step/1'),       # Canadian Rockies featuring Rocky Mountaineer and Calgary Stampede
            ('ColletteCC20', 'https://www.gocollette.com/en/tours/north-america/usa/canyon-country/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/canyon-country/booking?b=1#step/1'),      # Canyon Country featuring Arizona & Utah
            ('ColletteCFC20', 'https://www.gocollette.com/en/tours/north-america/canada/charming-french-canada/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/canada/charming-french-canada/booking?b=1#step/1'),     # Charming French Canada featuring Montréal, Quebec City, Charlevoix and Montebello
            ('ColletteCNE20', 'https://www.gocollette.com/en/tours/north-america/usa/colors-of-new-england/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/colors-of-new-england/booking?b=1#step/1'),     # Colors of New England featuring Coastal Maine
            ('ColletteCNEP20', 'https://www.gocollette.com/en/tours/north-america/usa/colors-of-new-england-featuring-portland/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/colors-of-new-england-featuring-portland/booking?b=1#step/1'),        # Colors of New England featuring Portland, Maine
            ('ColletteCR20', 'https://www.gocollette.com/en/tours/south-america/costa-rica/costa-rica/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/south-america/costa-rica/costa-rica/booking?b=1#step/1'),       # Costa Rica: A World of Nature featuring Tortuguero National Park, Arenal Volcano & Manuel Antonio National Park
            ('ColletteDP20', 'https://www.gocollette.com/en/tours/south-america/panama/discover-panama/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/south-america/panama/discover-panama/booking?b=1#step/1'),       # Discover Panama: The Land Between the Seas
            ('ColletteEC20', '', ''),       # Experience Colombia
            ('ColletteHA20', 'https://www.gocollette.com/en/tours/north-america/usa/hawaiian-adventure/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/hawaiian-adventure/booking?b=1#step/1'),      # Hawaiian Adventure Three Islands featuring Oahu, Kauai and Maui
            ('ColletteHOA20', 'https://www.gocollette.com/en/tours/north-america/usa/heritage-of-america/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/heritage-of-america/booking?b=1#step/1'),       # Heritage of America
            ('ColletteHOAVT20', 'https://www.gocollette.com/en/tours/north-america/usa/heritage-of-america-international-tattoo/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/heritage-of-america-international-tattoo/booking?b=1#step/1'),        # Heritage of America featuring the Virginia International Tattoo
            ('ColletteHSAAL20', '', ''),       # Highlights of South America Featuring the Andean Lakes Crossing, Buenos Aires & Rio de Janeiro
            ('ColletteHSA20', 'https://www.gocollette.com/en/tours/south-america/argentina/highlights-of-south-america/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/south-america/argentina/highlights-of-south-america/booking?b=1#step/1'),       # Highlights of South America featuring Buenos Aires, Iguazu Falls & Rio de Janeiro
            ('ColletteINE20', 'https://www.gocollette.com/en/tours/north-america/usa/islands-of-new-england/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/islands-of-new-england/booking?b=1#step/1'),      # Islands of New England
            ('ColletteJTSA20', 'https://www.gocollette.com/en/tours/south-america/argentina/journey-through-south-america/booking?b=1#step/1', ''),     # Journey Through South America featuring Santiago, Andean Lakes Crossing & Rio de Janeiro
            ('ColletteJTSAP20', 'https://www.gocollette.com/en/tours/south-america/argentina/journey-through-south-america-with-peru/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/south-america/argentina/journey-through-south-america-with-peru/booking?b=1#step/1'),       # Journey Through South America with Peru Featuring Machu Picchu, Andean Lakes Crossing & Rio de Janeiro
            ('ColletteMPGW20', 'https://www.gocollette.com/en/tours/south-america/peru/peru-and-galapagos-by-yacht/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/south-america/peru/peru-and-galapagos-by-yacht/booking?b=1#step/1'),        # Machu Picchu & Galapagos Wonders featuring a 4-Night Cruise
            ('ColletteMPGI20', 'https://www.gocollette.com/en/tours/south-america/ecuador/galapagos-islands/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/south-america/ecuador/galapagos-islands/booking?b=1#step/1'),       # Machu Picchu & the Galapagos Islands
            ('ColletteMPGICI20', 'https://www.gocollette.com/en/tours/south-america/peru/peru-and-galapagos-by-yacht-3-nights/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/south-america/peru/peru-and-galapagos-by-yacht-3-nights/booking?b=1#step/1'),       # Machu Picchu & the Galapagos Islands featuring a 3-Night Cruise & 1-Night Island Stay
            ('ColletteMI20', 'https://www.gocollette.com/en/tours/north-america/usa/mackinac-island/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/mackinac-island/booking?b=1#step/1'),     # Mackinac Island featuring the Grand Hotel & Chicago
            ('ColletteMITF20', 'https://www.gocollette.com/en/tours/north-america/usa/mackinac-island-with-tulip-festival/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/mackinac-island-with-tulip-festival/booking?b=1#step/1'),     # Mackinac Island featuring the Grand Hotel and the Tulip Time Festival
            ('ColletteMCW20', 'https://www.gocollette.com/en/tours/north-america/canada/maritimes-coastal-wonders/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/canada/maritimes-coastal-wonders/booking?b=1#step/1'),        # Maritimes Coastal Wonders featuring the Cabot Trail
            ('ColletteNSMH20', 'https://www.gocollette.com/en/tours/north-america/usa/bluegrass-smoky-mountains-holiday/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/bluegrass-smoky-mountains-holiday/booking?b=1#step/1'),       # Nashville & the Smoky Mountains Holiday featuring Gatlinburg & Asheville
            ('ColletteNPA20', 'https://www.gocollette.com/en/tours/north-america/usa/national-parks/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/national-parks/booking?b=1#step/1'),      # National Parks of America
            ('CollettePNWC20', 'https://www.gocollette.com/en/tours/north-america/usa/pacific-northwest--california/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/pacific-northwest--california/booking?b=1#step/1'),       # Pacific Northwest & California featuring Washington, Oregon and California
            ('CollettePCW20', 'https://www.gocollette.com/en/tours/north-america/usa/painted-canyons-of-the-west/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/painted-canyons-of-the-west/booking?b=1#step/1'),     # Painted Canyons of the West featuring Utah’s Five National Parks
            ('CollettePEW20', 'https://www.gocollette.com/en/tours/south-america/argentina/patagonia/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/south-america/argentina/patagonia/booking?b=1#step/1'),     # Patagonia: Edge of the World featuring Argentina, Chile, and a 4-Night Patagonia Cruise
            ('CollettePALM20', 'https://www.gocollette.com/en/tours/south-america/peru/peru-ancient-land-of-mysteries-featuring-puno/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/south-america/peru/peru-ancient-land-of-mysteries-featuring-puno/booking?b=1#step/1'),      # Peru: Ancient Land of Mysteries featuring Puno
            ('CollettePLSV20', 'https://www.gocollette.com/en/tours/south-america/peru/peru-ancient-land-of-mysteries/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/south-america/peru/peru-ancient-land-of-mysteries/booking?b=1#step/1'),     # Peru: From Lima to the Sacred Valley
            ('ColletteRCM20', 'https://www.gocollette.com/en/tours/north-america/usa/roaming-coastal-maine/booking?b=1#step/1', ''),       # Roaming Coastal Maine featuring Portland, Acadia & Penobscot Bay
            ('ColletteSC20', 'https://www.gocollette.com/en/tours/north-america/usa/southern-charm/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/southern-charm/booking?b=1#step/1'),      # Southern Charm featuring Jekyll Island, Savannah & Charleston
            ('ColletteSCH20', 'https://www.gocollette.com/en/tours/north-america/usa/southern-charm-holiday/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/southern-charm-holiday/booking?b=1#step/1'),      # Southern Charm Holiday
            ('ColletteSM20', 'https://www.gocollette.com/en/tours/north-america/canada/spotlight-on-montreal/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/canada/spotlight-on-montreal/booking?b=1#step/1'),        # Spotlight on Montréal
            ('ColletteSN20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-nashville/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/spotlight-on-nashville/booking?b=1#step/1'),      # Spotlight on Nashville
            ('ColletteSNO20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-new-orleans/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/spotlight-on-new-orleans/booking?b=1#step/1'),        # Spotlight on New Orleans
            ('ColletteSNOH20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-new-orleans-holiday/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/spotlight-on-new-orleans-holiday/booking?b=1#step/1'),      # Spotlight on New Orleans Holiday
            ('ColletteNOC20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlights-on-new-orleans-carnival/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/spotlights-on-new-orleans-carnival/booking?b=1#step/1'),        # Spotlight on New Orleans featuring Carnival
            ('ColletteSNOJF20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-new-orleans-jazz-festival/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/spotlight-on-new-orleans-jazz-festival/booking?b=1#step/1'),        # Spotlight on New Orleans featuring Jazz Fest
            ('ColletteSNYC20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-new-york/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/spotlight-on-new-york/booking?b=1#step/1'),       # Spotlight on New York City
            ('ColletteSNYCH20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-new-york-holiday/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/spotlight-on-new-york-holiday/booking?b=1#step/1'),       # Spotlight on New York City Holiday
            ('ColletteSSA20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-san-antonio/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/spotlight-on-san-antonio/booking?b=1#step/1'),        # Spotlight on San Antonio
            ('ColletteSSAH20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-san-antonio-holiday/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/spotlight-on-san-antonio-holiday/booking?b=1#step/1'),        # Spotlight on San Antonio Holiday
            ('ColletteSSASSR20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-san-antonio-stock-show-and-rodeo/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/spotlight-on-san-antonio-stock-show-and-rodeo/booking?b=1#step/1'),       # Spotlight on San Antonio featuring the San Antonio Stock Show & Rodeo
            ('ColletteSSF20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-santa-fe/booking?b=1#step/1', ''),       # Spotlight on Santa Fe
            ('ColletteSSFH20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-santa-fe-holiday/booking?b=1#step/1', ''),       # Spotlight on Santa Fe Holiday
            ('ColletteSSD20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-south-dakota/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/spotlight-on-south-dakota/booking?b=1#step/1'),       # Spotlight on South Dakota featuring Mount Rushmore & The Badlands
            ('ColletteSWDC20', 'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-washington-dc/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/spotlight-on-washington-dc/booking?b=1#step/1'),      # Spotlight on Washington, D.C. Exploring America's Capital
            ('ColletteBEC20', 'https://www.gocollette.com/en/tours/north-america/canada/the-best-of-eastern-canada/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/canada/the-best-of-eastern-canada/booking?b=1#step/1'),       # The Best of Eastern Canada featuring Montreal, Quebec City, Ottawa, Niagara Falls & Toronto
            ('ColletteCRNP20', 'https://www.gocollette.com/en/tours/north-america/usa/the-colorado-rockies/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/the-colorado-rockies/booking?b=1#step/1'),        # The Colorado Rockies featuring National Parks and Historic Trains
            ('ColletteCSA20', '', ''),       # The Complete South America Featuring Peru & Machu Picchu
            ('ColletteTCR20', 'https://www.gocollette.com/en/tours/south-america/costa-rica/tropical-costa-rica/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/south-america/costa-rica/tropical-costa-rica/booking?b=1#step/1'),      # Tropical Costa Rica
            ('ColletteWDCNFNYC20', 'https://www.gocollette.com/en/tours/north-america/usa/washington-dc-niagara-falls-new-york-city/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/washington-dc-niagara-falls-new-york-city/booking?b=1#step/1'),       # Washington D.C., Niagara Falls & NYC
            ('ColletteWY20', 'https://www.gocollette.com/en/tours/north-america/usa/winter-in-yellowstone/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/usa/winter-in-yellowstone/booking?b=1#step/1'),       # Winter in Yellowstone
            ('ColletteWNF20', 'https://www.gocollette.com/en/tours/north-america/canada/newfoundland-and-labrador/booking?b=1#step/1', 'https://www.gocollette.com/en-au/tours/north-america/canada/newfoundland-and-labrador/booking?b=1#step/1')        # Wonders of Newfoundland featuring Lighthouses, Iceburg Alley, & Gros Morne
        )

        print("\n")

        for trip in tqdm(coletteTrips):
        
            op_code = trip[0]
            linkUS = trip[1]
            linkAU = trip[2]

            if linkUS:
            
                previous_departure_date = ''
                duplicate_departure_count = 0
                
                driver = webdriver.Chrome()
                driver.get(linkUS)

                nameElement = driver.find_element_by_tag_name('h3')
                soup = bs4.BeautifulSoup(nameElement.get_attribute('innerHTML'), 'lxml')
                trip_name = soup.contents[0].text.strip()
                # print(trip_name)

                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'date-group-dates')))

                    monthElements = driver.find_elements_by_class_name('date-group-dates')
                    for month in monthElements:

                        departureElements = month.find_elements_by_class_name('date-group')
                        for departure in departureElements:

                            soup = bs4.BeautifulSoup(departure.get_attribute('innerHTML'), 'lxml')
                            # file.write(soup.prettify())

                            date_numbers = soup.find('div', class_='date').text.split()
                            departure_date = '{:02}-{}-{}'.format(int(date_numbers[1].strip(',')), date_numbers[0], date_numbers[2])
                            # print(departure_date)
                            
                            if departure_date == previous_departure_date:                   # check if duplicate departure
                                duplicate_departure_count += 1
                            else:
                                duplicate_departure_count = 0

                            departure_letter = str(chr(duplicate_departure_count + 97))
                            day = '{:02}'.format(int(date_numbers[1].strip(',')))
                            month = str(chr((datetime.strptime(date_numbers[0], '%b')).month + 64))
                            year = '{}'.format(date_numbers[2][-2:])
                            departure_code = '{}{}{}{}'.format(day, month, year, departure_letter)
                            departure_id = '{}-{}'.format(op_code, departure_code)
                            # print(departure_id)

                            notes = ''
                            if soup.find('div', class_='danger'):
                                status = 'Limited'
                                notes = soup.find('div', class_='danger').text.strip()
                                if soup.find('div', class_='date-alert').text.strip() == 'Guaranteed':
                                    notes = 'Guaranteed, {}'.format(notes)
                            elif soup.find('div', class_='date-alert'):
                                status = soup.find('div', class_='date-alert').text.strip()
                                if status == 'Call 800.340.5158 for details':
                                    status = 'Cancelled'
                                elif status == 'Guaranteed':
                                    notes = status
                                    status = 'Available'
                            else:
                                status = 'Available'
                            string_to_write = [trip_name,departure_id,departure_date,'Status',status]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)
                            if notes:
                                string_to_write = [trip_name,departure_id,departure_date,'Notes',notes]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)

                            if status == 'Cancelled' or status == 'Sold Out':
                                available = False
                            else:
                                available = True
                            string_to_write = [trip_name,departure_id,departure_date,'Available',available]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            actual_price = soup.find('span', class_='discountedPrice').text.strip().replace(',', '')
                            string_to_write = [trip_name,departure_id,departure_date,'ActualPriceUSD',actual_price]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            if soup.find('span', class_='crossout'):
                                original_price = soup.find('span', class_='crossout').text.strip().replace(',', '')
                            else:
                                original_price = actual_price
                            string_to_write = [trip_name,departure_id,departure_date,'OriginalPriceUSD',original_price]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            previous_departure_date = departure_date

                finally:
                    driver.quit()

            else:
                print('Missing US Link: {}'.format(op_code))

            
            if linkAU:
                
                previous_departure_date = ''
                duplicate_departure_count = 0
                driver = webdriver.Chrome()
                driver.get(linkAU)

                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'date-group-dates')))

                    monthElements = driver.find_elements_by_class_name('date-group-dates')
                    for month in monthElements:

                        departureElements = month.find_elements_by_class_name('date-group')
                        for departure in departureElements:

                            soup = bs4.BeautifulSoup(departure.get_attribute('innerHTML'), 'lxml')
                            # file.write(soup.prettify())

                            date_numbers = soup.find('div', class_='date').text.split()
                            departure_date = '{:02}-{}-{}'.format(int(date_numbers[1].strip(',')), date_numbers[0], date_numbers[2])
                            # print(departure_date)

                            if departure_date == previous_departure_date:                   # check if duplicate departure
                                duplicate_departure_count += 1
                            else:
                                duplicate_departure_count = 0

                            departure_letter = str(chr(duplicate_departure_count + 97))
                            day = '{:02}'.format(int(date_numbers[1].strip(',')))
                            month = str(chr((datetime.strptime(date_numbers[0], '%b')).month + 64))
                            year = '{}'.format(date_numbers[2][-2:])
                            departure_code = '{}{}{}{}'.format(day, month, year, departure_letter)
                            departure_id = '{}-{}'.format(op_code, departure_code)
                            # print(departure_id)

                            actual_price = soup.find('span', class_='discountedPrice').text.strip().replace(',', '')
                            string_to_write = [trip_name,departure_id,departure_date,'ActualPriceAUD',actual_price]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            if soup.find('span', class_='crossout'):
                                original_price = soup.find('span', class_='crossout').text.strip().replace(',', '')
                            else:
                                original_price = actual_price
                            string_to_write = [trip_name,departure_id,departure_date,'OriginalPriceAUD',original_price]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            previous_departure_date = departure_date

                finally:
                    driver.quit()

            else:
                print('Missing AU Link: {}'.format(op_code))

    print("\nDone!\n")

if __name__ == '__main__': main()