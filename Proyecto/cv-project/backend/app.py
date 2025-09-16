from flask import Flask, jsonify, request, abort, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import stripe
from scan_utils import scan_ports
from models import db, Profile, Experience, Education, Skill, ScanHistory, DonationHistory
from datetime import datetime
import time
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://cvuser:cvpassword@db:5432/cvproject')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Datos estáticos del CV (fallback si la BD no está disponible) - Solo datos de Luis Eduardo
CV_DATA = {
    "profile": {
        "name": "Luis Eduardo Mejia Aispuro",
        "title": "Estudiante de Ingeniería en Desarrollo de Software",
        "email": "luis.mejia@email.com",
        "phone": "+52 664 123 4567",
        "location": "Tijuana, Baja California, México",
        "summary": "Soy un desarrollador de software comprometido con la creación y mejora continua de soluciones tecnológicas eficientes. Me caracterizo por aprender rápidamente nuevos sistemas y adaptarme con facilidad a diferentes entornos de trabajo. Cuento con una sólida base en desarrollo de software y un enfoque orientado a la calidad, la funcionalidad y la experiencia del usuario. Mi compromiso, capacidad analítica y dedicación me permiten aportar valor real en cada proyecto, buscando siempre optimizar y evolucionar los sistemas que desarrollo."
    },
    "education": [
        {
            "institution": "CESUN Universidad (Plantel Morelos)",
            "degree": "Ing. en Desarrollo de Software",
            "period": "2023 - Actualidad (Cursando)",
            "location": "Tijuana, Baja California, México"
        },
        {
            "institution": "CECYTE BC (Plantel Zona Río)",
            "degree": "Técnico en Programación Orientada a Objetos",
            "period": "2016 - 2019",
            "location": "Tijuana, Baja California, México"
        }
    ],
    "experience": [
        {
            "company": "Foxconn BC",
            "position": "Supervisor Junior",
            "period": "2018 - 2025 (Actualidad)",
            "location": "Tijuana, Baja California, México",
            "responsibilities": [
                "Trabajo como Supervisor Jr. en Foxconn dentro del área de logística, supervisando personal operativo y asegurando el cumplimiento de los estándares establecidos en los planes de envío",
                "Me encargué del manejo de almacén e inventario, optimizando los procesos de recepción, resguardo y distribución de materiales",
                "Coordinación eficiente de recursos humanos para garantizar el flujo logístico diario"
            ]
        }
    ],
    "skills": {
        "backend_development": ["Desarrollo de software especializado en backend"],
        "programming_languages": ["Java", "React", "Node.js", "C#", "Python"],
        "databases": ["SQL Server", "MySQL", "MongoDB", "Manejo de cursores en bases de datos para control detallado de registros y flujos de datos"],
        "frameworks": ["FastAPI", ".NET Framework", "JSON"],
        "tools": ["Cursor (basado en VS Code con IA)", "Visual Studio", "Visual Studio Code", "NetBeans", "Packet Tracer", "WINDSURF"],
        "frontend": ["Diseño de interfaces y desarrollo en frontend (como complemento al enfoque backend)"],
        "office": ["Microsoft Office (Word, Excel, PowerPoint, Outlook) a nivel avanzado"],
        "security": ["Encriptación de contraseñas con KeePass", "Encriptación de discos con VeraCrypt", "Rapid7", "Kraken para pruebas éticas de ataques a BD"],
        "soft_skills": ["Trabajo en equipo", "Proactividad", "Comunicación efectiva", "Liderazgo y manejo de personal", "Pensamiento analítico", "Adaptabilidad", "Compromiso y responsabilidad", "Gestión del tiempo"],
        "certifications": ["EC0553 - Comunicación efectiva en el trabajo", "ISO 9001 - Sistema de Gestión de Calidad", "ISO 27001 - Política de seguridad de información y manejo de software", "EC0160"]
    }
}

