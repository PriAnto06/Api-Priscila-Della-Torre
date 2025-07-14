from math import ceil
import sqlite3
from flask import Flask, g, jsonify, request, url_for

def dict_factory(cursor, row):
  """Arma un diccionario con los valores de la fila."""
  fields = [column[0] for column in cursor.description]
  return {key: value for key, value in zip(fields, row)}

def abrirConexion():
   if 'db' not in g:
      g.db = sqlite3.connect("api.sqlite")
      g.db.row_factory = dict_factory
   return g.db

def cerrarConexion(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app = Flask(__name__)
app.teardown_appcontext(cerrarConexion)
resultados_por_pag = 10
@app.route("/api/genero")
def generos():
   args = request.args
   pagina = int(args.get('page', '1'))
   descartar = (pagina-1) * resultados_por_pag
   db = abrirConexion()
   cursor =db.cursor()
   cursor.execute("SELECT COUNT(*)AS cant FROM genres;")
   cant = cursor.fetchone()['cant']
   paginas = ceil(cant / resultados_por_pag)
   if pagina < 1 or pagina > paginas:
      return f"pagina inexistente:{pagina}",404
   cursor.execute(""" SELECT GenreId,Name 
                  FROM genres LIMIT ? OFFSET ?;""",
                     (resultados_por_pag,descartar))
  
   lista = cursor.fetchall()
   cerrarConexion()
   siguiente = None
   anterior = None 
   if pagina > 1:
         anterior = url_for('generos', page=pagina-1)
   if pagina < paginas:
         siguiente = url_for('generos', page=pagina+1)
   info = { 'count' : cant, 'pages': paginas,
               'next' : siguiente, 'prev' : anterior }
   res = { 'info' : info, 'results' : lista}
   return jsonify(res)

@app.route("/api/artista")
def artistas():
    args = request.args
    pagina = int(args.get('page', '1'))
    descartar = (pagina-1) * resultados_por_pag
    db = abrirConexion()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) AS cant FROM artists;")
    cant = cursor.fetchone()['cant']
    paginas = ceil(cant / resultados_por_pag)
    cursor.execute(""" SELECT ArtistId, Name 
                        FROM artists LIMIT ? OFFSET ?; """, 
                        (resultados_por_pag,descartar))
    lista = cursor.fetchall()
    cerrarConexion()
    siguiente = None
    anterior = None
    if pagina > 1:
       anterior = url_for('artistas', page=pagina-1)
    if pagina < paginas:
       siguiente = url_for('artistas', page=pagina+1)
    info = { 'count' : cant, 'pages': paginas,
             'next' : siguiente, 'prev' : anterior }
    res = { 'info' : info, 'results' : lista}
    return jsonify(res)


@app.route("/api/artista/<int:id>")
def artista(id):
    db = abrirConexion()
    cursor = db.cursor() 
    cursor.execute("SELECT ArtistId, Name FROM artists WHERE  ArtistId = ?", (id,))
    row= cursor.fetchone()
    if row:
        return jsonify({
            "id": row["ArtistId"],
            "name": row["Name"],
            "url": url_for("artista", id=row["ArtistId"], _external=True)
        })
    else:
        return jsonify({"error": "Artista no encontrado"}), 404


#esto tiene q devolver un json que represente un diccionario
#con id,name y url(con la direccion de la ruta,usar url_for)

@app.route("/api/album/<int:id>")
def album(id):
    db = abrirConexion()
    cursor = db.cursor() 
    cursor.execute("""SELECT ar.ArtistId,AlbumId, Title 
                   FROM albums al JOIN artists ar 
                   ON ar.ArtistId =al.ArtistId
                   WHERE  AlbumId= ?""", (id,))
    row= cursor.fetchone()
    if row:
        artista = {"Name":row["Name"],
                    "url": url_for("artista", id=row["ArtistId"], _external=True)}
        return jsonify({
            "id": row["AlbumId"],
            "name": row["Title"],
            "url": url_for("album", id=row["AlbumId"], _external=True),
            "artista":artista
        })
    else:
        return jsonify({"error": "album no encontrado"}), 404

#artista
#"ArtistId"	3
#"name"	"Aerosmith"
#url	"http://127.0.0.1:5000/api/artista/3"
#{
#id	2
#"Title"	"Balls to the Wall"
#"url"	"http://127.0.0.1:5000/api/album/2"
#"artist":

#{
#"AlbumId":3
#"url":"http://127.0.0.1:5000/api/album/3"

 #}	
#} 


#esto tiene q devolver un json que represente un diccionario
#con id,name y url(con la direccion de la ruta,usar url_for)
