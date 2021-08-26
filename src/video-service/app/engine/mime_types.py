# -*- coding: utf-8 -*-
"""
@Time    : 11/5/20 12:34 PM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : mime_types.py
@Desc    : Description about this file
"""
import os
import mimetypes

_SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))
MEDIA_MIMETYPES_FILES = [
    os.path.join(_SCRIPT_DIR, 'media.mimetypes'),
]

mimetypes.init(files=MEDIA_MIMETYPES_FILES)