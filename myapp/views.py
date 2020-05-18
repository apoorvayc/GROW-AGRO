import os
import time
from pathlib import Path
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from selenium import webdriver
from selenium.common.exceptions import *
import pandas as pd
from tkinter import Image
from firebase import firebase
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import ExtraTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from warnings import simplefilter



import pydotplus as pydotplus
from io import StringIO
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
# Visualization
from selenium.webdriver.common.keys import Keys
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')





# seeds per gram dataframe
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
webdriver_path = 'C:\\Users\\apoorvayc\\Downloads\\chromedriver_win32\\chromedriver.exe'  # Enter the file directory of the Chromedriver
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
browser.close()

# Create your views here
@csrf_exempt
def home(request) :

    if request.method == "POST" :
        query = request.POST['query']
        return price_comp(query)
    return render(request, "home.html",{"message": " " })
    
def price_comp(query):
    search_item = query + " seeds"
    df = pd.DataFrame(columns=['Name', 'Quantity', 'Price', 'Ratio', 'Link'])
##################### BIGHAAT ######################
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    webdriver_path = 'C:\\Users\\apoorvayc\\Downloads\\chromedriver_win32\\chromedriver.exe'  # Enter the file directory of the Chromedriver
    browser = webdriver.Chrome(webdriver_path, options=options)
    url = 'https://www.bighaat.com/'
    browser.get(url)
    search_bar = browser.find_element_by_name('q')
    search_bar.send_keys(search_item, Keys.RETURN)
    time.sleep(5)
    links = []
    try :
        t = browser.find_elements_by_xpath("//a[@class='product-grid-item']")
        links = [t1.get_attribute('href') for t1 in t]
    except :
        t = []
        pass
    for number,i in enumerate(t) :
        para = i.find_elements_by_css_selector('p')
        cost = i.find_elements_by_css_selector('small')
        q = ""
        try :
            if query.split()[0].upper() not in para[0].text.upper() :
                continue
            print(para[0].text)
            x2 = ""
            for q in para[2].text :
                if q.isdigit() :
                    x2 += str(q)
                else :
                    break
            x2 = float(x2)
            if para[2].text[len(para[2].text)-3:len(para[2].text)] == "gms" :
                m = df_spg[df_spg['Seed'] == query.upper()].index[0]
                n = df_spg.at[m,'SPG']
                x2 = x2*int(n)
                quantity = str(x2) + " seeds"
            elif para[2].text[len(para[2].text)-5:len(para[2].text)] == "seeds" :
                quantity = para[2].text
            else :
                continue

            y = float(cost[0].text[2:].replace(",",""))
            ratio = y/x2
            link = links[number]
            name = para[0].text
            company = para[1].text
            price = cost[0].text[2:]
            df = df.append({'Name': name, 'Quantity': quantity, 'Price': price, 'Ratio': ratio, 'Link': link}, ignore_index=True)


            print([name, quantity, price, ratio, link])


        except :
            pass

