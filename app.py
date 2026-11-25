import os
from flask import Flask, redirect, render_template, request, url_for

from db import db, IntegrityError
from flask_migrate import Migrate
from form import PostForm
from model import Post, Category
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


def create_category():
    cat_names = ['Other', 'Technology', 'Entertainment', 'Cooking', 'Comedy']
    try:
        for name in cat_names:
            category = Category.query.filter_by(name=name).first()

            if category is None:
                    
                    db.session.add(Category(name=name))
        db.session.commit()
            
    except IntegrityError as exc:
        db.session.rollback()

db.init_app(app)
with app.app_context():
    db.create_all()
    create_category()
migrate = Migrate (app, db)


@app.route('/', methods=['POST', 'GET'])
def homepage():
    posts = Post.query.all()
    form = PostForm()

    form.category.choices = [
                (category.id, category.name)
                for category in Category.query.all()
            ]
    if form.validate_on_submit():
        post_title = form.title.data
        post_content = form.content.data
        post_category = form.category.data

        
        # cat = Category.query.get(int(post_category))
        new_post = Post(title = post_title, content=post_content, cat_id=post_category)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('homepage'))

    return render_template('homepage2.html', form=form, posts = posts)


@app.route('/<int:id>')
def post(id: int):
    posts = Post.query.get_or_404(id, 'Post Not Found')

    return render_template('post.html', posts = posts)


@app.route('/search')
def search():
    query_word = request.args.get("search", "")

    posts = Post.query.filter(Post.title.ilike(f"%{query_word}%")).all()

    return render_template("homepage2.html", posts=posts)



@app.route ('/update-post/<int:id>', methods=['POST', 'GET'])
def update(id: int):
    posts = Post.query.get_or_404(id, 'Post Not Found')
    form = PostForm()
    form.category.choices = [
                    (category.id, category.name)
                    for category in Category.query.all()
                ]
    
    if request.method == 'GET':
        form.title.data = posts.title
        form.content.data = posts.content
        form.category.data = posts.cat_id

    if form.validate_on_submit():
        posts.title = form.title.data
        posts.content = form.content.data
        posts.cat_id = int(form.category.data)
        db.session.commit()
        return redirect(url_for('homepage'))
    
    

    return render_template('update.html', form=form, posts = posts)


@app.route('/delete-post/<int:id>', methods=['POST'])
def delete(id: int):
    posts = Post.query.get_or_404(id, 'Post not found')
    db.session.delete(posts)
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/categorypage')
def homepage():
    categories = Category.query.all()

    return render_template(
        'homepage2.html',
        categories=categories
    )

if __name__ == '__main__':
    app.run()