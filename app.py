from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
from sqlalchemy import create_engine, text
import os

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def format_phone_number(number):
    # Supondo que o número seja uma string de 10 ou 11 dígitos
    if len(number) == 10:
        return f"({number[:2]}) {number[2:6]}-{number[6:]}"
    elif len(number) == 11:
        return f"({number[:2]}) {number[2:7]}-{number[7:]}"
    return number


app.jinja_env.filters["format_phone"] = format_phone_number


def get_db_connection():
    return engine.connect()


@app.route("/")
def index():
    title = "Gerenciamento de Registros"
    with get_db_connection() as conn:
        registros = conn.execute(text("SELECT * FROM registros")).fetchall()
    return render_template("index.html", registros=registros, title=title)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/insert", methods=("GET", "POST"))
def insert():
    if request.method == "POST":
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        serie = request.form["serie"]
        contrato = request.form["contrato"]
        operadora = request.form["operadora"]
        numero = request.form["numero"]
        observacao = request.form["observacao"]

        try:
            with get_db_connection() as conn:
                conn.execute(
                    text(
                        "CALL inserir_registro(:latitude, :longitude, :serie, :contrato, :operadora, :numero, :observacao)"
                    ),
                    {
                        "latitude": latitude,
                        "longitude": longitude,
                        "serie": serie,
                        "contrato": contrato,
                        "operadora": operadora,
                        "numero": numero,
                        "observacao": observacao,
                    },
                )
                conn.commit()  # Comita a transação
        except Exception as e:
            conn.rollback()  # Reverte a transação em caso de erro
        return redirect(url_for("index"))
    return render_template("insert.html")


@app.route("/update/<int:id>", methods=("GET", "POST"))
def update(id):
    with get_db_connection() as conn:
        registro = conn.execute(
            text("SELECT * FROM registros WHERE id = :id"), {"id": id}
        ).fetchone()

    if request.method == "POST":
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        serie = request.form["serie"]
        contrato = request.form["contrato"]
        operadora = request.form["operadora"]
        numero = request.form["numero"]
        observacao = request.form["observacao"]

        try:
            with get_db_connection() as conn:
                conn.execute(
                    text(
                        "CALL atualizar_registro(:id, :latitude, :longitude, :serie, :contrato, :operadora, :numero, :observacao)"
                    ),
                    {
                        "id": id,
                        "latitude": latitude,
                        "longitude": longitude,
                        "serie": serie,
                        "contrato": contrato,
                        "operadora": operadora,
                        "numero": numero,
                        "observacao": observacao,
                    },
                )
                conn.commit()  # Comita a transação
        except Exception as e:
            conn.rollback()  # Reverte a transação em caso de erro
        return redirect(url_for("index"))

    return render_template("update.html", registro=registro)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
