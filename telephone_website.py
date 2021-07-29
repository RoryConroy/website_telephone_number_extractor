from bs4 import BeautifulSoup
import urllib
from urllib.request import Request, urlopen
import urllib.parse
from random import randint
import re
import pandas as pd
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

df = pd.read_csv("domains_in.csv")
print ("Loading an input file")


for index, row in df.iterrows():

    url = row['Website']

    if "http" not in url:
        url = "https://" + url

    #req = Request(url)
    #driver = webdriver.Chrome()


    #do not physcially open chromium browser
    options = Options()
    options.add_argument("--headless")


    driver = webdriver.Chrome(options=options)

    print("Checking a new website")
    print(url)

    try:
        print("Opening page")
        #html_page = urlopen(req, timeout = 5)
        html_page = driver.get(url)
        driver.set_page_load_timeout(5)

    except:
        print("Page Load Error")
        found = "Website Not Working"
        driver.quit()

    else:
        print("Page opened successfully")

        #soup = BeautifulSoup(html_page, "lxml")
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        links = []

        print("Finding all the links, getting rid of dups and irrelevant links")


        for link in soup.find_all('a'):
            print (link.get('href'))
            if link.get('href'):
                if "jpg" not in link.get('href'):
                    if "facebook" not in link.get('href'):
                        if "mailto" not in link.get('href'):
                            if "instagram" not in link.get('href'):
                                if "linkedin" not in link.get('href'):
                                    if "goo.gl " not in link.get('href'):
                                        if "mp4" not in link.get('href'):
                                            if "youtube" not in link.get('href'):
                                                if "png" not in link.get('href'):
                                                    if "#" not in link.get('href'):
                                                        links.append(link.get('href'))
        
        links = list(dict.fromkeys(links))
        print(links)

        found = "False"
        if len(links) > 60:
            print("Too many links.. Skipping...")
            found = "60 Redirects"
            pass

        else:
        
            def get_phone(soup):
                for link in links:
                    print("Checking out link")

                    time.sleep(randint(1, 2))
                    link = urllib.parse.urljoin(url, link)

                    print(link)
                    
                    req = Request(link)

                    try:
                        print("Pulling the link")

                        html_page = urlopen(req, timeout = 5)
                        soup = BeautifulSoup(html_page, "lxml")

                        try:
                            phone = soup.select("a[href*=callto]")[0].text
                            return phone
                        except:
                            pass

                        try:
                            phone = soup.select("a[href*=tel]")[0].text
                            return phone
                        except:
                            pass

                        try:
                            phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-][2-9][0-9]{2}[-][0-9]{4}\b', response.text)[0]
                            return phone
                        except:
                            pass
                            
                        try:
                            phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b', response.text)[-1]
                            return phone
                        

                        except:
                            print ('Phone number not found')
                            phone = ''
                            return phone
                        driver.quit()
                    except Exception as e:
                        print("Not sure what this exception is")
                        print (e)

            print("Finished with a website")
            phone = get_phone(soup)


            df.at[index, 'Phone_number'] = phone
            df.to_csv("domains_out.csv")

print(df)
df.to_csv("domains_out.csv")