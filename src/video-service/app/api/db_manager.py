#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.api.models import VideoIn
from app.api.db import database, video_record_detail, video_record_zip
# from starlette.requests import Request object, not fastapi
from starlette.requests import Request
import json
import base64
from phpserialize import loads
from Crypto.Cipher import AES
from ..utils.customUtils import merge_data
from sqlalchemy.sql import and_
import datetime
import time
import random
import shutil
import oss2
import re
import zipfile
import cv2
from ..utils.constants import ACCESS_KEY, ACCESS_KEY_SECRET
import os
import io
from starlette.responses import FileResponse, StreamingResponse
from time import time as timer
import urllib.request
import requests
from io import BytesIO
import glob
import sys

app_key = b''
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')


def decrypt(laravelEncrypedStringBase64, laravelAppKeyBase64):
    data = json.loads(base64.b64decode(laravelEncrypedStringBase64))
    value = base64.b64decode(data['value'])
    iv = base64.b64decode(data['iv'])
    key = base64.b64decode(laravelAppKeyBase64)
    decrypter = aesDecrypter(iv, key)
    decriptedSerailizedMessage = decrypter.decrypt(value)
    try:
        decriptedMessage = unserialize(decriptedSerailizedMessage)
        return str(decriptedMessage)
    except:
        raise Exception('Check you cyphered strings in Laravel using Crypt::encrypt() and NOT Crypt::encryptString()')

    return unserialize(mcrypt_decrypt(value, iv))


def aesDecrypter(iv, _key):
    decrypterAES_CBC = AES.new(key=_key, mode=AES.MODE_CBC, IV=iv)
    return decrypterAES_CBC


def unserialize(serialized):
    return loads(serialized)


async def check_auth(request: Request, auth, token):
    auth_info = bytes(auth, encoding='utf8')
    missing_padding = 4 - len(auth_info) % 4
    if missing_padding:
        auth_info += b'=' * missing_padding
    auth_info_decrypt = decrypt(auth_info, app_key)
    print(auth_info_decrypt, ' ------- auth info decrypt ------')
    global uid
    # 利用切片将auth_info_decrypt转为字符串，去掉首尾双引号仍然会有b''，此时为byte，因此从第三位开始截取
    uid = json.loads(auth_info_decrypt[2:-1])['uid']
    user_info = await get_token(request, uid)
    if user_info and user_info['token'] == token:
        print(user_info, ' ------- user info ---------')
        return user_info
        # return {'msg': 'login success', 'userInfo': user_info}
    return False


async def get_token(request: Request, uid):
    user_info = await request.app.state.redis.hget('userLoginToken', str(uid))
    print(user_info, ' ------ user info ---------')
    if user_info:
        return json.loads(user_info)
    else:
        return None


'''
chunk_size: null
client_files: ["VIRAT_S_010003_02_000165_000202.mp4"]
0: "VIRAT_S_010003_02_000165_000202.mp4"
compressed_chunk_type: "imageset"
frame_filter: ""
image_quality: 70
original_chunk_type: "imageset"
remote_files: []
server_files: []
size: 0
start_frame: 0
stop_frame: 0
use_cache: false
use_zip_chunks: false
'''
# async def upload_video(payload: VideoIn):
#     query = video.insert().values(**payload.dict())
#     return await database.execute(query=query)


'''
================================= 数据提交 ==================================
'''


async def save_redis(request: Request, dataKey, detail):
    # redis_data = await request.app.state.redis.get(dataKey)
    redis_data = await request.app.state.redis.execute('llen', dataKey)
    if redis_data == 0:
        await request.app.state.redis.execute('lpush', dataKey, detail)
        return {'message': 'success', 'code': 1, 'statusCode': 1}
    else:
        old_data_redis = await request.app.state.redis.lrange(dataKey, 0, 0)
        old_data = old_data_redis[0]
        new_data = merge_data(json.loads(old_data), json.loads(detail))
        await request.app.state.redis.execute('lpush', dataKey, new_data)
        return {'message': 'success', 'code': 1, 'statusCode': 1}

