from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import bleach

# Initialize the Flask application and configure the 'template_folder'
app = Flask(__name__, template_folder='static/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///congo_books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class BookReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    review = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<BookReview %r>' % self.title

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        review_content = request.form['review']

        sanitized_review = bleach.clean(review_content)

        new_review = BookReview(title=title, review=sanitized_review)

        try:
            db.session.add(new_review)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        return redirect(url_for('home'))

    reviews = BookReview.query.order_by(BookReview.id.desc()).all()
    return render_template('index.html', reviews=reviews)

@app.route('/review/<int:review_id>')
def show_review(review_id):
    review = BookReview.query.get_or_404(review_id)
    return render_template('review.html', review=review)

def init_db():
    with app.app_context():
        db.create_all()

init_db()

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
def init_db():
    with app.app_context():
        db.create_all()

