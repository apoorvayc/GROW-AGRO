import time

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import presence_of_element_located
# Data manipulation
import pandas as pd
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
webdriver_path = 'C:/WebDriver/chromedriver.exe'  # Enter the file directory of the Chromedriver
browser = webdriver.Chrome(webdriver_path, options=options)
url = 'https://greenharvest.com.au/SeedOrganic/SeedsPerGram.html'
browser.get(url)
time.sleep(5)
t = browser.find_elements_by_xpath("/html/body/div/div[2]/div/table/tbody/tr")
t1 = browser.find_elements_by_xpath("/html/body/div/div[2]/div/table/tbody/tr[1]/td")
x1, x2 = [], []
for i in range(2,len(t)+1) :
        x = browser.find_elements_by_xpath("/html/body/div/div[2]/div/table/tbody/tr["+str(i)+"]/td")
        spg = x[1].text[:-7].replace(" ","")
        try :
            z = spg.index("-")
            spg = spg[:z]
        except :
            pass
        try :
            if not spg[-1].isdigit() :
                continue
        except :
            pass
        x1.append(x[0].text.upper())
        x2.append(spg)
df_spg = pd.DataFrame(zip(x1,x2),columns=["Seed","SPG"])

query = "watermelon"
search_item = query + " seeds"
df = pd.DataFrame(columns=['Name', 'Quantity', 'Price', 'Ratio', 'Link'])
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
r
browser = webdriver.Chrome(webdriver_path, options=options)
url = 'https://www.bighaat.com/'
browser.get(url)
search_bar = browser.find_element_by_name('q')
search_bar.send_keys(search_item, Keys.RETURN)

links = []
try:
    t = browser.find_elements_by_xpath("//a[@class='product-grid-item']")
    links = [t1.get_attribute('href') for t1 in t]
except:
    t = []
    pass
for number, i in enumerate(t):
    para = i.find_elements_by_css_selector('p')
    cost = i.find_elements_by_css_selector('small')
    q = ""
    try:
        if query.split()[0].upper() not in para[0].text.upper():
            continue
        print(para[0].text)
        x2 = ""
        for q in para[2].text:
            if q.isdigit():
                x2 += str(q)
            else:
                break
        x2 = float(x2)
        if para[2].text[len(para[2].text) - 3:len(para[2].text)] == "gms":
            m = df_spg[df_spg['Seed'] == query.upper()].index[0]
            n = df_spg.at[m, 'SPG']
            x2 = x2 * int(n)
            quantity = str(x2) + " seeds"
        elif para[2].text[len(para[2].text) - 5:len(para[2].text)] == "seeds":
            quantity = para[2].text
        else:
            continue

        y = float(cost[0].text[2:].replace(",", ""))
        ratio = y / x2
        link = links[number]
        name = para[0].text
        company = para[1].text
        price = cost[0].text[2:]
        df = df.append({'Name': name, 'Quantity': quantity, 'Price': price, 'Ratio': ratio, 'Link': link},ignore_index=True)
    except:
        pass
print(df)
