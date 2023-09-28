import requests,timeit, sys, re, html, json
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
def main(lower_limit, upper_limit):
    name_list    = []
    address_list = []
    phone_list   = []
    
    # Looping from first page to end page
    for page in range(lower_limit,upper_limit+1):
        print("Page :", page)

        # Get item using this End Point
        list_api  = f'https://karir.com/search?q=&sort_order=urgent_job&job_function_ids=&industry_ids=&degree_ids=&major_ids=&location_ids=-10139-10140-10141-10142-10143-10144-10077-10078-10079-10080-10081-10082-10027-10158-10159-10160-10161-10162-10029-10030-10031-10032-10033-10034-10035-10036-10037-10038-10039-10040-10041-10042-10043-10044-47244-10045-10046-10047-10048-10049-10050-10051-10052-10053-10054-10055-10056-10057-10058-10059-10060-10061-10062-10063-10064-10065-10066-10067-10068-10069-10070-10071-10072-10073-10074-10075-10076-10083-10084-10085-10086-10087-10088-10089-10090-10091-10092-10093-10094-10095-10096-10097-10098-10155-10156-10157&location_id=&location=&salary_lower=0&salary_upper=100000000&page={page}&grid=list'
        get_html  = crawler(list_api)
        soup      = BeautifulSoup(get_html.content, "html.parser")
        find_list = soup.find("div",attrs={"data-react-class":"OpportunitiesLists"})
        
        count_item = len(re.findall(r'&quot;company&quot;',str(find_list)))

        for item in range(count_item):
            clear_item   = str(find_list).split("&quot;company&quot;:",item+1)[item+1].split(",&quot;location&quot;")[0]
            decoded_item = html.unescape(clear_item)
            clear_dict   = decoded_item.replace("\r\n","").split('_mission"')[0].replace(',"vision',"}")
            load_json    = json.loads(clear_dict)
            name_list.append(load_json["name"])
            address_list.append(load_json["address"])
            phone_list.append(load_json["phone"])
 
        print(f"Page {page} is done")

    # Set Dataframe to excel
    df = pd.DataFrame(list(zip(name_list,address_list,phone_list)),columns=['Company Name','Adress','Phone Number'])
    df = df.drop_duplicates()
    print(df)
    df.to_excel("karir.xlsx")

# Define time estimator function
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d jam, %02d menit, %02d detik" % (hour, minutes, seconds)

# Main function
if __name__ == "__main__":
    start = timeit.default_timer()
    if int(sys.argv[2]) > 255:
        stop = timeit.default_timer()
        print("Scraping is Error because maximum page is 255")
    else:
        main(int(sys.argv[1]), int(sys.argv[2]))
        stop = timeit.default_timer()
        print(f"Scraping is Done in {convert(stop-start)}")