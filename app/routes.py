from flask import Blueprint, request, jsonify
from app import db
from app.models import Building, Equipment, SensorReading
from datetime import datetime, timedelta
import statistics

bp = Blueprint('api', __name__, url_prefix='/api')

# Buildings endpoints
@bp.route('/buildings', methods=['GET'])
def get_buildings():
    buildings = Building.query.all()
    return jsonify([b.to_dict() for b in buildings])

@bp.route('/buildings', methods=['POST'])
def create_building():
    data = request.json
    building = Building(
        name=data.get('name'),
        location=data.get('location')
    )
    db.session.add(building)
    db.session.commit()
    return jsonify(building.to_dict()), 201

@bp.route('/buildings/<int:id>', methods=['GET'])
def get_building(id):
    building = Building.query.get_or_404(id)
    return jsonify(building.to_dict())


# Equipment endpoints
@bp.route('/equipment', methods=['GET'])
def get_equipment():
    equipment = Equipment.query.all()
    return jsonify([e.to_dict() for e in equipment])

@bp.route('/equipment', methods=['POST'])
def create_equipment():
    data = request.json
    
    install_date = None
    if data.get('install_date'):
        install_date = datetime.strptime(data['install_date'], '%Y-%m-%d').date()
    
    equipment = Equipment(
        building_id=data.get('building_id'),
        name=data.get('name'),
        type=data.get('type'),
        model=data.get('model'),
        install_date=install_date
    )
    db.session.add(equipment)
    db.session.commit()
    return jsonify(equipment.to_dict()), 201

@bp.route('/equipment/<int:id>', methods=['GET'])
def get_equipment_detail(id):
    equipment = Equipment.query.get_or_404(id)
    return jsonify(equipment.to_dict())

@bp.route('/equipment/<int:id>', methods=['PUT'])
def update_equipment(id):
    equipment = Equipment.query.get_or_404(id)
    data = request.json
    
    if 'name' in data:
        equipment.name = data['name']
    if 'type' in data:
        equipment.type = data['type']
    if 'model' in data:
        equipment.model = data['model']
    if 'status' in data:
        equipment.status = data['status']
    
    db.session.commit()
    return jsonify(equipment.to_dict())

@bp.route('/equipment/<int:id>', methods=['DELETE'])
def delete_equipment(id):
    equipment = Equipment.query.get_or_404(id)
    db.session.delete(equipment)
    db.session.commit()
    return jsonify({'message': 'Equipment deleted'}), 200


# Sensor data endpoint - this is where anomaly detection happens
@bp.route('/sensors', methods=['POST'])
def receive_sensor_data():
    data = request.json
    
    reading = SensorReading(
        equipment_id=data.get('equipment_id'),
        temperature=data.get('temperature'),
        vibration=data.get('vibration'),
        runtime_hours=data.get('runtime_hours')
    )
    
    # check for anomalies using basic stats approach
    # TODO: maybe use Isolation Forest model instead of this simple method
    equip_id = data.get('equipment_id')
    recent = SensorReading.query.filter_by(
        equipment_id=equip_id
    ).order_by(SensorReading.timestamp.desc()).limit(100).all()
    
    # need at least 20 readings to establish baseline
    if len(recent) >= 20:
        temps = [r.temperature for r in recent if r.temperature]
        vibes = [r.vibration for r in recent if r.vibration]
        
        if temps and vibes:
            avg_temp = statistics.mean(temps)
            std_temp = statistics.stdev(temps) if len(temps) > 1 else 0
            avg_vibe = statistics.mean(vibes)
            std_vibe = statistics.stdev(vibes) if len(vibes) > 1 else 0
            
            # flag if more than 2 std deviations away from mean
            temp_diff = abs(data.get('temperature', 0) - avg_temp)
            vibe_diff = abs(data.get('vibration', 0) - avg_vibe)
            
            if std_temp > 0 and temp_diff > (2 * std_temp):
                reading.anomaly_detected = True
            elif std_vibe > 0 and vibe_diff > (2 * std_vibe):
                reading.anomaly_detected = True
    
    db.session.add(reading)
    db.session.commit()
    
    # update equipment status based on anomalies
    update_equipment_status(equip_id)
    
    return jsonify(reading.to_dict()), 201


@bp.route('/equipment/<int:id>/health', methods=['GET'])
def get_equipment_health(id):
    equipment = Equipment.query.get_or_404(id)
    
    # grab last 24 hours of data
    day_ago = datetime.utcnow() - timedelta(hours=24)
    recent = SensorReading.query.filter(
        SensorReading.equipment_id == id,
        SensorReading.timestamp >= day_ago
    ).order_by(SensorReading.timestamp.desc()).all()
    
    anomaly_count = sum(1 for r in recent if r.anomaly_detected)
    
    return jsonify({
        'equipment_id': id,
        'equipment_name': equipment.name,
        'status': equipment.status,
        'recent_readings_count': len(recent),
        'anomalies_detected_24h': anomaly_count,
        'recent_readings': [r.to_dict() for r in recent[:10]]
    })


def update_equipment_status(equip_id):
    equipment = Equipment.query.get(equip_id)
    if not equipment:
        return
    
    day_ago = datetime.utcnow() - timedelta(hours=24)
    anomalies = SensorReading.query.filter(
        SensorReading.equipment_id == equip_id,
        SensorReading.timestamp >= day_ago,
        SensorReading.anomaly_detected == True
    ).count()
    
    # update status - might need to adjust these thresholds
    if anomalies >= 5:
        equipment.status = 'critical'
    elif anomalies >= 2:
        equipment.status = 'warning'
    else:
        equipment.status = 'healthy'
    
    db.session.commit()