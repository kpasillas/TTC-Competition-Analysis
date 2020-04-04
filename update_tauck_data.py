#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import bs4
import re
import csv
from datetime import date
from datetime import datetime
from time import sleep
from tqdm import tqdm

def main():

    today = date.today()
    file_name = 'tauck_data_{}.csv'.format(today.strftime("%m-%d-%y"))  
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','DepartureID','Departure Date','field','value']
        csv_writer.writerow(field_names)

        year = '2020'                     # OK to hard-code year value since separate links/report are needed for 2021
        
        linksUS = (                     # 45 total, 9 cruise (don't count)
            'https://www.tauck.com/tours/celebration-of-roses-escorted-tour-event?tcd=vr2020',      # A Celebration of Roses
            'https://www.tauck.com/tours/call-of-wild-alaska-guided-family-tour?tcd=ya2020',        # Alaska: Call of the Wild
            # 'https://www.tauck.com/tours/inside-passage-alaska-small-ship-cruise?tcd=xan2020',      # Alaska's Inside Passage
            'https://www.tauck.com/tours/american-canyonlands-grand-canyon-escorted-tour?tcd=cy2020',       # America's Canyonlands
            # 'https://www.tauck.com/tours/antarctica-cruise?tcd=xr2020',     # Antarctica
            'https://www.tauck.com/tours/best-of-canadian-rockies-escorted-tour?tcd=br2020',        # Best of the Canadian Rockies
            'https://www.tauck.com/tours/bluegrass-blue-ridges-louisville-kentucky-escorted-tour?tcd=ky2020',       # Bluegrass and Blue Ridges: Louisville to Nashville
            'https://www.tauck.com/tours/bugaboos-adventure-canadian-rockies-guided-tour?tcd=bg2020',       # Bugaboos Adventure: Featuring Heli-Exploring
            'https://www.tauck.com/tours/gold-coast-california-escorted-tour?tcd=ca2020',       # California's Gold Coast
            'https://www.tauck.com/tours/canada-capitals-niagara-falls-escorted-tours?tcd=cn2020',      # Canada's Capital Cities plus Niagara Falls
            'https://www.tauck.com/tours/canadian-maritimes-nova-scotia-cruise-and-escorted-tour?tcd=cm2020',       # Canadian Maritimes
            'https://www.tauck.com/tours/canadian-rockies-glacier-national-park-escorted-tour?tcd=cr2020',      # Canadian Rockies & Glacier National Park
            'https://www.tauck.com/tours/canadian-rockies-whistler-victoria-escorted-tour?tcd=gc2020',      # Canadian Rockies, Whistler & Victoria
            'https://www.tauck.com/tours/cape-cod-newport-new-england-escorted-tour-and-cruise?tcd=cc2020',     # Cape Cod, The Islands and Newport
            'https://www.tauck.com/tours/boulder-denver-colorado-escorted-tours?tcd=cl2020',        # Colorado: Denver, Boulder & the Rockies
            'https://www.tauck.com/tours/costa-rica-pura-vida-escorted-tour?tcd=co2020',        # Costa Rica - Pura Vida
            'https://www.tauck.com/tours/jungles-rainforests-costa-rica-guided-family-vacation?tcd=yo2020',     # Costa Rica: Jungles & Rainforests
            'https://www.tauck.com/tours/cowboy-country-wyoming-escorted-family-vacation?tcd=yyn2020',      # Cowboy Country
            # 'https://www.tauck.com/tours/cruising-the-galapagos-islands-cruise?tcd=ed2020',     # Cruising the Galapagos Islands
            # 'https://www.tauck.com/tours/chicago-toronto-great-lakes-cruise?tcd=gle2020',       # Cruising the Great Lakes Chicago to Toronto
            'https://www.tauck.com/tours/connecting-people-culture-escorted-cuba-tour?tcd=cv2020',      # Cuba: Connecting with People and Culture
            'https://www.tauck.com/tours/empire-of-incas-peru-bolivia-escorted-tour?tcd=pb2020',        # Empire of the Incas: Peru & Bolivia
            'https://www.tauck.com/tours/essence-of-south-america-brazil-argentina-escorted-tours?tcd=es2020',      # Essence of South America
            # 'https://www.tauck.com/tours/wildlife-wonderland-galapagos-escorted-family-tour?tcd=yg2020',        # Galapagos: Wildlife Wonderland
            # 'https://www.tauck.com/tours/grand-alaska-guided-tour-and-cruise?tcd=al2020',       # Grand Alaska
            'https://www.tauck.com/tours/grand-canadian-rockies-escorted-tour?tcd=rre2020',     # Grand Canadian Rockies
            'https://www.tauck.com/tours/grand-new-england-fall-foliage-guided-tour?tcd=gr2020',        # Grand New England
            # 'https://www.tauck.com/tours/hidden-galapagos-peru-escorted-tour?tcd=eb2020',       # Hidden Galapagos & Peru
            'https://www.tauck.com/tours/hidden-gems-new-england-guided-tour?tcd=ne2020',       # Hidden Gems of New England
            'https://www.tauck.com/tours/freedom-footsteps-philidelphia-washington-dc-guided-tour?tcd=wb2020',      # In Freedom's Footsteps: Philadelphia to Washington, DC
            'https://www.tauck.com/tours/legends-american-west-national-park-escorted-tour?tcd=jh2020',     # Legends of the American West
            'https://www.tauck.com/tours/california-family-tours-with-yosemite?tcd=yp2020',     # Majestic California: San Francisco, Yosemite & the Pacific
            'https://www.tauck.com/tours/manitoba-polar-bear-tours?tcd=vm2020',     # Manitoba: Polar Bear Adventure
            'https://www.tauck.com/tours/michigan-lakes-mackinac-island-escorted-tour?tcd=mi2020',      # Michigan's Lakes & Mackinac Island
            'https://www.tauck.com/tours/mystical-peru-family-vacation-package?tcd=zp2020',     # Mystical Peru
            'https://www.tauck.com/tours/land-of-enchantment-new-mexico-escorted-tour?tcd=nm2020',      # New Mexico: Land of Enchantment
            'https://www.tauck.com/tours/mississippi-new-orleans-plantation-escorted-tour?tcd=nn2020',      # New Orleans & Missippi River Plantation Country
            'https://www.tauck.com/tours/nova-scotia-prince-edward-island-escorted-tour-and-cruise?tcd=ac2020',     # Nova Scotia & Prince Edward Island
            'https://www.tauck.com/tours/pacific-northwest-escorted-tour?tcd=nw2020',       # Pacific Northwest
            'https://www.tauck.com/tours/patagonia-escorted-tour?tcd=pt2020',       # Patagonia
            # 'https://www.tauck.com/tours/peru-galapagos-guided-tour?tcd=eg2020',        # Peru and the Galapagos Islands
            'https://www.tauck.com/tours/red-rocks-painted-canyon-arizona-escorted-family-tour?tcd=yc2020',     # Red Rocks & Painted Canyons
            'https://www.tauck.com/tours/charleston-savannah-escorted-tours?tcd=cs2020',        # Southern Charms: Savannah Hilton Head & Charleston
            'https://www.tauck.com/tours/national-parks-southwest-escorted-tour?tcd=kd2020',        # Spirit of the Desert: The National Parks of the Southwest
            'https://www.tauck.com/tours/nashville-history-of-country-music-tour?tcd=kn2020',       # Tauck Nashville Country Music Event
            'https://www.tauck.com/tours/best-of-hawaii-escorted-tour?tcd=hw2020',      # The Best of Hawaii
            'https://www.tauck.com/tours/hudson-valley-escorted-tour?tcd=hv2020',       # The Hudson Valley
            # 'https://www.tauck.com/tours/costa-rica-and-panama-canal-cruise?tcd=pce2020',       # The Panama Canal & Costa Rica
            'https://www.tauck.com/tours/canadian-rockies-by-train?tcd=mt2020',     # Vancouver & the Rockies by Rocky Mountaineer
            'https://www.tauck.com/tours/wonderland-yellowstone-winter-escorted-tour?tcd=vw2020',       # Wonderland: Yellowstone in Winter
            'https://www.tauck.com/tours/canadian-rockies-family-tour?tcd=yr2020',       # Wonders of the Canadian Rockies
            'https://www.tauck.com/tours/grand-teton-yellowstone-escorted-tour?tcd=sln2020',        # Yellowstone & Grand Teton National Parks
            'https://www.tauck.com/tours/american-safari-tetons-yellowstone-escorted-tour?tcd=vy2020',      # Yellowstone & the Tetons: American Safari
            'https://www.tauck.com/tours/yosemite-and-sequoia-escorted-tour?tcd=km2020'     # Yostemite and Sequoia: John Muir's California
        )

        print()

        for link in tqdm(linksUS):

            driver = webdriver.Chrome()
            driver.get(link)

            nameElement = driver.find_element_by_tag_name('h1')
            soup = bs4.BeautifulSoup(nameElement.get_attribute('innerHTML'), 'lxml')
            trip_name = soup.contents[0].text.strip()
            # print(trip_name)
            code = link.split('=')[1][:-4].upper()
            op_code = 'Tauck{}{}'.format(code, year[-2:])
            # print(op_code)
            previous_departure_date = ''
            duplicate_departure_count = 0
            
            try:
                calendarElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sheet__data')))
                
                departureItems = calendarElement.find_elements_by_class_name('sheet__data__wrapper')
                for departure in departureItems:
                        
                    departureData = departure.find_elements_by_class_name('data-label')
                        
                    date_numbers = departureData[0].get_attribute('innerHTML').split()
                    departure_date = '{:02}-{}-{}'.format(int(date_numbers[1]), date_numbers[0], year)
                    # print(departure_date)

                    if departure_date == previous_departure_date:                   # check if duplicate departure
                        duplicate_departure_count += 1
                    else:
                        duplicate_departure_count = 0

                    departure_letter = str(chr(duplicate_departure_count + 97))
                    day = '{:02}'.format(int(date_numbers[1]))
                    month = str(chr((datetime.strptime(date_numbers[0], '%b')).month + 64))
                    departure_code = '{}{}{}{}'.format(day, month, year, departure_letter)
                    departure_id = '{}-{}'.format(op_code, departure_code)
                    # print(departure_id)

                    departure_type = departureData[2].get_attribute('innerHTML')
                    string_to_write = [trip_name,departure_id,departure_date,'Type',departure_type]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)

                    actual_price = departureData[4].get_attribute('innerHTML').strip().replace(',', '')
                    string_to_write = [trip_name,departure_id,departure_date,'ActualPriceUSD',actual_price]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)

                    notes = departureData[5].get_attribute('innerHTML')
                    string_to_write = [trip_name,departure_id,departure_date,'Notes',notes]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)

                    if notes == 'Soldout':
                        status = 'Sold Out'
                        available = False
                    elif notes == 'Not Available':
                        status = 'Cancelled'
                        available = False
                    elif notes == 'Limited':
                        status = 'Limited'
                        available = True
                    elif notes == 'Available':
                        status = 'Available'
                        available = True
                    else:
                        status = 'UNRECOGNIZED STATUS'
                    string_to_write = [trip_name,departure_id,departure_date,'Status',status]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)
                    string_to_write = [trip_name,departure_id,departure_date,'Available',available]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)

                    previous_departure_date = departure_date

                    # print()


            finally:
                driver.quit()
        
        
    new_file.close()

    print("\nDone!\n")

if __name__ == '__main__': main()