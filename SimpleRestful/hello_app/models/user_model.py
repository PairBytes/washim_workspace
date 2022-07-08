import bcrypt as bcrypt
from hello_app import db, app
from datetime import datetime


class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    designation = db.Column(db.String(255), default='')
    profile_pic = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    user_type = db.Column(db.String(64), default='client')
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)
    last_login = db.Column(db.DateTime, default=datetime.utcnow())
    country_code = db.Column(db.String(8))
    mobile_number = db.Column(db.String(20))
    social_type = db.Column(db.String(32), default='')
    access_token = db.Column(db.Text)
    email_verify = db.Column(db.Boolean, default=False)
    mobile_verify = db.Column(db.Boolean, default=False)
    signup_type = db.Column(db.String(64), default='')
    last_login_type = db.Column(db.String(64), default='')
    address_line1 = db.Column(db.Text)
    address_line2 = db.Column(db.Text)
    country = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(32))
    # zoho_id = db.Column(db.String(64))
    department_type = db.Column(db.String(512))
    pan_number = db.Column(db.String(120))
    # client_profiles = db.relationship('OrgProfileClient', back_populates='client')
    # vendor_profiles = db.relationship('OrgProfileVendor', back_populates='vendor')
    # device_lists = db.relationship("ListOfDevices", backref="device_list")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete()
        db.session.commit()

    def temp_save(self):
        db.session.add(self)
        db.session.flush()

    def to_json(self):
        not_convert_into_str = ['id', 'active', 'created_by', 'updated_by', 'email_verify', 'mobile_verify']
        user_data = {col.name: (str(getattr(self, col.name)) if (
                getattr(self, col.name) is not None and col.name not in not_convert_into_str) else getattr(self,
                                                                                                           col.name))
                for col in self.__table__.columns if col.name != 'password' and col.name != 'access_token'}
        return user_data

    def to_json_access_token(self):
        not_convert_into_str = ['id', 'active', 'created_by', 'updated_by', 'email_verify', 'mobile_verify']
        user_data = {col.name: (str(getattr(self, col.name)) if (
                getattr(self, col.name) is not None and col.name not in not_convert_into_str) else getattr(self,
                                                                                                           col.name))
                     for col in self.__table__.columns if col.name != 'password'}
        return user_data

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id, is_active=True):
        if is_active:
            return cls.query.filter_by(id=user_id, active=True).first()
        return cls.query.get(user_id)

    @classmethod
    def find_by_uuid(cls, user_uuid):
        return cls.query.filter_by(userid=user_uuid).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_mobile(cls, country_code, mobile):
        return cls.query.filter_by(country_code=country_code, mobile_number=mobile).first()

    @classmethod
    def find_all(cls):
        return [user.to_json() for user in cls.query.all()]

    @staticmethod
    def generate_password_hash(password):
        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(10))

    @staticmethod
    def verify_hash(password, hashed):
        return bcrypt.checkpw(password.encode('utf8'), hashed.encode('utf8'))

    @classmethod
    def find_by_email_and_usr_type(cls, email, user_type):
        return cls.query.filter_by(email=email, user_type=user_type).first()

    @classmethod
    def find_by_mobile_and_usr_type(cls, country_code, mobile, user_type):
        return cls.query.filter_by(country_code=country_code, mobile_number=mobile, user_type=user_type).first()

    @classmethod
    def find_by_zoho_id(cls, zoho_id):
        return cls.query.filter_by(zoho_id=zoho_id).first()

    @classmethod
    def find_by_user_type(cls,user_type):
        return cls.query.filter_by(user_type=user_type).all()

    @classmethod
    def find_by_id_user_type(cls, user_id, user_type):
        return cls.query.filter_by(id=user_id, user_type=user_type, active=True).first()
