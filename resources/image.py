from flask_restful import Resource
from flask import send_file,request
from flask_uploads import UploadNotAllowed
from flask_jwt_extended import jwt_required,get_jwt_identity

from schemas.image import ImageSchema

from libs import image_helper
from libs.strings import gettext

import traceback
import os

image_schema = ImageSchema()

class ImageUpload(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        try:
            image_path = image_helper.save_image(image=data['image'],folder=folder)
            image_basename = image_helper.get_basename(image_path)
            return {'message':f"image '{image_basename}' uploaded success"}
        except UploadNotAllowed:
            image_extension = image_helper.get_extension(image_path)
            return {'message':f"image with extension '{image_extension}' is not allowed"},400

class Image(Resource):
    @classmethod
    @jwt_required
    def get(cls,filename:str):
        user_id = get_jwt_identity()
        folder = f'user_{user_id}'
        image_path = image_helper.get_path(folder=folder,name=filename)
        try:
            return send_file(image_path)
        except FileNotFoundError:
            return {'message':'image not found'},404
    @classmethod
    @jwt_required
    def delete(cls,filename:str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        try:
            os.remove(image_helper.get_path(folder=folder,name=filename))
        except FileNotFoundError:
            return {'message':'image not found'},404
        except:
            traceback.print_exc()
            return {'message':'can\'t delete image'},400

class AvatarUpload(Resource):
    @classmethod
    @jwt_required
    def put(cls): 
        data = image_schema.load(request.files)
        filename = f'user_{get_jwt_identity()}'
        folder = 'avatars'
        avatar_path = image_helper.find_image_any_format(name=filename,folder=folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {'message':'avatar deleted failed'},500
        try:
            ext = image_helper.get_extension(data['image'].filename)
            avatar = filename + ext
            avatar_path = image_helper.save_image(data['image'],folder=folder,name=avatar)
            basename = image_helper.get_basename(avatar_path)
            return {'message':f'avatar with name \'{basename}\' uploaded successfully.'},200
        except UploadNotAllowed:
            extension = image_helper.get_extension(data['image'])
            return {'message':f'avatar extension {extension} is not allowed'},400

class Avatar(Resource):
    @classmethod
    def get(cls,user_id):
        folder = 'avatars'
        filename = f'user_{user_id}'
        avatar = image_helper.find_image_any_format(folder=folder,name=filename)
        if avatar:
            return send_file(avatar)
        return {'message':'avatar not found'}
