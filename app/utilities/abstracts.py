import abc
from abc import ABC


class CrawlerBase(ABC):

    @abc.abstractmethod
    def scrape_page(self) -> list:
        """
        爬資料
        :return:
        """
        pass

    @abc.abstractmethod
    def insert_to_database(self, result: list) -> None:
        """
        儲存資料
        :return:
        """
        pass

    @abc.abstractmethod
    def run(self) -> None:
        """
        工廠模式, ETL 入口
        :return:
        """
        pass
