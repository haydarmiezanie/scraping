import requests, timeit, sys
import pandas as pd
from tenacity import retry, wait_fixed

@retry(wait=wait_fixed(300))
def crawler(item):
    url = f'https://jobseeker.kalibrr.com/kjs/job_board/search?limit=15&offset={15*item}&location=Bekasi,Bogor,Dki%20Jakarta,Tangerang'
    header = {
        "accept": "application/json, text/plain, */*",    
        "accept-language": "en-US,en;q=0.9",
        "cookie": '_gcl_au=1.1.2121453133.1666941818; _fbp=fb.1.1666941817585.17922518; _gid=GA1.2.787954090.1667829262; __zlcmid=1CplMJ28IZImIYH; kb="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJtYXhfYWdlIjoyNDE5MjAwLCJ1dGNfb2Zmc2V0Ijo0MjAsImxhc3RfbmFtZSI6IkphbWlsIiwidGltZW91dCI6MTIwOTYwMCwicm9sZXMiOlsiY2FuZGlkYXRlIl0sInVzZWRfZ2xvYmFsIjpmYWxzZSwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcnN0X25hbWUiOiJIYXlkYXIgTWllemFuaWUgQWJkdWwgIiwiaWQiOjY0MTE5OTcsImxvY2FsZSI6ImVuX1BIIiwiZXhwaXJ5X2RhdGUiOiIyMDIyLTExLTA3IDE0OjA0OjI3IiwibG9jYXRpb25fbG9ubGF0IjpudWxsLCJjb3VudHJ5X2NvZGUiOiJJRCIsInRpbWUiOjE2Njc4Mjk1NjcuODQ3MDgxLCJzaWdudXBfYnJhbmQiOiJrYWxpYnJyIiwiZW1haWwiOiJoYXlkYXIubWllemFuaWVAbWVrYXJpLmNvbSIsIm1vYmlsZV9udW1iZXJfY29uZmlybWVkIjpmYWxzZSwibW9iaWxlX251bWJlcl9ub3JtYWxpemVkIjpudWxsfQ.k-makGiqLVTxuhKV9SmwcBXysvEB5GSzA6yutCxOEZSsy0JV6Q7uLDJWsrY0Vb5FTO4XLte2L2Wv4kowIb-xjIcQnkuU9eNt3SGQ62fkkqrx4cYxp5wGfC4kY69f1XkZBB83mRNb11ntArxzMoy9e3BaT0Nm-PzjlIKDejIHIzP9A_ZAd4ea8Sx6cBuBuR8nk5oQarCcahvLvSbu8iBxt6yezH3aAJJvY8ofU70Y9FtbqtEcxnw-Urfnt43Qfw6pBlVcNggyQhOr9AjvX_qcGdWiBsoMiKo2yXGzAmUl75lSo_YCzoqVtqyrqLhJsyqcjn0QQqrFbHHB-nVjfFyt2YhQ0bzjpsMsLKs0ialPz86PF-hGZNJWIoiN8AkaMEvonGG8DCkFtoN9FjSFqNhJ8iNsXdB2on9oycaBwA5gZvd0Hs5ugioil4E9qG3hXbtt2in3BhCidJqxKQXTIT1xCyQMfuTfwa5IMque2-8roKMKECHwINTa7JfIDXRK4zNX08xoiu1a8Ppjrer5SLW0OiIC6rcJqdc6QyGjfc2x7aCB6pzmQH7WbX9lDTE8PxTsqh2csit4hEJf_Y60HEuE1PqBZds1azhp7BTvZbMkuMCtVy-8pXSbUI7IRIQeaohDtVxb8S5VjBjPsVBMe_-4o3l2WnJgl2YFbeqEp7fbNi0"; _dc_gtm_UA-47900795-1=1; _ga_Q5JTLC9LMJ=GS1.1.1667829256.4.1.1667829761.0.0.0; _ga_X8GYQC04GE=GS1.1.1667829262.3.1.1667829761.0.0.0; _ga_CYKC6J5VY2=GS1.1.1667829256.4.1.1667829764.0.0.0; _ga=GA1.1.1662771428.1666941820',
        "referer": "https://jobseeker.kalibrr.com/job-board/l/Bekasi/l/Bogor/l/Dki-Jakarta/l/Tangerang/3?redirectTo=%2Fjob-board%2Fl%2FBekasi%2Fl%2FBogor%2Fl%2FDki-Jakarta%2Fl%2FTangerang%2F1",
        "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": '?0',
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36}'
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

def main(lower_limit, upper_limit):
    name_list    = []
    address_list = []
    city_list    = []
    for page in range(lower_limit-1, upper_limit+1):
        print(f"Currently on page: {page}")
        get_dict = crawler(page)
        for item in get_dict["jobs"]:
            name    = item["company"]["name"]
            name_list.append(name)
            try:
                city    = item["google_location"]["address_components"]["city"]
            except Exception:
                city = None
            city_list.append(city)
            try:
                address = item["google_location"]["address_components"]["address_line_1"]
            except Exception:
                address = None
            address_list.append(address) 


        df = pd.DataFrame(list(zip(name_list,address_list,city_list)),columns=['Company Name','Adress','City'])
        df = df.drop_duplicates(subset=['Company Name'])
        df = df.drop_duplicates(subset=['Adress'])
        print(f"Page {page} is done")
        df.to_excel("kalibrr.xlsx")

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