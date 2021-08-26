from typing import Optional
from fastapi import FastAPI, File, UploadFile
from tensorflow.python.ops.gen_math_ops import Imag
from utils.image_handler import ImageHandler
from utils.predict import predict

app = FastAPI()

@app.get('/')
def index():
	return {"Hello": "World!"}

@app.post('/predict/image')
async def predict_image(image_path: str):
	
	info = ImageHandler.read_image(image_path)
	result = predict(info)
	return {"result": result}