from extensions import db


class Features(db.Model):
    user_name = db.Column(db.String, primary_key=True)
    num_total_experiments = db.Column(db.Integer, nullable=False)
    average_experiments_amount = db.Column(db.Float, nullable=False)
    most_experimented_compound = db.Column(db.String, nullable=False)

    def __init__(self, user_name, num_total_experiments, average_experiments_amount, most_experimented_compound):
        self.user_name = user_name
        self.num_total_experiments = num_total_experiments
        self.average_experiments_amount = average_experiments_amount
        self.most_experimented_compound = most_experimented_compound