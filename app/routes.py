from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Gene, Organism


# Главная страница — список всех генов
@app.route('/')
def index():
    organisms = Organism.query.all()
    return render_template('index.html', organisms=organisms)


# Просмотр информации об организме
@app.route('/organism/<string:organism_id>')
def organism_detail(organism_id):
    organism = Organism.query.get_or_404(organism_id)
    return render_template('organism_detail.html', organism=organism)


# Добавление нового гена
@app.route('/add_gene', methods=['GET', 'POST'])
def add_gene():
    organisms = Organism.query.all()

    if request.method == 'POST':
        gene_id = request.form['id']
        sequence = request.form['sequence']
        organism_id = request.form['organism_id']

        # Проверка на дубликат
        existing_gene = Gene.query.get(gene_id)
        if existing_gene:
            flash(f'Ген с ID {gene_id} уже существует.', 'warning')
            return render_template('add_gene.html', organisms=organisms)

        organism = Organism.query.get(organism_id)
        if organism:
            new_gene = Gene(id=gene_id, sequence=sequence, organism_id=organism.id)
            db.session.add(new_gene)
            organism.update_gene_count()
            db.session.commit()
            flash(f'Ген с ID {gene_id} успешно добавлен.', 'success')

    return render_template('add_gene.html', organisms=organisms)


# Добавление нового организма
@app.route('/add_organism', methods=['GET', 'POST'])
def add_organism():
    if request.method == 'POST':
        organism_id = request.form['id']
        name = request.form['name']
        description = request.form['description']

        # Проверка на дубликат
        existing_organism = Organism.query.get(organism_id)
        if existing_organism:
            flash(f'Организм с ID {organism_id} уже существует.', 'warning')
            return render_template('add_organism.html')

        new_organism = Organism(id=organism_id, name=name, description=description)
        db.session.add(new_organism)
        db.session.commit()
        flash(f'Организм с ID {organism_id} и названием {name} успешно добавлен.', 'success')

    return render_template('add_organism.html')


# Изменение последовательности гена
@app.route('/edit_gene/<string:gene_id>', methods=['GET', 'POST'])
def edit_gene(gene_id):
    gene = Gene.query.get_or_404(gene_id)
    if request.method == 'POST':
        gene.sequence = request.form['sequence']
        db.session.commit()

        # Уведомление о том, что последовательность обновлена
        flash('Последовательность обновлена', 'success')

        # Остаёмся на той же странице
        return redirect(url_for('edit_gene', gene_id=gene.id))

    return render_template('edit_gene.html', gene=gene)


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


@app.route('/delete_all_genes/<string:organism_id>', methods=['POST'])
def delete_all_genes(organism_id):
    organism = Organism.query.get_or_404(organism_id)

    # Удаляем все гены этого организма
    Gene.query.filter_by(organism_id=organism.id).delete()
    db.session.commit()

    # Обновляем количество генов для организма
    organism.update_gene_count()

    return redirect(url_for('index'))


@app.route('/edit_organism_description/<string:organism_id>', methods=['GET', 'POST'])
def edit_organism_description(organism_id):
    organism = Organism.query.get_or_404(organism_id)

    if request.method == 'POST':
        new_description = request.form['description']
        if new_description.strip():  # Проверяем, что описание не пустое
            organism.description = new_description
        else:
            organism.description = "Описание не предоставлено"  # Если пусто, ставим дефолтное значение
        db.session.commit()
        flash('Описание организма обновлено.', 'success')
        return redirect(url_for('organism_detail', organism_id=organism.id))

    return render_template('edit_organism_description.html', organism=organism)


@app.route('/delete_organism/<string:organism_id>', methods=['POST'])
def delete_organism(organism_id):
    organism = Organism.query.get_or_404(organism_id)

    # Удаляем все гены этого организма
    genes = Gene.query.filter_by(organism_id=organism.id).all()
    for gene in genes:
        db.session.delete(gene)

    # Удаляем саму запись об организме
    db.session.delete(organism)
    db.session.commit()

    return redirect(url_for('index'))
