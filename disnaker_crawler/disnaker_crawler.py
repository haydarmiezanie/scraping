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
    name_list        = []
    address_list     = []
    phone_list       = []
    email_list       = []
    field_list       = []
    postal_code_list = []
    city_list        = []
    province_list    = []

    print("Scraping Just Starting")
    # Get item using this End Point
    list_api = 'https://disnaker.tangerangkota.go.id/perusahaan'
    get_html  = crawler(list_api)
    print("10%")

    soup      = BeautifulSoup(get_html.content, "html.parser")
    find_list = soup.find(id="tabel_perusahaan_aplikasi")

    # Find elements
    job_elements      = find_list.find_all("td")
    print("20%")
    # Comapny Name
    title_items = job_elements[::8]
    for title in title_items:
        title = title.text.strip()
        name_list.append(title)
    print("30%")
    # Address
    address_items     = job_elements[1::8]
    for address in address_items:
        address = address.text.strip()
        address_list.append(address)
    print("40%")
    # Phone
    phone_items       = job_elements[2::8]
    for phone in phone_items:
        phone = phone.text.strip()
        phone_list.append(phone)

    # Email
    email_items       = job_elements[3::8]
    for email in email_items:
        email = email.text.strip()
        email_list.append(email)
    print("50%")
    # Field
    field_items       = job_elements[4::8]
    for field in field_items:
        field = field.text.strip()
        field_list.append(field)
    print("60%")
    # Postal Code
    postal_code_items = job_elements[5::8]
    for postal_code in postal_code_items:
        postal_code = postal_code.text.strip()
        postal_code_list.append(postal_code)
    print("70%")
    # City
    city_items        = job_elements[6::8]
    for city in city_items:
        city = city.text.strip()
        city_list.append(city)
    print("80%")
    # Province
    province_items    = job_elements[7::8]
    for province in province_items:
        province = province.text.strip()
        province_list.append(province)
    print("90%")

    # Set Dataframe to excel
    df = pd.DataFrame(list(zip(name_list,address_list,phone_list, email_list, field_list, postal_code_list, city_list, province_list)),columns=['Company Name','Adress','Phone Number', 'Email', 'Field', 'Postal Code', 'City', 'Province'])
    df = df.drop_duplicates()
    print(df)
    df.to_excel("disnaker.xlsx")

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
    main()
    stop = timeit.default_timer()
    print(f"Scraping is Done in {convert(stop-start)}")