import re
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

## 몽고db 셋팅
client = MongoClient('mongodb://15.164.164.56', 27017, username="test", password="test")
db = client.oneplusone


## 리스트 얻어오기
def get_lists():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        "Accept": "text_html,application_xhtml+xml,application_xml;q=0.9,image_webp,**/**;q=0.8"}
    
    ## 제품 설정리스트 ex [1, 2, 3, 4] => 아이스크림도 긁어오기
    ## 1 : 음료
    ## 2 : 과자류
    ## 3 : 식품
    ## 4 : 아이스크림
    ## 5 : 생활용품
    product_list = [1]

    for each in product_list :

        html_data = requests.get(f"https://pyony.com/search/?event_type=1&category={each}&item=100&sort=&q=", headers=headers)
        soup = BeautifulSoup(html_data.text, "html.parser")

        ## col-md-6 클래스 모두를 리스트로 만들기
        divs = soup.find_all(class_="col-md-6")
        
        for each_product in divs :
            div_for_price = each_product.find(class_="py-2").select_one("div:nth-child(2) > span.text-muted.small").string
            conveni_before = each_product.find("small").string

            ## 음료 등등
            product_type = each
            ## 편의점 괄호뒤 문장제거 정규식 ex) cu(씨유) => cu
            conveni_store = re.sub("\(.*\)|\s-\s.*","", conveni_before)
            product_name = each_product.find("strong").string
            product_price = (int(div_for_price.replace("원", "")
                                .replace("(", "")
                                .replace(")", "")
                                .replace(",",""))) * 2
            product_img = each_product.find("img")["src"]

            doc = {
                "product_type" : product_type,
                "conveni_store" : conveni_store,
                "product_name" : product_name,
                "product_price" : product_price,
                "product_img" : product_img,
                "like": 0
            }
            db.product.insert_one(doc)




def insert_item():
    ## 몽고db 삭제
    db.product.drop()
    db.likes.drop()
    ## 자료얻어오기
    try:
        get_lists()
        print("완료")
        return
    except:
        print("에러발생")


##실행
insert_item()
