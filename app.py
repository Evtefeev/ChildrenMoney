from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from my_conf import children_names

app = Flask(__name__)
# Use SQLite database file named 'site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=True)


with app.app_context():
    db.create_all()


currencies = {
    'uah': 'грн'
}
currency = 'uah'

# Словарь для хранения баланса каждого ребенка
children_balances = {
    'child1': [],
    'child2': [],
}


@app.route('/')
def index():
    balances = {}
    children = ['child1', 'child2']

    for child in children:
        transactions = Transaction.query.filter_by(child_name=child).all()
        balances[child] = sum(
            transaction.amount for transaction in transactions)

    return render_template(
        'index.html',
        balances=balances,
        children=children,
        names=children_names,
        currency=currencies[currency],
        Transaction=Transaction
    )


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    child_name = request.form['child']
    description = request.form['description']
    amount = int(request.form['amount'])

    # Save transaction to the database
    transaction = Transaction(child_name=child_name,
                              amount=amount, description=description)
    db.session.add(transaction)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
