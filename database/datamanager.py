from database import db
from database.models import DataSet, TbTrace
from logger import Logger

log = Logger.log

def create_dataset(rows, id_dataset, filename, insertion_date):
	#def __init__(self, id_dataset, nom_dataset,  id_personne, nom_personne, prenom_personne, date_naissance,insertion_date=None):
	id_personne = rows[0]
	nom_personne = rows[1]
	prenom_personne = rows[2]
	date_naissance = rows[3]
	dataset = DataSet(id_dataset, filename, id_personne, nom_personne, prenom_personne, date_naissance, insertion_date)
	db.session.add(dataset)
	db.session.commit()

def create_trace( id_dataset, nom_dataset, status,nombre_total_ligne, lignes_corompus, insertion_date):

	trace = TbTrace(id_dataset, nom_dataset, status, nombre_total_ligne, lignes_corompus, insertion_date)
	db.session.add(trace)
	db.session.commit()

def delete_dataset(id_dataset):

	db.session.query(DataSet).filter(DataSet.id_dataset == id_dataset).delete()
	db.session.query(TbTrace).filter(TbTrace.id_dataset == id_dataset).delete()
	db.session.commit()