# 存储标注数据到mysql
async def save_redis_mysql(request: Request, payload):
    work_list = await request.app.state.redis.hget('productWorker' + str(payload.pid), 'uid' + str(uid))
    works = json.loads(work_list.strip("'<>() '").replace('\'', '\"'))
    for i in works:
        if int(i) == int(payload.did):
            works.remove(i)

    query = video_record_detail.update().where(
        and_(video_record_detail.c.id == payload.did, video_record_detail.c.pid == payload.pid)).values({
        'detail': str(payload.detail),
        'crtime': int(time.time()),
        'status': 1,
        'is_per': 1,
        'uid': uid,
        'accept_check': 0,
        'check': 0,
        'updated': int(time.time()),
        'classifications': payload.classifications
    })
    result = await database.execute(query)
    if result == 1:
        await request.app.state.redis.hset('productWorker' + str(payload.pid), 'uid' + str(uid), str(works))
    return result


async def update_mark_detail(payload):
    """更新标注数据

    Args:
        request (Request): [description]
        payload ([type]): [description]

    Returns:
        [type]: [description]
    """
    query = video_record_detail.update().where(
        and_(video_record_detail.c.id == payload.did, video_record_detail.c.pid == payload.pid)).values({
        'detail': str(payload.detail),
        'crtime': int(time.time()),
        'status': 1,
        'is_per': 1,
        'uid': uid,
        'accept_check': 0,
        'check': 0,
        'updated': int(time.time()),
        'classifications': payload.classifications
    })
    print(query, ' ---------- query ---------')
    result = await database.execute(query)
    return result

# 获取标注视频详情
async def get_video_detail(request: Request, payload):
    query = video_record_detail.select().where(
        and_(video_record_detail.c.pid == payload.pid, video_record_detail.c.id == payload.did))
    return await database.fetch_one(query=query)


'''
async def get_video_detail(request: Request, payload):

    data_type = payload.type
    data_id = payload.number
    data_quality = payload.quality

    possible_data_type_values = ('chunk', 'frame', 'preview')
    possible_quality_values = ('compressed', 'original')

    if not data_type or data_type not in possible_data_type_values:
        return {'statusCode': 400, 'code': 0, 'message': 'data type not specified or has wrong value'}
    elif data_type == 'chunk' or data_type == 'frame':
        if not data_id:
            return {'statusCode': 400, 'code': 0, 'message': 'id not specified'}
        elif data_quality not in possible_quality_values:
            return {'statusCode': 400, 'code': 0, 'message': 'wrong quality value'}
    '''

# 导出coco
async def export_detail_coco(request: Request, payload):
    query = video_record_detail.select().where(video_record_detail.c.pid == payload.pid)
    result = await database.fetch_all(query=query)
    return result

# 获取视频宽高，缩略图信息
async def save_video_thumb(payload):
    video_url = payload.url
    random_fps = random.randint(1, 100)
    video_cap = cv2.VideoCapture(video_url)
    h = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_cap.set(cv2.CAP_PROP_POS_FRAMES, random_fps)
    ok, frame = video_cap.read()
    if ok:
        cv2.imwrite('./app/video/thumb.jpg', frame)
        oss_auth = oss2.Auth(ACCESS_KEY, ACCESS_KEY_SECRET)
        current_date = datetime.datetime.now()
        bucketName = str(current_date).split(' ')[0].split('-')
        service = oss2.Bucket(oss_auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'test-jueixng-upload')
        file_path = '/'.join(bucketName)
        oss_result = service.put_object_from_file(str(uid) + '/' + str(file_path) + '/thumb.jpg',
                                                  './app/video/thumb.jpg')
        '''
        query = video_record_detail.update().where(and_(video_record_detail.c.id == payload.did, video_record_detail.c.pid == payload.pid)).values({
            'thumb_img': 'http://test-images-oss.awkvector.com/' + str(uid) + '/' + str(file_path) + '/thumb.jpg'
        })
        '''
        # return await database.execute(query)
        thumb_url = 'http://test-images-oss.awkvector.com/' + str(uid) + '/' + str(file_path) + '/thumb.jpg'
        video_detail = {
            'thumb_url': thumb_url,
            'video_height': h,
            'video_width': w
        }
        return video_detail


