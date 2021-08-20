from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StatusOrden(db.Model):
    __tablename__ = 'statusorden'
    id = db.Column(db.Integer, primary_key=True)
    inicio_fecha = db.Column(db.String(100), unique=False, nullable=False)
    final_fecha = db.Column(db.String(100), unique=False, nullable=True)
    status = db.Column(db.String(120), unique=False, nullable=False)
    minutostrabajados = db.Column(db.String(120), unique=False, nullable=False) #tiempo que se tardo en hacer una aplicacion
    url_foto_epp = db.Column(db.String(120), unique=False, nullable=False)
    url_foto_referencia = db.Column(db.String(200), unique=False, nullable=False)
    geo_lat = db.Column(db.String(120), unique=False, nullable=False)
    geo_lon = db.Column(db.String(120), unique=False, nullable=False)
    #IdForaneos
    id_userorden = db.Column(db.Integer, db.ForeignKey('userorden.id'))
    id_contrato = db.Column(db.Integer, db.ForeignKey('contrato.id'))

class Contrato(db.Model):
    __tablename__ = 'contrato'
    id = db.Column(db.Integer, primary_key=True)
    id_project = db.Column(db.String(60), unique=True, nullable=False)
    region = db.Column(db.String(100), unique=False, nullable=False)
    comuna = db.Column(db.String(100), unique=False, nullable=False)
    sector = db.Column(db.String(100), unique=False, nullable=False)
    cerco_geo_latitud = db.Column(db.String(120), unique=False, nullable=False)
    cerco_geo_longitud = db.Column(db.String(120), unique=False, nullable=False)
    plano = db.Column(db.String(120), unique=False, nullable=False)
    obra_descripcion = db.Column(db.String(200), unique=False, nullable=False)
    planta_matriz = db.Column(db.String(120), unique=False, nullable=False)
    hp = db.Column(db.Integer, unique=False, nullable=False)
    comentario = db.Column(db.String(120), unique=False, nullable=False)
    prioridad = db.Column(db.String(120), unique=False, nullable=False)
    #Relaciones
    statusOrden = db.relationship ('StatusOrden', backref="contrato", lazy=True)
    ordenTrabajo = db.relationship ('OrdenTrabajo', backref="contrato", lazy=True)

class OrdenTrabajo(db.Model):
    __tablename__ = 'ordentrabajo'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), unique=False, nullable=False)
    descripcion = db.Column(db.String(255), unique=False, nullable=False)
    #IdForaneo
    id_contrato = db.Column(db.Integer, db.ForeignKey('contrato.id'))
    #Relaciones
    detalleOrdenTrabajo = db.relationship ('DetalleOrdenTrabajo', backref="ordentrabajo", lazy=True)
    userOrden = db.relationship ('UserOrden', backref="ordentrabajo", lazy=True)

class DetalleOrdenTrabajo(db.Model):
    __tablename__ = 'detalleordentrabajo'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), unique=False, nullable=False)
    descripcion = db.Column(db.String(255), unique=False, nullable=False)
    #idForaneo
    id_ordentrabajo = db.Column(db.Integer, db.ForeignKey('ordentrabajo.id'))

class UserOrden(db.Model):
    __tablename__ = 'userorden'
    id = db.Column(db.Integer, primary_key=True)
    #IdForaneos
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_orden = db.Column(db.Integer, db.ForeignKey('ordentrabajo.id'))
    #Relación
    acreditacion = db.relationship ('Acreditacion', backref="userorden", lazy=True)
    statusOrden = db.relationship ('StatusOrden', backref="userorden", lazy=True)

class Acreditacion(db.Model):
    __tablename__ = 'acreditacion'
    id = db.Column(db.Integer, primary_key=True)
    url_foto = db.Column(db.String(255), unique=False, nullable=False)
    descripcion = db.Column(db.String(255), unique=False, nullable=False)
    #IdForeneo
    id_userorden = db.Column(db.Integer, db.ForeignKey('userorden.id'))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    rut = db.Column(db.String(12), unique=False, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    lastname = db.Column(db.String(100), unique=False, nullable=False)
    contact = db.Column(db.String(120), unique=False, nullable=False)
    register = db.Column(db.String(120), unique=False, nullable=False)
    perfil = db.Column(db.String(120), unique=False, nullable=False)
    fecha_nacimiento = db.Column(db.String(200), unique=False, nullable=False)
    #Relación
    userOrden = db.relationship ('UserOrden', backref="user", lazy=True)

    #def __repr__(self):
        #return '<User %r>' % self.username

    #def serialize(self):
        #return {
            #"id": self.id,
            #"email": self.email,
            # do not serialize the password, its a security breach
        #}