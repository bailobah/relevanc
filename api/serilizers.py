from flask_restplus import fields
from api.restplus import api

data = api.model('Dataset Model', {
    'id_personne': fields.String(readOnly=True, description='The unique identifier of row'),
    'nom_personne': fields.String(required=True, description='Name '),
    'prenom_personne': fields.String(required=True, description='First name'),
    'date_naissance': fields.String(required=True, description='Date birth'),
})

dataset_head= api.model('Model output if succes request', {
    'id_dataset' : fields.String(readOnly=True, description='The unique identifier of dataset'),
    'nom_dataset' : fields.String(readOnly=True, description='Dataset name'),
    'insertion_date': fields.String(required=True, description='Date insert dataset'),
})

dataset_kpis = api.model('Dataset stats', {
    'number_lines': fields.Integer(readOnly=True, description='Number lines containt in datset'),
    'number_bad_line': fields.Integer(readOnly=True, description='Number bad lines containt in datset'),
    'bad_lines': fields.List(fields.Integer),
})

dataset_response_succes = api.inherit('Dataset of results', dataset_head, {
    'kpis': fields.List(fields.Nested(dataset_kpis))
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_dataset = api.inherit('Page of dataset', pagination, {
    'items': fields.List(fields.Nested(data))
})

get_trace = api.model('Trace stats', {
    'id_dataset': fields.String(readOnly=True, description='The unique identifier of a dataset'),
    'nom_dataset' : fields.String(readOnly=True, description='Dataset name'),
    'nombre_total_ligne': fields.Integer(readOnly=True, description='Number lines containt in datset'),
    'status' : fields.String(readOnly=True, description='Status OK or KO (if not all rows insert, dataset containt bad lines)'),
    'lignes_corompus' : fields.String(readOnly=True, description='Bad line'),
    'insertion_date': fields.String(required=True, description='Date insert dataset'),
})


