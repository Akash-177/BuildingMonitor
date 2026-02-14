from app import db
from datetime import datetime

class Building(db.Model):
    __tablename__ = 'buildings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    equipment = db.relationship('Equipment', backref='building', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    model = db.Column(db.String(100))
    install_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='healthy')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    readings = db.relationship('SensorReading', backref='equipment', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'building_id': self.building_id,
            'name': self.name,
            'type': self.type,
            'model': self.model,
            'install_date': self.install_date.isoformat() if self.install_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SensorReading(db.Model):
    __tablename__ = 'sensor_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    temperature = db.Column(db.Float)
    vibration = db.Column(db.Float)
    runtime_hours = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    anomaly_detected = db.Column(db.Boolean, default=False)
    
    # added index for faster queries on equipment_id + timestamp
    __table_args__ = (
        db.Index('idx_equipment_time', 'equipment_id', 'timestamp'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'temperature': self.temperature,
            'vibration': self.vibration,
            'runtime_hours': self.runtime_hours,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'anomaly_detected': self.anomaly_detected
        }