@app.route('/api/cv', methods=['GET'])
def get_cv():
    """Endpoint que devuelve los datos del CV desde la base de datos"""
    try:
        # Get CV profile from database
        profile = CVProfile.query.first()
        
        if not profile:
            # If no profile exists, create default one
            profile = create_default_profile()
        
        # Build CV data structure
        cv_data = {
            'profile': profile.to_dict(),
            'experience': [exp.to_dict() for exp in profile.experiences],
            'education': [edu.to_dict() for edu in profile.educations],
            'skills': {}
        }
        
        # Organize skills by category
        for skill in profile.skills:
            cv_data['skills'][skill.category] = skill.skills_list
        
        if profile and profile.photo_filename:
            cv_data['profile']['photo_url'] = f"{request.host_url.rstrip('/')}/uploads/{profile.photo_filename}"
        else:
            cv_data['profile']['photo_url'] = None
        
        return jsonify(cv_data)
        
    except Exception as e:
        # Fallback to static data if database fails
        print(f"Database error, using static data: {e}")
        fallback_data = CV_DATA.copy()
        if fallback_data['profile'].get('photo_filename'):
            fallback_data['profile']['photo_url'] = f"{request.host_url.rstrip('/')}/uploads/{fallback_data['profile']['photo_filename']}"
        return jsonify(fallback_data)

@app.route('/api/scan', methods=['POST'])
def scan_network():
    """Endpoint para escanear puertos usando nmap y guardar en BD"""
    try:
        data = request.get_json()
        
        if not data or 'port_range' not in data:
            return jsonify({'error': 'Se requiere el campo port_range'}), 400
        
        port_range = data['port_range']
        target = data.get('target', 'localhost')
        
        # Validar que solo se permita localhost o 127.0.0.1
        if target not in ['localhost', '127.0.0.1']:
            return jsonify({'error': 'Solo se permite escanear localhost o 127.0.0.1'}), 400
        
        # Validar formato del rango de puertos
        if not port_range or '-' not in port_range:
            return jsonify({'error': 'Formato de rango de puertos inválido. Use formato: "22-443"'}), 400
        
        try:
            start_port, end_port = map(int, port_range.split('-'))
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                raise ValueError()
        except ValueError:
            return jsonify({'error': 'Rango de puertos inválido. Use números entre 1-65535'}), 400
        
        # Realizar el escaneo
        start_time = time.time()
        scan_results = scan_ports(target, port_range)
        duration = time.time() - start_time
        
        # Guardar en base de datos
        try:
            scan_record = ScanHistory(
                target=target,
                port_range=port_range,
                scan_results=scan_results,
                duration=duration
            )
            db.session.add(scan_record)
            db.session.commit()
        except Exception as db_error:
            print(f"Error saving scan to database: {db_error}")
        
        return jsonify({
            'target': target,
            'port_range': port_range,
            'results': scan_results,
            'timestamp': scan_results.get('timestamp', ''),
            'duration': duration
        })
        
    except Exception as e:
        return jsonify({'error': f'Error durante el escaneo: {str(e)}'}), 500

