from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Gene, Organism


# Главная страница — список всех генов
@app.route('/')
def index():
    genes = Gene.query.all()
    return render_template('index.html', genes=genes)


# Просмотр информации об организме
@app.route('/organism/<string:organism_id>')
def organism_detail(organism_id):
    organism = Organism.query.get_or_404(organism_id)
    return render_template('organism_detail.html', organism=organism)


# Добавление нового гена
@app.route('/add_gene', methods=['GET', 'POST'])
def add_gene():
    if request.method == 'POST':
        gene_id = request.form['id']
        sequence = request.form['sequence']
        organism_id = request.form['organism_id']

        organism = Organism.query.get(organism_id)
        if organism:
            new_gene = Gene(id=gene_id, sequence=sequence, organism_id=organism.id)
            db.session.add(new_gene)
            organism.update_gene_count()  # Обновление количества генов для организма
            db.session.commit()
            return redirect(url_for('index'))

    organisms = Organism.query.all()
    return render_template('add_gene.html', organisms=organisms)


# Добавление нового организма
@app.route('/add_organism', methods=['GET', 'POST'])
def add_organism():
    if request.method == 'POST':
        organism_id = request.form['id']
        name = request.form['name']
        description = request.form['description']

        new_organism = Organism(id=organism_id, name=name, description=description)
        db.session.add(new_organism)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_organism.html')


# Удаление гена
@app.route('/delete_gene/<string:gene_id>', methods=['GET', 'POST'])
def delete_gene(gene_id):
    gene = Gene.query.get_or_404(gene_id)
    organism_id = gene.organism.id
    db.session.delete(gene)
    organism = Organism.query.get(organism_id)
    organism.update_gene_count()  # Обновление количества генов для организма
    db.session.commit()
    return redirect(url_for('organism_detail', organism_id=organism_id))


# Изменение последовательности гена
@app.route('/edit_gene/<string:gene_id>', methods=['GET', 'POST'])
def edit_gene(gene_id):
    gene = Gene.query.get_or_404(gene_id)
    if request.method == 'POST':
        gene.sequence = request.form['sequence']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_gene.html', gene=gene)
