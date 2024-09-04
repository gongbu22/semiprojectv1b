from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base


# back_populates : 양방향 관계설정, 관계의 상호참조
class Gallery(Base):
    __tablename__ = 'gallery'
    __table_args__ = {'sqlite_autoincrement': True}

    gno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String(250), index=True)
    userid: Mapped[str] = mapped_column(String(18), ForeignKey('member.userid'), index=True) # 비식별관계     member.userid에 unique와 not null 을 주면 식별관계가 됨
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    views: Mapped[int] = mapped_column(default=0)
    contents: Mapped[str] = mapped_column(Text)
    attachs = relationship('GalAttach', back_populates='gallery') # 하나의 gallery는 하나 이상의 attach가 존재 (1:n)

class GalAttach(Base):
    __tablename__ = 'galattach'
    __table_args__ = {'sqlite_autoincrement': True}

    gano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    gno: Mapped[int] = mapped_column(ForeignKey('gallery.gno'), index=True)
    fname: Mapped[str] = mapped_column(String(35), nullable=False)
    fsize: Mapped[int] = mapped_column(default=0)  # 용량
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    gallery = relationship('Gallery', back_populates='attachs')  # 하나의 attach는 하나의 gallery에 속함
