from app import app, db, cli
from app.models import Request, Label, Prediction


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Request": Request, "Label": Label, "Prediction": Prediction}