@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Endpoint para crear una sesión de pago con Stripe y guardar en BD"""
    try:
        data = request.get_json()
        amount = data.get('amount', 500)  # Monto por defecto: $5.00 USD
        
        # Crear la sesión de checkout
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Donación - CV Project',
                        'description': 'Gracias por tu apoyo al proyecto CV',
                    },
                    'unit_amount': amount,  # Stripe usa centavos
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:5173/success',
            cancel_url='http://localhost:5173/cancel',
        )
        
        # Guardar en base de datos
        try:
            donation_record = DonationHistory(
                stripe_session_id=checkout_session.id,
                amount=amount,
                currency='usd',
                status='pending'
            )
            db.session.add(donation_record)
            db.session.commit()
        except Exception as db_error:
            print(f"Error saving donation to database: {db_error}")
        
        return jsonify({
            'checkout_url': checkout_session.url,
            'session_id': checkout_session.id
        })
        
    except Exception as e:
        return jsonify({'error': f'Error creando sesión de pago: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de salud para verificar que el servidor está funcionando"""
    return jsonify({
        'status': 'healthy',
        'message': 'CV Project API está funcionando correctamente'
    })

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload-photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo part in the request'}), 400
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Ensure a unique filename to prevent overwrites
        # For simplicity, we'll use the original name, but a better approach would be to use UUIDs
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Update profile in DB
        profile = Profile.query.first()
        if not profile:
            # If no profile exists, create one
            profile = create_default_profile()
            if not profile:
                return jsonify({'error': 'Could not create a default profile.'}), 500

        profile.photo_filename = filename
        db.session.commit()
        photo_url = f"{request.host_url.rstrip('/')}/uploads/{filename}"
        return jsonify({'status': 'success', 'message': 'Photo uploaded successfully', 'photo_url': photo_url})
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/reset-data', methods=['POST'])
def reset_data():
    """Endpoint para limpiar y recargar los datos del CV"""
    try:
        # Delete all existing data
        Profile.query.delete()
        Experience.query.delete()
        Education.query.delete()
        Skill.query.delete()
        db.session.commit()
        
        # Create fresh data
        profile = create_default_profile()
        
        if profile:
            return jsonify({
                'status': 'success',
                'message': 'Datos del CV actualizados correctamente',
                'profile_name': profile.name
            })
        else:
            return jsonify({'error': 'Error al crear el perfil'}), 500
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al resetear datos: {str(e)}'}), 500

def create_default_profile():
    """Crea un perfil por defecto en la base de datos"""
    try:
        # Always create new profile (don't check if exists)
        profile = Profile(
            name="Luis Eduardo Mejia Aispuro",
            title="Estudiante de Ingeniería en Desarrollo de Software",
            email="luis.mejia@email.com",
            phone="+52 664 123 4567",
            location="Tijuana, Baja California, México",
            summary="Soy un desarrollador de software comprometido con la creación y mejora continua de soluciones tecnológicas eficientes. Me caracterizo por aprender rápidamente nuevos sistemas y adaptarme con facilidad a diferentes entornos de trabajo. Cuento con una sólida base en desarrollo de software y un enfoque orientado a la calidad, la funcionalidad y la experiencia del usuario. Mi compromiso, capacidad analítica y dedicación me permiten aportar valor real en cada proyecto, buscando siempre optimizar y evolucionar los sistemas que desarrollo.",
            photo_filename='default.png'
        )
        db.session.add(profile)
        db.session.commit()
        
        # Create experiences
        experiences = [
            Experience(
                profile_id=profile.id,
                company="Foxconn BC",
                position="Supervisor Junior",
                period="2018 - 2025 (Actualidad)",
                location="Tijuana, Baja California, México",
                responsibilities=[
                    "Trabajo como Supervisor Jr. en Foxconn dentro del área de logística, supervisando personal operativo y asegurando el cumplimiento de los estándares establecidos en los planes de envío",
                    "Me encargué del manejo de almacén e inventario, optimizando los procesos de recepción, resguardo y distribución de materiales",
                    "Coordinación eficiente de recursos humanos para garantizar el flujo logístico diario"
                ]
            )
        ]
        
        for exp in experiences:
            db.session.add(exp)
        
        # Create education
        educations = [
            Education(
                profile_id=profile.id,
                institution="CESUN Universidad (Plantel Morelos)",
                degree="Ing. en Desarrollo de Software",
                period="2023 - Actualidad (Cursando)",
                location="Tijuana, Baja California, México"
            ),
            Education(
                profile_id=profile.id,
                institution="CECYTE BC (Plantel Zona Río)",
                degree="Técnico en Programación Orientada a Objetos",
                period="2016 - 2019",
                location="Tijuana, Baja California, México"
            )
        ]
        
        for edu in educations:
            db.session.add(edu)
        
        # Create skills
        skills = [
            Skill(profile_id=profile.id, category="backend_development", skills_list=["Desarrollo de software especializado en backend"]),
            Skill(profile_id=profile.id, category="programming_languages", skills_list=["Java", "React", "Node.js", "C#", "Python"]),
            Skill(profile_id=profile.id, category="databases", skills_list=["SQL Server", "MySQL", "MongoDB", "Manejo de cursores en bases de datos para control detallado de registros y flujos de datos"]),
            Skill(profile_id=profile.id, category="frameworks", skills_list=["FastAPI", ".NET Framework", "JSON"]),
            Skill(profile_id=profile.id, category="tools", skills_list=["Cursor (basado en VS Code con IA)", "Visual Studio", "Visual Studio Code", "NetBeans", "Packet Tracer", "WINDSURF"]),
            Skill(profile_id=profile.id, category="frontend", skills_list=["Diseño de interfaces y desarrollo en frontend (como complemento al enfoque backend)"]),
            Skill(profile_id=profile.id, category="office", skills_list=["Microsoft Office (Word, Excel, PowerPoint, Outlook) a nivel avanzado"]),
            Skill(profile_id=profile.id, category="security", skills_list=["Encriptación de contraseñas con KeePass", "Encriptación de discos con VeraCrypt", "Rapid7", "Kraken para pruebas éticas de ataques a BD"]),
            Skill(profile_id=profile.id, category="soft_skills", skills_list=["Trabajo en equipo", "Proactividad", "Comunicación efectiva", "Liderazgo y manejo de personal", "Pensamiento analítico", "Adaptabilidad", "Compromiso y responsabilidad", "Gestión del tiempo"]),
            Skill(profile_id=profile.id, category="certifications", skills_list=["EC0553 - Comunicación efectiva en el trabajo", "ISO 9001 - Sistema de Gestión de Calidad", "ISO 27001 - Política de seguridad de información y manejo de software", "EC0160"])
        ]
        
        for skill in skills:
            db.session.add(skill)
        
        db.session.commit()
        return profile
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating default profile: {e}")
        return None

