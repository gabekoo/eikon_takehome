import csv
from extensions import db
from flask import Flask
import os
from models import Features

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
with app.app_context():
    db.init_app(app)
    db.create_all()


def etl():
    # Load CSV files
    users = load_objs_from_file('data/users.csv', ['user_id', 'name', 'email', 'signup_date'])
    compounds = load_objs_from_file('data/compounds.csv', ['compound_id', 'compound_name', 'compound_structure'])
    user_experiments = load_objs_from_file('data/user_experiments.csv',
                                           ['experiment_id', 'user_id', 'experiment_compound_ids',
                                            'experiment_run_time'])
    users_map = {}
    # Create an id -> obj map to more easily reference users and compounds
    for user in users:
        users_map[user['user_id']] = user
    compounds_map = {}
    for compound in compounds:
        compounds_map[compound['compound_id']] = compound
    # Process files to derive features
    # Get intermediate data used to compute the final features
    intermediate = {}
    for exp in user_experiments:
        user_id = exp['user_id']
        if user_id not in intermediate.keys():
            intermediate[user_id] = {}
            intermediate[user_id]['num_experiments'] = 0
            intermediate[user_id]['compounds_used'] = {}
        intermediate[user_id]['num_experiments'] += 1
        compounds_used = exp['experiment_compound_ids'].split(';')
        for compound_id in compounds_used:
            if compound_id not in intermediate[user_id]['compounds_used'].keys():
                intermediate[user_id]['compounds_used'][compound_id] = 0
            intermediate[user_id]['compounds_used'][compound_id] += 1
    # Compute the final features for each user
    for user_id, data in intermediate.items():
        user_name = users_map[user_id]['name']
        num_total_experiments = data['num_experiments']
        num_total_compounds = 0
        most_used_compound_total = 0
        most_used_compounds = []
        for compound_id, compound_amount in data['compounds_used'].items():
            num_total_compounds += compound_amount
            if compound_amount == most_used_compound_total:
                most_used_compounds.append(compound_id)
            if compound_amount > most_used_compound_total:
                most_used_compounds.clear()
                most_used_compounds.append(compound_id)
                most_used_compound_total = compound_amount
        average_experiments_amount = num_total_compounds / num_total_experiments
        most_experimented_compound = ','.join([compounds_map[compound_id]['compound_name'] for compound_id in most_used_compounds])
    # Upload processed data into a database
        db.session.add(Features(user_name, num_total_experiments, average_experiments_amount, most_experimented_compound))
    db.session.commit()


def load_objs_from_file(file_name, field_names):
    obj_list = []
    with open(file_name) as file:
        reader = csv.reader(file)
        # Skip header
        next(reader)
        for line in reader:
            obj = {}
            for i in range(len(field_names)):
                obj[field_names[i]] = line[i].strip()
            obj_list.append(obj)
    return obj_list


# Your API that can be called to trigger your ETL process
@app.route("/etl")
def trigger_etl():
    # Trigger your ETL process here
    etl()
    return {"message": "ETL process started"}, 200
