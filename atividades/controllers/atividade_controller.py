from flask_restful import Resource, reqparse
from services.atividade_service import AtividadeService
from datetime import datetime

class AtividadeListController(Resource):
    def get(self):
        """
        Lista todas as atividades
        ---
        tags:
          - Atividades
        responses:
          200:
            description: Lista de atividades
          500:
            description: Erro interno do servidor
        """
        try:
            return AtividadeService.get_all_atividades()
        except Exception as e:
            return {'error': f'Erro ao listar atividades: {str(e)}'}, 500
    
    def post(self):
        """
        Cria uma nova atividade
        ---
        tags:
          - Atividades
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nome_atividade:
                  type: string
                descricao:
                  type: string
                peso_porcento:
                  type: integer
                data_entrega:
                  type: string
                  format: date
                turma_id:
                  type: integer
                professor_id:
                  type: integer
        responses:
          201:
            description: Atividade criada com sucesso
          400:
            description: Dados inválidos
        """
        parser = reqparse.RequestParser()
        parser.add_argument('nome_atividade', type=str, required=True, help='Nome da atividade é obrigatório')
        parser.add_argument('descricao', type=str, required=True, help='Descrição é obrigatória')
        parser.add_argument('peso_porcento', type=int, required=True, help='Peso em porcentagem é obrigatório')
        parser.add_argument('data_entrega', type=str, required=True, help='Data de entrega é obrigatória')
        parser.add_argument('turma_id', type=int, required=True, help='ID da turma é obrigatório')
        parser.add_argument('professor_id', type=int, required=True, help='ID do professor é obrigatório')
        args = parser.parse_args()
        
        # Validação da data
        try:
            datetime.strptime(args['data_entrega'], '%Y-%m-%d')
        except ValueError:
            return {'error': 'Data de entrega inválida. Use o formato YYYY-MM-DD'}, 400
        
        # Validação de campos vazios
        if not args['nome_atividade'].strip():
            return {'error': 'Nome da atividade não pode estar vazio'}, 400
        if not args['descricao'].strip():
            return {'error': 'Descrição não pode estar vazia'}, 400
        
        # Validação do peso
        if args['peso_porcento'] <= 0 or args['peso_porcento'] > 100:
            return {'error': 'Peso deve estar entre 1 e 100'}, 400
        
        # Validação de IDs
        if args['turma_id'] <= 0:
            return {'error': 'ID da turma deve ser um número positivo'}, 400
        if args['professor_id'] <= 0:
            return {'error': 'ID do professor deve ser um número positivo'}, 400
        
        try:
            return AtividadeService.create_atividade(args)
        except Exception as e:
            return {'error': f'Erro ao criar atividade: {str(e)}'}, 400

class AtividadeController(Resource):
    def get(self, id):
        """
        Busca atividade por ID
        ---
        tags:
          - Atividades
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Atividade encontrada
          404:
            description: Atividade não encontrada
        """
        try:
            return AtividadeService.get_atividade_by_id(id)
        except Exception as e:
            return {'error': f'Atividade não encontrada: {str(e)}'}, 404
    
    def put(self, id):
        """
        Atualiza uma atividade
        ---
        tags:
          - Atividades
        parameters:
          - name: id
            in: path
            type: integer
            required: true
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nome_atividade:
                  type: string
                descricao:
                  type: string
                peso_porcento:
                  type: integer
                data_entrega:
                  type: string
                  format: date
                turma_id:
                  type: integer
                professor_id:
                  type: integer
        responses:
          200:
            description: Atividade atualizada
          400:
            description: Dados inválidos
        """
        parser = reqparse.RequestParser()
        parser.add_argument('nome_atividade', type=str)
        parser.add_argument('descricao', type=str)
        parser.add_argument('peso_porcento', type=int)
        parser.add_argument('data_entrega', type=str)
        parser.add_argument('turma_id', type=int)
        parser.add_argument('professor_id', type=int)
        args = parser.parse_args()
        
        # Validação da data se for fornecida
        if args.get('data_entrega'):
            try:
                datetime.strptime(args['data_entrega'], '%Y-%m-%d')
            except ValueError:
                return {'error': 'Data de entrega inválida. Use o formato YYYY-MM-DD'}, 400
        
        # Validação do peso se for fornecido
        if args.get('peso_porcento') and (args['peso_porcento'] <= 0 or args['peso_porcento'] > 100):
            return {'error': 'Peso deve estar entre 1 e 100'}, 400
        
        try:
            return AtividadeService.update_atividade(id, args)
        except Exception as e:
            return {'error': f'Erro ao atualizar atividade: {str(e)}'}, 400
    
    def delete(self, id):
        """
        Exclui uma atividade
        ---
        tags:
          - Atividades
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Atividade excluída
          404:
            description: Atividade não encontrada
        """
        try:
            return AtividadeService.delete_atividade(id)
        except Exception as e:
            return {'error': f'Erro ao excluir atividade: {str(e)}'}, 404

