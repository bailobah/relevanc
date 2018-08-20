from flask_restplus import reqparse 
from werkzeug.datastructures import FileStorage

upload_arguments = reqparse.RequestParser()
upload_arguments.add_argument('header', type=bool, default=True, required=True, help="File content header ?")
upload_arguments.add_argument('file', type=FileStorage, location='files', help='Upload file', required=True)

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('bool', type=bool, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page {error_msg}')