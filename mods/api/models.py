# -*- coding: utf-8 -*-
# mymodule/models.py
from exts.sqlalchemy import db

from datetime import datetime
from uuid import uuid4

# SQLAlchemy Imports
from sqlalchemy import text, inspect, select, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

# INIT
Base = db.Model
metadata = Base.metadata

# BEGIN
EvalFiles = db.Table(
    'eval_files', metadata,
    db.Column('eval_id', db.Integer, db.ForeignKey('evals.id')),
    db.Column('file_id', db.Integer, db.ForeignKey('files.id')))


class Client(Base):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    fingerprint = db.Column(db.String(64), unique=True)
    last_ip = db.Column(
        db.String(32),
        nullable=False,
        unique=False,
        server_default=u'127.0.0.1')
    date_fseen = db.Column(
        db.DateTime, nullable=False, server_default=text("now()"))
    date_lseen = db.Column(
        db.DateTime, nullable=False, server_default=text("now()"))
    x509_serial = db.Column(db.String(64))
    x509_cname = db.Column(db.String(255))
    x509_email = db.Column(db.String(255))
    x509_orgdept = db.Column(db.String(255))
    x509_orgname = db.Column(db.String(255))
    x509_orgstate = db.Column(db.String(255))
    x509_data = db.Column(db.LargeBinary)
    evals = relationship("Eval", back_populates="client")

    @hybrid_property
    def evals_count(self):
        return len(self.evals)  # @note: use when non-dynamic relationship
        # return self.evals.count() # @note: use when dynamic relationship

    @evals_count.expression
    def evals_count(cls):
        return (select([func.count(
            Eval.id)]).where(Eval.client_id == cls.id).label("evals_count"))

    def toDict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }

    def __repr__(self):
        return '%s' % self.x509_cname

    def __str__(self):
        return '%s' % self.x509_cname


class Eval(Base):
    __tablename__ = 'evals'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = relationship("Client", back_populates="evals")
    uuid_f = db.Column(db.String(36), nullable=False, unique=True)
    corrid = db.Column(db.String(128))
    status_f = db.Column(db.String(32))
    date_f = db.Column(db.DateTime)
    date_b = db.Column(db.DateTime)
    score = db.Column(db.Integer)
    files = relationship("File", secondary=EvalFiles, backref="evals")

    @hybrid_property
    def files_count(self):
        return len(self.files)  # @note: use when non-dynamic relationship
        # return self.evals.count() # @note: use when dynamic relationship

    @files_count.expression
    def files_count(cls):
        return (select([
            func.count(EvalFiles.c.file_id)
        ]).where(EvalFiles.c.eval_id == cls.id).label("files_count"))

    def __init__(self,
                 uuid_f=None,
                 status_f="InProgress",
                 corrid=None,
                 date_f=None,
                 date_b=None,
                 score=0):
        if uuid_f is None:
            uuid_f = str(uuid4())
        self.uuid_f = uuid_f

        self.corrid = corrid
        self.status_f = status_f
        if date_f is None:
            date_f = datetime.now()
        self.date_f = date_f
        self.score = score

    def __repr__(self):
        return '%s' % self.uuid_f

    def getStatus(self):
        if self.status_f != "InProgress":
            return '%s' % self.status_f
        else:
            in_progress = 0
            is_error = 0
            is_complete = 0
            for file in self.files:
                if file.status_f == "InProgress":
                    in_progress += 1
                elif file.status_f == "Error":
                    is_error += 1
                else:
                    is_complete += 1
            if in_progress > 0:
                self.status_f = "InProgress"
            elif is_error > 0:
                self.status_f = "Error"
            else:
                self.status_f = "Complete"
            return '%s' % self.status_f

    def toDict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }


class File(Base):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    mtype = db.Column(db.Text, nullable=False)
    md5 = db.Column(db.String(32), nullable=True)
    sha1 = db.Column(db.String(40), nullable=True)
    hash = db.Column(db.String(64), nullable=False, unique=True)
    uuid_f = db.Column(db.String(36), nullable=False, unique=True)
    status_f = db.Column(db.String(32))
    date_b = db.Column(db.DateTime)
    exec_time = db.Column(db.Float)
    score = db.Column(db.Integer)
    expect_sandbox = db.Column(db.Boolean)
    message = db.Column(db.Text, nullable=True)
    results = db.Column(db.JSON)

    def __init__(self,
                 name=None,
                 mtype=None,
                 hash=None,
                 uuid_f=None,
                 status_f="InProgress",
                 date_b=None,
                 exec_time=0.00,
                 sha1=None,
                 md5=None,
                 score=0,
                 expect_sandbox=False,
                 results={}):
        self.name = name
        self.mtype = mtype
        self.hash = hash
        self.sha1 = sha1
        self.md5 = md5

        if uuid_f is None:
            uuid_f = str(uuid4())
        self.uuid_f = uuid_f

        self.status_f = status_f

        if date_b is None:
            date_b = datetime.now()
        self.date_b = date_b

        self.exec_time = exec_time
        self.score = score
        self.expect_sandbox = expect_sandbox
        self.results = results

    def __repr__(self):
        return '%s' % self.name

    @hybrid_property
    def evals_count(self):
        return len(self.evals)  # @note: use when non-dynamic relationship
        # return self.evals.count() # @note: use when dynamic relationship

    @evals_count.expression
    def evals_count(cls):
        return (select([
            func.count(EvalFiles.c.eval_id)
        ]).where(EvalFiles.c.file_id == cls.id).label("evals_count"))

    def toDict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }


# END
