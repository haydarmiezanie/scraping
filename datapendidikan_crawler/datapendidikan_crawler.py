import requests,json, timeit, sys
from tenacity import retry, wait_fixed
import pandas as pd


# Define crawler with return json
@retry(wait=wait_fixed(300))
def main_crawler(additional):
    
    url = f'https://www.datapendidikan.com/json/kabupaten{additional}'
    try:
        # Get all company on lists
        get_item = requests.get(url=url)
        return get_item.json()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

def main(province):
    province         = f"Prov. {province}"
    name_list        = []
    address_list     = []
    subdistrict_list = []
    ward_list        = []

    # Get list city
    print(f" {province} is start")
    specific_city          = main_crawler('.json')
    # Get province
    for find_prov in specific_city:
        print(find_prov["nama_prop"])
        if find_prov["nama_prop"] not in province:
            continue


        prov = find_prov["kode_kab"]
        print(prov)

        # Get data
        all_data     = main_crawler(f"/{prov}.json")
        for data in all_data:
            name_list.append(data["nama"])
            address     = data["alamat"]
            address_list.append(address)
            subdistrict = data["nama_kec"]
            subdistrict_list.append(subdistrict)
            ward        = data["kelurahan"]
            ward_list.append(ward)
    # Set Dataframe    
    df = pd.DataFrame(list(zip(name_list,address_list,subdistrict_list, ward_list)),columns=['Company Name','Adress','Subdistrict','Ward'])
    df.drop_duplicates()
    print(f" {province} is done")
    # Dump to excel
    df.to_excel(f"datapendidikan_{province}.xlsx")

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d jam, %02d menit, %02d detik" % (hour, minutes, seconds)

if __name__ == "__main__":
    start = timeit.default_timer()
    main(str(sys.argv[1]))
    stop = timeit.default_timer()
    print(f"Scraping is Done in {convert(stop-start)}")