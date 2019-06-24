from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from models import Author, Picture, get_database_connect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from uuid import uuid4
from time import sleep

main_url = r"https://www.tretyakovgallery.ru/en"


def find_picture(picture_name):
    u"""
    Проверка наличия автора в базе
    """
    engine = create_engine(get_database_connect(), echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    instance = session.query(Picture).filter(Picture.name.like("%{}%".format(picture_name)))

    return instance


def get_request(url):
    u"""
    Формирование заголовка запроса
    """
    return Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/35.0.1916.47 Safari/537.36'
        }
    )


def session_commit(data):
    u"""
    Сохранение в базу
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(data)
    session.commit()


def check_author(author_name):
    u"""
    Проверка наличия автора в базе
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    instance = session.query(Author).filter_by(name=author_name).first()
    return instance.id if instance else None


def get_author_name(bsObj):
    u"""
    Получение имени автора
    """
    author = bsObj.find('div', {"class": "exhibit-info__author"})
    author_name = author.get_text().strip()
    return author_name


def get_picture_name(bsObj):
    u"""
    Получение названия картины
    """
    picture = bsObj.find('div', {"class": "exhibit-info__title"})
    picture_name = picture.get_text().strip()
    return picture_name


def get_sizes(bsObj):
    u"""
    Получение размеров картины
    """
    size = bsObj.find_all('span', {"class": "exhibit-info__service"})
    sizes = []
    for s in size:
        sizes.append(s.get_text().strip())

    return sizes


def get_description(bsObj):
    u"""
    Получение описания картины
    """
    description = bsObj.find('div', {"class": "col-md-7"})

    try:
        description = description.p.p.get_text().strip()
    except:
        description = description.p.get_text().strip()

    return description


def parse(url):
    while True:
        try:
            full_url = main_url + url
            html = urlopen(get_request(full_url))
        except urllib.error.URLError as err:
            print(err)
            continue
        except ConnectionResetError as err:
            print(err)
            sleep(300)
            continue
        except TimeoutError as err:
            print(err)
            sleep(300)
            continue

        bsObj = BeautifulSoup(html.read(), 'html.parser')

        author_name = get_author_name(bsObj)
        picture_name = get_picture_name(bsObj)
        sizes = get_sizes(bsObj)
        description = get_description(bsObj)

        author_id = check_author(author_name)
        if not author_id:
            author_id = uuid4()
            db_author = Author(id=author_id, name=author_name)
            session_commit(db_author)

        session_commit(Picture(id=uuid4(), name=picture_name, description=description, author_id=author_id,\
                                  size=sizes[0], type=sizes[1], url=full_url))

        url = bsObj.find('a', {"class": "exhibit-preview _right"})["href"]


if __name__ == "__main__":
    engine = create_engine(get_database_connect(), echo=False)
    parse(r"/collection/berezovaya-roshcha/")