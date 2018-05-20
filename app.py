from flask import Flask, render_template, redirect, url_for , request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SECRET_KEY'] = 'itssecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
db = SQLAlchemy(app)


class BloodBlog(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(30))
	subtitle = db.Column(db.String(80))
	author = db.Column(db.String(30))
	date = db.Column(db.DateTime)
	content = db.Column(db.Text)


##index page
@app.route('/')
def index():
	posts = BloodBlog.query.order_by(BloodBlog.date.desc()).all()

	return render_template('index.html', posts = posts)

##post page
@app.route('/post/<int:post_id>' )
def post(post_id):
	post = BloodBlog.query.filter_by(id=post_id).one()
	return render_template('post.html', post=post)

##	about page
@app.route('/about')
def about():
	return render_template('about.html')

##add
@app.route('/add')
def add():
	return render_template('add.html')

@app.route('/addpost', methods = ['POST'])
def addpost():
	title =request.form['title'] 
	subtitle = request.form['subtitle']
	author = request.form['author']
	content = request.form['content']

	post = BloodBlog(title = title, subtitle = subtitle, author = author, content = content, date = datetime.now())

	db.session.add(post)
	db.session.commit()

	return redirect(url_for('index'))




if __name__ == '__main__':
	app.run(debug=True)
