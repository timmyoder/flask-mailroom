"""Mailroom donations webapp"""
import os
from flask import Flask, render_template, request, redirect, url_for
from peewee import IntegrityError, DoesNotExist
from model import Donor, Donation


app = Flask(__name__)


@app.route('/')
def home():
    """homepage"""
    return redirect(url_for('all_donations'))


@app.route('/donations/')
def all_donations():
    """list all donations in the db"""
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """If the handler receives a GET request,
    then it should render the template for the donation creation page.

    If the handler receives a POST request (a form submission),
    then it should attempt to retrieve the name of the donor and the
    amount of the donation from the form submission.
    It should retrieve the donor from the database with the indicated name,
    and create a new donation with the indicated donor and donation amount.
    Then it should redirect the visitor to the home page.
    """

    if request.method == 'POST':
        donor_name = request.form['name']

        try:
            # add the donor to the db if the record doesn't exist
            donor = Donor.create(name=donor_name)
        except IntegrityError:
            # if donor already exists, retrieve donor
            donor = Donor.get(Donor.name == donor_name)

        # add donation to db
        Donation.create(donor=donor,
                        value=request.form['value'])

        return redirect(url_for('all_donations'))

    else:
        return render_template('create.jinja2')


@app.route('/single_donor', methods=['GET', 'POST'])
def single_donor():
    """get all donations for a single donor"""
    if request.method == 'POST':
        try:
            donor_name = request.form['name']
            donor = Donor.get(Donor.name == donor_name)
            donations = Donation.select().where(Donation.donor_id == donor.id)
        except DoesNotExist:
            return "sorry, user doesn't exist"

        return render_template('single_donor.jinja2',
                               donor_name=donor_name,
                               donations=donations)
    else:
        return render_template('ask_for_donor.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