#####################AGRIBEGRI#####################
    print("hi")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    agribegri_url = 'https://agribegri.com/'
    browser.get(agribegri_url)
    time.sleep(5)
    search_bar = browser.find_element_by_id('search_product')
    search_bar.send_keys(search_item, Keys.RETURN)
    time.sleep(5)
    i = 1
    x = []
    y = []
    try :
        x = browser.find_elements_by_xpath(
            "/html/body/section/div/div/div/div/div[2]/div[2]/ul/li[" + str(i) + "]/div[2]/div/div/div[1]/h4[1]")
        y = browser.find_elements_by_xpath(
            "/html/body/section/div/div/div/div/div[2]/div[2]/ul/li[" + str(i) + "]/div[2]/div/div/div[1]/div/p[2]")
        t = browser.find_element_by_xpath('//*[@id="all-products"]/li[' + str(i) + ']/div[2]/a')
    except :
        pass
    while x and y:
        cost = y[0].text.split()[-1]
        str1 = str(x[0].text.split()[-2]) + " " + str(x[0].text.split()[-1])
        namee = x[0].text.replace(str1, "")
        try :
            print(namee)
            if query.split()[0].upper() not in namee.replace(" ", "").upper():
                i += 1
                x = browser.find_elements_by_xpath(
                    "/html/body/section/div/div/div/div/div[2]/div[2]/ul/li[" + str(
                        i) + "]/div[2]/div/div/div[1]/h4[1]")
                y = browser.find_elements_by_xpath(
                    "/html/body/section/div/div/div/div/div[2]/div[2]/ul/li[" + str(
                        i) + "]/div[2]/div/div/div[1]/div/p[2]")

                continue
            x5 = []
            for q in str1:
                if q.isdigit():
                    x5.append(int(q))
                else:
                    break

            x6 = ""
            for val in x5:
                x6 += str(val)
            x6 = int(x6)
            print("step 3", x6)

            if str1[len(str1) - 2:len(str1)].upper() == "GM":
                m = df_spg[df_spg['Seed'] == query.upper()].index[0]
                n = df_spg.at[m, 'SPG']
                x6 = x6 * int(n)

                print("step 4.1", x6)

            print(namee)
            name = namee
            company = "-"
            price = cost
            rat = float(cost) / x6
            ratio = rat
            quantity = str1
            link = t.get_attribute('href')
            df = df.append({'Name': name, 'Quantity': quantity, 'Price': price, 'Ratio': ratio, 'Link': link}, ignore_index=True)
            print([name, quantity, price, ratio, link])



            i += 1
            try:
                x = browser.find_elements_by_xpath("/html/body/section/div/div/div/div/div[2]/div[2]/ul/li[" + str(
                    i) + "]/div[2]/div/div/div[1]/h4[1]")
                y = browser.find_elements_by_xpath("/html/body/section/div/div/div/div/div[2]/div[2]/ul/li[" + str(
                    i) + "]/div[2]/div/div/div[1]/div/p[2]")
                t = browser.find_element_by_xpath('//*[@id="all-products"]/li[' + str(i) + ']/div[2]/a')
                # link.append(t.get_attribute('href'))
            except:
                break

        except:

            i += 1
            try:
                x = browser.find_elements_by_xpath("/html/body/section/div/div/div/div/div[2]/div[2]/ul/li[" + str(
                    i) + "]/div[2]/div/div/div[1]/h4[1]")
                y = browser.find_elements_by_xpath("/html/body/section/div/div/div/div/div[2]/div[2]/ul/li[" + str(
                    i) + "]/div[2]/div/div/div[1]/div/p[2]")
                t = browser.find_element_by_xpath('//*[@id="all-products"]/li[' + str(i) + ']/div[2]/a')
                # link.append(t.get_attribute('href'))
            except:
                break


    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    url = 'https://www.flipkart.com/'
    browser.get(url)
    search_bar = browser.find_element_by_name('q')
    search_bar.send_keys(search_item, Keys.RETURN)
    time.sleep(10)
    i = 1
    t1 = browser.find_elements_by_class_name('_2cLu-l')
    t2 = browser.find_elements_by_class_name('_1rcHFq')
    t3 = browser.find_elements_by_class_name('_1vC4OE')
    t4 = browser.find_elements_by_class_name('Zhf2z-')
    for i in range(len(t1)):
        # if query.upper() in t1[i].get_attribute('title').upper() :
        # print("yes")
        # print(t1[i].get_attribute('title').upper())
        if query.split()[0].upper() in t1[i].get_attribute('title').upper():

            x6 = ""
            for q in t2[i].text:
                if q.isdigit():
                    x6 += str(q)
                else:
                    break
            x6 = float(x6)
            quantity = x6
            price = (t3[i].text)[1:]
            company = "-"
            name = t1[i].get_attribute('title')
            link = t4[i].get_attribute('href')

            ratio = float((t3[i].text)[1:]) / x6
            df = df.append({'Name': name, 'Quantity': quantity, 'Price': price, 'Ratio': ratio, 'Link': link}, ignore_index=True)
    browser.close()
    print(df)
    optimal_ratio = df['Ratio'].min()
    optimal_link = df.at[df[df['Ratio']==optimal_ratio].index[0],'Link']
    # dfL = dfL.sort_values(by='Ratio')
    print(df)
    # dfL.to_csv('optimalwebiste2.csv')
    print(optimal_link)
    # dfL.to_csv('a1aa.csv')
    # my_file = Path('website1.csv')
    # if my_file.is_file():
    #     os.remove('combined_csv.csv')

    return redirect(optimal_link)
    #return render(request, "home.html",{"message": " " })
