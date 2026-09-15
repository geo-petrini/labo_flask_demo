from models.conn import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(260))
    price = db.Column(db.Float, nullable=False)
    category_id  = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('product', lazy=True))
    
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'description':self.description,
            'price':self.price,
            'category':self.category.to_dict() if self.category else None
        }
        
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
        }
        
def seed_categories():
    names = ["Electronics","Clothing","Food","Other"]
    for name in names:
        if not Category.query.filter_by(name=name).first():
            db.session.add( Category(name=name) )
    db.session.commit()
