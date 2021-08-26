#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sqlalchemy import (
    Column, create_engine, MetaData, Table, Integer, String, DateTime, Text, ForeignKey
)
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import mapper, relationship
from databases import Database
import datetime

DATABASE_URI = ''
engine = create_engine(DATABASE_URI)

metadata = MetaData()



video_record_detail = Table(
    'video_record_detail',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False, comment='主键'),
    Column('pid', Integer, comment='项目ID'),
    Column('rid', Integer, comment='数据集ID'),
    Column('rdid', Integer, comment='数据ID'),
    Column('imagepath', String(100), comment='视频地址'),
    Column('detail', LONGTEXT, comment='标记详情'),  # 更新
    Column('crtime', Integer, comment='标注所花时间'),  # 具体标注时间
    Column('created', Integer, comment='创建时间'),
    Column('checked', Integer, comment='检票时间'),
    Column('status', Integer, default=0, comment='状态：0、默认 1、初审 2、跳过'),  # 提交改为1 跳过改为2
    Column('check', Integer, default=0, comment='状态：0、默认 1、通过 2、未通过 3、已修改'),
    Column('uid', Integer, comment='最后修改人'),  # 标注人员
    Column('updated', Integer, comment='修改时间'),  # 实时更新时间
    Column('count', Integer, comment='复审次数'),
    Column('remark', Text, comment='备注信息'),
    Column('rname', String(255), comment='数据集名称'),
    Column('uname', String(255), comment='标注员名称'),
    Column('iname', String(255), comment='视频名称'),
    Column('filesize', Integer, comment='视频大小'),
    Column('height', Integer, comment='视频高度'),
    Column('check_uid', Integer, comment='审核用户ID'),
    Column('check_num', Integer, comment='质检次数'),
    Column('width', Integer, comment='视频宽度'),
    Column('cctime', String(100), comment='单张质检总时间'),
    Column('accept_check', Integer, default=0, comment='超管质检状态：0 默认 1、通过 2、未通过 3、已修改'),
    Column('accept_check_num', Integer, default=0, comment='超管质检次数 默认0'),
    Column('accept_cctime', Integer, comment='超管质检所需时间'),
    Column('accept_check_uid', Integer, comment='验收员ID'),
    Column('is_per', Integer, default=0, comment='是否需要执行定时任务：默认0、否 1、是'),  # 提交后改为1
    Column('label_counts', Integer, comment='标签数量'),
    Column('thumb_img', String(512), comment='缩略图地址'),
    Column('pcd_path', String(512), comment='PCD文件地址'),
    Column('filetype', Integer, comment='数据类型，图片默认为0， 点云为1，视频为2'),
    Column('classifications', LONGTEXT, comment='视频属性'),
)


class VideoRecordDetail(object):
    def __init__(self, id, pid, rid, rdid, imagepath, detail,
                 crtime, created, checked, status, check,
                 uid, updated, count, remark, rname, uname, iname,
                 filesize, height, check_uid, check_num, width, cctime,
                 accept_check, accept_check_num, accept_cctime,
                 accept_check_uid, is_per, label_counts, thumb_img,
                 pcd_path, filetype, classifications):
        self.id = id
        self.pid = pid
        self.rid = rid
        self.rdid = rdid
        self.imagepath = imagepath
        self.detail = detail
        self.crtime = crtime
        self.created = created
        self.checked = checked
        self.status = status
        self.check = check
        self.uid = uid
        self.updated = updated
        self.count = count
        self.remark = remark
        self.rname = rname
        self.uname= uname
        self.iname = iname
        self.filesize = filesize
        self.height = height
        self.check_uid = check_uid
        self.check_num = check_num
        self.width = width
        self.cctime = cctime
        self.accept_check = accept_check
        self.accept_check_num = accept_check_num
        self.accept_cctime = accept_cctime
        self.accept_check_uid = accept_check_uid
        self.is_per = is_per
        self.label_counts = label_counts
        self.thumb_img = thumb_img
        self.pcd_path = pcd_path
        self.filetype = filetype
        self.classifications = classifications

    def __repr__(self):
        return f'<VideoRecordDetail({self.id}, {self.iname})>'

video_record_zip = Table(
    'record_video_detail',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False, comment='主键'),
    Column('uid', Integer, comment='用户id'),
    Column('rid', Integer, comment='数据集id'),
    Column('rdid', Integer, comment='数据详情id'),
    Column('url', String(512), comment='链接地址'),
    Column('ctime', DateTime, comment='创建时间'),
    Column('utime', DateTime, comment='更新时间'),
    Column('status', Integer, default=0, comment='状态')
)

class VideoRecordZip(object):
    def __init__(self, id, uid, rid, rdid, url, ctime, utime, status):
        self.id = id
        self.uid = uid
        self.rid = rid
        self.rdid = rdid
        self.url = url
        self.ctime = ctime
        self.utime = utime
        self.status = status

    def __repr__(self):
        return f'<VideoRecordZip({self.id}, {self.iname})>'

mapper(VideoRecordDetail, video_record_detail)
mapper(VideoRecordZip, video_record_zip)

database = Database(DATABASE_URI)
