# -*- coding: utf-8 -*-
"""Declare the celery tasks."""
import io
import json
from os import path

import numpy as np
from flask import current_app
from PIL import Image

from .extensions.extensions import celery, s3


@celery.task(name="delete_image")
def delete_file_s3(filename):
    """Delete profile pic."""
    s3.delete_object(
        Bucket=current_app.config["S3_BUCKET"], Key=filename
    )


@celery.task(name="upload_image")
def upload_file_to_s3(json_data, filename, bucket_name):
    """Upload a file to S3."""
    img = Image.fromarray(np.array(json.loads(json_data), dtype="uint8"))
    in_mem_file = io.BytesIO()
    img.save(in_mem_file, format="png")
    in_mem_file.seek(0)

    s3.upload_fileobj(in_mem_file, bucket_name, filename)

    data = f"{current_app.config['S3_LOCATION']}{filename}"
    return {"image": data}
