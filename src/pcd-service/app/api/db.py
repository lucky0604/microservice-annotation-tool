# -*- coding: utf-8 -*-
"""
@Time    : 9/21/20 12:52 PM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : db.py
@Desc    : Description about this file
"""
import os
from sqlalchemy import (Column, Integer, MetaData, String, Table, create_engine, ARRAY, Boolean, DateTime, JSON,
                        ForeignKey, UniqueConstraint)
from sqlalchemy.orm import mapper, relationship
from databases import Database
import datetime
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = ''

engine = create_engine(DATABASE_URI)

metadata = MetaData()

Base = declarative_base()

project = Table('projects', metadata,
                Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
                Column('name', String(50), nullable=False, unique=True),
                Column('settings', JSON, nullable=True)
                )


class Project(object):

    def __repr__(self):
        return f'<Project({self.id}, {self.name})>'


image = Table(
    'images',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('project_id', Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=True),
    Column('name', String(50), nullable=False),
    Column('tags', JSON, nullable=False)
)


class Image(object):
    __table_args__ = (UniqueConstraint('project_id', 'name'),)

    def __repr__(self):
        return f'<Image({self.id}, {self.name})>'


tag = Table(
    'tags',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('project_id', Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=True),
    Column('image_ids', JSON, nullable=True)
)


class Tag(object):
    __table_args__ = (UniqueConstraint('project_id', 'name'),)

    @staticmethod
    def update_tags_references(db, project_id, image, new_tags):
        new_tag_names = set(tag['label'] for tag in new_tags)
        old_tag_names = set(tag['label'] for tag in image.tags)

        # retrive only tags that will need update (^ operator is union - intersection)
        tags_to_update = new_tag_names ^ old_tag_names
        tags = {tag.name: tag
                for tag in db.query(Tag).filter(
                (Tag.project_id == project_id)
                & (Tag.name.in_(tags_to_update)))}

        # tags added to the image
        for tagname in (new_tag_names - old_tag_names):
            # exsiting Tag: add image_id to the list
            if tagname in tags:
                tags[tagname].image_ids.append(image.id)
            # create new Tag with this image_id as first reference
            else:
                db.add(Tag(project_id=project_id, name=tagname, image_ids=[image.id]))

        # Tags removed from the image
        for tagname in (old_tag_names - new_tag_names):
            # defensive: requests that update Tag references may have failed previously
            if tagname not in tags or image.id not in tags[tagname].image_ids:
                continue
            # remove image_id from this Tag's list
            tags[tagname].image_ids.remove(image.id)
            # if not further images are using this Tag, remove it
            if (not len(tags[tagname].image_ids)):
                db.delete(tags[tagname])


mapper(Project, project, properties={
    'images': relationship(Image, backref='project')
})
mapper(Image, image)
mapper(Tag, tag)
database = Database(DATABASE_URI)
