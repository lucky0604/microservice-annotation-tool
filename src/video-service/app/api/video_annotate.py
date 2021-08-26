#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from starlette.requests import Request
from starlette.websockets import WebSocket
from ..utils.test import TEST_HELLO

from app.api.db_manager import get_token, check_auth, save_redis, save_redis_mysql, get_video_detail, \
    export_detail_coco, save_video_thumb, track_detail, get_video_chunk_files, update_mark_detail, \
    video_chunk_detail
from app.api.models import VideoIn, UserSignIn, DetailIn, DetailOut, ExportData, OSSVideoModel, BBoxDetail, VideoOut, ChunkVideoModel, ChunkVideoDetailModel
import cv2
import json
import base64
from phpserialize import loads
from ..utils.constants import StatusCode
from ..utils.result import ResultCommon

import datetime

video_annotate = APIRouter()


@video_annotate.get('/', summary="测试API", tags=["Test"], description="")
async def test_video():
    return {"message": TEST_HELLO}


@video_annotate.post('/upload_video', status_code=201, summary="上传视频到服务器本地API", tags=["Frontend"])
async def upload_video(file: UploadFile = File(...)):
    contents = await file.read()
    print(file.filename, '---- filename -----')
    with open('./app/video/' + file.filename, 'wb') as f:
        f.write(contents)
    '''
    container = av.open('./app/video/' + file.filename)
    for frame in container.decode(video = 0):
        frame.to_image().save('./app/video/frame-%04d.jpg' % frame.index)
    print(file, ' ----- file detail ------')
    '''
    '''
    # cut image by using frame
    vidcap = cv2.VideoCapture('./app/video/' + file.filename)
    image_dir = './app/video/'
    frame_frequency = 25    # cut an image every frame_frequency frame
    total_frame = 0
    id = 0
    while True:
        ret, frame = vidcap.read()
        if ret is False:
            break
        total_frame += 1
        if total_frame % frame_frequency == 0:
            id += 1
            image_name = image_dir + str(id) + '.jpg'
            cv2.imwrite(image_name, frame)
    '''
    vidcap = cv2.VideoCapture('./app/video/' + file.filename)
    length = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)  # get all frames
    h = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))  # get frame rate
    c = 0
    rval = vidcap.isOpened()
    print(fps, ' ------- fps -----')
    print(length, ' ------ length ------')
    print((w, h), ' ------- size -------')
    # 获取指定位置的帧
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, 10)
    flag, frame = vidcap.read()
    if flag:
        cv2.imwrite('./app/video/' + '10.jpg', frame)
    '''
    # 视频转图片
    while rval:
        c = c + 1
        rval, frame = vidcap.read()
        if rval:
            cv2.imwrite('./app/video/' + str(c) + '.jpg', frame)
            cv2.waitKey(1)
    vidcap.release()
    '''
    return {'message': file}


@video_annotate.get('/test_redis', summary="测试权限验证", description="", tags=["Backend"], deprecated=True)
async def auth(request: Request, user: UserSignIn = Depends(UserSignIn.as_form)):
    # 手动写入redis数据用以测试
    # await request.app.state.redis.execute('set', 3066, '{"uid":3066,"pwd":"MTIzNDU2YQ==","rand":"159489699811021495","token":"2ccf093f147e7d88d7610a8be2bdcf66","save_time":1749139200,"time":1594902356}')
    result = await check_auth(request, user.auth, user.token)
    if result:
        return {'message': 'login success', 'userInfo': result}
    return {'message': 'login error'}


'''
parameter:
started: 1602845041         // optional
pid: 4899
did: 1258225
checkType: 
ended: 1602845064   // optional
detail: {}
language: zh-cn
token: 1f99c8537e87cb5fcde9fbb72e688c83
auth: xxxx
'''


