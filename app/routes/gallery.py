from collections import defaultdict
from typing import List

from fastapi import APIRouter, Request, UploadFile, File
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.schema.gallery import NewGallery
from app.service.gallery import get_gallery_data, process_upload, GalleryService
gallery_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@gallery_router.get('/list/{cpg}', response_class=HTMLResponse)
async def glist(req: Request, cpg: int, db: Session = Depends(get_db)):
    try:
        galist = GalleryService.select_gallery(cpg, db)

        return templates.TemplateResponse('gallery/list.html',
                                          {'request': req, 'galist': galist})

    except Exception as ex:
        print(f'▷▷▷ list 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)   # 응답을 보냄

@gallery_router.get('/write', response_class=HTMLResponse)
async def write(req: Request):
    return templates.TemplateResponse('gallery/write.html', {'request': req})

@gallery_router.post('/write', response_class=HTMLResponse)
async def writeok(req: Request, gallery: NewGallery = Depends(get_gallery_data),
                files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
        print(gallery)
        attachs = await process_upload(files)
        print(attachs)
        if GalleryService.insert_gallery(gallery, attachs, db):
            return RedirectResponse('/gallery/list/1', 303)

    except Exception as ex:
        print(f'▷▷▷ writeok 오류발생 {str(ex)}')
        return RedirectResponse('member/error.html', 303)


@gallery_router.get('/view/{gno}', response_class=HTMLResponse)
async def view(req: Request, gno: int, db: Session = Depends(get_db)):
    try:
        # sql문을 두개 작성하고 값을 2개 가져온다. 그래서 rs1 과 rs2
        rows = GalleryService.selectone_gallery(gno, db)

        gallery_dict = defaultdict(list)
        for row in rows:
            gallery, gal_attach = row
            gallery_dict[gallery].append(gal_attach)

        return templates.TemplateResponse('gallery/view.html',
                                          {'request': req, 'galleries': gallery_dict.items()})
    except Exception as ex:
        print(f'▷▷▷ view 오류발생 {str(ex)}')
        return RedirectResponse('member/error.html', 303)