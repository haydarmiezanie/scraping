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
def main(lower_limit, upper_limit):
    name_list    = []
    address_list = []
    phone_list   = []

    # Looping from first page to end page
    for page in range(lower_limit,upper_limit+1):
        print("Page :", page)

        # Get item using this End Point
        list_api  = f'https://klikalamat.com/daftar-alamat-terbaru/page/{page}/'
        get_html  = crawler(list_api)
        soup      = BeautifulSoup(get_html.content, "html.parser")
        find_list = soup.find(id="loop_listing_taxonomy")

        # Find company name
        find_title = find_list.find_all("h2", class_="entry-title")
        for title_list in find_title:
            title = title_list.find_all("a")
            name_list.extend(company["title"] for company in title)
        # Find phone number
        find_phone = find_list.find_all("p", class_="phone")
        for list_number in find_phone:
            phone_number=list_number.text.strip()
            phone_list.append(phone_number)

        # Find address
        find_address = find_list.find_all("p", class_="address")
        for list_addres in find_address:
            address=list_addres.text.strip()
            address_list.append(address)

        print(f"Page {page} is done")

    # Set Dataframe to excel
    df = pd.DataFrame(list(zip(name_list,address_list,phone_list)),columns=['Company Name','Adress','Phone Number'])
    df.drop_duplicates()
    print(df)
    df.to_excel("klikalamat.xlsx")

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
    if int(sys.argv[2]) > 26:
        stop = timeit.default_timer()
        print("Scraping is Error because maximum page is 26")
    else:
        main(int(sys.argv[1]), int(sys.argv[2]))
        stop = timeit.default_timer()
        print(f"Scraping is Done in {convert(stop-start)}")