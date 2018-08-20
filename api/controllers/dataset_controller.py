import os
import sys
import uuid
import shutil
import tempfile
import datetime
from logger import Logger
from flask import request
from flask_restplus import Resource
from werkzeug.utils import secure_filename
from flask_restplus import abort
from sqlalchemy.orm import load_only

from database.models import DataSet
from api.parsers import upload_arguments, pagination_arguments 
from api.serilizers import page_of_dataset, dataset_response_succes, data
from api.restplus import api
from database.datamanager import create_dataset, create_trace, delete_dataset

log = Logger.log

ALLOWED_EXTENSIONS = set(['.txt', '.csv'])
LENGHT_COLOMN = 4
FORMAT = "%Y-%m-%dT%H:%M:%S"

ns = api.namespace('dataset/upload', description='Operations related to upload dataset or restution')

def is_extension_allowed(filename, allowed_extensions_with_dot):
	[fname, ext] = os.path.splitext(filename)
	return ext in allowed_extensions_with_dot

@ns.route('/')
@api.doc(responses={
  200: 'Update success.',
  418: 'Illegal file extension.',
  419: 'Error saving page files.',
})
class DataSetCollection(Resource):
	"""docstring for ClassName"""

	@api.expect(pagination_arguments)
	@api.marshal_with(page_of_dataset)
	def get(self):
		"""
		Returns dataset by collection with page of page.
		"""
		args = pagination_arguments.parse_args(request)
		page = args.get('page', 1)
		per_page = args.get('per_page', 10)

		dataset_query = DataSet.query.options(load_only("id_personne", "nom_personne", "prenom_personne", "date_naissance"))

		dataset_page = dataset_query.paginate(page, per_page, error_out=False)

		return dataset_page

	@api.expect(upload_arguments)
	@api.marshal_with(dataset_response_succes, 200)
	def post(self):
		"""
		This method upload dataset file
		There accept extensions : (.csv, .txt).
		The columns must be separated by comma(,)

		Example schemat :

			id,nom,prenom,date_naissance
			1, Debegny, olivier, 2000/08/05
			2, BAH, Bailo, 2000/08/05
			3, Wan, Dong, 1000/02/30
			4, Debegny, olivier, 2000/08/05, Paris   !!!(attention, this line will not be inserted, colomns row > 4 colomns )
			5, Debe, Christ, 1986/08/03
			6, Toto, 2018/06/05                      (this is a bad row < 4 colomns)

		"""
		args = upload_arguments.parse_args(request)
		file = request.files['file']

		filename = secure_filename(file.filename)
		log.info('Input file name {}'.format(filename))		

		if not file or not is_extension_allowed(filename, ALLOWED_EXTENSIONS):

			message = "Only these extensionsa are allowed: %(exts)s, but filename is %(filename)s" % dict(exts=str(ALLOWED_EXTENSIONS), filename=filename) 
			log.error(message)
			abort(404, message)

		insertion_date = datetime.datetime.utcnow().strftime(FORMAT)
		log.info("Date insert :[ {} ]".format(insertion_date))
		
		dirpath = tempfile.mkdtemp()
		log.info("Create tmp directory : {}".format(dirpath))
		
		file.save(os.path.join(dirpath, filename)) 

		id_dataset = str(uuid.uuid4())
		log.info("Unique dateset id : {}".format(id_dataset))

		bad_lines = []
		number_bad_line = 0
		rows_insert = 0
		with open(os.path.join(dirpath, filename), 'r') as filehandle:  
			
			#check dateset containt header
			if request.args.get('header') == "true":
				next(filehandle)
			
			for cnt, line in enumerate(filehandle):

				rows = line.strip().split(',')
				if len(rows) != LENGHT_COLOMN :
					number_bad_line += 1
					bad_lines.append(cnt)
				#log.debug("Get first line : {}".format(line))
				else :
					rows_insert +=1
					log.info("Nombre de ligne inseré : {} ".format(rows_insert))
					create_dataset(rows, id_dataset, filename, insertion_date)
		filehandle.close() 
		shutil.rmtree(dirpath)

		if rows_insert == 0:
			abort(404, message="DataSet {} doesn't respect schemat {} ".format(id_dataset, str(data)))
			
		status = "OK"
		if len(bad_lines) > 0:
			status = "KO"

		create_trace( id_dataset, filename, status,cnt, ','.join(map(str,bad_lines)), insertion_date)
		
		data = {}
		data['kpis'] = {}
		data['id_dataset'] = id_dataset
		data['nom_dataset'] = filename
		data['insertion_date'] = insertion_date
		data['kpis']['number_lines'] = cnt
		data['kpis']['number_bad_line'] = number_bad_line
		data['kpis']['bad_lines'] = bad_lines
        
		return data, 200

@ns.route('/<string:id_dataset>')
class DataItem(Resource):

	@api.marshal_with(data, code=200)
	def get(self, id_dataset):
		"""
		Returns dataset with id_dataset .
		"""
		dataset = DataSet.query\
				.filter_by(id_dataset = id_dataset)\
				.options(\
					load_only("id_personne", "nom_personne", "prenom_personne", "date_naissance"))\
				.all()
		if not dataset:
			abort(404, message="DataSet {} doesn't exist".format(id_dataset))
			
		return dataset, 200

	@api.response(200, 'DataSet successfully deleted.')
	def delete(self, id_dataset):
		"""
        Deletes dataset.
        """	
		try:
			dataset = DataSet.query.filter(DataSet.id_dataset == id_dataset).first()

			if not dataset:
				return {'message': "DataSet {} doesn't exist".format(id_dataset)}, 404
			
			delete_dataset(id_dataset)			
		except Exception as e:
			log.error("An internal error occurred : {}".format(e.message))
			return {'success': False, 'message': 'Internal error'}, 500
			
		return {'success': True, 'message': 'record deleted'}, 200

"""
	def _allowed_file(self,filename):
		return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""