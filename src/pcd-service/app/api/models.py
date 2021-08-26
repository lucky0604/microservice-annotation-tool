# -*- coding: utf-8 -*-
"""
@Time    : 9/21/20 1:06 PM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : models.py
@Desc    : Description about this file
"""
from pydantic import BaseModel
from typing import List, Optional, Dict

class BaseLabel(BaseModel):
    id: int
    name: str

class ShowLabel(BaseLabel):
    settings : Optional[Dict] = None

class ProjectIn(BaseModel):
    name: str
