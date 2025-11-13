from datetime import datetime

class Atividade:
    def __init__(self, id, nome_atividade, descricao, peso_porcento, data_entrega, turma_id, professor_id, status="pendente"):
        self.id = id
        self.nome_atividade = nome_atividade.strip() if nome_atividade else nome_atividade
        self.descricao = descricao.strip() if descricao else descricao
        self.peso_porcento = peso_porcento
        self.data_entrega = data_entrega
        self.turma_id = turma_id
        self.professor_id = professor_id
        self.status = status
    
    def to_dict(self):
        """Serializa a atividade para dicionário"""
        return {
            'id': self.id,
            'nome_atividade': self.nome_atividade,
            'descricao': self.descricao,
            'peso_porcento': self.peso_porcento,
            'data_entrega': self.data_entrega,
            'turma_id': self.turma_id,
            'professor_id': self.professor_id,
            'status': self.status,
            'dias_para_entrega': self.calcular_dias_para_entrega()
        }
    
    def calcular_dias_para_entrega(self):
        """Calcula quantos dias faltam para a data de entrega"""
        try:
            data_entrega = datetime.strptime(self.data_entrega, '%Y-%m-%d').date()
            hoje = datetime.now().date()
            dias = (data_entrega - hoje).days
            return max(dias, 0)  # Não retorna valores negativos
        except (ValueError, TypeError):
            return None
    
    def esta_atrasada(self):
        """Verifica se a atividade está atrasada"""
        try:
            data_entrega = datetime.strptime(self.data_entrega, '%Y-%m-%d').date()
            hoje = datetime.now().date()
            return hoje > data_entrega and self.status in ['pendente', 'em_andamento']
        except (ValueError, TypeError):
            return False
    
    def __repr__(self):
        return f'<Atividade {self.nome_atividade} (ID: {self.id})>'

class Nota:
    def __init__(self, id, nota, aluno_id, atividade_id):
        self.id = id
        self.nota = max(0.0, min(nota, 10.0))  # Garante que a nota esteja entre 0 e 10
        self.aluno_id = aluno_id
        self.atividade_id = atividade_id
    
    def to_dict(self):
        """Serializa a nota para dicionário"""
        return {
            'id': self.id,
            'nota': self.nota,
            'aluno_id': self.aluno_id,
            'atividade_id': self.atividade_id,
            'conceito': self.obter_conceito()
        }
    
    def obter_conceito(self):
        """Retorna o conceito baseado na nota"""
        if self.nota >= 9.0:
            return "Excelente"
        elif self.nota >= 7.0:
            return "Bom"
        elif self.nota >= 5.0:
            return "Regular"
        else:
            return "Insuficiente"
    
    def esta_aprovado(self, nota_minima=5.0):
        """Verifica se o aluno foi aprovado na atividade"""
        return self.nota >= nota_minima
    
    def __repr__(self):
        return f'<Nota {self.nota} (Aluno: {self.aluno_id}, Atividade: {self.atividade_id})>'