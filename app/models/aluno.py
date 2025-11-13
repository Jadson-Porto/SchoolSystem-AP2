from app import db
from sqlalchemy import event
from datetime import datetime

class Aluno(db.Model):
    __tablename__ = 'aluno'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=True)
    nota_primeiro_semestre = db.Column(db.Float, default=0.0)
    nota_segundo_semestre = db.Column(db.Float, default=0.0)
    media_final = db.Column(db.Float, default=0.0)
    ativo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Aluno {self.nome} (ID: {self.id})>'
    
    def to_dict(self):
        """Método para serializar o objeto Aluno para JSON"""
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'turma_id': self.turma_id,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'nota_primeiro_semestre': self.nota_primeiro_semestre,
            'nota_segundo_semestre': self.nota_segundo_semestre,
            'media_final': self.media_final,
            'ativo': self.ativo
        }

@event.listens_for(Aluno, 'before_update')
@event.listens_for(Aluno, 'before_insert')
def calcular_media(mapper, connection, target):
    """Calcula a média final automaticamente quando as notas são inseridas ou atualizadas"""
    if target.nota_primeiro_semestre is not None and target.nota_segundo_semestre is not None:
        target.media_final = (target.nota_primeiro_semestre + target.nota_segundo_semestre) / 2
    else:
        target.media_final = 0.0