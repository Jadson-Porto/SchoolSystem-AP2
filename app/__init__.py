from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import os

db = SQLAlchemy()

def create_app():
    """Factory function para criar e configurar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///school_app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Inicializar extensões
    db.init_app(app)
    
    # Configurar Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }
    
    Swagger(app, config=swagger_config)
    
    from app.routes import register_routes
    register_routes(app)
    
    with app.app_context():
        try:
            db.create_all()
            print(" Tabelas criadas com sucesso!")
        except Exception as e:
            print(f" Erro ao criar tabelas: {e}")
    
    @app.route('/health')
    def health_check():
        """Endpoint para verificar se a aplicação está rodando"""
        return {'status': 'healthy', 'service': 'App'}, 200
    
    @app.route('/')
    def home():
        """Página inicial da API"""
        return {
            'message': 'Microsserviço App - Gerenciamento de Alunos, Professores e Turmas',
            'endpoints': {
                'docs': '/docs/',
                'health': '/health',
                'alunos': '/alunos',
                'professores': '/professores', 
                'turmas': '/turmas'
            }
        }, 200
    
    return app