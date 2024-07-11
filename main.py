from fastapi import FastAPI, BackgroundTasks
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from app.config.db_manager import create_session
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from app.dao.dashboard import CompanyInquiry
from app.utilities.taiwan_company_ranking import Crawler

app = FastAPI()
# static file 存放處
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", description="查詢頁面")
def root(request: Request, company: str = None, unified_no: str = None, db: Session = Depends(create_session)):
    try:
        data = CompanyInquiry.search(db=db, company=company, unified_no=unified_no)
        return templates.TemplateResponse("index.html", {"request": request,
                                                         "data": data,
                                                         "unified_no": unified_no if unified_no else '',
                                                         "company": company if company else ''})
    except Exception as e:
        raise e


@app.get("/run_crawler", description="爬蟲Trigger")
def run_crawler(background_tasks: BackgroundTasks):
    # Crawler(idle_time=5, ranking=500).run()
    background_tasks.add_task(start_crawler, idle_time=5, ranking=500)
    return {"message": f"爬蟲程式已經啟動, 請稍後再回來..."}


def start_crawler(idle_time: int, ranking: int) -> None:
    crawler = Crawler(idle_time=idle_time, ranking=ranking)
    crawler.run()
