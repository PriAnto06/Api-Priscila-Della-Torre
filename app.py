import sqlite3
from flask import Flask

app = Flask(__name__)
resultados_por_pag = 10
@app.route("/api/artista")
def artistas():
   args = request.args
   pagina = int(args.get('page','1'))
   descartar = (pagina-1)*resultados_por_pag
   abrirConexion()
   cursor = db.cursor()
   cursor.execute("SELECT COUNT(*) AS cant FROM artists; ")
   cant = cursor.fetchone()['cant']
   paginas = ceil(cant/ resultados_por_pag)
   cursor.execute("SELECT ArtistId,Name " \
   "               FROM artists LIMIT ? OFFSET ?;""",
                    (resultados_por_pag),descartar)

   db = sqlite3.connect("")
   db.row_factory = dict_factory

   
def dict_factory(cursor, row):
  """Arma un diccionario con los valores de la fila."""
  fields = [column[0] for column in cursor.description]
  return {key: value for key, value in zip(fields, row)}




def cerrarConexion():
   global db
   db.close()
   db = None


@app.route("/test-db") 
def testDB():
   abrirConexion()
   cursor = db.cursor()
   cursor.execute("SELECT COUNT(*) AS cant FROM usuarios; ")
   res = cursor.fetchone()
   registros = res["cant"]
   cerrarConexion()
   return f"Hay {registros} registros en la tabla usuarios"
