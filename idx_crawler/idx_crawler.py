from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json, timeit, openpyxl
import pandas as pd


# Define Main Function
def main(): 
    name_list    = []
    address_list = []
    phone_list   = []
    fax_list     = []
    email_list   = []

    # Initiati chrome driver and get url
    print("Start Scraping using Chrome Bot")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.idx.co.id/primary/ListedCompany/GetCompanyProfiles?emitenType=s&start=0&length=9999')
    
    # Get json
    content = driver.page_source.split("</pre")[0].split(';">')[-1].replace('\\r',',').replace('\\n','').replace('\\t','')
    driver.close()

    # load to dict
    dic = json.loads(content)

    # Get data
    for data in dic['data']:
        address = data['Alamat']
        name    = data['NamaEmiten']
        phone   = data['Telepon']
        fax     = data['Fax']
        email   = data['Email']

        address_list.append(address)
        name_list.append(name)
        phone_list.append(phone)
        fax_list.append(fax)
        email_list.append(email)

    # Set Dataframe to excel
    df = pd.DataFrame(list(zip(name_list,address_list,phone_list,fax_list,email_list)),columns=['Company Name','Adress','Phone','Fax','Email'])
    df.drop_duplicates()
    print(df)
    df.to_excel("idx.xlsx")

# Define time estimator function
def convert(seconds): 
    seconds  = seconds % (24 * 3600)
    hour     = seconds                // 3600
    seconds %= 3600
    minutes  = seconds                // 60
    seconds %= 60
     
    return "%d jam, %02d menit, %02d detik" % (hour, minutes, seconds)

# Main function
if __name__ == "__main__":
   start     = timeit.default_timer()
   main()
   stop = timeit.default_timer()
   print(f"Scraping is Done in {convert(stop-start)}")