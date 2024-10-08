from math import ceil

from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.schema.board import NewReply
from app.service.board import BoardService

board_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

# 페이징 알고리즘
# 페이지당 게시글 수 : 25
# 1page : 1 ~ 25
# 2page : 26 ~ 50
# 3page : 51 ~ 75
# ...
# npage : (n - 1) * 25 + 1  ~ (n - 1) * 25 + 25

# 페이지네이션 알고리즘
# 현재페이지에 따라 보여줄 페이지 블록 결정
# ex) 총 페이지수 : 27일때
# => select count(bno) 총게시글수, ceil(count(bno)/25) 총페이지수 from board;

# cpg = 1: 1 2 3 4 5 6 7 8 9 10
# cpg = 3: 1 2 3 4 5 6 7 8 9 10
# cpg = 9: 1 2 3 4 5 6 7 8 9 10
# cpg = 11: 11 12 13 14 15 16 17 18 19 20
# cpg = 17: 11 12 13 14 15 16 17 18 19 20
# cpg = 23: 21 22 23 24 25 26 27
# startpage(stpgb) = ((cpg - 1) / 10) * 10 + 1

# 게시판 댓글 처리 : reply
# 댓글번호   댓글내용    작성자     작성일    부모글번호   부모댓글번호
# 1         헬로우염      123abc  20210611    100      1
# 4       왜영어로인사...  xyz987  20210611    100      1
# 2         방가방가     abc123  20210611    100       2
# 3         안녕하세요    xyz987  20210611    100      3
#
# => 댓글 출력 순서는 부모글번호로 추려낸후 부모댓글번호로 정렬

@board_router.get('/list/{cpg}', response_class=HTMLResponse)
async def list(req: Request, cpg: int,  db: Session = Depends(get_db)):
    try:
        stpgb = int((cpg - 1) / 10) * 10 + 1
        bdlist, cnt = BoardService.select_board(db, cpg)
        allpage = ceil(cnt / 25) # 총 페이지 수

        return templates.TemplateResponse('board/list.html',
                        {'request': req, 'bdlist': bdlist,
                         'cpg': cpg, 'stpgb': stpgb, 'allpage': allpage,
                         'baseurl': '/board/list/'})

    except Exception as ex:
        print(f'▷▷▷ list 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)   # 응답을 보냄

@board_router.get('/write', response_class=HTMLResponse)
async def write(req: Request):
    if 'logined_uid' not in req.session: # 로그인하지 않으면 글쓰기 금지!
        return RedirectResponse('/member/login', 303)

    return templates.TemplateResponse('board/write.html', {'request': req})


@board_router.get('/view/{bno}', response_class=HTMLResponse)
async def view(req: Request, bno: int, db: Session = Depends(get_db)):
    try:
        boards = BoardService.selectone_board(bno, db)
        return templates.TemplateResponse('board/view.html',
                                          {'request': req, 'boards': boards})

    except Exception as ex:
        print(f'▷▷▷ view 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)   # 응답을 보냄


@board_router.get('/list/{ftype}/{fkey}/{cpg}', response_class=HTMLResponse)
async def find(req: Request, ftype: str, fkey: str,
               cpg: int,  db: Session = Depends(get_db)):
    try:
        stpgb = int((cpg - 1) / 10) * 10 + 1
        bdlist, cnt = BoardService.find_select_board(db, ftype, '%'+fkey+'%', cpg)
        allpage = ceil(cnt / 25)

        return templates.TemplateResponse('board/list.html',
                                          {'request': req, 'bdlist': bdlist,
                                           'cpg': cpg, 'stpgb': stpgb, 'allpage': allpage,
                                           'baseurl': f'/board/list/{ftype}/{fkey}/'})

    except Exception as ex:
        print(f'▷▷▷ find 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)   # 응답을 보냄


@board_router.post('/reply', response_class=HTMLResponse)
async def replyok(reply: NewReply, db: Session = Depends(get_db)):
    try:
        if BoardService.insert_reply(db, reply):
            return RedirectResponse(f'/board/view/{reply.bno}',303)

    except Exception as ex:
        print(f'▷▷▷ replyok 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)   # 응답을 보냄

@board_router.post('/rreply', response_class=HTMLResponse)
async def rreplyok(reply: NewReply, db: Session = Depends(get_db)):
    try:
        if BoardService.insert_rreply(db, reply):
            return RedirectResponse(f'/board/view/{reply.bno}',303)

    except Exception as ex:
        print(f'▷▷▷ rreplyok 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)   # 응답을 보냄