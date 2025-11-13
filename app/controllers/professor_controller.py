from flask_restful import Resource
from flask import request
from app.services.professor_service import ProfessorService

class ProfessorListResource(Resource):
    def get(self):
        """
        Listar todos os Professores
        ---
        tags:
          - Professores
        responses:
          200:
            description: Lista de Professores cadastrados
        """
        try:
            professores = ProfessorService.get_all_professores()
            return [{
                'id': p.id, 
                'nome': p.nome, 
                'idade': p.idade,
                'materia': p.materia,
                'observacoes': p.observacoes
            } for p in professores], 200
        except Exception as e:
            return {'error': f'Erro ao listar professores: {str(e)}'}, 500
    
    def post(self):
        """
        Criar um novo Professor
        ---
        tags:
          - Professores
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                idade:
                  type: integer
                materia:
                  type: string
                observacoes:
                  type: string
              required:
                - nome
                - idade
                - materia
        responses:
          201:
            description: Professor criado com sucesso
          400:
            description: Dados inválidos
        """
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados JSON são obrigatórios'}, 400
        
        required_fields = ['nome', 'idade', 'materia']
        for field in required_fields:
            if field not in data:
                return {'error': f'Campo {field} é obrigatório'}, 400
        
        # Validações adicionais
        if data['idade'] < 18 or data['idade'] > 100:
            return {'error': 'Idade deve estar entre 18 e 100 anos'}, 400
            
        if len(data['nome'].strip()) < 2:
            return {'error': 'Nome deve ter pelo menos 2 caracteres'}, 400
            
        if len(data['materia'].strip()) < 2:
            return {'error': 'Matéria deve ter pelo menos 2 caracteres'}, 400
        
        try:
            professor = ProfessorService.create_professor(data)
            return {
                'id': professor.id, 
                'nome': professor.nome, 
                'idade': professor.idade,
                'materia': professor.materia,
                'observacoes': professor.observacoes
            }, 201
        except Exception as e:
            return {'error': f'Erro ao criar professor: {str(e)}'}, 400


class ProfessorResource(Resource):
    def get(self, id):
        """
        Buscar Professor por ID
        ---
        tags:
          - Professores
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Professor encontrado
          404:
            description: Professor não encontrado
        """
        try:
            professor = ProfessorService.get_professor_by_id(id)
            return {
                'id': professor.id, 
                'nome': professor.nome, 
                'idade': professor.idade,
                'materia': professor.materia,
                'observacoes': professor.observacoes
            }, 200
        except Exception as e:
            return {'error': f'Professor não encontrado: {str(e)}'}, 404
    
    def put(self, id):
        """
        Atualizar Professor por ID
        ---
        tags:
          - Professores
        parameters:
          - name: id
            in: path
            type: integer
            required: true
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                idade:
                  type: integer
                materia:
                  type: string
                observacoes:
                  type: string
        responses:
          200:
            description: Professor atualizado com sucesso
          404:
            description: Professor não encontrado
        """
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados JSON são obrigatórios'}, 400
        
        # Validações
        if 'idade' in data and (data['idade'] < 18 or data['idade'] > 100):
            return {'error': 'Idade deve estar entre 18 e 100 anos'}, 400
            
        if 'nome' in data and len(data['nome'].strip()) < 2:
            return {'error': 'Nome deve ter pelo menos 2 caracteres'}, 400
            
        if 'materia' in data and len(data['materia'].strip()) < 2:
            return {'error': 'Matéria deve ter pelo menos 2 caracteres'}, 400
        
        try:
            professor = ProfessorService.update_professor(id, data)
            return {
                'id': professor.id, 
                'nome': professor.nome, 
                'idade': professor.idade,
                'materia': professor.materia,
                'observacoes': professor.observacoes
            }, 200
        except Exception as e:
            return {'error': f'Erro ao atualizar professor: {str(e)}'}, 400
    
    def delete(self, id):
        """
        Deletar Professor por ID
        ---
        tags:
          - Professores
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Professor deletado com sucesso
          404:
            description: Professor não encontrado
        """
        try:
            ProfessorService.delete_professor(id)
            return {'message': 'Professor deletado com sucesso'}, 200
        except Exception as e:
            return {'error': f'Erro ao deletar professor: {str(e)}'}, 404