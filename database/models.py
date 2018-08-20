from datetime import datetime
from database import db

class DataSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_dataset = db.Column(db.String(200), nullable=False)
    nom_dataset = db.Column(db.String(80))
    id_personne = db.Column(db.Integer)
    nom_personne = db.Column(db.String(80))
    prenom_personne = db.Column(db.String(80))
    date_naissance = db.Column(db.String(80))
    #insertion_date = db.Column(db.DateTime)
    insertion_date = db.Column(db.String(80))

    def __init__(self, id_dataset, nom_dataset,  id_personne, nom_personne, prenom_personne, date_naissance,insertion_date=None):
        self.id_dataset = id_dataset
        self.nom_dataset = nom_dataset
        self.id_personne = id_personne
        self.nom_personne = nom_personne
        self.prenom_personne = prenom_personne
        self.date_naissance = date_naissance
        self.insertion_date = insertion_date

    def __repr__(self):
        return '<DataSet %r>' % self.id_dataset

class TbTrace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_dataset = db.Column(db.String(50))
    nom_dataset = db.Column(db.String(50))
    nombre_total_ligne = db.Column(db.Integer)
    status = db.Column(db.String(50))
    lignes_corompus = db.Column(db.String(200))
    insertion_date = db.Column(db.String(80))

    def __init__(self, id_dataset, nom_dataset, status, nombre_total_ligne, lignes_corompus, insertion_date):
        self.id_dataset = id_dataset
        self.nom_dataset = nom_dataset
        self.status = status
        self.nombre_total_ligne = nombre_total_ligne
        self.lignes_corompus = lignes_corompus
        self.insertion_date = insertion_date
        
    def __repr__(self):
        return '<TbTrace %r>' % self.id_dataset