print(">>> Cờ số 1: Bắt đầu nạp thư viện...")
import pandas as pd
import time
import random
import requests
from bs4 import BeautifulSoup
print(">>> Cờ số 2: Đã nạp xong toàn bộ thư viện!")

def crawl():
    data=[]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    for page in range(1,345):
        print(f"---> Đang hốt trọn ổ trang {page}...")
        url = f"https://phongtro123.com/tinh-thanh/ha-noi?page={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        listings =soup.find_all("div",class_="flex-grow-1")
        if response.status_code == 200:
            for item in listings:
                try:
                    title_tag = item.find("a",class_="line-clamp-2")
                    title=title_tag.text.strip() if title_tag else "N/A"

                    price_tag= item.find("span",class_="text-green")
                    price=price_tag.text.strip() if price_tag else "N/A"

                    info_div = item.find("div", class_="line-clamp-1")
                    area="N/A"
                    if info_div:
                        spans = info_div.find_all("span")
                        if len(spans) >= 3:
                            area = spans[2].text.strip() if area else "N/A"

                    location_tag =item.find("a", class_="text-body")
                    location=location_tag.text.strip() if location_tag else "N/A"

                    if title == "N/A":
                        print(f"  [!] Tin không có tiêu đề, bỏ qua.")
                        continue

                    data.append({
                        "Tiêu đề": title,
                        "giá": price,
                        "diện tích": area,
                        "địa chỉ": location
                    })

                except Exception as e:
                    print(f"  [!] Lỗi bóc tách 1 tin: {e}")
                    continue
            delay = random.uniform(3, 6)
            time.sleep(delay)
        else:
            print("lỗi kết nối",response.status_code)
    if data:
        df = pd.DataFrame(data)
        df.to_csv("data/raw/data_phongtro_chuan.csv", index=False, encoding="utf-8-sig")
if __name__ == "__main__":
    crawl()
    

    
        