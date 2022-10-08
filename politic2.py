import requests
from bs4 import BeautifulSoup
import time
import json
from db_data import host, user, password, db_name
import psycopg2

#Получение ссылки на саму новость
def get_links():
    res = requests.get(
        url=f"https://ria.ru/politics/",
        headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
    )
    if res.status_code != 200:
        return
    for page in range(0, 5):
        try:
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, "lxml")
                for a in soup.find('div', class_='list').find_all('a', {'class': 'list-item__title'}):
                    print(f'{a.attrs["href"].split("?")[0]}')
                    yield f'{a.attrs["href"].split("?")[0]}'
        except Exception as e:
            print(f"{e}")
        time.sleep(1)

#получение отдельных атрибутов страницы
def get_resume(link):
    data = requests.get(
        url=link,
        headers={"user-agent": "text"}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        name = soup.find(attrs={"class": "article__title"}).text.strip()
    except:
        name = ""
    try:
        img_news = soup.find(attrs={"class": "media__size"}).find_all('img')
        for image in img_news:
            img = image['src']
    except:
        img = ""
    try:
        published = soup.find(attrs={"class": "article__info-date"}).text
    except:
        published = []
    try:
        text1 = soup.find(attrs={"class": "article__body"}).find_all(attrs={"class": "article__block"})
        text2=""
        for text in text1:
            text2 += text.find(attrs={"class": "article__text"}).text.replace("\xa0", " ")
    except:
        text1 = ""
    #формирование удобной записи
    resume = {
        "name": name,
        "img_news": img,
        "published": published,
        "text1": text2,
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
            if i != 20:
                data.append(get_resume(a))
                k = get_resume(a)
                print(k)
                #Запись в БД
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"INSERT INTO news_biznes VALUES ('{k['source']}', '{k['name']}',  '{k['text1']}', '{k['img_news']}', '{k['published']}')")

                time.sleep(1)
                #Запись в JSON
                with open("data2.json", "w", encoding="utf-8") as f:
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
