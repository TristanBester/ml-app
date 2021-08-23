import uuid
import numpy as np
from datetime import datetime
from faker import Faker
from app import app, db
from app.models import Request, Prediction, Label, ExperimalGroup


@app.cli.group()
def database():
    pass


@database.command()
def init():
    db.drop_all()
    db.create_all()
    print("Database initilialised.")


@database.command()
def populate():
    # Add experimental groups.
    experimental_group = ExperimalGroup(
        group_name="experiment",
        description=" The experimental group used in the experiment.",
    )
    control_group = ExperimalGroup(
        group_name="control", description=" The control group used in the experiment."
    )

    db.session.add(experimental_group)
    db.session.add(control_group)
    db.session.commit()

    # Add requests.
    requests = []
    fake = Faker()

    for i in range(300):
        request = Request(
            request_uuid=i,
            request_time=fake.date_between(start_date="-1y", end_date="today"),
            feature_one=np.random.normal(),
            feature_two=np.random.normal(),
            feature_three=np.random.randint(low=0, high=5),
            feature_four=np.random.randint(low=0, high=5),
            experimental_group=experimental_group
            if np.random.uniform() > 0.2
            else control_group,
        )
        requests.append(request)
    db.session.add_all(requests)
    db.session.commit()

    # Add predictions.
    predictions = []

    for request in requests:
        prediction = Prediction(
            prediction=np.random.normal(),
            model_name="test model",
            request_id=request.request_id,
        )
        predictions.append(prediction)
    db.session.add_all(predictions)
    db.session.commit()

    # # Add labels.
    # labels = []

    # for request in requests[:250]:
    #     label = Label(
    #         label=np.random.randint(low=0, high=5), request_id=request.request_id
    #     )
    #     labels.append(label)

    # db.session.add_all(labels)
    # db.session.commit()
    print("Database populated sucessfully.")
