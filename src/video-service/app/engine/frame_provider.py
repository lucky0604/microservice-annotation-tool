# -*- coding: utf-8 -*-
"""
@Time    : 11/5/20 6:03 PM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : frame_provider.py
@Desc    : Description about this file
"""
import math
from enum import Enum
from io import BytesIO
import cv2
import numpy as np
from PIL import Image
from ..engine.mime_types import mimetypes
from ..engine.media_extractors import VideoReader, ZipReader
# from ..api.db import DataChoice, StorageMethodChoice
from ..engine.cache import CacheInteraction

class RandomAccessIterator:
    def __init__(self, iterable):
        self.iterable = iterable
        self.iterator = None
        self.pos = -1

    def __iter__(self):
        return self

    def __next__(self):
        return self[self.pos + 1]

    def __getitem__(self, idx):
        assert 0 <= idx
        if self.iterator is None or idx <= self.pos:
            self.reset()

        v = None
        while self.pos < idx:
            # don't keep the last item in self, it can be expensive
            v = next(self.iterator)
            self.pos += 1
        return v

    def reset(self):
        self.iterator = iter(self.iterable)
        self.pos = -1


class FrameProvider:
    VIDEO_FRAME_EXT = '.PNG'
    VIDEO_FRAME_MIME = 'image/png'

    class Quality(Enum):
        COMPRESSED = 0
        ORIGINAL = 100

    class Type(Enum):
        BUFFER = 0
        PIL = 1
        NUMPY_ARRAY = 2

    class ChunkLoader:
        def __init__(self, reader_class, path_getter):
            self.chunk_id = None
            self.chunk_reader = None
            self.reader_class = reader_class
            self.get_chunk_path = path_getter

        def load(self, chunk_id):
            if self.chunk_id != chunk_id:
                self.chunk_id = chunk_id
                self.chunk_reader = RandomAccessIterator(
                    self.reader_class([self.get_chunk_path(chunk_id)])
                )
            return self.chunk_reader

    def __init__(self, db_data):
        self._db_data = db_data
        self._loaders = {}

        reader_class = {
            DataChoice.IMAGESET: ZipReader,
            DataChoice.VIDEO: VideoReader,
        }

        if db_data.storage_method == StorageMethodChoice.CACHE:
            cache = CacheInteraction()

            self._loaders[self.Quality.COMPRESSED] = self.BuffChunkLoader(
                reader_class[db_data.compressed_chunk_type],
                cache.get_buff_mime,
                self.Quality.COMPRESSED,
                self._db_data
            )
            self._loaders[self.Quality.ORIGINAL] = self.BuffChunkLoader(
                reader_class[db_data.original_chunk_type],
                cache.get_buff_mime,
                self.Quality.ORIGINAL,
                self._db_data
            )
        else:
            self._loaders[self.Quality.COMPRESSED] = self.ChunkLoader(
                reader_class[db_data.compressed_chunk_type],
                db_data.get_compressed_chunk_path
            )
            self._loaders[self.Quality.ORIGINAL] = self.ChunkLoader(
                reader_class[db_data.original_chunk_type],
                db_data.get_original_chunk_path
            )

    def __len__(self):
        return self._db_data.size

    def _validate_frame_number(self, frame_number):
        frame_number_ = int(frame_number)
        if frame_number_ < 0 or frame_number_ >= self._db_data.size:
            raise Exception('Incorrect requested frame number: {}'.format(frame_number_))

        chunk_number = frame_number_ // self._db_data.chunk_size
        frame_offset = frame_number_ % self._db_data.chunk_size

        return frame_number_, chunk_number, frame_offset

    def _validate_chunk_number(self, chunk_number):
        chunk_number_ = int(chunk_number)
        if chunk_number_ < 0 or chunk_number_ >= math.ceil(self._db_data.size / self._db_data.chunk_size):
            raise Exception('requested chunk does not exist')

        return chunk_number_

    @staticmethod
    def _av_frame_to_png_bytes(av_frame):
        pil_img = av_frame.to_image()
        buf = BytesIO()
        pil_img.save(buf, format = 'PNG')
        buf.seek(0)
        return buf

    def _convert_frame(self, frame, reader_class, out_type):
        if out_type == self.Type.BUFFER:
            return self._av_frame_to_png_bytes(frame) if reader_class is VideoReader else frame
        elif out_type == self.Type.PIL:
            return frame.to_image() if reader_class is VideoReader else Image.open(frame)
        elif out_type == self.Type.NUMPY_ARRAY:
            if reader_class is VideoReader:
                image = np.array(frame.to_image())
            else:
                image = np.array(Image.open(frame))
            if len(image.shape) == 3 and image.shape[2] in {3, 4}:
                image[:, :, :3] = image[:, :, 2::-1]        # RGB to BGR
            return image
        else:
            raise Exception('unsupported output type')

    def get_preview(self):
        return self._db_data.get_preview_path()

    def get_chunk(self, chunk_number, quality = Quality.ORIGINAL):
        chunk_number = self._validate_chunk_number(chunk_number)
        if self._db_data.storage_method == StorageMethodChoice.CACHE:
            return self._loaders[quality].get_chunk_path(chunk_number, quality, self._db_data)
        return self._loaders[quality].get_chunk_path(chunk_number)

    def get_frame(self, frame_number, quality = Quality.ORIGINAL, out_type = Type.BUFFER):
        _, chunk_number, frame_offset = self._validate_frame_number(frame_number)
        loader = self._loaders[quality]
        chunk_reader = loader.load(chunk_number)
        frame, frame_name, _ = chunk_reader[frame_offset]

        frame = self._convert_frame(frame, loader.reader_class, out_type)
        if loader.reader_class is VideoReader:
            return (frame, 'image/png')
        return (frame, mimetypes.guess_type(frame_name))

    def get_frames(self, quality = Quality.ORIGINAL, out_type = Type.BUFFER):
        for idx in range(self._db_data.size):
            yield self.get_frame(idx, quality=quality, out_type=out_type)

