from fastapi import FastAPI, HTTPException, Request
from typing import Dict, Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup
from urllib.request import urlparse, urljoin


class TestItem(BaseModel):
    name: str
    desc: Optional[str] = None
    pric: float
    tax: Optional[float] = None


# query should be formatted using + instead sapce

google_url_tmplt = "google.com/search?q={query}&start={start}"
yahoo_url_tmplt  = "https://search.yahoo.com/search?p={query}&b={start}"
bing_url_tmplt   = "https://www.bing.com/search?q={query}&first={start}"
step = 10
# step*(page-1) + 1

# for accessing google links -> find the all a tags which has property url in them
# then inside the a tag get the text of h3




def ranking(search_result: Dict[str, str]):
    # TODO: ranking the results of different search engines
    return [
        {
            'link': 'test1',
            'title': 'test1',
        },
        {
            'link': 'test2',
            'title': 'test2',
        },
        {
            'link': 'test3',
            'title': 'test3',
        },
    ]


def search_google(query: str, indx: int =0) -> list:
    for j in search(query, tld="co.in", num=5, start=1, pause=2):
        print(j)

def search_yahoo(query: str, indx: int =0) -> list:
    # TODO: search yahoo and return the list of results
    pass


def search_bing(query: str, indx: int=0):
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue

        href = urljoin(url, href)

def search(s_q: str):
    return ranking({})


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_index_hdml(request: Request):
    """this is the main function for getting the home or index.html
    """
    # return '<center><h1>hello</h1></center>'
    # return {
    #     "index": "html1"
    # }
    return templates.TemplateResponse(
        "index.html", {
            "request": request
        }
    )


@app.get("/search/")
async def get_search(request: Request, s_query: str, indx: Optional[int] =0):
    if s_query.strip() != "":
        if indx < 0:
            indx = 0
        return templates.TemplateResponse(
            "search_result.html", {
                "request": request,
                "s_query": s_query,
                "page": indx,
                "items": search(s_query)
            }
        )

@app.post("/test-post/")
async def test_post(item: TestItem):
    return item


@app.post("/test-item/")
async def create_item(item: TestItem):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# return {"item_id": item_id, **item.dict()}
# if item_id not in items:
#     raise HTTPException(
#         status_code=404,
#         detail="Item not found",
#         headers={"X-Error": "There goes my error"},
#     )