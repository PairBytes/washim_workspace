from student_app import db, app

class Student(db.Model):
    __tablename__ ="Student_Table"

    Name = db.Column(db.String(25))
    Mobile = db.Column(db.Integer, primary_key=True)
    Address = db.Column(db.String(64))
    Education = db.Column(db.String(30))

    def save(self):
        db.session.add(self)
        db.session.commit()