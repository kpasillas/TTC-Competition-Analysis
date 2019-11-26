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
    file_name = 'cosmos_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','Departure Date','field','value']
        csv_writer.writerow(field_names)

        linksUS = (
            'https://www.cosmos.com/tour/alaska-the-yukon/8360/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/americas-greatest-treasure-with-rapid-city-start/8855/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/atlantic-canadas-coastal-wonders/8820/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/brazil-argentina-chile-unveiled/1100/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/brazil-argentina-chile-unveiled-with-peru/1105/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/canadian-train-odyssey-with-alaska-cruise/8965/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/canadian-train-odyssey/8960/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/circle-the-american-west/8160/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/cities-of-the-great-east/8460/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/classic-new-england-with-400th-mayflower-sailing/8105/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/classic-new-england/8100/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/dixieland-rhythms/8240/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/eastern-us-canada-grand-vacation/8200/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/exploring-americas-national-park/8620/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/exploring-the-eastern-seaboard/8310/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/geysers-to-glaciers/8710/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/golden-west-adventure/8500/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/grand-alaskan-adventure/8420/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/hawaiian-islands/8140/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/heart-of-the-canadian-rockies-with-alaska-cruise/8915/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/heart-of-the-canadian-rockies-with-calgary-stampede/8550/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/heart-of-the-canadian-rockies/8910/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/high-desert-discovery/8120/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/highlights-of-route-66-with-mother-road-albuquerque-balloon-fiesta/8580/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/highlights-of-route-66/8530/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/highlights-of-the-canyonlands/8520/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/historic-trails-blue-ridge-mountains/8720/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/mysteries-of-the-inca-empire/1300/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/national-parks-canyon-country-with-rapid-city-start/8605/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/new-york-niagara-falls-washington-dc/8000/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/ontario-french-canada/8330/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/rocky-mountain-discovery-with-rail/8630/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/southern-sounds/8730/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/the-best-of-brazil-argentina/1000/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/the-canadian-rockies-with-alaska-cruise/8904/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/the-canadian-rockies/8900/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/the-lone-star-state-to-the-french-quarter/8090/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/the-old-south-florida/8290/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/ultimate-south-america/1200/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/via-rail-and-the-canadian-rockies-with-alaska-cruise/8940/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/western-canada-by-rail-with-alaska-cruise/8934/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/western-canada-with-inside-passage-calgary-stampede/8385/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/western-canada-with-inside-passage/8380/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/western-wonders/8510/?nextyear=true&content=price'
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

            linkAU = "https://www.cosmostours.com.au/booking?tour={}&season=2020".format(code)
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