@video_annotate.post('/auto_submit', summary="自动提交存入Redis", description="自动提交标注数据存入redis API", deprecated=True, tags=['Frontend'])
async def auto_submit_detail(request: Request, detail: DetailIn = Depends(DetailIn.as_form)):
    user_info_redis = await check_auth(request, detail.auth, detail.token)
    user_info = str(detail.pid) + '-' + str(detail.did) + '-' + str(user_info_redis['userInfo']['uid'])
    annotate_detail = detail.detail
    result = await save_redis(request, user_info, annotate_detail)
    if result['code'] == 0:
        return {'message': 'success', 'code': 1, 'statusCode': 1}
    else:
        return result
    return {'message': 'redis server error'}


@video_annotate.post('/handle_submit', summary="视频标注提交", description="提交视频标注数据API", tags=['Frontend'])
async def handle_submit_detail(request: Request, detail: DetailIn = Depends(DetailIn.as_form)):
    '''
    视频标注提交
    :param request:
    :param detail: auth, token, **kwargs
    :return:
    '''
    user_info_redis = await check_auth(request, detail.auth, detail.token)
    if user_info_redis:
        result = await save_redis_mysql(request, detail)
        if result == 0: return ResultCommon.fail(0, StatusCode.FAILED.get_code(), StatusCode.FAILED.get_msg())
        return ResultCommon.success(1, StatusCode.SUCCESS.get_code(), StatusCode.SUCCESS.get_msg())
    else:
        raise ResultCommon.fail(0, StatusCode.UNLOGIN.get_code(), StatusCode.UNLOGIN.get_msg())

@video_annotate.post('/update_video_detail', summary="更新视频标注", description="更新视频标注数据详情API", tags=['Frontend'])
async def handle_update_submit(request: Request, detail: DetailIn = Depends(DetailIn.as_form)):
    user_info_redis = await check_auth(request, detail.auth, detail.token)
    if user_info_redis:
        result = await update_mark_detail(detail)
        if result == 0: return ResultCommon.fail(0, StatusCode.FAILED.get_code(), StatusCode.FAILED.get_msg())
        return ResultCommon.success(1, StatusCode.SUCCESS.get_code(), StatusCode.SUCCESS.get_msg())
    else:
        return ResultCommon.fail(0, StatusCode.UNLOGIN.get_code(), StatusCode.UNLOGIN.get_msg())

@video_annotate.post('/get_detail', summary="获取视频标注数据", description="获取视频标注数据详情API", tags=['Frontend'])
async def get_detail(request: Request, detail: DetailIn = Depends(DetailIn.as_form)):
    user_info_redis = await check_auth(request, detail.auth, detail.token)
    # user_info_redis = True
    if user_info_redis:
        result = await get_video_detail(request, detail)
        return result
    else:
        return {'message': 'login error', 'code': 0, 'statusCode': 0}


'''
@video_annotate.post('/get_detail')
async def get_video_detail(request: Request, payload: VideoOut):
    user_info_redis = await check_auth(request, payload.auth, payload.token)
    if user_info_redis:
        result = await get_video_detail(payload)
        return result
    else:
        return {'message': 'login error', 'code': 0, 'statusCode': 0}
'''


@video_annotate.post('/export_detail', summary="导出", description="视频数据导出API", tags=['Frontend'])
async def export_detail(request: Request, exportData: ExportData = Depends(ExportData.as_form)):
    user_info_redis = await check_auth(request, exportData.auth, exportData.token)
    if user_info_redis:
        if exportData.exportType == 'coco':
            result = await export_detail_coco(request, exportData)
            print(result, '-----action result- ----')
    else:
        return {'message': 'login error', 'code': 0, 'status': 0}


