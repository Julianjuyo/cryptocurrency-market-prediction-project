from models import Base
from models.exchange import Exchange
from models.price import Price
from models.asset import Asset
from models.indicator import Indicator


def from_dict(dict, model_instance):
    for c in model_instance.__table__.columns:
        setattr(model_instance, c.name, dict[c.name])
