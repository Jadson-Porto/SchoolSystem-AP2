from flask_restful import Api
from app.controllers.professor_controller import ProfessorListResource, ProfessorResource
from app.controllers.aluno_controller import AlunoListResource, AlunoResource
from app.controllers.turma_controller import TurmaListResource, TurmaResource

def register_routes(app):
    

    api = Api(app, prefix='/api/v1')
    

    api.add_resource(ProfessorListResource, '/professores')
    api.add_resource(ProfessorResource, '/professores/<int:id>')
    

    api.add_resource(AlunoListResource, '/alunos')
    api.add_resource(AlunoResource, '/alunos/<int:id>')
    

    api.add_resource(TurmaListResource, '/turmas')
    api.add_resource(TurmaResource, '/turmas/<int:id>')
    
    
    print(" Rotas registradas com sucesso:")
    with app.app_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
                print(f"   {methods:20} {rule.rule}")