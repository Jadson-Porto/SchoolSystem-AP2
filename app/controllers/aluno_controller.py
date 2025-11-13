from flask_restful import Resource
from flask import request
from app.services.aluno_service import AlunoService

class AlunoListResource(Resource):
    def get(self):
        """
        Listar todos os Alunos
        ---
        tags:
          - Alunos
        responses:
          200:
            description: Lista de Alunos cadastrados
        """
        try:
            alunos = AlunoService.get_all_alunos()
            return [{
                'id': a.id,
                'nome': a.nome,
                'idade': a.idade,
                'turma_id': a.turma_id,
                'data_nascimento': a.data_nascimento.isoformat() if a.data_nascimento else None,
                'nota_primeiro_semestre': a.nota_primeiro_semestre,
                'nota_segundo_semestre': a.nota_segundo_semestre,
                'media_final': a.media_final,
                'ativo': a.ativo
            } for a in alunos], 200
        except Exception as e:
            return {'error': f'Erro ao listar alunos: {str(e)}'}, 500
    
    def post(self):
        """
        Criar um novo Aluno
        ---
        tags:
          - Alunos
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
                turma_id:
                  type: integer
                data_nascimento:
                  type: string
                  format: date
                nota_primeiro_semestre:
                  type: number
                  format: float
                nota_segundo_semestre:
                  type: number
                  format: float
                ativo:
                  type: boolean
              required:
                - nome
                - idade
                - turma_id
        responses:
          201:
            description: Aluno criado com sucesso
          400:
            description: Dados inválidos
        """
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados JSON são obrigatórios'}, 400
        
        required_fields = ['nome', 'idade', 'turma_id']
        for field in required_fields:
            if field not in data:
                return {'error': f'Campo {field} é obrigatório'}, 400
        
        # Validações adicionais
        if data['idade'] < 0 or data['idade'] > 120:
            return {'error': 'Idade deve estar entre 0 e 120'}, 400
            
        if data.get('nota_primeiro_semestre') and (data['nota_primeiro_semestre'] < 0 or data['nota_primeiro_semestre'] > 10):
            return {'error': 'Nota do primeiro semestre deve estar entre 0 e 10'}, 400
            
        if data.get('nota_segundo_semestre') and (data['nota_segundo_semestre'] < 0 or data['nota_segundo_semestre'] > 10):
            return {'error': 'Nota do segundo semestre deve estar entre 0 e 10'}, 400
        
        try:
            aluno = AlunoService.create_aluno(data)
            return {
                'id': aluno.id,
                'nome': aluno.nome,
                'idade': aluno.idade,
                'turma_id': aluno.turma_id,
                'data_nascimento': aluno.data_nascimento.isoformat() if aluno.data_nascimento else None,
                'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
                'nota_segundo_semestre': aluno.nota_segundo_semestre,
                'media_final': aluno.media_final,
                'ativo': aluno.ativo
            }, 201
        except Exception as e:
            return {'error': f'Erro ao criar aluno: {str(e)}'}, 400


class AlunoResource(Resource):
    def get(self, id):
        """
        Buscar Aluno por ID
        ---
        tags:
          - Alunos
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Aluno encontrado
          404:
            description: Aluno não encontrado
        """
        try:
            aluno = AlunoService.get_aluno_by_id(id)
            return {
                'id': aluno.id,
                'nome': aluno.nome,
                'idade': aluno.idade,
                'turma_id': aluno.turma_id,
                'data_nascimento': aluno.data_nascimento.isoformat() if aluno.data_nascimento else None,
                'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
                'nota_segundo_semestre': aluno.nota_segundo_semestre,
                'media_final': aluno.media_final,
                'ativo': aluno.ativo
            }, 200
        except Exception as e:
            return {'error': f'Aluno não encontrado: {str(e)}'}, 404
    
    def put(self, id):
        """
        Atualizar Aluno por ID
        ---
        tags:
          - Alunos
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
                turma_id:
                  type: integer
                data_nascimento:
                  type: string
                  format: date
                nota_primeiro_semestre:
                  type: number
                  format: float
                nota_segundo_semestre:
                  type: number
                  format: float
                ativo:
                  type: boolean
        responses:
          200:
            description: Aluno atualizado com sucesso
          404:
            description: Aluno não encontrado
        """
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados JSON são obrigatórios'}, 400
        
        # Validações
        if 'idade' in data and (data['idade'] < 0 or data['idade'] > 120):
            return {'error': 'Idade deve estar entre 0 e 120'}, 400
            
        if 'nota_primeiro_semestre' in data and (data['nota_primeiro_semestre'] < 0 or data['nota_primeiro_semestre'] > 10):
            return {'error': 'Nota do primeiro semestre deve estar entre 0 e 10'}, 400
            
        if 'nota_segundo_semestre' in data and (data['nota_segundo_semestre'] < 0 or data['nota_segundo_semestre'] > 10):
            return {'error': 'Nota do segundo semestre deve estar entre 0 e 10'}, 400
        
        try:
            aluno = AlunoService.update_aluno(id, data)
            return {
                'id': aluno.id,
                'nome': aluno.nome,
                'idade': aluno.idade,
                'turma_id': aluno.turma_id,
                'data_nascimento': aluno.data_nascimento.isoformat() if aluno.data_nascimento else None,
                'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
                'nota_segundo_semestre': aluno.nota_segundo_semestre,
                'media_final': aluno.media_final,
                'ativo': aluno.ativo
            }, 200
        except Exception as e:
            return {'error': f'Erro ao atualizar aluno: {str(e)}'}, 400
    
    def delete(self, id):
        """
        Deletar Aluno por ID
        ---
        tags:
          - Alunos
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Aluno deletado com sucesso
          404:
            description: Aluno não encontrado
        """
        try:
            AlunoService.delete_aluno(id)
            return {'message': 'Aluno deletado com sucesso'}, 200
        except Exception as e:
            return {'error': f'Erro ao deletar aluno: {str(e)}'}, 404