from sqlite3 import Cursor

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from forms import AddPostForm, UpdateForm

app = Flask(__name__)
app.secret_key = 'jdsfnansofnoq'


def create_connection():
    conn = sqlite3.connect('sqlite.db', check_same_thread=False)
    conn.row_factory = sqlite3.row
    return conn


def create_cursor(conn):
    return conn.cursor


conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()
cursor.execute("""create table if not exists posts 
            (id integer primary key,
            title text,
            content text,
            date_created DATETIME DEFAULT CURRENT_TIMESTAMP)""")
conn.commit()


@app.route('/add_post', methods=["POST", "GET"])
def add_post():
    form = AddPostForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            print(title, content)
            conn = sqlite3.connect('sqlite.db')
            cursor = conn.cursor()
            cursor.execute("""
            insert into posts (title, content) values (?, ?)""", (title, content))
            conn.commit()
            conn.close()
        return redirect(url_for('view_posts'))

    return render_template('addpost.html', form=form)


@app.route('/')
def view_posts():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    cursor.execute("""
    select * from posts
    """)
    posts = cursor.fetchall()
    return render_template('posts.html', posts=posts)


@app.route('/update_post/<int:post_id>', methods=["GET", "POST"])
def update_post(post_id):
    form = UpdateForm()
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    post = cursor.execute("""
    select * from posts where id = ?
    """, (post_id,)).fetchone()
    conn.commit()
    conn.close()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                update posts set title=?, content=? where id=?
                """, (title, content, post_id))
            conn.commit()
            conn.close()
            flash('Post updated successfully', 'success')
            return redirect(url_for('view_posts'))
    return render_template('update.html', post=post, form=form)


@app.route('delete_post/<int:post_id>', methods=["POST"])
def delete_post(post_id):
    conn = sqlite3.connect('sqlite.db')
    cursor = create_cursor()
    post = cursor.execute("""
    select * from users where id = ?
    """, (post_id,))
    if not post.fetchone():
        flash("post with this id does not exist")
        return redirect(url_for('view_posts'))
    cursor.execute("""
    delete from posts where id =?""", (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_posts'))
if __name__ == '__main__':
    app.run(debug=True)
