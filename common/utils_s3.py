import os
import uuid
import boto3
from botocore.exceptions import ClientError
from django.conf import settings


def upload_file_to_s3(file_obj, folder="artworks", filename=None):
    """
    Завантажує файл у бакет AWS S3 або повертає локальний URL у разі відсутності S3.
    
    :param file_obj: об'єкт файлу з request.FILES (UploadedFile)
    :param folder: папка в S3 (напр. 'artworks', 'avatars')
    :param filename: кастомна назва файлу (якщо не вказана, генерується UUID)
    :return: URL завантаженого зображення або None при помилці
    """
    use_s3 = getattr(settings, 'USE_S3', False)

    if not filename:
        ext = file_obj.name.split('.')[-1] if '.' in file_obj.name else 'jpg'
        filename = f"{uuid.uuid4().hex}.{ext}"

    s3_key = f"{folder}/{filename}"

    if use_s3:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
            region_name=getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-1')
        )
        bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')

        try:
            s3_client.upload_fileobj(
                file_obj,
                bucket_name,
                s3_key,
                ExtraArgs={'ContentType': file_obj.content_type}
            )
            return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}"
        except ClientError as e:
            print(f"⚠️ [S3 Upload Error]: {e}")
            return None
    else:
        # Локальне збереження для розробки
        save_dir = os.path.join(settings.MEDIA_ROOT, folder)
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, filename)

        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        return f"{settings.MEDIA_URL}{folder}/{filename}"


def delete_file_from_s3(file_url):
    """
    Видаляє файл із S3 за його повним URL або з локального сховища.
    """
    use_s3 = getattr(settings, 'USE_S3', False)
    if not file_url:
        return False

    if use_s3:
        try:
            domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', '')
            if domain in file_url:
                s3_key = file_url.split(f"{domain}/")[-1]
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', None),
                    aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
                    region_name=getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-1')
                )
                bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')
                s3_client.delete_object(Bucket=bucket_name, Key=s3_key)
                return True
        except Exception as e:
            print(f"⚠️ [S3 Delete Error]: {e}")
            return False
    else:
        # Видалення з локальної папки media/
        if file_url.startswith(settings.MEDIA_URL):
            relative_path = file_url.replace(settings.MEDIA_URL, '')
            full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
    return False