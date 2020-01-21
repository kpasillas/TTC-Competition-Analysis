#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import bs4
import csv
from datetime import date
from tqdm import tqdm

def main():

    today = date.today()
    file_name = 'collette_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','Departure Date','field','value']
        csv_writer.writerow(field_names)
        # print(field_names)
    
        linkUS = (
            'https://www.gocollette.com/en/tours/north-america/usa/alaska-and-the-yukon/booking?b=1#step/1',        # Alaska & the Yukon
            'https://www.gocollette.com/en/tours/north-america/usa/alaska-discovery/booking?b=1#step/1',        # Alaska Discovery Land & Cruise
            'https://www.gocollette.com/en/tours/north-america/usa/alaskas-northern-lights/booking?b=1#step/1',     # Alaska's Northern Lights
            'https://www.gocollette.com/en/tours/north-america/usa/alaskas-northern-lights-featuring-iditarod-race/booking?b=1#step/1',     # Alaska's Northern Lights with Iditarod
            'https://www.gocollette.com/en/tours/north-america/usa/albuquerque-balloon-fiesta/booking?b=1#step/1',      # Albuquerque Balloon Fiesta
            'https://www.gocollette.com/en/tours/north-america/usa/americas-cowboy-country/booking?b=1#step/1',     # America’s Cowboy Country
            'https://www.gocollette.com/en/tours/north-america/usa/americas-music-cities/booking?b=1#step/1',       # America’s Music Cities
            'https://www.gocollette.com/en/tours/north-america/usa/americas-music-cities-jazz-festival/booking?b=1#step/1',     # America’s Music Cities with Jazz Fest
            'https://www.gocollette.com/en/tours/north-america/usa/americas-music-cities-holiday/booking?b=1#step/1',       # America's Music Cities Holiday
            'https://www.gocollette.com/en/tours/north-america/usa/americas-national-parks-and-denver/booking?b=1#step/1',      # America's National Parks and Denver
            'https://www.gocollette.com/en/tours/north-america/usa/autumn-in-vermont/booking?b=1#step/1',       # Autumn in Vermont
            'https://www.gocollette.com/en/tours/north-america/usa/bluegrass-smoky-mountains/booking?b=1#step/1',       # Bluegrass Country & the Smoky Mountains
            'https://www.gocollette.com/en/tours/north-america/canada/canadian-rockies--glacier-national-park/booking?b=1#step/1',      # Canadian Rockies & Glacier National Park
            'https://www.gocollette.com/en/tours/north-america/canada/canadian-rockies-glacier-national-park-with-calgary-stampede/booking?b=1#step/1',     # Canadian Rockies & Glacier National Park with Calgary Stampede
            'https://www.gocollette.com/en/tours/north-america/canada/canadian-rockies-by-train/booking?b=1#step/1',        # Canadian Rockies by Train
            'https://www.gocollette.com/sitecore/content/interval/tours/north-america/canada/canadian-rockies-by-train-with-calgary-stampede/booking?b=1&sc_lang=en#step/1',        # Canadian Rockies by Train with Calgary Stampede
            'https://www.gocollette.com/en/tours/north-america/canada/canadian-rockies-featuring-rocky-mountaineer/booking?b=1#step/1',     # Canadian Rockies with Rocky Mountaineer
            'https://www.gocollette.com/en/tours/north-america/canada/canadian-rockies-featuring-rocky-mountaineer-with-calgary-stampede/booking?b=1#step/1',       # Canadian Rockies with Rocky Mountaineer and Calgary Stampede
            'https://www.gocollette.com/en/tours/north-america/usa/canyon-country/booking?b=1#step/1',      # Canyon Country
            'https://www.gocollette.com/sitecore/content/interval/tours/north-america/canada/charming-french-canada/booking?b=1&sc_lang=en#step/1',     # Charming French Canada
            'https://www.gocollette.com/sitecore/content/interval/tours/north-america/usa/colors-of-new-england/booking?b=1&sc_lang=en#step/1',     # Colors of New England
            'https://www.gocollette.com/en/tours/north-america/usa/colors-of-new-england-featuring-portland/booking?b=1#step/1',        # Colors of New England with Portland, Maine
            'https://www.gocollette.com/en/tours/south-america/costa-rica/costa-rica/booking?b=1#step/1',       # Costa Rica: A World of Nature
            'https://www.gocollette.com/en/tours/north-america/usa/hawaiian-adventure/booking?b=1#step/1',      # Hawaiian Adventure
            'https://www.gocollette.com/sitecore/content/interval/tours/north-america/usa/heritage-of-america/booking?b=1&sc_lang=en#step/1',       # Heritage of America
            'https://www.gocollette.com/en/tours/north-america/usa/heritage-of-america-international-tattoo/booking?b=1#step/1',        # Heritage of America with Virginia International Tattoo
            'https://www.gocollette.com/en/tours/south-america/argentina/highlights-of-south-america/booking?b=1#step/1',       # Higlights of South America Featuring Buenos Aires, Iguazu Falls & Rio de Janeiro
            'https://www.gocollette.com/en/tours/north-america/usa/islands-of-new-england/booking?b=1#step/1',      # Islands of New England
            'https://www.gocollette.com/en/tours/south-america/argentina/journey-through-south-america/booking?b=1#step/1',     # Journey Through South America Featuring Santiago, Andean Lakes Crossing & Rio de Janeiro
            'https://www.gocollette.com/en/tours/south-america/peru/peru-and-galapagos-by-yacht/booking?b=1#step/1',        # Machu Picchu & Galapagos Wonders featuring a 4-Night Cruise
            'https://www.gocollette.com/en/tours/south-america/ecuador/galapagos-islands/booking?b=1#step/1',       # Machu Picchu & the Galapagos Islands
            'https://www.gocollette.com/en/tours/south-america/peru/peru-and-galapagos-by-yacht-3-nights/booking?b=1#step/1',       # Machu Picchu & the Galapagos Islands Featuring a 3-Night Cruise & 1-Night Island Stay
            'https://www.gocollette.com/en/tours/north-america/usa/mackinac-island/booking?b=1#step/1',     # Mackinac Island
            'https://www.gocollette.com/en/tours/north-america/usa/mackinac-island-with-tulip-festival/booking?b=1#step/1',     # Mackinac Island with Tulip Festival
            'https://www.gocollette.com/en/tours/north-america/canada/maritimes-coastal-wonders/booking?b=1#step/1',        # Maritimes Coastal Wonders
            'https://www.gocollette.com/en/tours/north-america/usa/bluegrass-smoky-mountains-holiday/booking?b=1#step/1',       # Nashville & the Smoky Mountains Holiday
            'https://www.gocollette.com/en/tours/north-america/usa/national-parks/booking?b=1#step/1',      # National Parks of America
            'https://www.gocollette.com/en/tours/north-america/usa/pacific-northwest--california/booking?b=1#step/1',       # Pacific Northwest & California
            'https://www.gocollette.com/en/tours/north-america/usa/painted-canyons-of-the-west/booking?b=1#step/1',     # Painted Canyons of the West
            'https://www.gocollette.com/en/tours/south-america/argentina/patagonia/booking?b=1#step/1',     # Patagonia: Edge of the World Featuring Argentina, Chile and a 4 Night Patagonia Cruise
            'https://www.gocollette.com/en/tours/south-america/peru/peru-ancient-land-of-mysteries-featuring-puno/booking?b=1#step/1',      # Peru: Ancient Land of Mysteries
            'https://www.gocollette.com/en/tours/south-america/peru/peru-ancient-land-of-mysteries/booking?b=1#step/1',     # Peru: From Lima to the Sacred Valley
            'https://www.gocollette.com/en/tours/north-america/usa/roaming-coastal-maine/booking?b=1#step/1',       # Roaming Coastal Maine
            'https://www.gocollette.com/en/tours/north-america/usa/southern-charm/booking?b=1#step/1',      # Southern Charm
            'https://www.gocollette.com/en/tours/north-america/usa/southern-charm-holiday/booking?b=1#step/1',      # Southern Charm Holiday
            'https://www.gocollette.com/en/tours/north-america/canada/spotlight-on-montreal/booking?b=1#step/1',        # Spotlight on Montréal
            'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-nashville/booking?b=1#step/1',      # Spotlight on Nashville
            'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-new-orleans/booking?b=1#step/1',        # Spotlight on New Orleans
            'https://www.gocollette.com/sitecore/content/interval/tours/north-america/usa/spotlight-on-new-orleans-holiday/booking?b=1&sc_lang=en#step/1',      # Spotlight on New Orleans Holiday
            'https://www.gocollette.com/sitecore/content/interval/tours/north-america/usa/spotlights-on-new-orleans-carnival/booking?b=1&sc_lang=en#step/1',        # Spotlight on New Orleans with Carnival
            'https://www.gocollette.com/sitecore/content/interval/tours/north-america/usa/spotlight-on-new-orleans-jazz-festival/booking?b=1&sc_lang=en#step/1',        # Spotlight on New Orleans with Jazz Fest
            'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-new-york/booking?b=1#step/1',       # Spotlight on New York City
            'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-new-york-holiday/booking?b=1#step/1',       # Spotlight on New York City Holiday
            'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-san-antonio/booking?b=1#step/1',        # Spotlight on San Antonio
            'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-san-antonio-holiday/booking?b=1#step/1',        # Spotlight on San Antonio Holiday
            'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-san-antonio-stock-show-and-rodeo/booking?b=1#step/1',       # Spotlight on San Antonio with Stock Show
            'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-santa-fe/booking?b=1#step/1',       # Spotlight on Santa Fe
            'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-santa-fe-holiday/booking?b=1#step/1',       # Spotlight on Santa Fe Holiday
            'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-south-dakota/booking?b=1#step/1',       # Spotlight on South Dakota
            'https://www.gocollette.com/en/tours/north-america/usa/spotlight-on-washington-dc/booking?b=1#step/1',      # Spotlight on Washington, D.C.
            'https://www.gocollette.com/en/tours/north-america/canada/the-best-of-eastern-canada/booking?b=1#step/1',       # The Best of Eastern Canada
            'https://www.gocollette.com/en/tours/north-america/usa/the-colorado-rockies/booking?b=1#step/1',        # The Colorado Rockies
            'https://www.gocollette.com/en/tours/south-america/costa-rica/tropical-costa-rica/booking?b=1#step/1',      # Tropical Costa Rica
            'https://www.gocollette.com/en/tours/north-america/usa/washington-dc-niagara-falls-new-york-city/booking?b=1#step/1',       # Washington D.C., Niagara Falls & NYC
            'https://www.gocollette.com/en/tours/north-america/usa/winter-in-yellowstone/booking?b=1#step/1',       # Winter in Yellowstone
            'https://www.gocollette.com/en/tours/north-america/canada/newfoundland-and-labrador/booking?b=1#step/1'        # Wonders of Newfoundland
        )

        print("\n")

        for link in tqdm(linkUS):
        
            driver = webdriver.Chrome()
            driver.get(link)

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

                        if soup.find('div', class_='date-alert'):
                            notes = soup.find('div', class_='date-alert').text.strip()
                            string_to_write = [trip_name,departure_date,'Notes',notes]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                        actual_price = soup.find('span', class_='discountedPrice').text.strip()
                        string_to_write = [trip_name,departure_date,'Actual Price USD',actual_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

                        if soup.find('span', class_='crossout'):
                            original_price = soup.find('span', class_='crossout').text.strip()
                        else:
                            original_price = actual_price
                        string_to_write = [trip_name,departure_date,'Original Price USD',original_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

            finally:
                driver.quit()

            split_link = link.split('/')
            linkAU = '{}//{}/{}-au/{}/{}/{}/{}/{}/{}'.format(split_link[0], split_link[2], split_link[3], split_link[4], split_link[5], split_link[6], split_link[7], split_link[8], split_link[9])
            # print(linkAU)

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

                        actual_price = soup.find('span', class_='discountedPrice').text.strip()
                        string_to_write = [trip_name,departure_date,'Actual Price AUD',actual_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

                        if soup.find('span', class_='crossout'):
                            original_price = soup.find('span', class_='crossout').text.strip()
                        else:
                            original_price = actual_price
                        string_to_write = [trip_name,departure_date,'Original Price AUD',original_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

            finally:
                driver.quit()

    new_file.close()

    print("\nDone!\n")

if __name__ == '__main__': main()