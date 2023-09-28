import requests,timeit, sys
import pandas as pd
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
def main(lower_limit, upper_limit): 
    name_list    = []
    address_list = []
    phone_list   = []
    
    # Looping from first page to end page
    for page in range(lower_limit,upper_limit+1): 
        print("Page :", page)

        # Get item using this End Point
        list_api  = f'https://manufakturindo.com/company/all-categories/all-province/all-companies/page/{page}'
        get_html  = crawler(list_api)
        soup      = BeautifulSoup(get_html.content, "html.parser")
        find_list = soup.find(id="list-fact")

        # Find company name & address
        find_name_and_address = find_list.find_all("div", class_="list-content col-xs-4")
        for item in find_name_and_address: 
            company_name = item.find_all("a")
            for company in company_name: 
                name = company.text.strip()
                name_list.append(name)
            
            address_name = item.find_all("span")
            for address_ls in address_name: 
                address = address_ls.text.strip()
                address_list.append(address)

        # Find phone number
        find_phone = find_list.find_all("div", class_="list-contact col-xs-4")
        for list_number in find_phone: 
            phone_ls       = list_number.find_all("a", title="call company")
            if len(phone_ls) != 0:
                # Condition if company had more than one phone number
                if len(phone_ls) >= 2:
                    phone_list_new  = []
                    for ls_count in phone_ls: 
                        phone_number = ls_count.text.strip()
                        phone_list_new.append(phone_number)
                    split_phone = split_list(phone_list_new)
                    
                    phone_list.append(str(split_phone))
                else: 
                    for ls_count in phone_ls: 
                        phone_number = ls_count.text.strip()
                        phone_list.append(phone_number)
                        
                
            else: 
                phone_number = "-"
                phone_list.append(phone_number)
            
                   

        print(f"Page {page} is done")
    print(phone_list)
    # Set Dataframe to excel
    df = pd.DataFrame(list(zip(name_list,address_list,phone_list)),columns=['Company Name','Adress','Phone Number'])
    df.drop_duplicates()
    print(df)
    df.to_excel("manufakturindo.xlsx")

# Define time estimator function
def convert(seconds): 
    seconds  = seconds % (24 * 3600)
    hour     = seconds                // 3600
    seconds %= 3600
    minutes  = seconds                // 60
    seconds %= 60
     
    return "%d jam, %02d menit, %02d detik" % (hour, minutes, seconds)

# Define function to split list
def split_list(a_list): 
    half = len(a_list)  //2
    return [a_list[:half], a_list[half:]]

# Main function
if __name__ == "__main__":
   start     = timeit.default_timer()
   if int(sys.argv[2]) > 210: 
        stop = timeit.default_timer()
        print(f"Scraping is Error because maximum page is 210") 
   else: 
        main(int(sys.argv[1]), int(sys.argv[2]))
        stop = timeit.default_timer()
        print(f"Scraping is Done in {convert(stop-start)}")