#!/usr/bin/env python3

import requests
import bs4

def main():
    res = requests.get('https://www.globusjourneys.com/tour/canyon-country-adventure/av/?nextyear=true&content=price')

    soup = bs4.BeautifulSoup(res.text, 'lxml')
    # print(soup.prettify())
    # print(soup.find_all(class_="date-numbers"))
    for link in soup.find_all(class_="date-numbers"):
        newTag = link
        dayStr = (newTag.contents[1].text).strip()
        monYrStr = newTag.contents[2].strip()
        monYrStr = monYrStr.replace(' ', '')
        monYrStr = monYrStr.replace('\r\n', '-')
        print("{}-{}".format(dayStr, monYrStr))

if __name__ == '__main__': main()
