from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:change-me@127.0.0.1:5432/voting'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Poll model
class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('polls', lazy=True))
    options = db.relationship('Option', backref='poll', lazy=True, cascade='all, delete-orphan')

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)

# Vote model
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)
    poll = db.relationship('Poll', backref=db.backref('votes', lazy=True))
    user = db.relationship('User', backref=db.backref('votes', lazy=True))
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    polls = Poll.query.all()
    return render_template('index.html', polls=polls)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/create_poll', methods=['GET', 'POST'])
@login_required
def create_poll():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        options = request.form.getlist('options')
        
        poll = Poll(title=title, description=description, creator=current_user)
        for option_text in options:
            if option_text.strip():
                option = Option(text=option_text, poll=poll)
                db.session.add(option)
        
        db.session.add(poll)
        db.session.commit()
        
        flash('Poll created successfully.', 'success')
        return redirect(url_for('index'))
    
    return render_template('create_poll.html')

# @app.route('/vote/<int:poll_id>', methods=['GET', 'POST'])
# def vote(poll_id):
#     poll = Poll.query.get_or_404(poll_id)
    
#     if request.method == 'POST':
#         choice_id = request.form.get('choice')
#         if not choice_id:
#             flash('Please select an option to vote.', 'error')
#             return redirect(url_for('vote', poll_id=poll.id))
        
#         choice = Option.query.get(choice_id)
#         if choice not in poll.options:
#             flash('Invalid option selected.', 'error')
#             return redirect(url_for('vote', poll_id=poll.id))
        
#         if current_user.is_authenticated:
#             existing_vote = Vote.query.filter_by(poll_id=poll.id, user_id=current_user.id).first()
#             if existing_vote:
#                 existing_vote.choice_id = choice.id
#             else:
#                 vote = Vote(poll=poll, user=current_user, choice=choice)
#                 db.session.add(vote)
#         else:
#             vote = Vote(poll=poll, choice=choice)
#             db.session.add(vote)
        
#         db.session.commit()
#         flash('Vote recorded successfully.', 'success')
#         return redirect(url_for('results', poll_id=poll.id))
    
#     return render_template('vote.html', poll=poll)

@app.route('/vote/<int:poll_id>', methods=['GET', 'POST'])
@login_required
def vote(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    
    if request.method == 'POST':
        choice_id = request.form.get('choice')
        if not choice_id:
            flash('Please select an option to vote.', 'error')
            return redirect(url_for('vote', poll_id=poll.id))
        
        choice = Option.query.get(choice_id)
        if choice not in poll.options:
            flash('Invalid option selected.', 'error')
            return redirect(url_for('vote', poll_id=poll.id))
        
            existing_vote.choice_id = choice.id
        else:
            vote = Vote(poll_id=poll.id, user_id=current_user.id, choice_id=choice.id)
            db.session.add(vote)
        
        db.session.commit()
        flash('Vote recorded successfully.', 'success')
        return redirect(url_for('results', poll_id=poll.id))
    
    return render_template('vote.html', poll=poll)


@app.route('/results/<int:poll_id>')
def results(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    results = db.session.query(Option.text, db.func.count(Vote.id)).join(Vote).filter(Vote.poll_id == poll.id).group_by(Option.id).all()
    total_votes = sum(count for _, count in results)
    return render_template('results.html', poll=poll, results=results, total_votes=total_votes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)