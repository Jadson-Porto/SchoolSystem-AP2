from datetime import datetime

class Reserva:
    def __init__(self, id, num_sala, lab, data, turma_id, status="ativa"):
        self.id = id
        self.num_sala = num_sala
        self.lab = lab
        self.data = data
        self.turma_id = turma_id
        self.status = status
    
    def to_dict(self):
        return {
            'id': self.id,
            'num_sala': self.num_sala,
            'lab': self.lab,
            'data': self.data,
            'turma_id': self.turma_id,
            'status': self.status,
            'dias_para_reserva': self._calcular_dias_para_reserva()
        }
    
    def _calcular_dias_para_reserva(self):
        try:
            data_reserva = datetime.strptime(self.data, '%Y-%m-%d').date()
            hoje = datetime.now().date()
            return (data_reserva - hoje).days
        except ValueError:
            return None