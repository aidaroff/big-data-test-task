import csv

from collections import namedtuple

import requests

from bs4 import BeautifulSoup


URL = 'https://tengrinews.kz'
COMMENTS_URL = 'http://c.tn.kz/comments/get/list/'
SPECIAL_CHARS = '"?!@#$%^&*(),.\n«»<>'


def generate_comments(filename):
    news_items = _parse()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, quotechar='"')
        for news_item in news_items:
            print(f'\nwriting rows for {news_item.title}')
            for comment in news_item.comments:
                try:
                    writer.writerow([_clean_comment(comment)])
                except:
                    print(f'printing error comment: "{comment}" in {news_item.title}')


def _parse():
    front_page_response = requests.get(URL)
    front_page_response.raise_for_status()
    frontpage_soup = BeautifulSoup(front_page_response.text)

    NewsItem = namedtuple('NewsItem', ['title', 'url', 'tengri_id', 'comments'])
    top_news = frontpage_soup.findAll('div', {'class': 'tn-main-news-item'})[:7]
    parse_title = lambda n: n.find('span').contents[0]
    parse_url = lambda n: URL + n.find('a')['href']
    news_tuples = [
        NewsItem(
            title=parse_title(n),
            url=parse_url(n),
            tengri_id=parse_url(n).split('-')[-1].split('/')[0],
            comments=[]
        ) for n in top_news
    ]

    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    updated_news_items = []
    # tengri loads comments on clientside now so we have to find
    # a way to fetch comments in a separate request
    for news_item in news_tuples:
        payload = {
            'id': news_item.tengri_id,
            'lang': 'ru',
            'sort': 'best',
            'type': 'news',
        }
        headers = {'User-Agent': ua}
        comments_resp = requests.get(COMMENTS_URL, json=payload)
        comments_resp.raise_for_status()
        comments_data = comments_resp.json()
        top_comments = comments_data['list']

        print(f'\ntotal comment count in "{news_item.title}" is {comments_data["count"]}')

        comments_texts = []
        for comment in top_comments:
            comments_texts.extend(_get_child_comments_texts(comment, acc=[]))

        print(f'count of comments pulled from the response is {len(comments_texts)}')

        updated_news_items.append(
            NewsItem(
                title=news_item.title,
                url=news_item.url,
                tengri_id=news_item.tengri_id,
                comments=comments_texts[:100],
            )
        )

    return updated_news_items


def _comment_has_child_comments(comment):
    return len(comment.get('child')) > 0


def _get_child_comments_texts(comment, acc=[]):
    if not _comment_has_child_comments(comment):
        return [*acc, comment['text']]
    for child_comment in comment['child']:
        acc.extend(_get_child_comments_texts(child_comment, acc=[]))
    return [*acc, comment['text']]


def _clean_comment(comment: str):
    for char in SPECIAL_CHARS:
        comment = comment.replace(char, ' ')
    return comment.lower()


