from sqlalchemy import BigInteger, Column, DateTime, String, Integer, create_engine
from sqlalchemy.orm import declarative_base

from app.config.db_manager import ConnectionString

Base = declarative_base()

# 创建数据库引擎
engine = create_engine(ConnectionString.official.value)


class Information(Base):
    __tablename__ = "information"
    __table_args__ = {"comment": "公司資訊檔"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    unified_no = Column(String(16), nullable=True, comment="統一編號")
    c_name = Column(String(128), nullable=True, comment="公司中文名稱")
    e_name = Column(String(128), nullable=True, comment="公司英文名稱")
    responsible_person = Column(String(64), nullable=True, comment="代表人姓名")
    c_address = Column(String(512), nullable=True, comment="公司所在地(中文)")
    e_address = Column(String(512), nullable=True, comment="公司所在地(英文)")
    approve_date = Column(String(32), nullable=True, comment="設立核准日期")
    modified_date = Column(String(32), nullable=True, comment="最後核准變更日期")
    cancel = Column(Integer, nullable=False, comment="是否生效", index=True)
    create_time = Column(DateTime, nullable=False, comment="建立時間")
    update_time = Column(DateTime, nullable=True, comment="修改時間", server_default=None)


Base.metadata.create_all(engine)
