from pydantic import BaseModel, Field
from typing import List, Optional


class Paragraph(BaseModel):
    text: str


class Image(BaseModel):
    src: str


class AdditionalContent(BaseModel):
    weiwenti: Optional[str] = Field(alias="微问题", default="")
    guanjianci: Optional[str] = Field(alias="关键词", default="")
    weiboshi: Optional[str] = Field(alias="微博士", default="")
    shiyanchang: Optional[str] = Field(alias="实验场", default="")
    kexueren: Optional[str] = Field(alias="科学人", default="")


class Section(BaseModel):
    title: str
    paragraphs: List[Paragraph]
    images: List[Image]
    additional_content: Optional[AdditionalContent] = None


class XHTMLDocument(BaseModel):
    sections: List[Section]


class CardRet(BaseModel):
    id: int = 0
    catagory: str = "天文"
    img: str = ""
    title: str = ""
    aud: str = ""
    tags: list[str] = []
    link: str = ""
