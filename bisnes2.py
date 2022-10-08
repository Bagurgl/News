import requests
from bs4 import BeautifulSoup
import time
import json
from db_data import host, user, password, db_name
import psycopg2


def get_links():
    res = requests.get(
        url=f"https://www.forbes.ru/biznes",
        headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
    )
    if res.status_code != 200:
        return
    for page in range(0, 5):
        try:
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, "lxml")
                for a in soup.find('div', class_='_3ohr0').find_all('a', {'class': '_3eGVH'}):
                    yield f'https://www.forbes.ru/{a.attrs["href"].split("?")[0]}'
        except Exception as e:
            print(f"{e}")
        time.sleep(1)


def get_resume(link):
    data = requests.get(
        url=link,
        headers={"user-agent": "text"}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        name = soup.find(attrs={"class": "_3o-RD"}).text.strip()
    except:
        name = ""
    try:
        k=0
        img_news = soup.find(attrs={"class": "_2sbCR"}).find_all('img')
        for image in img_news:
            if k==0:
                img = image['src']
                k=1
    except:
        img = ""
    try:
        published = []
    except:
        published = []
    try:
        text1 = soup.find(attrs={"class": "_3Ywvx"}).text.replace("\xa0", " ").strip()
        text2 = soup.find(attrs={"class": "_1eYTt"}).find_all('p')
        for text in text2:
            text1 += text.text.replace("\xa0", " ")
    except:
        text1 = ""
    resume = {
        "name": name,
        "img_news": img,
        "published": published,
        "text1": text1,
        "source": link,
    }
    return resume


if __name__ == "__main__":
    # connect to exist database
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    try:
        connection.autocommit = True
        data = []
        k = []
        i = 0
        for a in get_links():
            if i != 10:
                data.append(get_resume(a))
                k = get_resume(a)
                print(k)
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"INSERT INTO news_biznes VALUES ('{k['source']}', '{k['name']}',  '{k['text1']}', '{k['img_news']}', '{k['published']}')")

                time.sleep(1)
                with open("data1.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                i += 1

            else:
                break

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            # cursor.close()
            connection.close()
            print("[INFO] PostgreSQL connection closed")
