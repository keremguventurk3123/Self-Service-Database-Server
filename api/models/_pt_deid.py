from datetime import datetime

from api.core import Mixin
from api.models.base import db


class pt_deid(Mixin, db.Model):
    """pt_deid table
    """

    __tablename__ = "pt_deid"
    pt_id = db.Column(db.INT, unique=True, primary_key=True)
    dob = db.Column(db.DateTime, nullable=False)
    over_90 = db.Column(db.SMALLINT)
    race_1 = db.Column(db.VARCHAR)

    diagnosis_deid = db.relationship(
        "diagnosis_deid", backref="pt_deid", lazy="dynamic"
    )
    exam_deid = db.relationship("exam_deid", backref="pt_deid", lazy="dynamic")
    image_deid = db.relationship("image_deid", backref="pt_deid", lazy="dynamic")

    lab_value_deid = db.relationship(
        "lab_value_deid", backref="pt_deid", lazy="dynamic"
    )
    medication_administration_deid = db.relationship(
        "medication_administration_deid", backref="pt_deid", lazy="dynamic"
    )
    medication_deid = db.relationship(
        "medication_deid", backref="pt_deid", lazy="dynamic"
    )
    smart_data_deid = db.relationship(
        "smart_data_deid", backref="pt_deid", lazy="dynamic"
    )
    visit_movement_deid = db.relationship(
        "visit_movement_deid", backref="pt_deid", lazy="dynamic"
    )

    def __repr__(self):
        return "<pt_deid {!r}>".format(self.pt_id)

    @staticmethod
    def get_all_pt_ids():
        """Get all pt_id available
        """
        qry = pt_deid.query.with_entities(pt_deid.pt_id).distinct()
        return [v.pt_id for v in qry.all()]

    @staticmethod
    def get_pt_id_by_age_or_race_1(
        race_1: list = None, younger_than: datetime = None, older_than: datetime = None,
    ) -> list:
        """Filter pt_id by age and/or race_1

        :param race_1 <list<str>>
        :param younger_than <DateTime> earliest DoB
        :param older_than <DateTime> latest DoB
        :returns <list<int>> pt_id
        """

        qry = pt_deid.query.with_entities(pt_deid.pt_id).distinct()

        if younger_than != None:
            qry = qry.filter(pt_deid.dob > younger_than)
        if older_than != None:
            qry = qry.filter(pt_deid.dob < older_than)
        if race_1:
            qry = qry.filter(pt_deid.race_1.in_(race_1))

        return [v.pt_id for v in qry.all()]
