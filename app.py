import flask
from flask import Flask, request
import sqlite3

app = Flask(__name__)


def init_db():
    con = sqlite3.connect("movies.db")
    with open('create_table.sql', 'r') as f:
        script = f.read()
    con.executescript(script)


def database(func):
    def with_connection(*args, **kwargs):
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        try:
            res = func(cur, *args, **kwargs)
        except sqlite3.ProgrammingError:
            con.rollback()
            raise ValueError("Invalid database request.")
        else:
            con.commit()
        finally:
            con.close()
        return res

    return with_connection


@database
def update_movie(cur, movie_id, m):
    m['id'] = movie_id
    res = cur.execute("UPDATE movie "
                      "SET title = :title,"
                      "description = :description,"
                      "release_year = :release_year "
                      "WHERE id = :id", m)
    if res.rowcount == 0:
        flask.abort(404)


@database
def post_movie(cur, m):
    cur.execute("INSERT INTO movie(title, description, release_year)"
                "VALUES(:title, :description, :release_year)", m)
    res = cur.execute("SELECT last_insert_rowid()")
    id = res.fetchone()
    return id[0]


@database
def get_movies(cur):
    res = cur.execute("SELECT * FROM movie")
    return res.fetchall()


@database
def get_movie(cur, movie_id):
    res = cur.execute("SELECT * FROM movie WHERE id = ?", (movie_id,))
    movies = res.fetchall()
    if len(movies) == 0:
        flask.abort(404)
    return movies


@app.put('/movies/<int:id>')
def put(id):
    p = request.get_json()
    update_movie(id, p)
    return get_movie(id)


@app.post('/movies')
def post():
    p = request.get_json()
    try:
        id = post_movie(p)
    except ValueError:
        flask.abort(400)
        return
    return get_movie(id)


@app.route('/movies')
def get_all():
    return get_movies()


@app.route('/movies/<int:id>')
def get_one(id):
    return get_movie(id)


if __name__ == '__main__':
    init_db()
    app.run(port=5000, host='0.0.0.0')
