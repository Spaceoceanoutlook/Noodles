from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Noodles, NoodlesSchema, Country
from werkzeug.utils import secure_filename

load_dotenv()

# Папка для загрузки фото из браузера
UPLOAD_FOLDER = "static/img"

# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Создаем объект приложения
app = Flask(__name__)

# Создаем в словаре(config) ключ и значение-ссылку для хранения фото
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Получаем подключение из переменных окружения
url = os.getenv('DATABASE_URL')

# Создаем движок
engine = create_engine(url, echo=True)

# Создаем экземпляр сессии
Session = sessionmaker(bind=engine)

# Создаем объект сессии
session = Session()


@app.get("/")
def get_all_noodles():
    noodles = session.query(Noodles).order_by(-Noodles.id)
    return render_template("index.html", result=noodles)


@app.get("/<int:param>")
def get_param(param):
    noodles = session.query(Noodles).filter_by(country_id=param)
    return render_template("index.html", result=noodles)


@app.get("/<param>")
def get_true_or_false_noodles(param):
    if param == "True":
        noodles = session.query(Noodles).filter_by(recommendation=param)
    else:
        noodles = session.query(Noodles).filter_by(recommendation=False)
    return render_template("index.html", result=noodles)


@app.route("/edit_noodles/<int:noodle_id>", methods=['get', 'post'])
def edit_noodles(noodle_id):
    get_noodle = session.query(Noodles).get(noodle_id)
    if request.method == 'GET':
        return render_template("edit_noodles.html", res=get_noodle)
    if request.method == 'POST':
        if request.form.get('name'):
            get_noodle.name_of_noodles = request.form.get('name')
        if request.form.get('description'):
            get_noodle.description = request.form.get('description')
        if request.form.get('country'):
            country_id = session.query(Country).filter_by(name_of_country=f'{request.form.get('country')}')
            get_noodle.country_id = country_id.first().id
        if request.form.get('flag'):
            get_noodle.recommendation = bool(request.form.get('flag'))
        else:
            get_noodle.recommendation = False
        if request.files['file']:
            filename = secure_filename(request.files['file'].filename)
            request.files['file'].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            get_noodle.image = filename
        session.commit()
        return redirect('/')


@app.get("/delete_noodles/<int:noodle_id>")
def delete_noodles(noodle_id):
    noodle = session.query(Noodles).filter(Noodles.id == noodle_id).one()
    filename = noodle.image
    if filename:
        os.remove(f'static/img/{filename}')
    session.delete(noodle)
    session.commit()
    return redirect('/')


@app.route("/add_noodles", methods=['get', 'post'])
def add_noodles():
    if request.method == 'GET':
        return render_template("add_noodles.html")
    name = request.form.get('name')
    description = request.form.get('description')
    country = request.form.get('country')
    recommendation = request.form.get('flag')

    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = ''
    if recommendation is None:
        recommendation = False
    country_id = session.query(Country).filter_by(name_of_country=f'{country}')
    if country_id.first() is None:
        new_country = Country(
            name_of_country=f"{country}")
        session.add(new_country)
        session.commit()
        country_id = session.query(Country).filter_by(name_of_country=f'{country}')
    new_noodle = Noodles(
        name_of_noodles=f"{name}",
        description=f"{description}",
        recommendation=bool(recommendation),
        image=filename,
        country_id=country_id.first().id)
    session.add(new_noodle)
    session.commit()
    return redirect('/')


@app.get("/api/v1/")
def get_json_all_noodles():
    noodles = session.query(Noodles)
    noodles_schema = NoodlesSchema(many=True)
    result = noodles_schema.dumps(noodles, ensure_ascii=False)
    return result


if __name__ == '__main__':
    app.run(debug=True)

