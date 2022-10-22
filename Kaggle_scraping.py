
# Import libraries
import requests
import pandas as pd
import time
import os
import sys
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller

def switchIP():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM)
        print("New Tor connection processed")
        
def get_tor_session():
    session = requests.session()
    session.proxies = {}
    session.proxies['http'] = 'socks5://localhost:9150' #9150 for browser; 9050 for TOR service
    session.proxies['https'] = 'socks5://localhost:9150'
    print("New Tor session processed") 
    #print(f"New IP is:", session.get("http://httpbin.org/ip").text)  # uncomment to test how ip changes.
    return session

def download_kaggle_pages_tor(folder, users):  
    session = get_tor_session()
    for i, user in enumerate(users.UserName):
        headers = {"User_Agent":UserAgent().random}
        url = session.get("https://www.kaggle.com/{}".format(user),headers=headers) # get url      
        
        if url.status_code==200:
            page = url.content.decode()
            with open(f'{folder}/{user}_kaggle.txt', 'w', encoding="utf-8") as f:
                f.write(page)      
            
        else:
            switchIP()
            session = get_tor_session()
            print(f"Iteration number: {i+1}, Skip user: {user}")
            print(f"Error code: {url.status_code}, Wait for 1 minute")
            time.sleep(60)
        time.sleep(1) 

            

if __name__ == "__main__":
    users = pd.read_csv("Users.csv") # change this path if needed to locate Users.csv   
    performanceTiers = dict()
    for k,v in users.groupby('PerformanceTier'):
        performanceTiers[k]=v
        print(f"Size of tier {k} is {v.shape[0]}")

    for name, df in sorted(performanceTiers.items(),reverse=True):
        folder = f'kaggle_pages/{name}'
        if not os.path.exists(folder):
            os.makedirs(folder)

        collect = df # select which records to collect        
        temp = 0
        while collect.shape[0]!=temp: # Break from while if the current #ofrecords to collect is equal to the previous #ofrecords to collect
            # It means that we could not collect any new records in this while loop, because
            # we could not find kaggle pages for users which are left in the collect. (kaggle.com/user gives 404) 
            # This could happen if they have deleted their accounts, and our users.csv is outdated.

            collected=[] #records which were collected prior to this while loop
            temp = collect.shape[0] # temp saves number of records to collect 
            
            for file in os.listdir(folder): # look for users which we have already collected
                user = os.path.splitext(file)[0].split(sep='_')[0] #parse username from filename
                collected.append(user)  # append user to collected
            collect = collect[~collect['UserName'].isin(collected)] # Collect users which we didn't collect before 
                                                                    #collect are NOT in collected. 
            
            try:
                download_kaggle_pages_tor(folder, collect) 

                # Scraping without using TOR: speed will
                # throttle after collecting first ~400 users, and you will have to wait a long delays (10 minutes by default) 
                # between collecting each 50-200 users. Scraping speed will be approximately ~400-600 users per hour
                # With TOR we can achieve more than 1000 users per hour and don't wait for delays, by simply switching IP.
            except:
                print(sys.exc_info()[0], "occurred.") # Catch exception, but still continue collecting data (e.g. internet error)
                if(sys.exc_info()[0]==KeyboardInterrupt): # Break from loop by KeyboardInterrupt
                    break
            print('*********************Collected batch, wait 5 minutes***************************')
            time.sleep(300)
        print(f'********************* Finished tier {name} *********************')