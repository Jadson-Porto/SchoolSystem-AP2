from flask_restful import Resource
from flask import request
from app.services.turma_service import TurmaService

class TurmaListResource(Resource):
    def get(self):
        """
        Listar todas as Turmas
        ---
        tags:
          - Turmas
        responses:
          200:
            description: Lista de Turmas cadastradas
        """
        try:
            turmas = TurmaService.get_all_turmas()
            return [{
                'id': t.id, 
                'descricao': t.descricao, 
                'professor_id': t.professor_id,
                'ativo': t.ativo
            } for t in turmas], 200
        except Exception as e:
            return {'error': f'Erro ao listar turmas: {str(e)}'}, 500
    
    def post(self):
        """
        Criar uma nova Turma
        ---
        tags:
          - Turmas
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                descricao:
                  type: string
                professor_id:
                  type: integer
                ativo:
                  type: boolean
              required:
                - descricao
                - professor_id
        responses:
          201:
            description: Turma criada com sucesso
          400:
            description: Dados inválidos
        """
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados JSON são obrigatórios'}, 400
        
        required_fields = ['descricao', 'professor_id']
        for field in required_fields:
            if field not in data:
                return {'error': f'Campo {field} é obrigatório'}, 400
        
        # Validações adicionais
        if len(data['descricao'].strip()) < 2:
            return {'error': 'Descrição deve ter pelo menos 2 caracteres'}, 400
            
        if data['professor_id'] <= 0:
            return {'error': 'ID do professor deve ser um número positivo'}, 400
        
        try:
            turma = TurmaService.create_turma(data)
            return {
                'id': turma.id, 
                'descricao': turma.descricao, 
                'professor_id': turma.professor_id,
                'ativo': turma.ativo
            }, 201
        except Exception as e:
            return {'error': f'Erro ao criar turma: {str(e)}'}, 400


class TurmaResource(Resource):
    def get(self, id):
        """
        Buscar Turma por ID
        ---
        tags:
          - Turmas
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Turma encontrada
          404:
            description: Turma não encontrada
        """
        try:
            turma = TurmaService.get_turma_by_id(id)
            return {
                'id': turma.id, 
                'descricao': turma.descricao, 
                'professor_id': turma.professor_id,
                'ativo': turma.ativo
            }, 200
        except Exception as e:
            return {'error': f'Turma não encontrada: {str(e)}'}, 404
    
    def put(self, id):
        """
        Atualizar Turma por ID
        ---
        tags:
          - Turmas
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
                descricao:
                  type: string
                professor_id:
                  type: integer
                ativo:
                  type: boolean
        responses:
          200:
            description: Turma atualizada com sucesso
          404:
            description: Turma não encontrada
        """
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados JSON são obrigatórios'}, 400
        
        # Validações
        if 'descricao' in data and len(data['descricao'].strip()) < 2:
            return {'error': 'Descrição deve ter pelo menos 2 caracteres'}, 400
            
        if 'professor_id' in data and data['professor_id'] <= 0:
            return {'error': 'ID do professor deve ser um número positivo'}, 400
        
        try:
            turma = TurmaService.update_turma(id, data)
            return {
                'id': turma.id, 
                'descricao': turma.descricao, 
                'professor_id': turma.professor_id,
                'ativo': turma.ativo
            }, 200
        except Exception as e:
            return {'error': f'Erro ao atualizar turma: {str(e)}'}, 400
    
    def delete(self, id):
        """
        Deletar Turma por ID
        ---
        tags:
          - Turmas
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Turma deletada com sucesso
          404:
            description: Turma não encontrada
        """
        try:
            # Verifica se a turma existe antes de deletar
            turma = TurmaService.get_turma_by_id(id)
            if not turma:
                return {'error': 'Turma não encontrada'}, 404
                
            TurmaService.delete_turma(id)
            return {'message': 'Turma deletada com sucesso'}, 200
        except Exception as e:
            return {'error': f'Erro ao deletar turma: {str(e)}'}, 404