import sys
import xml.dom.minidom
from datetime import datetime
from slugify import slugify
from threading import Thread
from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from django.core.management.base import BaseCommand, CommandError

from catalog.models import Genre, Movie

locker = Lock()


# service functions


def clear_review_text(review_raw):
    is_review_text = False
    review_text = ''
    review_list = review_raw[0].text.split('\n')
    for list_key in review_list:
        if "critic's rating" in list_key:
            is_review_text = True
            continue
        if "Trailer" in list_key:
            continue
        if is_review_text:
            review_text += list_key + '\n'

    review = '\n'.join([f'<p>{p}</p>' for p in review_text.split('\n') if p])
    return review


def get_sources_urls():
    with open('upload/sitemap.xml') as fxml:
        xml_obj = xml.dom.minidom.parse(fxml)

    urls = xml_obj.getElementsByTagName('loc')
    urls = [url.firstChild.data for url in urls if '/reviews/' in url.firstChild.data]
    return urls


# main functions


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    name = response.html.xpath("//h2[@class='mov_name']/text()")[0].strip()
    slug = slugify(name)
    img_source = response.html.xpath("//figure[@class='mov_poster']//img[@src]/@src")[0].strip()

    try:
        with HTMLSession() as session2:
            img_resp = session2.get(img_source)

        image_name = 'books_images/' + slug + img_source[-4:]

        with open(f'media/{image_name}', 'wb') as imgf:
            imgf.write(img_resp.content)

        del img_resp

    except Exception as e:
        print(e, type(e), sys.exc_info()[-1].tb_lineno)
        image_name = 'default.jpg'

    review_raw = response.html.xpath("//section[@class='main-c']//div[@class='review-subTabs']//div[@class='tab-content']")
    review = clear_review_text(review_raw)

    review_date = response.html.xpath("//h2[@class='mov_name']//span[@itemprop='name']/text()")[0].strip()
    review_date = ''.join(review_date.split(',')[1:]).strip()
    review_date = datetime.strptime(review_date, '%B %d %Y')

    duration = response.html.xpath("//table[@class='table mov-details']//tr[last()]/td[2]/text()")[0].strip()
    cast = response.html.xpath("//table[@class='table mov-details']//tr[1]/td[2]/text()")[0].strip()
    director = response.html.xpath("//table[@class='table mov-details']//tr[2]/td[2]/text()")[0].strip()
    trailer = response.html.xpath("//div[@class='reviewTabs']//iframe/@src")[0].strip()

    rate = response.html.xpath("//div[@class='rvw-right']/div/span[@class='review_css_style'][text()]")[0].text.strip()
    rate = rate.split('/')[0]

    genres = []
    genres_raw = response.html.xpath("//table[@class='table mov-details']//tr[3]/td[2]/text()")[0].strip()
    for genre in genres_raw.split(','):
        genres.append(genre.strip())

    movie = {
        'name': name,
        'slug': slug,
        'review': review,
        'img': image_name,
        'duration': duration,
        'img_source': img_source,
        'review_date': review_date,
        'cast': cast,
        'director': director,
        'trailer': trailer,
        'rate': rate,
        'movie_source': url,
    }

    try:
        with locker:
            movie = Movie.objects.create(**movie)
    except Exception as e:
        print(e, type(e), sys.exc_info()[-1].tb_lineno)
        print('Failed')
        return

    for genre in genres:
        genre = {'name': genre, 'slug': slugify(genre), 'description': ''}
        with locker:
            genre, created = Genre.objects.get_or_create(**genre)
        movie.genre.add(genre)

    print('Success:', url)


def run_crawler(task):
    task.status = 'start parsing'
    task.save()
    sources_urls = get_sources_urls()
    url_gen = url_generator(sources_urls, task)
    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(crawler, url_gen)
    task.status = 'finished'
    task.end_time = datetime.now()
    task.save()


def url_generator(sources_urls, task):
    i = 1
    for url in sources_urls:
        with locker:
            task.status = f'scrape id: {i}'
            task.save()
        i += 1
        yield url


class Command(BaseCommand):
    help = 'Run movies scraper'

    def handle(self, *args, **options):
        from task.models import Task

        task = Task.objects.create(task='run_scraper')
        run_crawler(task)

