import requests,timeit, sys, json
import pandas as pd
from tenacity import retry, wait_fixed
from bs4 import BeautifulSoup

# Define crawler function & retry if there's error
@retry(wait=wait_fixed(300))
def crawler(url):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
            }
        return requests.get(url,headers=headers)
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
    
    # Looping from first page to end page
    for page in range(lower_limit,upper_limit+1):
        print("Page :", page)

        # Get item using this End Point
        list_api     = f'https://www.loker.id/cari-lowongan-kerja/page/{page}?q&lokasi=jakarta&category=0&pendidikan=0'
        get_html     = crawler(list_api)
        soup         = BeautifulSoup(get_html.content, "html.parser")
        job_elements = soup.find_all("div",class_="media-body")

        # Find Elements
        for job_element in job_elements:
            find_link = job_element.find_all("a",href=True)

            # Get Link
            for link in find_link:
                get_item     = crawler(link['href'])
                soup2        = BeautifulSoup(get_item.content, "html.parser")
                results      = soup2.find("script",type="application/ld+json")
                final_result = results.text.replace("\r","").replace("\n","")
                dump_to_dict = json.loads(final_result,strict=False)
                # Get address
                address      = dump_to_dict['jobLocation']['address']['streetAddress']
                address_list.append(address)
                # Get Name
                name = dump_to_dict["hiringOrganization"]["name"]
                name_list.append(name)


        print(f"Page {page} is done")

    # Set Dataframe to excel
    df = pd.DataFrame(list(zip(name_list,address_list)),columns=['Company Name','Adress'])
    df = df.drop_duplicates()
    print(df)
    df.to_excel("loker.xlsx")

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
    if int(sys.argv[2]) > 234:
        stop = timeit.default_timer()
        print("Scraping is Error because maximum page is 234")
    else:
        main(int(sys.argv[1]), int(sys.argv[2]))
        stop = timeit.default_timer()
        print(f"Scraping is Done in {convert(stop-start)}")