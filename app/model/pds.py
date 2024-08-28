from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base


# back_populates : 양방향 관계설정, 관계의 상호참조
class Pds(Base):
    __tablename__ = 'pds'

    pno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    userid: Mapped[str] = mapped_column(ForeignKey('member.userid'), index=True) # 비식별관계     member.userid에 unique와 not null 을 주면 식별관계가 됨
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    views: Mapped[int] = mapped_column(default=0)
    contents: Mapped[str]
    attachs = relationship('PdsAttach', back_populates='pds') # 하나의 gallery는 하나 이상의 attach가 존재 (1:n)

class PdsAttach(Base):
    __tablename__ = 'pdsattach'

    pano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    pno: Mapped[int] = mapped_column(ForeignKey('pds.pno'), index=True)
    fname: Mapped[str] = mapped_column(nullable=False)
    fsize: Mapped[int] = mapped_column(default=0)  # 용량
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    pds = relationship('Pds', back_populates='attachs')  # 하나의 attach는 하나의 gallery에 속함
