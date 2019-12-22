from .base import db
from api.core import Mixin


class lab_value_deid(Mixin, db.Model):
    """lab_value_deid table
    """

    __tablename__ = "lab_value_deid"
    name = db.Column(db.VARCHAR)
    pt_id = db.Column(db.INT)
    lab_value_id = db.Column(db.INT, unique=True, primary_key=True)
    loinc_code = db.Column(db.VARCHAR)
    value = db.Column(db.VARCHAR)

    reference_high = db.Column(db.VARCHAR)
    reference_low = db.Column(db.VARCHAR)
    reference_normal = db.Column(db.VARCHAR)
    reference_unit = db.Column(db.VARCHAR)
    result_category = db.Column(db.VARCHAR)

    order_dt = db.Column(db.DateTime)
    result_dt = db.Column(db.DateTime)
    value_numeric = db.Column(db.DECIMAL(18, 0))
