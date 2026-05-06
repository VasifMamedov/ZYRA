from src.ext import db

class BaseModel(db.Model):
    __abstract__ = True

    def create(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()