# 從typing引入TypedDict
from typing import TypedDict


class CompaniesList(TypedDict):
    """
    公司清單
    """
    # 公司Summary href
    href: str

    # 公司代碼
    company_no: str

    # 公司名稱
    name: str


class CompaniesInfo(TypedDict):
    """
    公司資訊
    """
    # 統一編號
    unified_no: str

    # 公司中文名稱
    c_name: str

    # 公司英文名稱
    e_name: str

    # 代表人姓名
    responsible_person: str

    # 公司所在地址(中文)
    c_address: str

    # 公司所在地址(英文)
    e_address: str

    # 設立核准日期
    approve_date: str

    # 最後核准變更日期
    modified_date: str
