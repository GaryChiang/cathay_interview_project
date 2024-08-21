import time, queue
from datetime import datetime, timedelta
from sqlalchemy import update
import requests
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.db_manager import ConnectionString
from app.config.web_info import TaiwanCompanyRanking
from bs4 import BeautifulSoup
import threading
from app.model.company import Information
from app.schema.taiwan_company_ranking import CompaniesList, CompaniesInfo
from app.utilities.abstracts import CrawlerBase


class Crawler(CrawlerBase):
    """
    爬蟲邏輯 (實作CrawlerBase)
    """

    def __init__(self, idle_time: int, ranking: int = 500) -> None:
        """
        initial
        :param ranking: 取排名前幾名
        :param idle_time: 每筆資料抓取的間隔時間(秒)
        """
        # 網頁資訊
        self.landing_page = TaiwanCompanyRanking.landing_page.value
        self.summary = TaiwanCompanyRanking.company_summary.value
        self.detail = TaiwanCompanyRanking.company_detail.value
        # 預設header
        self.headers = TaiwanCompanyRanking.default_header.value
        # 取得排行前幾名的公司
        self.ranking = ranking
        # 資料抓取間隔
        self.idle_time = idle_time
        # 蒐集所有爬下來的結果
        self.q = queue.Queue()

    def scrape_page(self) -> list[CompaniesInfo]:
        try:
            # 公司清單
            companies = self.get_company_list()

            # 切割公司清單成為10個子列表
            sub_list = [companies[i::10] for i in range(10)]

            threads = []
            for i in range(10):
                # Create a new thread for each chunk of companies
                thread = threading.Thread(target=self.extract_info, args=(sub_list[i],))
                threads.append(thread)
                thread.start()

            # 等待所有執行緒結束
            for thread in threads:
                thread.join()

            # 遍訪問隊列，並把所有結果收集到一個list中
            results = []
            while not self.q.empty():
                results.extend(self.q.get())

            return results
        except Exception as e:
            raise e

    def get_company_list(self) -> list[CompaniesList]:
        """
        爬網頁取得公司清單
        :return:
        回傳公司清單
        [{'href': 公司summary連結, 'company_no': 公司代碼, 'name': 公司名稱}]
        """
        try:
            result = []

            html = requests.get(url=self.landing_page, headers=self.headers, verify=False)
            beautiful_soup = BeautifulSoup(html.text, features='lxml')

            a_tags = beautiful_soup.select('table.table a')[:self.ranking]
            for a_tag in a_tags:
                href = str(a_tag.get('href'))
                company_no = href.split('?no=')[1]
                name = str(a_tag.get('title'))

                # 整理資料輸出
                data: CompaniesList = {'href': href, 'company_no': company_no, 'name': name}
                result.append(data)

            return result
        except Exception as e:
            raise e

    def extract_info(self, companies: list[CompaniesList]):
        """
        清理資料
        :param companies: 
        :return: 
        """
        try:
            result = []
            for company in companies:

                html = requests.get(url=self.detail + company['company_no'], headers=self.headers, verify=False,
                                    data=None)
                beautiful_soup = BeautifulSoup(html.text, features='lxml')
                tr_tags = beautiful_soup.select('table.table.table-striped#basic-data tr')

                data: CompaniesInfo = {'unified_no': None, 'c_name': None, 'e_name': None,
                                       'responsible_person': None, 'c_address': None, 'e_address': None,
                                       'approve_date': None, 'modified_date': None}
                # 整理輸出資料
                for tr_tag in tr_tags:
                    td_tags = tr_tag.find_all('td')
                    if '統一編號' in str(td_tags[0]):
                        data['unified_no'] = td_tags[1].text

                    if '公司名稱' in str(td_tags[0]):
                        data['c_name'] = td_tags[1].text

                    if '英文名稱' in str(td_tags[0]):
                        data['e_name'] = td_tags[1].text

                    if '代表人姓名' in str(td_tags[0]):
                        data['responsible_person'] = td_tags[1].text.strip()

                    if '公司所在地' in str(td_tags[0]):
                        data['c_address'] = td_tags[1].text.strip()

                    if '英文地址' in str(td_tags[0]):
                        data['e_address'] = td_tags[1].text.strip()

                    if '核准設立日期' in str(td_tags[0]):
                        data['approve_date'] = self.to_ad_year_format(td_tags[1].text)

                    if '最後核准變更日期' in str(td_tags[0]):
                        data['modified_date'] = self.to_ad_year_format(td_tags[1].text)

                result.append(data)
                # 間隔時間, 預防被源站封鎖
                time.sleep(self.idle_time)

            self.q.put(result)
        except Exception as e:
            raise e

    @staticmethod
    def to_ad_year_format(val: str) -> str:
        """
        轉西元年
        :param val: 民國年字串
        :return: 西元字串
        074年5月13日 -> 1984年5月13日
        """
        try:
            val = val.strip().split('年')
            year = int(val[0]) + 1911
            return str(year) + '年' + val[1]
        except Exception as e:
            raise e

    def insert_to_database(self, data: list[CompaniesInfo]) -> None:
        """
        爬蟲資料寫進ＤＢ
        :param data: 需insert to DB 的資料集
        :return:
        """
        try:
            # 创建数据库引擎
            engine = create_engine(ConnectionString.official.value)
            # 创建会话类
            session = sessionmaker(bind=engine)
            # 创建会话实例
            session = session()
            self.update_check_time(session)

            insert_collection = []

            for item in data:
                insert_collection.append(
                    Information(
                        unified_no=item['unified_no'],
                        c_name=item['c_name'],
                        e_name=item['e_name'],
                        responsible_person=item['responsible_person'],
                        c_address=item['c_address'],
                        e_address=item['e_address'],
                        approve_date=item['approve_date'],
                        modified_date=item['modified_date'],
                        cancel=0,
                        create_time=self.tw_now_time()

                    )
                )

            if len(data) > 0:
                session.bulk_save_objects(insert_collection)
                session.commit()
            else:
                session.rollback()

        except Exception as e:
            raise e

    def update_check_time(self, session: sqlalchemy.orm.Session) -> None:
        """
        更新資料, 將所有資料的cancel => 1.
        :param session: sqlalchemy.orm.Session
        :return:
        """
        try:
            stmt_q = (
                update(Information)
                .where(Information.cancel == 0)
                .values(cancel=1, update_time=self.tw_now_time())
            )
            session.execute(stmt_q)
            # session.commit()
        except Exception as ex:
            raise ex

    def run(self) -> None:
        """
        工廠模式 入口
        :return:
        """
        try:
            # 爬取資料
            data = self.scrape_page()
            # 寫進資料庫
            self.insert_to_database(data)
        except Exception as e:
            raise e

    @staticmethod
    def tw_now_time() -> datetime:
        """
        回傳當下台灣時間
        :return:
        """
        try:
            utc_now = datetime.utcnow()  # 獲取 UTC 現在時間
            return utc_now + timedelta(hours=8)  # 台灣時間
        except Exception as e:
            raise e
