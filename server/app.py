from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Apartment, Tenant, Lease

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )

api = Api(app)

class Apartments(Resource):
    def get(self):
        apartments = Apartment.query.all()
        apartment_list = [apartment.to_dict() for apartment in apartments]

        return make_response(apartment_list, 200)
    
    def post(self):
        data = request.get_json()

        new_apartment = Apartment(
            number=data['number']
        )
        if new_apartment:
            db.session.add(new_apartment)
            db.session.commit()
            return make_response(new_apartment.to_dict(), 200)
        else:
            return make_response({"error":"new apartment invalid data"}, 404)
        
api.add_resource(Apartments, "/apartments")

class ApartmentsByID(Resource):
    def get(self,id):
        apartment = Apartment.query.filter_by(id=id).first().to_dict()
        return make_response(apartment, 200)
    
    def patch(self,id):
        data = request.get_json()

        apartment = Apartment.query.filter_by(id=id).first()

        for attr in data:
            setattr(apartment, attr, data[attr])

        db.session.add(apartment)
        db.session.commit()
        
        return make_response(apartment.to_dict(), 200)
    
    def delete(self, id):
        apartment = Apartment.query.filter_by(id=id).first()

        db.session.delete(apartment)
        db.session.commit()

        return make_response({},204)

api.add_resource(ApartmentsByID, '/apartments/<int:id>')

class Tenants(Resource):
    def get(self):
        tenants = Tenant.query.all()
        tenant_list = [tenant.to_dict() for tenant in tenants]

        return make_response(tenant_list, 200)
    
    def post(self):
        data = request.get_json()

        new_tenant = Tenant(
            name=data['name'],
            age=data['age']
        )
        if new_tenant:
            db.session.add(new_tenant)
            db.session.commit()
            return make_response(new_tenant.to_dict(), 200)
        else:
            return make_response({"error":"new tenant invalid data"}, 404)
        
api.add_resource(Tenants, "/tenants")

class TenantsByID(Resource):
    def get(self,id):
        tenant = Tenant.query.filter_by(id=id).first().to_dict()
        return make_response(tenant, 200)
    
    def patch(self,id):
        data = request.get_json()

        tenant = Tenant.query.filter_by(id=id).first()

        for attr in data:
            setattr(tenant, attr, data[attr])

        db.session.add(tenant)
        db.session.commit()
        
        return make_response(tenant.to_dict(), 200)
    
    def delete(self, id):
        tenant = Tenant.query.filter_by(id=id).first()

        db.session.delete(tenant)
        db.session.commit()

        return make_response({},204)

api.add_resource(TenantsByID, '/tenants/<int:id>')

class Leases(Resource):
    def get(self):
        leases = Tenant.query.all()
        lease_list = [lease.to_dict() for lease in leases]

        return make_response(lease_list, 200)
    def post(self):
        data = request.get_json()

        new_lease = Tenant(
            rent=data['rent']
        )
        if new_lease:
            db.session.add(new_lease)
            db.session.commit()
            return make_response(new_lease.to_dict(), 200)
        else:
            return make_response({"error":"new lease invalid data"}, 404)

api.add_resource(Leases, "/leases")

class LeasesByID(Resource):
    def get(self, id):
        lease = Lease.query.filter_by(id=id).first().to_dict()
        if lease:
            return make_response(lease, 200)
        else:
            return make_response({"error":"invalid id"}, 404)
        
    def delete(self, id):
        lease = Lease.query.filter_by(id=id).first()
        if lease:
            db.session.delete(lease)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error":"invalid id"}, 404)
        
api.add_resource(LeasesByID, '/leases/<int:id>')

        

if __name__ == '__main__':
    app.run( port = 3000, debug = True )