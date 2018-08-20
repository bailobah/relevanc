import datetime
from flask import request
from flask_restplus import Resource
from flask_restplus import abort
from sqlalchemy.orm import load_only

from logger import Logger
from api.serilizers import dataset_response_succes, get_trace
from api.restplus import api
from database.models import TbTrace

log = Logger.log

ns = api.namespace('trace/kpis', description='kpis des datasets')

@ns.route('/')
@api.doc(responses={
  200: 'Update success.'
})
class TraceCollection(Resource):
	"""docstring for TraceCollection"""

	@api.marshal_with(get_trace)
	def get(self):
		"""
		Returns collection trace.
		"""

  
		tbtrace_query = TbTrace.query\
				.options(load_only('id_dataset', 'nom_dataset','nombre_total_ligne','status','lignes_corompus','insertion_date'))\
				.all()

		return tbtrace_query

	

@ns.route('/<string:id_dataset>')
class DataItem(Resource):

	@api.marshal_with(get_trace, code=200)
	def get(self, id_dataset):
		"""
		Returns All trace id_dataset.
		"""
	
		data = TbTrace.query\
				.options(load_only('id_dataset', 'nom_dataset','nombre_total_ligne','status','lignes_corompus','insertion_date'))\
				.filter_by(id_dataset = id_dataset).all()
		if len(data) == 0:
			
			abort(400, 'This id_dataset not in database', id=id_dataset)
					
		return data, 200
