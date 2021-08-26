#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydantic import BaseModel
from fastapi import Form
from typing import Optional


class AuthModel(BaseModel):
    auth: str
    token: str


class VideoIn(BaseModel):
    name: str


class VideoOut(BaseModel):
    pid: str
    did: str

    @classmethod
    def as_form(cls, pid: str = Form(...), did: str = Form(...)):
        return cls(pid = pid, did = did)


class UserSignIn(BaseModel):
    auth: str
    token: str

    @classmethod
    def as_form(
            cls,
            auth: str = Form(...),
            token: str = Form(...),
    ):
        return cls(auth=auth, token=token)


class DetailIn(AuthModel):
    pid: int
    detail: str
    did: int
    check: str
    language: str
    started: Optional[int]
    ended: Optional[int]
    status: int
    classifications: str

    @classmethod
    def as_form(cls, pid: int = Form(...), detail: str = Form(...), auth: str = Form(...), token: str = Form(...),
                did: int = Form(...), check: str = Form(...), language: str = Form(...), status: int = Form(...), classifications: str = Form(...)):
        return cls(pid=pid, detail=detail, auth=auth, token=token, did=did, check=check, language=language, status=status, classifications=classifications)

class DetailOut(BaseModel):
    detail: Optional[str] = None
    message: Optional[str] = None
    code: int = 1
    statusCode: int = 1

    @classmethod
    def as_form(cls, detail: str = Form(...), code: int = Form(...), statusCode: int = Form(...)):
        return cls(detail = detail, code = code, statusCode = statusCode)
'''
class VideoOut(BaseModel):
    type: str
    number: int
    quality: str

    @classmethod
    def as_form(cls, type: str = Form(...), number: int = Form(...), quality: str = Form(...)):
        return cls(type = type, number = number, quality = quality)
'''
'''
pid=4965
language=en
auth=eyJpdiI6InhrdEhDeSt2anJ3TWVvQTdFUHpIZ2c9PSIsInZhbHVlIjoid0hpMFNEZURhZTYrM1lDaXVxdjlcLzkzS2hZMzU0MjgxdWdaeFFJbkIyUUI5RGVmUVdHZDJXeFwvdGg4Q1NnSXRZcENVNzBpZVwvT1c1dWNBWGNmcmw0blE9PSIsIm1hYyI6IjU4ZDU2Mjc3MjY3NTVhY2YzYzdhNTJhNWExZjVlOGI1ZmU2MmNlMmUyZmZkNGVhODNiZDA5MjVjZTI4ZTdjZWQifQ==
token=03fadf6fe11c30d87db3db98afcd0658
exportType=json
starttime=
endtime=
imageName=
check=-1
status=-1
userid=
drawColor=
'''
class ExportData(AuthModel):
    exportType: str
    pid: int
    language: str
    starttime: Optional[str] = None
    endtime: Optional[str] = None
    imageName: Optional[str] = None
    check: int
    status: int
    userid: Optional[int] = None
    drawColor: Optional[str] = None

    @classmethod
    def as_form(cls, exportType: str = Form(...), pid: int = Form(...), language: str = Form(...),
                starttime: Optional[str] = Form(...), endtime: Optional[str] = Form(...), imageName: Optional[str] = Form(...), check: int = Form(...),
                status: str = Form(...), userid: Optional[int] = Form(...), drawColor: Optional[str] = Form(...), auth: str = Form(...), token: str = Form(...)):
        return cls(auth = auth, token = token, exportType = exportType, pid = pid, language = language, stattime = starttime, endtime = endtime, imageName = imageName, check = check, status = status, userid = userid, drawColor = drawColor )


class OSSVideoModel(AuthModel):
    url: str

    @classmethod
    def as_form(cls, url: str = Form(...), auth: str = Form(...), token: str = Form(...)):
        return cls(auth = auth, token = token, url = url)


class BBoxDetail(AuthModel):
    bbox: str
    frame_index: int
    # url: str
    record_name: str
    uid: int
    rdid:int

    @classmethod
    def as_form(cls, auth: str = Form(...), token: str = Form(...), frame_index: str = Form(...), bbox: str = Form(...), record_name: str = Form(...), uid: int = Form(...), rdid: int = Form(...)):
        return cls(auth = auth, token = token, frame_index = frame_index, bbox = bbox, record_name = record_name, uid = uid, rdid = rdid)


class ChunkVideoModel(BaseModel):
    url: str
    uid: int
    
    @classmethod
    def as_form(cls, url: str = Form(...), uid: int = Form(...)):
        return cls(url = url, uid = uid)

class ChunkVideoDetailModel(AuthModel):
    rdid: int

    @classmethod
    def as_form(cls, rdid: int = Form(...), token: str = Form(...), auth: str = Form(...)):
        return cls(auth = auth, token = token, rdid = rdid)