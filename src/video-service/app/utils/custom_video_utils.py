# -*- coding: utf-8 -*-
"""
@Time    : 11/9/20 5:22 PM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : custom_video_utils.py
@Desc    : Description about this file
"""
import rq
from urllib import error as urlerror
from urllib import parse as urlparse
from urllib import request as urlrequest
import os
import av

def download_data(urls, upload_dir):
    print(urls, ' -------- down load urls -----------')
    job = rq.get_current_job()
    local_files = {}
    for url in urls:
        name = os.path.basename(urlrequest.url2pathname(urlparse.urlparse(url).path))
        if name in local_files:
            raise Exception('filename collision: {}'.format(name))
        job.meta['status'] = '{} is being downloaded...'.format(url)
        job.save_meta()
        req = urlrequest.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urlrequest.urlopen(req) as fp, open(os.path.join(upload_dir, name), 'wb') as tfp:
                while True:
                    block = fp.read(8192)
                    if not block:
                        break
                    tfp.write(block)
        except urlerror.HTTPError as err:
            raise Exception('Failed to download ' + url + '. ' + str(err.code) + ' - ' + err.reason)
        except urlerror.URLError as err:
            raise Exception('Invalid URL: ' + url + '. ' + err.reason)
        local_files[name] = True
    return list(local_files.keys())

# create pyav container
def create_av_container(path, w, h, rate, options, f = 'mp4'):
    print(path, ' ------- video path ----------')
    # x264 requires width and height must be divisible by 2 for yuv420p
    if h % 2:
        h += 1
    if w % 2:
        w += 1
    count = 0
    container = av.open(path)
    stream = container.streams.video[0]
    for frame in container.decode(stream):
        print(round(float(frame.pts * stream.time_base), 2), ' ----------- video time -------------')
    # for packet in container.demux():
    #     if packet.stream.type == 'video':
    #         for frame in packet.decode():
    #             if count % 2.3 == 0:
    #                 frame.to_image().save('./app/images/%04d.png' % count)
    #             count += 1
    
    return container
