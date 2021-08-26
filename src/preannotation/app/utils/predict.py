import os
import pathlib
import tensorflow as tf
import time
from object_detection.utils import label_map_util
import numpy as np
from tensorflow.python.eager.context import num_gpus

PATH_TO_MODEL = 'my_model/saved_model'
PATH_TO_LABELS = 'my_label/label.pbtxt'


detect_fn = tf.saved_model.load(PATH_TO_MODEL)
category_index = label_map_util.create_categories_from_labelmap(PATH_TO_LABELS, use_display_name=True)

def predict(image):
	image_np = np.array(image)
	input_tensor = tf.convert_to_tensor(image_np)
	input_tensor = input_tensor[tf.newaxis, ...]
	detections = detect_fn(input_tensor)
	num_detections = int(detections.pop('num_detections'))
	detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
	detections['num_detections'] = num_detections
	detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
	boxes = detections['detection_boxes']
	max_boxes_to_draw = boxes.shape[0]
	scores = detections['detection_scores']
	min_score_thresh = 0.4		# NMS
	coord = []
	for i in range(min(max_boxes_to_draw, boxes.shape[0])):
		print(scores)
		print("===")
		print(boxes)
		print("====")
		print(detections['detection_classes'])
		if scores is None or scores[i] > min_score_thresh:
			points = {}
			class_name = category_index[detections['detection_classes'][i]]['name']
			(ymin, xmin, ymax, xmax) = boxes[i]
			width, height = image.size
			points['xmin'] = xmin * width
			points['xmax'] = xmax * width
			points['ymin'] = ymin * height
			points['ymax'] = ymax * height
			points['class'] = class_name
			coord.append(points)
		
	
	return coord