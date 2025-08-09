from models.sport_type import SportType
from schemas.sport_type_s import SportTypeSchema
from app.extensions import db

sport_type_schema = SportTypeSchema()
sport_types_schema = SportTypeSchema(many=True)

def create_sport_type(data):
    validated_data = sport_type_schema.load(data)
    new_sport = SportType(**validated_data)
    db.session.add(new_sport)
    db.session.commit()
    return sport_type_schema.dump(new_sport)

def get_all_sport_types():
    sport_types = SportType.query.all()
    return sport_types_schema.dump(sport_types)

def get_sport_type_by_id(sport_id):
    sport_type = SportType.query.get(sport_id)
    if sport_type:
        return sport_type_schema.dump(sport_type)
    return None

def update_sport_type(sport_id, data):
    sport_type = SportType.query.get(sport_id)
    if sport_type:
        validated_data = sport_type_schema.load(data, partial=True)
        for key, value in validated_data.items():
            setattr(sport_type, key, value)
        db.session.commit()
        return sport_type_schema.dump(sport_type)
    return None

def delete_sport_type(sport_id):
    sport_type = SportType.query.get(sport_id)
    if sport_type:
        db.session.delete(sport_type)
        db.session.commit()
        return True
    return False
