from app import db
from app.models.aluno import Aluno
from datetime import datetime

class AlunoService:
    @staticmethod
    def get_all_alunos():
        """Retorna todos os alunos ordenados por nome"""
        return Aluno.query.order_by(Aluno.nome).all()
    
    @staticmethod
    def get_aluno_by_id(id):
        """Busca aluno por ID, retorna 404 se não encontrado"""
        return Aluno.query.get_or_404(id)
    
    @staticmethod
    def get_alunos_ativos():
        """Retorna apenas os alunos ativos"""
        return Aluno.query.filter_by(ativo=True).order_by(Aluno.nome).all()
    
    @staticmethod
    def get_alunos_por_turma(turma_id):
        """Retorna alunos de uma turma específica"""
        return Aluno.query.filter_by(turma_id=turma_id, ativo=True).order_by(Aluno.nome).all()
    
    @staticmethod
    def create_aluno(data):
        """Cria um novo aluno"""
        # Converter data_nascimento se for fornecida
        data_nascimento = None
        if data.get('data_nascimento'):
            try:
                data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Data de nascimento inválida. Use o formato YYYY-MM-DD")
        
        aluno = Aluno(
            nome=data['nome'].strip(),
            idade=data['idade'],
            turma_id=data['turma_id'],
            data_nascimento=data_nascimento,
            nota_primeiro_semestre=data.get('nota_primeiro_semestre', 0.0),
            nota_segundo_semestre=data.get('nota_segundo_semestre', 0.0),
            ativo=data.get('ativo', True)
        )
        db.session.add(aluno)
        db.session.commit()
        return aluno
    
    @staticmethod
    def update_aluno(id, data):
        """Atualiza um aluno existente"""
        aluno = Aluno.query.get_or_404(id)
        
        # Atualizar campos se fornecidos
        if 'nome' in data:
            aluno.nome = data['nome'].strip()
        if 'idade' in data:
            aluno.idade = data['idade']
        if 'turma_id' in data:
            aluno.turma_id = data['turma_id']
        if 'ativo' in data:
            aluno.ativo = data['ativo']
        if 'nota_primeiro_semestre' in data:
            aluno.nota_primeiro_semestre = data['nota_primeiro_semestre']
        if 'nota_segundo_semestre' in data:
            aluno.nota_segundo_semestre = data['nota_segundo_semestre']
        
        # Atualizar data_nascimento se for fornecida
        if data.get('data_nascimento'):
            try:
                aluno.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Data de nascimento inválida. Use o formato YYYY-MM-DD")
        
        db.session.commit()
        return aluno
    
    @staticmethod
    def delete_aluno(id):
        """Exclui um aluno (exclusão física)"""
        aluno = Aluno.query.get_or_404(id)
        db.session.delete(aluno)
        db.session.commit()
        return aluno
    
    @staticmethod
    def desativar_aluno(id):
        """Desativa um aluno (exclusão lógica)"""
        aluno = Aluno.query.get_or_404(id)
        aluno.ativo = False
        db.session.commit()
        return aluno