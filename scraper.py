import requests
from bs4 import BeautifulSoup
from requests.structures import CaseInsensitiveDict


# adding headers to request for eng respose
headers = CaseInsensitiveDict()
headers["Connection"] = "keep-alive"
headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
headers["Upgrade-Insecure-Requests"] = "1"
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
headers["Accept-Language"] = "en-US,en;q=0.9"
headers["Accept-Encoding"] = "gzip, deflate"


# adding these headers will confuse bing because it will response empty to requests from python
# it makes you to go and buy some services
headers["sec-ch-ua-platform"] = "Linux"
headers["sec-ch-ua"] = 'Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"'


# query should be formatted using + instead sapce
# step*(page-1) + 1

STEP = lambda : 10
GOOGLE_TMPLT = lambda query, start: f"https://google.com/search?q={query}&start={start}"
# YAHOO_TMPLT  = lambda query, start: f"https://search.yahoo.com/search?p={query}&b={start}"
BING_TMPLT   = lambda query, start: f"https://www.bing.com/search?q={query}&start={start}"


def ranking(search_result):
    # TODO: ranking the results of different search engines
    # having the same links means to delete one
    answer = []
    bing_links = [item['link'] for item in search_result['bing']]
    google_iterated_links = []
    '''
        data = {
            'google': [
                {
                    'link': 'href link'
                    'text': 'text should be shown'
                    'rank': count
                },
            ],
            'bing': [
                {
                    'link': 'href link'
                    'text': 'text should be shown'
                    'rank': count
                },
            ],
    '''
    ALPHA = 0.4 # because google is more valuable for us
    tmp = []
    # first appending the common links
    for item in search_result['google']:
        if item['link'] in bing_links:
            bing_index = next((i for i, it in enumerate(search_result['bing']) if it['link'] == item['link']), -1)
            bing_rank = search_result['bing'][bing_index]['rank'] 
            google_rank = item['rank'] 
            google_iterated_links.append(item['link'])
            new_rank = ALPHA*item['rank'] + (1-ALPHA)*bing_rank
            tmp.append({
                'link': item['link'],
                'text': item['text'], 
                'rank': int(new_rank), 
            })
            del search_result['bing'][bing_index]
    tmp = sorted(tmp, key=lambda a: (a['rank'], len(a['link'])))
    print(tmp)
    for item in tmp:
        answer.append({
            'href': item['link'],
            'text': item['text']
        })
    
    tmp = []
    # second appending remainder of google links to answer
    for item in search_result['google']:
        if item['link'] not in google_iterated_links:
            tmp.append(item)

    tmp = sorted(tmp, key=lambda a: (a['rank'], len(a['link'])))
    print(tmp)
    for item in tmp:
        answer.append({
            'href': item['link'],
            'text': item['text']
        })
    
    # third appending the bing remainder links to the answer
    tmp = []
    for item in search_result['bing']:
        tmp.append(item)

    tmp = sorted(tmp, key=lambda a: (a['rank'], len(a['link'])))
    print(tmp)
    for item in tmp:
        answer.append({
            'href': item['link'],
            'text': item['text']
        })
    

    '''
        answer = [
            {
                'href': 'link site',
                'text': 'title site'
            },
            {
                'href': 'link site',
                'text': 'title site'
            },
            {
                'href': 'link site',
                'text': 'title site'
            },
        ]
    '''
    return answer


def search_google(query: str, indx: int=1):
    # regex to extract: {'link': '/url?sa=t&source=web&rct=j&url=https://fast.com/&ved=2ahUKEwjpzJXL9cD1AhW6SmwGHfJ9D4c4ARAWegQIBBAB', 'text': 'Fast.com: Internet Speed Test'},
    if indx < 1:
        indx = 1
    urls = list()
    
    # domain name of the URL without the protocol
    url = GOOGLE_TMPLT(query.replace(' ', '+'), ((indx-1)*STEP()+1))
    
    resp = requests.get(
            url,
            headers=headers
    )
    

    soup = BeautifulSoup(
        resp.content, 
        "html.parser"
    )
    rank = 1
    for a_tag in soup.select('a'):
        if 'href' in a_tag.attrs and \
            "search?q=" not in a_tag.attrs.get("href"):
            if 'ping' in a_tag.attrs.keys():
                try:
                    href = a_tag.attrs.get("href")
                    h3_child = a_tag.findChild('h3')
                    if h3_child is not None:
                        text = h3_child.get_text()
                        urls.append({
                            'link': href,
                            'text': text,
                            'rank': rank 
                        })
                        rank += 1
                        '''
                        urls = [
                            {
                                'link': 'href link'
                                'text': 'text should be shown'
                                'rank': count
                            },
                        ]
                        '''
                except AttributeError:
                    pass
    
    return urls


def search_bing(query: str, indx: int=1):
    if indx < 1:
        indx = 1
    urls = list()
    # domain name of the URL without the protocol
    url = BING_TMPLT(query.replace(' ', '+'), ((indx-1)*STEP()+1))
    resp = requests.get(
            url,
            headers=headers,
    )
    

    soup = BeautifulSoup(
        resp.content, 
        "html.parser"
    )
    rank = 1
    for a_tag in soup.select("li h2 a"):
        href = a_tag.attrs.get("href")
        text = a_tag.get_text()
        if "search?q=" not in href:
            # print(20*"#", href, text)
            urls.append({
                'link': href,
                'text': text,
                'rank': rank
            })
            rank += 1
            '''
            urls = [
                {
                    'link': 'href link'
                    'text': 'text should be shown'
                    'rank': count
                },
            ]
            '''

    return urls


def search(s_q: str, indx: int):
    data = {
        'google': search_google(s_q, indx),
        'bing': search_bing(s_q, indx)
    }
    '''
        data = {
            'google': [
                {
                    'link': 'href link'
                    'text': 'text should be shown'
                    'rank': count
                },
            ],
            'bing': [
                {
                    'link': 'href link'
                    'text': 'text should be shown'
                    'rank': count
                },
            ],
    '''
    return ranking(data)


if __name__ == "__main__":
    print(search('internet speedtest', 1))