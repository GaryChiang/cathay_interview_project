from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from app.model.company import Information


class CompanyInquiry:
    @staticmethod
    def search(db: Session, company: str = '', unified_no: str = '') -> list[Information]:
        """
        查詢500強公司資訊
        :param unified_no: 統編
        :param company: 公司名稱
        :param db: sqlalchemy session
        :return:
        """
        try:
            stmt_q = select(Information).where(Information.cancel == 0)

            # 統編有查詢值
            if unified_no:
                stmt_q = stmt_q.where(Information.unified_no.like("%" + unified_no + "%"))
            # 公司有查詢值
            if company:
                stmt_q = stmt_q.where(
                    or_(
                        Information.c_name.like("%" + company + "%"),
                        Information.e_name.like("%" + company + "%"),
                    )
                )

            return db.execute(stmt_q).scalars().all()

        except Exception as e:
            raise e
