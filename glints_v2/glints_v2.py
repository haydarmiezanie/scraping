import requests,timeit, sys
import pandas as pd
from tenacity import retry, wait_fixed

# Define crawler function with header & retry if there's error
@retry(wait=wait_fixed(300))
def crawler(url):
    header = {
        'accept'                   : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #'accept-encoding'          : 'gzip, deflate, br',
        'accept-language'          : 'en-US,en;q=0.9',
        'cache-control'            : 'max-age=0',
        "cookie"                   : '_gcl_au=1.1.335808438.1666586777; _ga=GA1.2.1752982995.1666586777; _fbp=fb.1.1666586777524.1455137107; _tgpc=0efc026f-295e-51e5-aff1-b972c8d4891c; _tt_enable_cookie=1; _ttp=95dd1c6d-f131-4111-b809-3770d694e80e; g_state={"i_l":0}; builderSessionId=9880c05ccef4494196621031bc81d652; _gid=GA1.2.1057802343.1671092443; ln_or=eyIxNjA0MzUiOiJkIn0%3D; tg=d41d8cd98f00b204e9800998ecf8427e; _tguatd=eyJ0Z3NvdXJjZSI6IihkaXJlY3QpIn0=; _tgci=d8a426d0-aa9c-5d0a-9af8-bbbd0c7b67fd; _tgrsid=c4f603a1-cd24-5ab5-8b21-8869f39b53e7; _tgsc=c4f603a1-cd24-5ab5-8b21-8869f39b53e7:-1; _tglksd=eyJzIjoiYzRmNjAzYTEtY2QyNC01YWI1LThiMjEtODg2OWYzOWI1M2U3Iiwic3QiOjE2NzEwOTI0NDMzODgsInNvZCI6IihkaXJlY3QpIiwic29kdCI6MTY3MTA5MjQ0MzM4OCwic29kcyI6ImMiLCJzb2RzdCI6MTY3MTA5MjQ2MDQzNX0=; _tgtim=c4f603a1-cd24-5ab5-8b21-8869f39b53e7:1671092446799:-1; _tgsid=eyJscGQiOiJleUpzWVc1a2FXNW5YM0JoWjJWZmRYSnNJam9pYUhSMGNITWxNMEVsTWtZbE1rWm5iR2x1ZEhNdVkyOXRKVEpHYVdRbE1rWmpiMjF3WVc1cFpYTWxNMFpqYjNWdWRISnBaWE1sTTBSSlJDVXlObkJoWjJVbE0wUXpOaUlzSW14aGJtUnBibWRmY0dGblpWOTBhWFJzWlNJNklsQmxjblZ6WVdoaFlXNGxNakJKYm1SdmJtVnphV0VsTWpCNVlXNW5KVEl3VFdWdFluVnJZU1V5TUV4dmQyOXVaMkZ1SlRJd1MyVnlhbUVsTWpBdEpUSXdTR0ZzWVcxaGJpVXlNRE0ySlRJd0pUZERKVEl3UjJ4cGJuUnpJbjA9IiwicGFnZV9zZXNzaW9uIjoiYzViYWVhNzQtM2FhMy00ZmQyLTk2YjMtZjU0ZTBmMDIzNTYwIiwiZXZlbnRfY291bnQiOiI1IiwicGFnZXZpZXciOiJ0cnVlIn0=; session=Fe26.2**ce34281ce12f2b1d12dd5f06fe3fe68859ec17ef55cdad7c7999d1fbe5621a97*wwLnBNFNu6pWKkyQWtO9tA*0all4c3VKy34Slfa_bfuYNX-IylPldqWNiG1mCpo_wS0HAKisprhw4kNJQlWdLAk**69df5c8c8c7ff02aba863b911f6e613d87b4abeaa2743d927347779fb2f3e2b3*zXtgtM5wKS7ho_8tkfC8WiiG0he0HlsQczXijF0uOw4; amplitude_id_26bdf4b56b304d7bfc6275ea77f2310cglints.com=eyJkZXZpY2VJZCI6IjNkYzY1MDljLTY0ZjUtNGVhZS1hNjBjLTcyMDNkMTRiMzk3YVIiLCJ1c2VySWQiOiJjYWNjZjIxMC05M2Y4LTQ1MjYtODEyYS00MzVkODkwMGFmMGIiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE2NzEwOTI0NDMyODYsImxhc3RFdmVudFRpbWUiOjE2NzEwOTI1ODI2MDAsImV2ZW50SWQiOjExOCwiaWRlbnRpZnlJZCI6NzQsInNlcXVlbmNlTnVtYmVyIjoxOTJ9',
        'referer'                  : 'https://www.google.com/',
        'sec-ch-ua'                : '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile'         : '?0',
        'sec-ch-ua-platform'       : '"macOS"',
        'sec-fetch-dest'           : 'document',
        'sec-fetch-mode'           : 'navigate',
        'sec-fetch-site'           : 'same-origin',
        'sec-fetch-user'           : '?1',
        'upgrade-insecure-requests': '1',
        'user-agent'               : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
    try :
        payload = requests.get(url,headers=header)
        return payload.json()
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
    city_list    = []

    # Looping from first page to end page
    for page in range(lower_limit,upper_limit+1):
        print("Page :", page)

        # Get item using this End Point
        list_api    = f'https://glints.com/api/companies?limit=30&offset={30*(page-1)}&attributes=[%22id%22,%22logo%22,%22name%22,%22updatedAt%22,%22IndustryId%22,%22CountryCode%22,%22CityId%22]&include=[%7B%22association%22:%22Industry%22,%22attributes%22:[%22name%22]%7D,%7B%22association%22:%22Jobs%22,%22attributes%22:[%22id%22,%22status%22,%22isPublic%22,%22updatedAt%22]%7D,%7B%22association%22:%22City%22,%22attributes%22:[%22name%22]%7D,%7B%22association%22:%22Country%22,%22attributes%22:[%22name%22]%7D]&where=%7B%22status%22:%7B%22not%22:[%22REJECTED%22]%7D,%22name%22:%7B%22not%22:null%7D,%22CountryCode%22:%22ID%22%7D&order=magic'
        get_id_list = crawler(list_api)
        get_list    = get_id_list['data']

        # Looping from first item to last item
        for item in get_list:
            get_id = item['id']
            try:
                city = item["links"]["city"]["name"]
            except Exception:
                city = None

            # Get item using this End Point
            list_item   = f'https://glints.com/api/companies/{get_id}?include=[%7B%22association%22:%22Industry%22,%22attributes%22:[%22name%22]%7D,%7B%22association%22:%22Country%22,%22attributes%22:[%22name%22]%7D]'
            get_item    = crawler(list_item)
            name        = get_item['data']['name']
            address     = get_item['data']['address']

            # Name, City, and Address Append
            name_list.append(name)
            city_list.append(city)
            address_list.append(address)
        print(f"Page {page} is done")

    # Set Dataframe to excel
    df = pd.DataFrame(list(zip(name_list,address_list,city_list)),columns=['Company Name','Adress','City'])
    df.drop_duplicates()
    print(f"Page {page+1} is done")
    df.to_excel("Glints.xlsx")


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
    main(int(sys.argv[1]), int(sys.argv[2]))
    stop = timeit.default_timer()
    print(f"Scraping is Done in {convert(stop-start)}")