from api.core import Mixin, KEYWORDS
from api.models.base import db


def _parse_vision(raw_data):
    """ Splits 20/30 type string data to extract the 2 digits right after /
    """
    if raw_data:
        return int(raw_data.split("/")[1].split("-")[0].split("+")[0])
    return None


def _vision_filter(lst, more_than, less_than):
    """Helper function that takes a list of tuples<pt_id, val>
    filter for val between more_than and less_than for vision
    
    """
    more_than = 0 if more_than is None else more_than
    less_than = 1000 if less_than is None else less_than
    return [
        (pt_id, val)
        for pt_id, val in lst
        if more_than <= _parse_vision(val) <= less_than
    ]


def _pressure_filter(lst, more_than, less_than):
    """Helper function that takes a list of tuples<pt_id, val>
    filter for val between more_than and less_than for pressure
    """
    more_than = 0 if more_than is None else int(more_than)
    less_than = 1000 if less_than is None else int(less_than)
    return [(pt_id, val) for pt_id, val in lst if more_than <= int(val) <= less_than]


def _filter_vis_pres_range(
    elem_keywords, value_range, value_validation_regex, vision=False
):

    qry = smart_data_deid.query.with_entities(
        smart_data_deid.pt_id, smart_data_deid.smrtdta_elem_value
    )
    qry = qry.filter(
        db.and_(
            smart_data_deid.element_name.ilike(elem_keywords),
            smart_data_deid.smrtdta_elem_value.ilike(value_validation_regex),
        )
    )
    pt_ids = qry.all()

    if vision:
        pt_ids = list(set(v[0] for v in _vision_filter(pt_ids, *value_range)))
    else:  # Pressure
        pt_ids = list(set(v[0] for v in _pressure_filter(pt_ids, *value_range)))

    return pt_ids


class smart_data_deid(Mixin, db.Model):
    """smart_data_deid table
    """

    __tablename__ = "smart_data_deid"
    smart_data_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT, db.ForeignKey("pt_deid.pt_id"))

    element_name = db.Column(db.VARCHAR, nullable=False)
    smrtdta_elem_value = db.Column(db.VARCHAR)
    value_dt = db.Column(db.DateTime)

    def __repr__(self):
        return "<smart_data_deid {!r}, pt_id {!r}>".format(
            self.smart_data_id, self.pt_id
        )

    @staticmethod
    def get_pt_id_by_vision(data: dict) -> set:
        """ Take the json data from filters
        and filter for the pt_ids with vision

        params:
            data: <dict> input filter json

        returns:
            pt_ids: <set>

        """
        pt_ids = []

        for field in ("left_vision", "right_vision"):
            if field in data:
                less_than = _parse_vision(data.get(field).get("less"))
                more_than = _parse_vision(data.get(field).get("more"))

                pt_ids.extend(
                    _filter_vis_pres_range(
                        KEYWORDS[field],
                        (more_than, less_than),
                        KEYWORDS["vision_value_regex"],
                        vision=True,
                    )
                )

        return set(pt_ids)

    @staticmethod
    def get_pt_id_by_pressure(data: dict) -> set:
        """ Take the json data from filters
        and filter for the pt_ids with pressure

        params:
            data: <dict> input filter json

        returns:
            pt_ids: <set>
        """

        pt_ids = []
        for field in ("left_pressure", "right_pressure"):
            if field in data:
                less_than = data.get(field).get("less")
                more_than = data.get(field).get("more")

                pt_ids.extend(
                    _filter_vis_pres_range(
                        KEYWORDS[field],
                        (more_than, less_than),
                        KEYWORDS["pressure_value_regex"],
                        vision=False,
                    )
                )
        return set(pt_ids)

    @staticmethod
    def get_data_for_pt_id(pt_id, pressure=False, vision=False):
        if not pressure ^ vision:
            raise ValueError(
                "get_data_for_pt_id: set either pressure or vision to True"
            )

        if pressure:
            kws = KEYWORDS["pressure"]
        elif vision:
            kws = KEYWORDS["vision"]

        qry = (
            smart_data_deid.query.with_entities(
                smart_data_deid.element_name,
                smart_data_deid.smrtdta_elem_value,
                smart_data_deid.smart_data_id,
                smart_data_deid.value_dt,
            )
            .filter(
                db.and_(
                    smart_data_deid.pt_id == pt_id,
                    smart_data_deid.element_name.ilike(kws),
                )
            )
            .order_by(smart_data_deid.value_dt.desc())
        )
        res = qry.all()
        return res