# ===== CLASSES DE NOTAS (QUE ESTAVAM FALTANDO) =====

class NotaController(Resource):
    def get(self, atividade_id):
        """
        Lista todas as notas de uma atividade
        ---
        tags:
          - Notas
        parameters:
          - name: atividade_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Lista de notas
        """
        try:
            return AtividadeService.get_notas_by_atividade(atividade_id)
        except Exception as e:
            return {'error': f'Erro ao listar notas: {str(e)}'}, 500
    
    def post(self, atividade_id):
        """
        Adiciona uma nota à atividade
        ---
        tags:
          - Notas
        parameters:
          - name: atividade_id
            in: path
            type: integer
            required: true
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nota:
                  type: number
                  minimum: 0
                  maximum: 10
                aluno_id:
                  type: integer
        responses:
          201:
            description: Nota criada com sucesso
          400:
            description: Dados inválidos
        """
        parser = reqparse.RequestParser()
        parser.add_argument('nota', type=float, required=True, help='Nota é obrigatória')
        parser.add_argument('aluno_id', type=int, required=True, help='ID do aluno é obrigatório')
        args = parser.parse_args()
        args['atividade_id'] = atividade_id
        
        # Validação da nota
        if args['nota'] < 0 or args['nota'] > 10:
            return {'error': 'Nota deve estar entre 0 e 10'}, 400
        
        try:
            return AtividadeService.create_nota(args)
        except Exception as e:
            return {'error': f'Erro ao criar nota: {str(e)}'}, 400

class NotaDetailController(Resource):
    def get(self, id):
        """
        Busca nota por ID
        ---
        tags:
          - Notas
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Nota encontrada
          404:
            description: Nota não encontrada
        """
        try:
            return AtividadeService.get_nota_by_id(id)
        except Exception as e:
            return {'error': f'Nota não encontrada: {str(e)}'}, 404
    
    def put(self, id):
        """
        Atualiza uma nota
        ---
        tags:
          - Notas
        parameters:
          - name: id
            in: path
            type: integer
            required: true
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nota:
                  type: number
                  minimum: 0
                  maximum: 10
        responses:
          200:
            description: Nota atualizada
          400:
            description: Dados inválidos
        """
        parser = reqparse.RequestParser()
        parser.add_argument('nota', type=float, required=True, help='Nota é obrigatória')
        args = parser.parse_args()
        
        # Validação da nota
        if args['nota'] < 0 or args['nota'] > 10:
            return {'error': 'Nota deve estar entre 0 e 10'}, 400
        
        try:
            return AtividadeService.update_nota(id, args)
        except Exception as e:
            return {'error': f'Erro ao atualizar nota: {str(e)}'}, 400
    
    def delete(self, id):
        """
        Exclui uma nota
        ---
        tags:
          - Notas
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Nota excluída
          404:
            description: Nota não encontrada
        """
        try:
            return AtividadeService.delete_nota(id)
        except Exception as e:
            return {'error': f'Erro ao excluir nota: {str(e)}'}, 404

class NotaAlunoController(Resource):
    def get(self, aluno_id):
        """
        Lista todas as notas de um aluno
        ---
        tags:
          - Notas
        parameters:
          - name: aluno_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Lista de notas do aluno
          500:
            description: Erro interno do servidor
        """
        try:
            return AtividadeService.get_notas_by_aluno(aluno_id)
        except Exception as e:
            return {'error': f'Erro ao listar notas do aluno: {str(e)}'}, 500