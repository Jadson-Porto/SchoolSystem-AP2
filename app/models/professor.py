from app import db

class Professor(db.Model):
    __tablename__ = 'professor'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.Text)
    
    turmas = db.relationship('Turma', backref='professor', lazy=True)
    
    def __repr__(self):
        return f'<Professor {self.nome} (ID: {self.id})>'
    
    def to_dict(self):
        """Método para serializar o objeto Professor para JSON"""
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'materia': self.materia,
            'observacoes': self.observacoes,
            'quantidade_turmas': len(self.turmas) if self.turmas else 0
        }
    
    def turmas_ativas(self):
        """Retorna apenas as turmas ativas do professor"""
        return [turma for turma in self.turmas if turma.ativo] if self.turmas else []