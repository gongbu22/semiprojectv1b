from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.model.board import Board


class BoardService:
    @staticmethod
    def select_board(db, cpg):
        try:
            stdno = (cpg - 1) * 25
            stmt = select(Board.bno, Board.title, Board.userid,
                          Board.regdate, Board.views)\
                    .order_by(Board.bno.desc())\
                    .offset(stdno).limit(25)
            result = db.execute(stmt)

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_board 오류 발생 : {str(ex)}')