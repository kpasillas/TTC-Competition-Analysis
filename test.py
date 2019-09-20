#!/usr/bin/env python3

import requests
import bs4
import re

def main():
    res = requests.get('https://www.globusjourneys.com/tour/canyon-country-adventure/av/?nextyear=true&content=price')

    soup = bs4.BeautifulSoup(res.text, 'lxml')

    # departure = soup.find('div', class_='listing')

    # date_numbers = departure.find('p', class_='date-numbers').text.split()
    # print("Departure Date: {}-{}-{}".format(date_numbers[0], date_numbers[1], date_numbers[2]))

    # actual_price = departure.find('p', class_='price-actual').text
    # print(actual_price)

    # if departure.find('p', class_='price-strike') != None:
    #     original_price = departure.find('p', class_='price-strike').text
    # else:
    #     original_price = None
    # print(original_price)

    # if departure.find('div', class_='popular-message') != None:
    #     popular_departure = departure.find('div', class_='popular-message').text
    # else:
    #     popular_departure = "False"
    # print(popular_departure)

    # listing_status = departure.find('div', class_='listing-status').text
    # print(listing_status)

    # if departure.find('div', class_='listing-buttons-contain').text != None:
    #     available_status = departure.find('div', class_='listing-buttons-contain').text
    #     print((available_status))

    trip_name = soup.find("h1").text

    for departure in soup.find_all('div', class_='listing'):

        date_numbers = departure.find('p', class_='date-numbers').text.split()
        
        actual_price = departure.find('p', class_='price-actual').text.strip()
        
        if departure.find('p', class_='price-strike') == None:
            original_price = None
        else:
            original_price = departure.find('p', class_='price-strike').text
        
        if departure.find('div', class_='popular-message'):
            popular_departure = True
        else:
            popular_departure = False
        
        listing_status = departure.find('div', class_='listing-status').text.strip()
        
        if re.search( "Not Available", departure.find('div', class_='listing-buttons-contain').text):
            available_status = False
        else:
            available_status = True
        

        # print("Departure Date: {}-{}-{}, ".format(date_numbers[0], date_numbers[1], date_numbers[2]))
        # print("Actual Price: {}".format(actual_price))
        # print("Original Price: {}".format(original_price))
        # print("Popular Departure: {}".format(popular_departure))
        # print("Listing Status: {}".format(listing_status))
        # print("Available Status: {}".format(available_status))
        print("Trip Name: {}, ".format(trip_name), "Departure Date: {}-{}-{}, ".format(date_numbers[0], date_numbers[1], date_numbers[2]), "Actual Price: {}, ".format(actual_price), "Original Price: {}, ".format(original_price), "Popular Departure: {}, ".format(popular_departure), "Listing Status: {}".format(listing_status), "Available Status: {}".format(available_status))
    
if __name__ == '__main__': main()
