from minio import Minio
from fastapi import File, UploadFile
import io

Endpoint = "127.0.0.1:9000"
Access_key = "minioadmin"
screate_key = "minioadmin"
Bucket_name = "documents"

minio_client = Minio(
    endpoint=Endpoint,
    access_key=Access_key,
    secret_key=screate_key,
    secure=False
)

async def uplode_file(file: UploadFile):
    file_read = await file.read()

    file_like = io.BytesIO(file_read)

    minio_client.put_object(
        bucket_name=Bucket_name,
        object_name=file.filename,
        data=file_like,
        content_type=file.content_type,
        length=len(file_read)
    )

    data = {
        "url": f"http://{Endpoint}/{Bucket_name}/{file.filename}",
        "document_name": file.filename,
        "document_type": file.content_type
    }

    return data