async def track_detail(payload):
    query = video_record_zip.select().where(video_record_zip.c.rdid == payload.rdid)
    result = await database.fetch_one(query = query)
    # 1, downlaod zip file from alioss
    starttime = datetime.datetime.now()
    # request = requests.get('http://test-images-oss.awkvector.com/3066/2020/11/13/7ad1215abcab93099d79e9bd0294dae5.zip')
    request = requests.get(result['url'])
    zip_file = zipfile.ZipFile(BytesIO(request.content))
    image_path = os.path.join('./app/images/', str(payload.uid) + '/' + str(payload.rdid) + '/')
    video_path = os.path.join('./app/videos/', str(payload.uid) + '/' + str(payload.rdid) + '/')
    # 2, extract zip
    if os.path.exists(image_path):
        shutil.rmtree(image_path)
    if os.path.exists(video_path):
        shutil.rmtree(video_path)
    os.makedirs(video_path)
    os.makedirs(image_path)
    zip_file.extractall(image_path)
    # 3, convert to video
    img_arr = []
    for filename in glob.glob(image_path + '*.jpg'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_arr.append(img)

    out = cv2.VideoWriter(video_path + '/' + payload.record_name + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, size)
    for i in range(len(img_arr)):
        out.write(img_arr[i])
    out.release()
    # 4, return track data
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == 'CSRT':
            tracker = cv2.TrackerCSRT_create()

    bbox = json.loads(payload.bbox)
    video_cap = cv2.VideoCapture(video_path + '/' + payload.record_name + '.mp4')
    ok, frame = video_cap.read()
    if not ok:
        return

    bbox_init = (bbox[0]['x'], bbox[0]['y'], bbox[2]['x'] - bbox[0]['x'], bbox[3]['y'] - bbox[0]['y'])
    ok = tracker.init(frame, bbox_init)
    track_result = []
        # track_index = int(payload.frame_index)
    track_index = payload.frame_index
    while True:
        track_index += 1
        ok, frame = video_cap.read()
        if not ok:
            break
        ok, bbox_result = tracker.update(frame)
        p1 = {'x': bbox_result[0], 'y': bbox_result[1]}
        p2 = {'x': bbox_result[0], 'y': bbox_result[1] + bbox_result[3]}
        p3 = {'x': bbox_result[0] + bbox_result[2], 'y': bbox_result[1] + bbox_result[3]}
        p4 = {'x': bbox_result[0] + bbox_result[2], 'y': bbox_result[1]}
        rec = [p1, p2, p3, p4]
        obj = {str(track_index): rec}
        track_result.append(obj)
    return track_result


async def get_video_chunk_files(request, payload):
    # TODO: 1, extract video into png
    count = 1
    # TODO: 3, send zip files to frontend by using sendfile()
    vidcap = cv2.VideoCapture(payload.url)
    file_name = payload.url.split('/')[-1].split('.')[0]
    if os.path.exists(os.path.join('app/data/' + file_name)):
        shutil.rmtree(os.path.join('app/data', file_name))
    os.makedirs('app/data/' + file_name)

    def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:
            cv2.imwrite("app/data/" + str(file_name) + '/' +str(count)+".jpg", image, [cv2.IMWRITE_JPEG_QUALITY,50]) # Save frame as JPG file
        return hasFrames
    sec = 0
    frameRate = 0.1 # Change this number to 1 for each 1 second

    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec)
    vidcap.release()

    if os.path.exists(os.path.join('app/zip', file_name)):
        shutil.rmtree(os.path.join('app/zip', file_name))
    os.makedirs('app/zip/' + file_name)

    # TODO: 2, chunk files and zip images
    import zipfile
    zip_name = file_name + '.zip'
    z = zipfile.ZipFile('app/zip/' + file_name + '/' + zip_name, 'w', zipfile.ZIP_DEFLATED)


    # 压缩整个文件夹
    for dirpath, dirnames, filenames in os.walk('app/data/' + str(file_name)):
        print(dirpath, ' ------ dir path -----')
        print(dirnames, ' -------- dirnames ------')
        print(filenames, ' ------- filenames -------')
        fpath = dirpath.replace('app/data/' + str(file_name), '')
        print(fpath, ' ---------- fpath before -----------')
        fpath = fpath and fpath + os.sep or ''
        print(fpath, ' ---------- fpath after ---------')
        for filename in filenames:
            print(filename, ' ------- file name --------')
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()

    main_list = next(os.walk('app/data/' + file_name))[2]
    main_list.sort(key = lambda x: int(x[:-4]))
    files = [os.path.join('app/data/' + str(file_name), f) for f in main_list]
    i = 0
    curr_subdir = None
    for f in files:
        if i % 100 == 0:
            subdir_name = os.path.join('app/data/' + file_name, str(int(i / 100 + 1)))
            os.mkdir(subdir_name)
            curr_subdir = subdir_name
        # move file to current_dir
        f_base = os.path.basename(f)
        shutil.move(f, os.path.join(subdir_name, f_base))
        i += 1

    sub_z = os.listdir('app/data/' + file_name)
    print(sub_z, ' ------ sub dir --------')
    for sub_dir in sub_z:
        sub_zip_file = file_name + '-' + sub_dir + '.zip'
        sub_zip = zipfile.ZipFile('app/zip/' + file_name + '/' + sub_zip_file, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk('app/data/' + str(file_name) + '/' + sub_dir):
            print(dirpath, ' ------ dir path -----')
            print(dirnames, ' -------- dirnames ------')
            print(filenames, ' ------- filenames -------')
            fpath = dirpath.replace('app/data/' + str(file_name) + '/' + sub_dir, '')
            print(fpath, ' ---------- fpath before -----------')
            fpath = fpath and fpath + os.sep or ''
            print(fpath, ' ---------- fpath after ---------')
            for filename in filenames:
                print(filename, ' ------- file name --------')
                sub_zip.write(os.path.join(dirpath, filename), fpath + filename)
        sub_zip.close()

    # TODO: 3, upload zip to ali oss
    url_result = []
    for zip_file in os.listdir('app/zip/' + file_name):
        single_url = {}
        if os.path.exists('app/zip/' + file_name):
            oss_auth = oss2.Auth(ACCESS_KEY, ACCESS_KEY_SECRET)
            current_data = datetime.datetime.now()
            bucketName = str(current_data).split(' ')[0].split('-')
            service = oss2.Bucket(oss_auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'test-jueixng-upload')
            file_path = '/'.join(bucketName)
            # return {'code': 1, 'statusCode': 1, 'message': 'success'}
            res = service.put_object_from_file(str(payload.uid) + '/' + file_path + '/' + file_name + '/' + zip_file + '.zip', 'app/zip/' + file_name + '/' + zip_file)
            print(res, ' --------- res code ------')
            if res.status == 200:
                single_url['zip_name'] = zip_file
                single_url['zip_url'] = 'http://test-images-oss.awkvector.com/' + str(payload.uid) + '/' + file_path + '/' + file_name + '/' + zip_file
                # return {'message': 'sucess', 'code': 1, 'statusCode': 1, 'url': 'http://test-images-oss.awkvector.com/' + str(uid) + '/' + file_path + '/' + file_name + '/' + zip_file + '.zip'}
            else:
                return {'code': 0, 'statusCode': 0, 'message': 'OSS server error'}
        url_result.append(single_url)
    print(url_result, ' --------- url result -----------')
    return url_result
    # return {'code': 0, 'statusCode': 0, 'message': 'server error'}

async def video_chunk_detail(payload):
    query = video_record_zip.select().where(video_record_zip.c.rdid == payload)
    result = await database.fetch_one(query = query)
    filename = result['url'].split('/')[-1]
    if os.path.exists(os.path.join('./', filename)):
        os.remove(os.path.join('./', filename))
    # urllib.request.urlretrieve(result['url'], os.path.join('./', filename))
    download_file = requests.get(result['url'])
    with open(os.path.join('./', filename), 'wb') as f:
        f.write(download_file.content)
    '''
    if os.path.exists(os.path.join('./', filename)):
        return FileResponse(os.path.join('./', filename), media_type='application/zip')
    '''
    if os.path.exists(os.path.join('./', filename)):
        f = open(os.path.join('./', filename), 'rb')
        return StreamingResponse(f)
