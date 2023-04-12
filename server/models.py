from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Apartment(db.Model, SerializerMixin):
    __tablename__ = "apartments"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    leases = db.relationship('Lease', back_populates = 'apartment')
    tenants = association_proxy('leases', 'apartment')

    serialize_rules = ('-created_at','-updated_at','-tenants.created_at', '-tenants.updated_at','-tenants.apartments','-leases')


class Tenant(db.Model, SerializerMixin):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    leases = db.relationship('Lease', back_populates = 'tenant')
    apartments = association_proxy('leases', 'tenant')

    serialize_rules = ('-created_at','-updated_at','-apartments.created_at', '-apartments.updated_at','-apartments.tenants','-leases')

    @validates('name')
    def validate_name(self, key, name):
        if len(name) < 1:
            raise ValueError("Name must be present")
        return name
    
    @validates("age")
    def validate_age(self, key, age):
        if age < 18:
            raise ValueError("Tenant too young")
        return age
    

class Lease(db.Model, SerializerMixin):
    __tablename__ = 'leases'

    id = db.Column(db.Integer, primary_key = True)
    rent = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    
    apartment = db.relationship('Apartment', back_populates = 'leases')
    tenant = db.relationship('Tenant', back_populates = 'leases')

    serialize_rules = ('-created_at', '-updated_at', '-apartment.leases', '-tenant.leases', '-apartment.tenants', '-tenant.apartments')
    


