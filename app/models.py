from app import db


# Модель для таблицы Организмов
class Organism(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    gene_count = db.Column(db.Integer, default=0)
    description = db.Column(db.String, default="Описание не предоставлено")  # Значение по умолчанию

    # Связь с таблицей генов (один-ко-многим)
    genes = db.relationship('Gene', backref='organism', lazy=True)

    def update_gene_count(self):
        self.gene_count = len(self.genes)
        db.session.commit()


# Модель для таблицы Генов
class Gene(db.Model):
    id = db.Column(db.String, primary_key=True)
    sequence = db.Column(db.Text, nullable=False)
    organism_id = db.Column(db.String, db.ForeignKey('organism.id'), nullable=False)
