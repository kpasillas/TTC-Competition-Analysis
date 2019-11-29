#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import bs4
import re
import csv
from datetime import date
from time import sleep
from tqdm import tqdm

def main():

    today = date.today()
    file_name = 'tauck_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','Departure Date','field','value']
        csv_writer.writerow(field_names)


        linksUS = (
            'https://www.tauck.com/tours/celebration-of-roses-escorted-tour-event?tcd=vr2020',
            'https://www.tauck.com/tours/call-of-wild-alaska-guided-family-tour?tcd=ya2020',
            'https://www.tauck.com/tours/inside-passage-alaska-small-ship-cruise?tcd=xan2020',
            'https://www.tauck.com/tours/american-canyonlands-grand-canyon-escorted-tour?tcd=cy2020',
            'https://www.tauck.com/tours/antarctica-cruise?tcd=xr2020',
            'https://www.tauck.com/tours/best-of-canadian-rockies-escorted-tour?tcd=br2020',
            'https://www.tauck.com/tours/bluegrass-blue-ridges-louisville-kentucky-escorted-tour?tcd=ky2020',
            'https://www.tauck.com/tours/bugaboos-adventure-canadian-rockies-guided-tour?tcd=bg2020',
            'https://www.tauck.com/tours/gold-coast-california-escorted-tour?tcd=ca2020',
            'https://www.tauck.com/tours/canada-capitals-niagara-falls-escorted-tours?tcd=cn2020',
            'https://www.tauck.com/tours/canadian-maritimes-nova-scotia-cruise-and-escorted-tour?tcd=cm2020'
            'https://www.tauck.com/tours/canadian-rockies-glacier-national-park-escorted-tour?tcd=cr2020',
            'https://www.tauck.com/tours/canadian-rockies-whistler-victoria-escorted-tour?tcd=gc2020',
            'https://www.tauck.com/tours/cape-cod-newport-new-england-escorted-tour-and-cruise?tcd=cc2020',
            'https://www.tauck.com/tours/boulder-denver-colorado-escorted-tours?tcd=cl2020',
            'https://www.tauck.com/tours/costa-rica-pura-vida-escorted-tour?tcd=co2020',
            'https://www.tauck.com/tours/jungles-rainforests-costa-rica-guided-family-vacation?tcd=yo2020',
            'https://www.tauck.com/tours/cowboy-country-wyoming-escorted-family-vacation?tcd=yyn2020',
            'https://www.tauck.com/tours/cruising-the-galapagos-islands-cruise?tcd=ed2020',
            'https://www.tauck.com/tours/chicago-toronto-great-lakes-cruise?tcd=gle2020',
            'https://www.tauck.com/tours/connecting-people-culture-escorted-cuba-tour?tcd=cv2020',
            'https://www.tauck.com/tours/empire-of-incas-peru-bolivia-escorted-tour?tcd=pb2020',
            'https://www.tauck.com/tours/essence-of-south-america-brazil-argentina-escorted-tours?tcd=es2020',
            'https://www.tauck.com/tours/wildlife-wonderland-galapagos-escorted-family-tour?tcd=yg2020',
            'https://www.tauck.com/tours/grand-alaska-guided-tour-and-cruise?tcd=al2020',
            'https://www.tauck.com/tours/grand-canadian-rockies-escorted-tour?tcd=rre2020',
            'https://www.tauck.com/tours/grand-new-england-fall-foliage-guided-tour?tcd=gr2020',
            'https://www.tauck.com/tours/hidden-galapagos-peru-escorted-tour?tcd=eb2020',
            'https://www.tauck.com/tours/hidden-gems-new-england-guided-tour?tcd=ne2020',
            'https://www.tauck.com/tours/freedom-footsteps-philidelphia-washington-dc-guided-tour?tcd=wb2020',
            'https://www.tauck.com/tours/legends-american-west-national-park-escorted-tour?tcd=jh2020',
            'https://www.tauck.com/tours/san-francisco-yosemite-majestic-california-guided-family-tour?tcd=yp2020',
            'https://www.tauck.com/tours/manitoba-polar-bear-tours?tcd=vm2020',
            'https://www.tauck.com/tours/michigan-lakes-mackinac-island-escorted-tour?tcd=mi2020',
            'https://www.tauck.com/tours/mystical-peru-family-vacation-package?tcd=zp2020',
            'https://www.tauck.com/tours/land-of-enchantment-new-mexico-escorted-tour?tcd=nm2020',
            'https://www.tauck.com/tours/mississippi-new-orleans-plantation-escorted-tour?tcd=nn2020',
            'https://www.tauck.com/tours/nova-scotia-prince-edward-island-escorted-tour-and-cruise?tcd=ac2020',
            'https://www.tauck.com/tours/pacific-northwest-escorted-tour?tcd=nw2020',
            'https://www.tauck.com/tours/patagonia-escorted-tour?tcd=pt2020',
            'https://www.tauck.com/tours/peru-galapagos-guided-tour?tcd=eg2020',
            'https://www.tauck.com/tours/red-rocks-painted-canyon-arizona-escorted-family-tour?tcd=yc2020',
            'https://www.tauck.com/tours/charleston-savannah-escorted-tours?tcd=cs2020',
            'https://www.tauck.com/tours/national-parks-southwest-escorted-tour?tcd=kd2020',
            'https://www.tauck.com/tours/nashville-history-of-country-music-tour?tcd=kn2020',
            'https://www.tauck.com/tours/best-of-hawaii-escorted-tour?tcd=hw2020',
            'https://www.tauck.com/tours/hudson-valley-escorted-tour?tcd=hv2020',
            'https://www.tauck.com/tours/costa-rica-and-panama-canal-cruise?tcd=pce2020',
            'https://www.tauck.com/tours/canadian-rockies-by-train?tcd=mt2020',
            'https://www.tauck.com/tours/wonderland-yellowstone-winter-escorted-tour?tcd=vw2020',
            'https://www.tauck.com/tours/wonders-canadian-rockies-escorted-tours?tcd=yr2020',
            'https://www.tauck.com/tours/grand-teton-yellowstone-escorted-tour?tcd=sln2020',
            'https://www.tauck.com/tours/american-safari-tetons-yellowstone-escorted-tour?tcd=vy2020',
            'https://www.tauck.com/tours/yosemite-and-sequoia-escorted-tour?tcd=km2020'
        )

        print()

        for link in tqdm(linksUS):

            driver = webdriver.Chrome()
            driver.get(link)

            nameElement = driver.find_element_by_tag_name('h1')
            soup = bs4.BeautifulSoup(nameElement.get_attribute('innerHTML'), 'lxml')
            trip_name = soup.contents[0].text.strip()
            # print(trip_name)
            
            try:
                calendarElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-pricing-availability__calendar')))
                
                monthItems = calendarElement.find_elements_by_class_name('month-item')
                for month in monthItems:
                    
                    ActionChains(driver).click(month).perform()
                    sleep(0.5)                                      # manually wait for departure info to load after month clicked, ideally replaced by 'WebDriverWait'
                    # monthElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sheet__data__wrapper')))

                    yearElement = month.find_element_by_class_name('label-year')
                    year = yearElement.get_attribute('innerHTML')
                    
                    departureItems = calendarElement.find_elements_by_class_name('sheet__data__wrapper')
                    for departure in departureItems:
                        
                        departureData = departure.find_elements_by_class_name('data-label')
                        
                        date_numbers = departureData[0].get_attribute('innerHTML').split()
                        departure_date = '{}-{}-{}'.format(date_numbers[1], date_numbers[0], year)
                        # print(departure_date)

                        departure_type = departureData[2].get_attribute('innerHTML')
                        string_to_write = [trip_name,departure_date,'Departure Type',departure_type]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

                        actual_price = departureData[4].get_attribute('innerHTML').strip()
                        string_to_write = [trip_name,departure_date,'Actual Price USD',actual_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

                        available_status = departureData[5].get_attribute('innerHTML')
                        string_to_write = [trip_name,departure_date,'Available Status',available_status]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

                        # print()


            finally:
                driver.quit()
        
        
    new_file.close()

    print("\nDone!\n")

if __name__ == '__main__': main()