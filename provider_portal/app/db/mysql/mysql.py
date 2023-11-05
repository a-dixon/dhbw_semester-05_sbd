from app import mysql_db as db


class Customers(db.Model):
    uid = db.Column(db.String, primary_key=True, nullable=False)
    api_key = db.Column(db.String, index=True, unique=True, nullable=False)


    def __repr__(self):
        return '<Customer {}>'.format(self.uid)


class Meters(db.Model):
    uid = db.Column(db.String, primary_key=True, nullable=False)
    # certificate

    def __repr__(self):
        return '<Meter {}>'.format(self.uid)


class CustomersMeters(db.Model):
    customer_uid = db.Column(db.String, db.ForeignKey('customers.uid'), primary_key=True, nullable=False)
    meter_uid = db.Column(db.String, db.ForeignKey('meters.uid'), primary_key=True, nullable=False)


    def __repr__(self):
        return 'Customer-Meter {}-{}>'.format(self.customer_uid, self.meter_uid)


class Users(db.Model):
    uid = db.Column(db.String, primary_key=True, nullable=False)
    api_key = db.Column(db.String, index=True, unique=True, nullable=False)
    username = db.Column(db.String, index=True, unique=True, nullable=False)


    def __init__(self, uid: str, api_key: str, username: str):
        self.uid = uid
        self.api_key = api_key
        self.username = username


    def __repr__(self):
        return '<User {}>'.format(self.username)
