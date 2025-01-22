  student_id=db.Column(db.Integer,db.ForeignKey("students.id", ondelete="CASCADE"),nullable=False)#ondelete="CASCADE" means when a student is deleted, the parent will also be deleted
