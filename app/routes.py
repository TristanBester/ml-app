import datetime
import numpy as np
from flask import request
from app import app, db
from app.models import (
    ExperimalGroup,
    Request,
    Prediction,
    Label,
    MonitoringComparisonStatistics,
)


@app.route("/")
def index():
    return "Running"


@app.route("/sample/<days>")
def data_sample(days):
    try:
        days = int(days)
    except:
        return "Invalid time window.", 400

    delta = datetime.timedelta(days=days)
    end_date = datetime.datetime.now()
    start_date = end_date - delta

    exp_group = ExperimalGroup.query.filter_by(group_name="experiment").first()
    requests = (
        Request.query.filter(
            (Request.group_id == exp_group.group_id)
            & (Request.request_time > start_date)
        )
        .order_by(Request.request_time)
        .all()
    )

    return {"requests": [r.to_dict() for r in requests]}


@app.route("/predict", methods=["POST"])
def predict():
    json = request.json

    # Store requests.
    requests = []
    exp_group = ExperimalGroup.query.filter_by(group_name="experiment").first()

    for r in json["requests"]:
        req = Request(
            uuid=r["uuid"],
            feature_one=r["feature_one"],
            feature_two=r["feature_two"],
            feature_three=r["feature_three"],
            feature_four=r["feature_four"],
            group_id=exp_group.group_id,
        )
        requests.append(req)
    db.session.add_all(requests)
    db.session.commit()

    # Store predictions.
    predictions = []

    for req in requests:
        prediction = Prediction(
            prediction=np.random.normal(),
            model_name="production model",
            request_id=req.request_id,
        )
        predictions.append(prediction)
    db.session.add_all(predictions)
    db.session.commit()

    responses = {}
    for req, prediction in zip(requests, predictions):
        responses[req.uuid] = prediction.prediction

    return responses


@app.route("/control", methods=["POST"])
def control():
    json = request.json

    # Store requests.
    requests = []
    response = {}
    control_group = ExperimalGroup.query.filter_by(group_name="control").first()

    for r in json["requests"]:
        req = Request(
            uuid=r["uuid"],
            feature_one=r["feature_one"],
            feature_two=r["feature_two"],
            feature_three=r["feature_three"],
            feature_four=r["feature_four"],
            group_id=control_group.group_id,
        )
        requests.append(req)
        response[req.uuid] = 999
    db.session.add_all(requests)
    db.session.commit()

    return response


@app.route("/uuids")
def uuids():
    uuids = Request.query.with_entities(Request.request_uuid).all()
    uuids = [u[0] for u in uuids]

    return {"uuids": uuids}


@app.route("/label", methods=["POST"])
def route():
    json = request.json

    uuids = []
    labels = []

    for record in json["labels"]:
        uuid = list(record.keys())[0]
        label_value = list(record.values())[0]

        req = Request.query.filter_by(request_uuid=uuid).first()

        try:
            req.label.label = label_value
            continue
        except:
            label = Label(label=label_value, request_id=req.request_id)
            db.session.add(label)

    db.session.commit()
    return ""


@app.route("/monitoring", methods=["POST"])
def monitoring():
    json = request.json

    all_statistics = []

    for r in json["statistics"]:
        statistics = MonitoringComparisonStatistics(
            num_days_sample_one=r["num_days_sample_one"],
            num_days_sample_two=r["num_days_sample_two"],
            feature_one_JS=r["feature_one_JS"],
            feature_one_KS=r["feature_two_KS"],
            feature_two_JS=r["feature_two_JS"],
            feature_two_KS=r["feature_two_KS"],
            feature_three_JS=r["feature_three_JS"],
            feature_three_chi=r["feature_three_chi"],
            feature_four_JS=r["feature_four_JS"],
            feature_four_chi=r["feature_four_chi"],
        )
        all_statistics.append(statistics)
    db.session.add_all(all_statistics)
    db.session.commit()

    return ""
