from pydantic import BaseModel

# class LoginMember(BaseModel):
#     userid: str
#     passwd: str
#
# class NewMember(LoginMember):
#     name: str
#     email: str
#     captcha: str


class NewGallery(BaseModel):
    userid: str
    title: str
    contents: str
    # captcha: str
