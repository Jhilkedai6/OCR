from celery import Celery
from fastapi import UploadFile
from io import BytesIO
from PIL import Image
import pytesseract


celery_app = Celery(
    'worker',
    broker='pyamqp://guest@localhost//',   # RabbitMQ broker URL
    backend='rpc://'  # RabbitMQ does not store results by default; use rpc for simple results
)

@celery_app.task
def extract_text(file: bytes):

    image = Image.open(BytesIO(file))
    text = pytesseract.image_to_string(image)

    return text
