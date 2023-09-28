import requests,timeit, sys, string
import pandas as pd
from string import digits
from tenacity import retry, wait_fixed
from bs4 import BeautifulSoup

# Define crawler function & retry if there's error
@retry(wait=wait_fixed(300))
def crawler(url): 
    try         : 
        payload = requests.get(url)
        return payload
    except requests.exceptions.HTTPError as errh: 
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc: 
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt: 
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err: 
        print ("OOps: Something Else",err)

# Define Main Function
def main(city,first_page,last_page): 
    name_list    = []
    address_list = []
    phone_list   = []
    
    for page in range(first_page,last_page+1):
        print(f"Scraping start on {city} Page {page}")
    
        url = f'http://telpon.info/location/{city.lower()}/page-{page}.html'
        try:
            get_data = crawler(url)
        except:
            raise("Check your city")
        soup     = BeautifulSoup(get_data.content, "html.parser").find_all("div",class_="listing-body")

        for data in soup:
            name = data.find("div", class_="listing-title").text.strip().split(". ")[1]
            name_list.append(name)
            address = data.find("div", class_="company-address").text.strip().split("(")[0]
            address_list.append(address)
            phone = data.find("div", class_="detail phone").text.strip()
            phone_list.append(phone)

        print(f"Scraping done on {city} Page {page}")
    # Set Dataframe to excel
    df = pd.DataFrame(list(zip(name_list,address_list,phone_list)),columns=['Company Name','Adress','Phone'])
    df.drop_duplicates()
    print(df)
    df.to_excel("telpon.xlsx")

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
   main(str(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
   stop = timeit.default_timer()
   print(f"Scraping is Done in {convert(stop-start)}")