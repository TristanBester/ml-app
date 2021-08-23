from datetime import datetime
from app import app, db


class ExperimalGroup(db.Model):
    __tablename__ = "experimental_group"

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255))
    description = db.Column(db.String)
    requests = db.relationship("Request", backref="experimental_group", lazy="select")


class Request(db.Model):
    __tablename__ = "request"

    request_id = db.Column(db.Integer, primary_key=True)
    request_uuid = db.Column(db.String(255))
    request_time = db.Column(db.Date, default=datetime.now())
    feature_one = db.Column(db.Float)
    feature_two = db.Column(db.Float)
    feature_three = db.Column(db.Integer)
    feature_four = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey("experimental_group.group_id"))
    label = db.relationship("Label", backref="request", uselist=False)
    prediction = db.relationship("Prediction", backref="request", uselist=False)

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "request_time": self.request_time,
            "feature_one": self.feature_one,
            "feature_two": self.feature_two,
            "feature_three": self.feature_three,
            "feature_four": self.feature_four,
        }


class Label(db.Model):
    __tablename__ = "label"

    label_id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Integer)
    request_id = db.Column(db.Integer, db.ForeignKey("request.request_id"))


class Prediction(db.Model):
    __tablename__ = "prediction"

    prediction_id = db.Column(db.Integer, primary_key=True)
    prediction = db.Column(db.Float)
    model_name = db.Column(db.String(255))
    request_id = db.Column(db.Integer, db.ForeignKey("request.request_id"))


class MonitoringComparisonStatistics(db.Model):
    __tablename__ = "monitoring_comparison_statistics"

    comparison_id = db.Column(db.Integer, primary_key=True)
    comparison_date = db.Column(db.Date, default=datetime.now())
    num_days_sample_one = db.Column(db.Integer)
    num_days_sample_two = db.Column(db.Integer)
    feature_one_JS = db.Column(db.Float)
    feature_one_KS = db.Column(db.Float)
    feature_two_JS = db.Column(db.Float)
    feature_two_KS = db.Column(db.Float)
    feature_three_JS = db.Column(db.Float)
    feature_three_chi = db.Column(db.Float)
    feature_four_JS = db.Column(db.Float)
    feature_four_chi = db.Column(db.Float)
