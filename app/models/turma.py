from app import db

class Turma(db.Model):
    __tablename__ = 'turma'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    
    alunos = db.relationship('Aluno', backref='turma', lazy=True)
    
    def __repr__(self):
        return f'<Turma {self.descricao} (ID: {self.id})>'
    
    def to_dict(self):
        """Método para serializar o objeto Turma para JSON"""
        return {
            'id': self.id,
            'descricao': self.descricao,
            'professor_id': self.professor_id,
            'ativo': self.ativo,
            'quantidade_alunos': len(self.alunos) if self.alunos else 0,
            'alunos_ativos': len([aluno for aluno in self.alunos if aluno.ativo]) if self.alunos else 0
        }
    
    def alunos_ativos(self):
        """Retorna apenas os alunos ativos da turma"""
        return [aluno for aluno in self.alunos if aluno.ativo] if self.alunos else []
    
    def media_da_turma(self):
        """Calcula a média geral dos alunos ativos da turma"""
        alunos_ativos = self.alunos_ativos()
        if not alunos_ativos:
            return 0.0
        
        soma_medias = sum(aluno.media_final for aluno in alunos_ativos if aluno.media_final is not None)
        return round(soma_medias / len(alunos_ativos), 2)