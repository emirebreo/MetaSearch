from fastapi import FastAPI, Request
from typing import Optional
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from scraper import search
from starlette.exceptions import HTTPException as StarletteHTTPException



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_index_hdml(request: Request):
    return templates.TemplateResponse(
        "index.html", {
            "request": request
        }
    )


@app.get("/search/")
async def get_search(request: Request, s_query: str="", indx: Optional[int] =1):
    if s_query.strip() != "":
        if indx < 1:
            indx = 1
        return templates.TemplateResponse(
            "search_result.html", {
                "request": request,
                "s_query": s_query,
                "page": indx,
                "items": search(s_query, indx)
            }
        )
    else:
        return templates.TemplateResponse(
            "index.html", {
                "request": request
            }
        )




@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return templates.TemplateResponse(
        "error-page.html", {
            "request": request
        }
    )