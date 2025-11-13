from flask import Flask
from flask_restful import Api
from flasgger import Swagger
import os

from controllers.reserva_controller import (
    ReservaController, 
    ReservaListController,
    ReservaTurmaController,  
    ReservaSalaController    
)

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'reservas-secret-key')
    
    api = Api(app, prefix='/api/v1')
    
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
        "specs_route": "/docs/",
        "title": "Microsserviço Reservas API",
        "version": "1.0.0",
        "description": "API para gerenciamento de reservas de recursos"
    }
    
    Swagger(app, config=swagger_config)
    
    api.add_resource(ReservaListController, '/reservas')
    api.add_resource(ReservaController, '/reservas/<int:id>')
    
    api.add_resource(ReservaTurmaController, '/turmas/<int:turma_id>/reservas')
    api.add_resource(ReservaSalaController, '/salas/<int:num_sala>/reservas')
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'Reservas'}, 200
    
    @app.route('/')
    def home():
        return {
            'message': 'Microsserviço Reservas - Gerenciamento de Reservas de Recursos',
            'version': '1.0.0',
            'endpoints': {
                'docs': '/docs/',
                'health': '/health',
                'reservas': '/api/v1/reservas',
                'reservas_por_turma': '/api/v1/turmas/{id}/reservas',
                'reservas_por_sala': '/api/v1/salas/{num_sala}/reservas'
            }
        }, 200
    
    print(" Microsserviço Reservas iniciado!")
    print(" Rotas registradas com sucesso:")
    with app.app_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
                print(f"   {methods:25} {rule.rule}")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)