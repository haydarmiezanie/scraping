import requests,json, timeit, sys
from tenacity import retry, wait_fixed
import pandas as pd

# Define Header
header = {
"accept"                   : "application/vnd.linkedin.normalized+json+2.1",
"accept-encoding"          : "gzip, deflate, br",
"accept-language"          : "en-US,en;q=0.9",
"cookie"                   : 'bcookie="v=2&6c3f22a6-a881-4b1e-8673-2c89652e41f2"; li_sugr=61fa0f4d-f8da-4ec1-84cf-a1452133d093; bscookie="v=1&202209260045433b679b1f-b60b-4eeb-825b-aeb1242fdc35AQFbVtIp3mAUt9gBBHPCx1JewF0RqsOz"; aam_uuid=78502315039243166920781632042519440064; G_ENABLED_IDPS=google; _gcl_au=1.1.1802840903.1664155429; timezone=Asia/Jakarta; li_theme=light; li_theme_set=app; _guid=7c3244c0-3bbf-4dc2-956d-cce7a3cb38ae; mbox=session#a0b800679648458a98a1676c1a55cbde#1667878588|PC#a0b800679648458a98a1676c1a55cbde.38_0#1683428728; s_fid=3023B0912F94A859-1C9682F6C69AD3E6; li_rm=AQE1F0BczpSJ1AAAAYRVWKty4dz0FMb4rMTn_bH9lLRX6jABMo16rIRquR5RwWT_wMBznSs1fLd0LrCOMdALRSGS8lFL6TqZg2q_WEIv3ncfYPiBqb0tyOikmWE0KAt88hr7Vy2L4reOU0JnlZIOs_ppXReWcO1hAghjH5SQFGGw9ysmocvWO5ak4cKEIPCXDQpHw6S3pMriVVDC-5WVZTBUSmSuTVCB8ML8j-Y8TxCqoG0aFoJoSkr40t8qqcbOsWzHMVI5rCzC64_qN649IsGtTcQqIveGRdnlzFATmrlRxlIqp6wI4L-EFvT6c92GPd8qgJuSKcWZHPkOmRA; visit=v=1&M; JSESSIONID="ajax:8064119261076569804"; gpv_pn=www.linkedin.com%2Flearning%2Fpostgresql-advanced-queries; s_tslv=1670997707527; s_ips=1006; s_tp=3239; AnalyticsSyncHistory=AQJKAJeEPD1G7AAAAYUoMX0rt8PXx7GGO2nAPmu8AXLUcxYgcaqqsChdzgIizrUNIviOrpLp50jJuOEd8X_mPA; lms_ads=AQEB9zJOzKwVOgAAAYUoMX5glvRiyedGxoKJXaOvZXYr-arNonF6__ok1qPHH2OSYNlec4q2899h0KSJV9_wZhC9zAdUrGow; lms_analytics=AQEB9zJOzKwVOgAAAYUoMX5glvRiyedGxoKJXaOvZXYr-arNonF6__ok1qPHH2OSYNlec4q2899h0KSJV9_wZhC9zAdUrGow; lang=v=2&lang=en-us; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19346%7CMCMID%7C77998659835820589750727266533924788491%7CMCAAMLH-1672110124%7C3%7CMCAAMB-1672110124%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1671512524s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1752947655; liap=true; li_at=AQEDASbYFqIB6QHiAAABhS2iyqYAAAGFUa9OplYAWsRk-QQWRDyNSKCOYf8xbp0m2bJJPViRoxnrlKpoTqllp7qBeBLDA9XzOXf7__4ruV0IBh8xjerCqAVhJvlNXA_qrk9WRyQjxmsZUSfjBj_luy7t; UserMatchHistory=AQKx48-9rXCaXQAAAYUtqzY7XCl34cNCSKsgV6i0LNDNacvGCcjA3W2VXSvxxJe2TogqIAAnOxA4_OXOdKFQMTeNJ8QL2p4c4rHrCAFf7hkdR-x5ClZdSHEMqw6eiGM3LZk5y8aEEa5voDlnaK7mngOVDOt9PabBtGsPPZqpB0ijTnO-FiWAGqMXna2cA-I6n96WHMIH-kmtTf0P4ucT8OoRTnKIQ7Bo6ZJsHcoR_yZPpLq6IM1C3vk3BtVcAC407o18dVhYMkMyfMJy5kFjT1gsd3VboT9hgf2RhKE; lidc="b=OB78:s=O:r=O:a=O:p=O:g=2606:u=528:x=1:i=1671508547:t=1671580811:v=2:sig=AQHKazH-WIaidWX7ShuOa1ePuoiMLMY-"',
"csrf-token"               : "ajax:8064119261076569804",
"referer"                  : "https://www.linkedin.com/company/pertamina/about/",
"sec-ch-ua"                : '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
"sec-ch-ua-mobile"         : '?0',
"sec-ch-ua-platform"       : '"macOS"',
"sec-fetch-dest"           : "empty",
"sec-fetch-mode"           : "cors",
"sec-fetch-site"           : "same-origin",
"user-agent"               : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
"x-li-lang"                : "en_US",
"x-li-page-instance"       : 'urn:li:page:d_flagship3_company;hmRlEU4URAG4TYlaXANd7g==',
"x-li-track"               : '{"clientVersion":"1.11.5785","mpVersion":"1.11.5785","osName":"web","timezoneOffset":7,"timezone":"Asia/Jakarta","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":3360,"displayHeight":2100}',
"x-restli-protocol-version": "2.0.0"
}

