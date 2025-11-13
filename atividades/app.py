from flask import Flask
from flask_restful import Api
from flasgger import Swagger
import os

from controllers.atividade_controller import (
    AtividadeController, 
    AtividadeListController, 
    NotaController, 
    NotaDetailController, 
    NotaAlunoController
)

def create_app():
    """Factory function para criar e configurar a aplicação Flask"""
    app = Flask(__name__)
    

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'atividades-secret-key')
    

    api = Api(app, prefix='/api/v1')
    
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
        "specs_route": "/docs/",
        "title": "Microsserviço Atividades API",
        "version": "1.0.0",
        "description": "API para gerenciamento de atividades e notas"
    }
    
    Swagger(app, config=swagger_config)
    

    api.add_resource(AtividadeListController, '/atividades')
    api.add_resource(AtividadeController, '/atividades/<int:id>')
    

    api.add_resource(NotaController, '/atividades/<int:atividade_id>/notas')
    api.add_resource(NotaDetailController, '/notas/<int:id>')
    api.add_resource(NotaAlunoController, '/alunos/<int:aluno_id>/notas')
    

    @app.route('/health')
    def health_check():
        """Endpoint para verificar se a aplicação está rodando"""
        return {'status': 'healthy', 'service': 'Atividades'}, 200
    
    @app.route('/')
    def home():
        """Página inicial da API"""
        return {
            'message': 'Microsserviço Atividades - Gerenciamento de Atividades e Notas',
            'version': '1.0.0',
            'endpoints': {
                'docs': '/docs/',
                'health': '/health',
                'atividades': '/api/v1/atividades',
                'notas_por_atividade': '/api/v1/atividades/{id}/notas',
                'notas_por_aluno': '/api/v1/alunos/{id}/notas',
                'nota_especifica': '/api/v1/notas/{id}'
            }
        }, 200
    

    print("🚀 Microsserviço Atividades iniciado!")
    print("✅ Rotas registradas com sucesso:")
    with app.app_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
                print(f"   {methods:25} {rule.rule}")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5002)