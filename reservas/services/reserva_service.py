from models.reserva import Reserva
from datetime import datetime
import requests


reservas_db = []
current_id = 1

class ReservaService:
    

    
    @staticmethod
    def get_all_reservas():
        reservas_ordenadas = sorted(reservas_db, key=lambda x: x.data)
        return [reserva.to_dict() for reserva in reservas_ordenadas], 200
    
    @staticmethod
    def get_reserva_by_id(id):
        reserva = next((r for r in reservas_db if r.id == id), None)
        if reserva:
            return reserva.to_dict(), 200
        return {'error': 'Reserva não encontrada'}, 404
    
    @staticmethod
    def _validar_turma_existe(turma_id):
        try:
            response = requests.get(f'http://app:5000/api/v1/turmas/{turma_id}', timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    @staticmethod
    def create_reserva(data):
  
        global current_id
        

        if 'turma_id' not in data or 'num_sala' not in data or 'lab' not in data or 'data' not in data:
            return {'error': 'Campos obrigatórios: turma_id, num_sala, lab, data'}, 400
        
        if not ReservaService._validar_turma_existe(data['turma_id']):
            return {'error': 'Turma não encontrada no sistema'}, 400
        
        try:
            data_reserva = datetime.strptime(data['data'], '%Y-%m-%d').date()
            if data_reserva < datetime.now().date():
                return {'error': 'Data da reserva deve ser futura'}, 400
        except ValueError:
            return {'error': 'Data da reserva inválida. Use formato YYYY-MM-DD'}, 400
        
 
        conflito = ReservaService._verificar_conflito_reserva(
            data['num_sala'], 
            data['lab'],
            data['data']
        )
        if conflito:
            return {'error': f'Conflito de reserva: {conflito}'}, 400
        
        nova_reserva = Reserva(
            id=current_id,
            num_sala=data['num_sala'],
            lab=data['lab'],
            data=data['data'],
            turma_id=data['turma_id']
        )
        reservas_db.append(nova_reserva)
        current_id += 1
        return nova_reserva.to_dict(), 201
    
    @staticmethod
    def update_reserva(id, data):

        reserva = next((r for r in reservas_db if r.id == id), None)
        if not reserva:
            return {'error': 'Reserva não encontrada'}, 404
        

        if 'num_sala' in data or 'lab' in data or 'data' in data:
            num_sala = data.get('num_sala', reserva.num_sala)
            lab = data.get('lab', reserva.lab)
            data_reserva = data.get('data', reserva.data)
            
            conflito = ReservaService._verificar_conflito_reserva(num_sala, lab, data_reserva, id)
            if conflito:
                return {'error': f'Sala já reservada para esta data: {conflito}'}, 400
        

        if 'num_sala' in data:
            reserva.num_sala = data['num_sala']
        if 'lab' in data:
            reserva.lab = data['lab']
        if 'data' in data:

            try:
                data_reserva = datetime.strptime(data['data'], '%Y-%m-%d').date()
                if data_reserva < datetime.now().date():
                    return {'error': 'Data da reserva deve ser futura'}, 400
            except ValueError:
                return {'error': 'Data da reserva inválida. Use formato YYYY-MM-DD'}, 400
            reserva.data = data['data']
        if 'turma_id' in data:

            if not ReservaService._validar_turma_existe(data['turma_id']):
                return {'error': 'Turma não encontrada no sistema'}, 400
            reserva.turma_id = data['turma_id']
        
        return reserva.to_dict(), 200
    
    @staticmethod
    def delete_reserva(id):
        global reservas_db
        original_len = len(reservas_db)
        reservas_db = [r for r in reservas_db if r.id != id]
        if len(reservas_db) == original_len:
            return {'error': 'Reserva não encontrada'}, 404
        return {'message': 'Reserva excluída com sucesso'}, 200
    

    
    @staticmethod
    def get_reservas_by_turma(turma_id):
        reservas_turma = [r for r in reservas_db if r.turma_id == turma_id]
        reservas_ordenadas = sorted(reservas_turma, key=lambda x: x.data)
        return [reserva.to_dict() for reserva in reservas_ordenadas], 200
    
    @staticmethod
    def get_reservas_by_sala(num_sala):
        reservas_sala = [r for r in reservas_db if r.num_sala == num_sala]
        reservas_ordenadas = sorted(reservas_sala, key=lambda x: x.data)
        return [reserva.to_dict() for reserva in reservas_ordenadas], 200
    
    @staticmethod
    def get_reservas_por_data(data):
        try:
            data_formatada = datetime.strptime(data, '%Y-%m-%d').date()
            reservas_data = [
                r for r in reservas_db 
                if datetime.strptime(r.data, '%Y-%m-%d').date() == data_formatada
            ]
            reservas_ordenadas = sorted(reservas_data, key=lambda x: x.num_sala)
            return [reserva.to_dict() for reserva in reservas_ordenadas], 200
        except ValueError:
            return {'error': 'Data inválida. Use o formato YYYY-MM-DD'}, 400

    
    @staticmethod
    def _verificar_conflito_reserva(num_sala, lab, data, reserva_id=None):
        for reserva in reservas_db:
            if reserva_id and reserva.id == reserva_id:
                continue
            
            if (reserva.num_sala == num_sala and 
                reserva.lab == lab and 
                reserva.data == data):
                return f"Reserva #{reserva.id} - Sala {reserva.num_sala} ({'Lab' if reserva.lab else 'Sala'})"
        return None