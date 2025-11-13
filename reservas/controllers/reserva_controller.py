from flask_restful import Resource, reqparse
from services.reserva_service import ReservaService
from datetime import datetime

class ReservaListController(Resource):
    def get(self):
        """
        Lista todas as reservas
        ---
        tags:
          - Reservas
        responses:
          200:
            description: Lista de reservas
          500:
            description: Erro interno do servidor
        """
        try:
            return ReservaService.get_all_reservas()
        except Exception as e:
            return {'error': f'Erro ao listar reservas: {str(e)}'}, 500
    
    def post(self):
        """
        Cria uma nova reserva
        ---
        tags:
          - Reservas
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                num_sala:
                  type: integer
                lab:
                  type: boolean
                data:
                  type: string
                  format: date
                turma_id:
                  type: integer
        responses:
          201:
            description: Reserva criada com sucesso
          400:
            description: Dados inválidos
        """
        parser = reqparse.RequestParser()
        parser.add_argument('num_sala', type=int, required=True, help='Número da sala é obrigatório')
        parser.add_argument('lab', type=bool, required=True, help='Informe se é laboratório (true/false)')
        parser.add_argument('data', type=str, required=True, help='Data da reserva é obrigatória')
        parser.add_argument('turma_id', type=int, required=True, help='ID da turma é obrigatório')
        args = parser.parse_args()
        

        try:
            datetime.strptime(args['data'], '%Y-%m-%d')
        except ValueError:
            return {'error': 'Data da reserva inválida. Use o formato YYYY-MM-DD'}, 400
        

        if args['num_sala'] <= 0:
            return {'error': 'Número da sala deve ser um número positivo'}, 400
        

        if args['turma_id'] <= 0:
            return {'error': 'ID da turma deve ser um número positivo'}, 400
        
        try:
            return ReservaService.create_reserva(args)
        except Exception as e:
            return {'error': f'Erro ao criar reserva: {str(e)}'}, 400

class ReservaController(Resource):
    def get(self, id):
        """
        Busca reserva por ID
        ---
        tags:
          - Reservas
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Reserva encontrada
          404:
            description: Reserva não encontrada
        """
        try:
            return ReservaService.get_reserva_by_id(id)
        except Exception as e:
            return {'error': f'Reserva não encontrada: {str(e)}'}, 404
    
    def put(self, id):
        """
        Atualiza uma reserva
        ---
        tags:
          - Reservas
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
                num_sala:
                  type: integer
                lab:
                  type: boolean
                data:
                  type: string
                  format: date
                turma_id:
                  type: integer
        responses:
          200:
            description: Reserva atualizada
          400:
            description: Dados inválidos
        """
        parser = reqparse.RequestParser()
        parser.add_argument('num_sala', type=int)
        parser.add_argument('lab', type=bool)
        parser.add_argument('data', type=str)
        parser.add_argument('turma_id', type=int)
        args = parser.parse_args()
        

        if args.get('data'):
            try:
                datetime.strptime(args['data'], '%Y-%m-%d')
            except ValueError:
                return {'error': 'Data da reserva inválida. Use o formato YYYY-MM-DD'}, 400
        
        # Validação de num_sala se for fornecido
        if args.get('num_sala') and args['num_sala'] <= 0:
            return {'error': 'Número da sala deve ser um número positivo'}, 400
        
        # Validação de turma_id se for fornecido
        if args.get('turma_id') and args['turma_id'] <= 0:
            return {'error': 'ID da turma deve ser um número positivo'}, 400
        
        try:
            return ReservaService.update_reserva(id, args)
        except Exception as e:
            return {'error': f'Erro ao atualizar reserva: {str(e)}'}, 400
    
    def delete(self, id):
        """
        Exclui uma reserva
        ---
        tags:
          - Reservas
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Reserva excluída
          404:
            description: Reserva não encontrada
        """
        try:
            return ReservaService.delete_reserva(id)
        except Exception as e:
            return {'error': f'Erro ao excluir reserva: {str(e)}'}, 404


class ReservaTurmaController(Resource):
    def get(self, turma_id):
        """
        Lista todas as reservas de uma turma
        ---
        tags:
          - Reservas
        parameters:
          - name: turma_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Lista de reservas da turma
          500:
            description: Erro interno do servidor
        """
        try:
            return ReservaService.get_reservas_by_turma(turma_id)
        except Exception as e:
            return {'error': f'Erro ao listar reservas da turma: {str(e)}'}, 500

class ReservaSalaController(Resource):
    def get(self, num_sala):
        """
        Lista todas as reservas de uma sala específica
        ---
        tags:
          - Reservas
        parameters:
          - name: num_sala
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Lista de reservas da sala
          500:
            description: Erro interno do servidor
        """
        try:
            return ReservaService.get_reservas_by_sala(num_sala)
        except Exception as e:
            return {'error': f'Erro ao listar reservas da sala: {str(e)}'}, 500