'''
获取视频宽高等详情信息
'''
@video_annotate.post('/get_video_detail', summary="获取视频高度宽度", description="老版获取视频宽度高度API", deprecated=True, tags=['Backend'])
async def get_video_thumb(request: Request, data: UserSignIn = Depends(UserSignIn.as_form)):
    user_info_redis = await check_auth(request, data.auth, data.token)
    if user_info_redis:
        vid_cap = cv2.VideoCapture(
            'http://test-images-oss.awkvector.com/mp4/3066/2020/10/876e5c1b57c794e7d97f2d8970f00888.mp4')
        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        return {'imgHeight': h, 'imgWidth': w, 'code': 1, 'success': 1}
    else:
        return {'message': 'login error', 'code': 0, 'status': 0}


# TODO: 获取视频第一帧作为缩略图
@video_annotate.post('/get_video_thumb', summary="获取视频缩略图，宽度，高度", description="新版获取视频缩略图，视频宽高API", tags=['Backend'])
async def get_video_thumb(request: Request, data: OSSVideoModel = Depends(OSSVideoModel.as_form)):
    '''
    获取视频详细信息
    :param request:
    :param data:
    :return: 视频高度，宽度，缩略图
    '''
    user_info_redis = await check_auth(request, data.auth, data.token)
    if user_info_redis:
        result = await save_video_thumb(data)
        return {'message': 'success', 'code': 1, 'statusCode': 1, 'data': result}


'''
arr = [
    {"x":190.46987951807228,"y":158.93975903614458},
    {"x":309.9759036144578,"y":158.93975903614458},
    {"x":309.9759036144578,"y":227.1807228915663},
    {"x":195.46987951807228,"y":227.1807228915663}
]
bbox = (arr[0].x, arr[0].y, arr[2].x - arr[0].x, arr[3].y - arr[0].y)
'''


@video_annotate.post('/auto_track', summary="视频追踪", description="", tags=['Frontend'])
async def get_object_track(request: Request, data: BBoxDetail = Depends(BBoxDetail.as_form)):
    user_info_redis = await check_auth(request, data.auth, data.token)
    if user_info_redis:
        result = await track_detail(data)
        if result is None: return ResultCommon.fail(0, StatusCode.FAILED.get_code(), StatusCode.FAILED.get_msg())
        # return {'message': 'success', 'code': 1, 'statusCode': 1, 'data': result}
        return ResultCommon.success(1, StatusCode.SUCCESS.get_code(), StatusCode.SUCCESS.get_msg(), result)
    else:
        return ResultCommon.fail(0, StatusCode.UNLOGIN.get_code(), StatusCode.UNLOGIN.get_msg())

# 获取视频标注界面数据
@video_annotate.post('/get_video_chunk', summary="获取视频zip AliOSS地址", description="获取视频拆帧后压缩为zip文件上传至阿里OSS", tags=['Backend'])
async def get_video_chunk(request: Request, detail: ChunkVideoModel = Depends(ChunkVideoModel.as_form)):
    # user_info_redis = await check_auth(request, detail.auth, detail.token)
    # if user_info_redis:
    res = await get_video_chunk_files(request, detail)
    return res

@video_annotate.post('/video_chunk_detail', summary="获取视频zip数据", description="", tags=['Frontend'])
async def get_video_chunk_detail(request: Request, detail: ChunkVideoDetailModel = Depends(ChunkVideoDetailModel.as_form)):
    user_info_redis = await check_auth(request, detail.auth, detail.token)
    if user_info_redis:
        result = await video_chunk_detail(detail.rdid)
        if result is None: return ResultCommon.fail(0, StatusCode.FAILED.get_code(), StatusCode.FAILED.get_msg())
        return result
    else:
        return ResultCommon.fail(0, StatusCode.UNLOGIN.get_code(), StatusCode.UNLOGIN.get_msg())
# @video_annotate.websocket('/video_chunk_detail')
# async def get_video_chunk_detail(websocket: WebSocket, rdid: int):
#     await websocket.accept()
#     result = await video_chunk_detail(rdid)
#     if result is None: return ResultCommon.fail(0, StatusCode.FAILED.get_code(), StatusCode.FAILED.get_msg())
#     while True:
#         await websocket.send_bytes(result)