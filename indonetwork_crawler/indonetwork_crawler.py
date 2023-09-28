import requests,timeit, sys
import pandas as pd
from tenacity import retry, wait_fixed
from bs4 import BeautifulSoup

# Define crawler function & retry if there's error
@retry(wait=wait_fixed(300))
def crawler(url): 
    try: 
        return requests.get(url)
    except requests.exceptions.HTTPError as errh: 
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc: 
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt: 
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err: 
        print ("OOps: Something Else",err)

# Define Main Function
def main(): 
    name_list    = []
    address_list = []

    # Get item using this End Point
    list_api = 'https://www.indonetwork.co.id'
    get_html = crawler(f'{list_api}/k')
    soup      = BeautifulSoup(get_html.content, "html.parser").find_all("div",class_="first-title py-md-3 align-items-center")

    # Find company name
    for lst in soup:
        for url in lst.find_all("a"):
            url=url["href"]
            print(f"{url.split('/')[-1]} is start")
            for page in range(1,6):
                get_data    = crawler(list_api+url+'/perusahaan/'+str(page))
                soup2       = BeautifulSoup(get_data.content, "html.parser")
                all_address = soup2.find_all("div",class_="ms-2")
                for data in all_address:
                    for page_item in data.find_all("div"):
                        pg = page_item.text.strip()
                        if pg == 'Alamat':
                            continue
                        else:
                            address=pg.replace("<strong>","").replace("<br />","").replace("<br","").replace("</strong>","")
                        address_list.append(address)
                all_name = soup2.find_all("div",class_="col-12 name mb-3 d-flex")
                for name in all_name:
                    name_list.extend(find_name.text.strip() for find_name in name.find_all("a"))
                print(f"Page {page} is done")

        print(f"{url.split('/')[-1]} is done")
    # Set Dataframe to excel
    df = pd.DataFrame(list(zip(name_list,address_list)),columns=['Company Name','Adress'])
    df.drop_duplicates()
    print(df)
    df.to_excel("indonetwork.xlsx")

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