def price_comp2(request,msg) :
    return price_comp(msg)
def crop_pred(request):
    #Reading the csv file
    data=pd.read_csv('cpdata.csv')
    print(data.head(1))
    data = data.round()
    #Creating dummy variable for target i.e label
    label= pd.get_dummies(data.label).iloc[: , 1:]
    data= pd.concat([data,label],axis=1)
    data.drop('label', axis=1,inplace=True)
    print('The data present in one row of the dataset is')
    print(data.head(1))
    train=data.iloc[:, [0,1,2,3]].values
    test=data.iloc[: ,4:].values

    #Dividing the data into training and test set
    X_train,X_test,y_train,y_test=train_test_split(train,test,test_size=0.3)
    print(X_test)
    
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    print(X_test)
    #Importing Decision Tree classifier
    # from sklearn.tree import DecisionTreeRegressor
    # clf=DecisionTreeRegressor()
    
    # ignore all future warnings
    simplefilter(action='ignore', category=FutureWarning)
    # Support multilabel:
    


    model = []  
    model.append(DecisionTreeClassifier())
    model.append(ExtraTreeClassifier())
    model.append(ExtraTreesClassifier())
    model.append(KNeighborsClassifier())
    model.append(RadiusNeighborsClassifier())
    model.append(RandomForestClassifier())
    index = 0
    algo = ""
    a = []
    b = []
    for i in model :
        clf = i
        #Fitting the classifier into training set
        clf.fit(X_train,y_train)
        try :
            pred=clf.predict(X_test)
        except :
            pass
    
        # Finding the accuracy of the model
        a.append(accuracy_score(y_test,pred))
        b.append(i)
        print("The accuracy of this model is: ", accuracy_score(y_test,pred)*100)
    index2 = max(a)
    algo = b[a.index(index2)]
    print(index2,algo.__class__.__name__)
    # from sklearn.linear_model import LinearRegression
    # clf = LinearRegression()
    # clf.fit(X_train, y_train)
    # pred = clf.predict(X_test)
    # print(accuracy_score(y_test,pred.round())*100)

    # Using firebase to import data to be tested
    from firebase import firebase
    firebase =firebase.FirebaseApplication('https://cropit-eb156.firebaseio.com/')
    tp=firebase.get('/Realtime',None)


    ah=tp['Air Humidity']
    atemp=tp['Air Temp']
    shum=tp['Soil Humidity']
    pH=tp['Soil pH']
    rain=tp['Rainfall']


    l=[]
    l.append(atemp)
    l.append(ah)
    l.append(pH)
    l.append(rain)
    l = [33,64,pH,rain]

    predictcrop=[l]
    # Putting the names of crop in a single list
    crops=['wheat','mungbean','Tea','millet','maize','lentil','jute','cofee','cotton','ground nut','peas','rubber','sugarcane','tobacco','kidney beans','moth beans','coconut','blackgram','adzuki beans','pigeon peas','chick peas','banana','grapes','apple','mango','muskmelon','orange','papaya','watermelon','pomegranate']
    cr='rice'
    clf = algo
    clf.fit(train,test)
    pred=clf.predict(X_test)

    #Predicting the crop
    # predictions = algo.predict(predictcrop)
    predictcrop = sc.transform(predictcrop)
    predictions = clf.predict(predictcrop)
    count=0
    for i in range(0,30):
        if(predictions[0][i]==1):
            c=crops[i]
            print(i)
            count=count+1
            break
        i=i+1
    
    if(count==0):
        product=cr
        print('The predicted crop is %s'%cr)
    else:
        product=c
        print('The predicted crop is %s'%c)
    # b = [str(i._class.name_) for i in b]
    # plt.plot([i for i in range(1,len(a)+1)],a)
    # plt.xticks([i for i in range(1,len(a)+1)],b)
    # plt.xticks(rotation=45)
    # plt.grid(axis='x',linestyle='--')
    # plt.show()
    
    #return price_comp(product)     #Need to be added to directly give inout to price comparison module

    return render(request, "home.html",{"message": product })


