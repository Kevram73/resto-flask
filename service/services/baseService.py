from service import db

class BaseService:
    def __init__(self, session):
        self.session = session

    def create(self, model, data):
        try:
            new_entry = model(**data)
            self.session.add(new_entry)
            self.session.commit()
            return new_entry.to_dict()
        except Exception as e:
            self.session.rollback()
            return {'error': str(e)}

    def get(self, model, id):
        entry = model.query.get(id)
        return entry.to_dict() if entry else False

    def update(self, model, id, data):
        entry = model.query.get(id)
        if not entry:
            return False
        try:
            for key, value in data.items():
                setattr(entry, key, value)
            self.session.commit()
            return entry.to_dict()
        except Exception as e:
            self.session.rollback()
            return {'error': str(e)}

    def delete(self, model, id):
        entry = model.query.get(id)
        if not entry:
            return False
        try:
            self.session.delete(entry)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return {'error': str(e)}

    def get_all(self, model):
        entries = model.query.all()
        return [entry.to_dict() for entry in entries]