# Define crawler with return json
@retry(wait=wait_fixed(300))
def main_crawler(company):
    
    url = f'https://www.linkedin.com/voyager/api/voyagerOrganizationDashCompanies?decorationId=com.linkedin.voyager.dash.deco.organization.CompanyGroupedLocations-1&q=universalName&universalName={company}'
    try:
        # Get all company on lists
        get_item = requests.get(url=url,headers=header)
        return get_item.json()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

# Define crawler with return text
@retry(wait=wait_fixed(300))
def company_name(page):
    url = f"https://www.linkedin.com/search/results/COMPANIES/?companyHqGeo=%5B%22102478259%22%5D&industry=%5B%22116%22%2C%2225%22%5D&origin=FACETED_SEARCH&page={page}&sid=%40qu"    
    try:
        # Get all company data 
        get_name = requests.get(url=url,headers=header)
        return get_name.text
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

def main(lower_limit, upper_limit):
    name_list        = []
    address_list     = []
    city_list        = []
    postal_code_list = []
    # Looping on page
    for page in range(lower_limit, upper_limit+1):
        print(f"Currently on page: {page}")
        # Try if data exist & doing some cleansing
        get_name          = company_name(page)
        try:
            replace_delimiter = get_name.replace("&quot;",'"')
            text_payload      = '{"data":{"metadata"'+replace_delimiter.split('{"data":{"metadata"')[1].split("\n</code>")[0]
            json_payload      = json.loads(text_payload)
        except Exception:
            print("Skip because data is invalid")
            continue
        # Get item by dict list from 11 to 21
        for item in range(11,22):
            # Check if url and company name exist
            try:
                url_loc      = json_payload["included"][item]["navigationUrl"].split("/")[-2]
                name_company = json_payload["included"][item]["title"]["text"]
                get_item     = main_crawler(url_loc)["included"][0]["groupedLocations"]
            except Exception:
                continue
            # Looping on company data
            for page_item in get_item:
                # Get address in 1st way
                try:
                    define_country = page_item["locations"][0]["address"]["country"]
                    # Define Indonesia
                    if define_country == 'ID':
                        # Get all data
                        try:
                            address_1   = page_item["locations"][0]["address"]["line1"]
                            postal_code = page_item["locations"][0]["address"]["postalCode"]
                            city        = page_item["locations"][0]["address"]["city"]
                        except Exception:
                            address_1   = None
                            postal_code = None
                            city        = None
                        # Check for the 2nd address
                        try:
                            address_2 = page_item["locations"][0]["address"]["line2"]
                            address_total = address_1 + ", " + address_2
                        except Exception:
                            address_total = address_1
                        name_list.append(name_company)
                        address_list.append(address_total)
                        postal_code_list.append(postal_code)
                        city_list.append(city)
                except Exception:
                    alt_item = page_item["locations"]
                    for idx, it in enumerate(alt_item):
                        define_country = alt_item[idx]["address"]["country"]
                        # Define Indonesia
                        if define_country == 'ID':
                            # Get all data
                            try:
                                address_1   = alt_item[idx]["address"]["line1"]
                                postal_code = alt_item[idx]["address"]["postalCode"]
                                city        = alt_item[idx]["address"]["geographicArea"]
                            except Exception:
                                address_1   = None
                                postal_code = None
                                city        = None
                            # Check for the 2nd address
                            try:
                                address_2 = alt_item[idx]["address"]["line2"]
                                address_total = address_1 + ", " + address_2
                            except Exception:
                                address_total = address_1
                            name_list.append(name_company)
                            address_list.append(address_total)
                            postal_code_list.append(postal_code)
                            city_list.append(city)
        # Set Dataframe    
        df = pd.DataFrame(list(zip(name_list,address_list,postal_code_list,city_list)),columns=['Company Name','Adress','Postal Code','City'])
        df.drop_duplicates()
        print(f"Page {page} is done")
        # Dump to excel
        df.to_excel("linkedin.xlsx")

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d jam, %02d menit, %02d detik" % (hour, minutes, seconds)

if __name__ == "__main__":
    start = timeit.default_timer()
    main(int(sys.argv[1]), int(sys.argv[2]))
    stop = timeit.default_timer()
    print(f"Scraping is Done in {convert(stop-start)}")