@app.route('/api/scan-history', methods=['GET'])
def get_scan_history():
    """Obtener historial de escaneos"""
    try:
        scans = ScanHistory.query.order_by(ScanHistory.timestamp.desc()).limit(10).all()
        return jsonify([scan.to_dict() for scan in scans])
    except Exception as e:
        return jsonify({'error': f'Error obteniendo historial: {str(e)}'}), 500

@app.route('/api/donation-history', methods=['GET'])
def get_donation_history():
    """Obtener historial de donaciones"""
    try:
        donations = DonationHistory.query.order_by(DonationHistory.created_at.desc()).limit(10).all()
        return jsonify([donation.to_dict() for donation in donations])
    except Exception as e:
        return jsonify({'error': f'Error obteniendo historial: {str(e)}'}), 500

if __name__ == '__main__':
    # Verificar que las variables de entorno estén configuradas
    if not os.getenv('STRIPE_SECRET_KEY'):
        print("⚠️  ADVERTENCIA: STRIPE_SECRET_KEY no está configurada en .env")
    
    # Create tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Tablas de base de datos creadas")
        except Exception as e:
            print(f"⚠️  Error creando tablas: {e}")
    
    print("🚀 Iniciando servidor Flask...")
    print("📋 Endpoints disponibles:")
    print("   GET  /api/cv - Obtener datos del CV")
    print("   POST /api/scan - Escanear puertos con nmap")
    print("   POST /api/create-checkout-session - Crear sesión de pago")
    print("   GET  /api/health - Verificar estado del servidor")
    print("   GET  /api/scan-history - Obtener historial de escaneos")
    print("   GET  /api/donation-history - Obtener historial de donaciones")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
