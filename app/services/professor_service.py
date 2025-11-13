from app import db
from app.models.professor import Professor

class ProfessorService:
    @staticmethod
    def get_all_professores():
        """Retorna todos os professores ordenados por nome"""
        return Professor.query.order_by(Professor.nome).all()
    
    @staticmethod
    def get_professor_by_id(id):
        """Busca professor por ID, retorna 404 se não encontrado"""
        return Professor.query.get_or_404(id)
    
    @staticmethod
    def get_professores_por_materia(materia):
        """Retorna professores por matéria específica"""
        return Professor.query.filter_by(materia=materia).order_by(Professor.nome).all()
    
    @staticmethod
    def get_professores_com_turmas():
        """Retorna professores que possuem turmas atribuídas"""
        return Professor.query.filter(Professor.turmas.any()).order_by(Professor.nome).all()
    
    @staticmethod
    def create_professor(data):
        """Cria um novo professor"""
        professor = Professor(
            nome=data['nome'].strip(),
            idade=data['idade'],
            materia=data['materia'].strip(),
            observacoes=data.get('observacoes', '').strip()
        )
        db.session.add(professor)
        db.session.commit()
        return professor
    
    @staticmethod
    def update_professor(id, data):
        """Atualiza um professor existente"""
        professor = Professor.query.get_or_404(id)
        
        # Atualizar campos se fornecidos
        if 'nome' in data:
            professor.nome = data['nome'].strip()
        if 'idade' in data:
            professor.idade = data['idade']
        if 'materia' in data:
            professor.materia = data['materia'].strip()
        if 'observacoes' in data:
            professor.observacoes = data['observacoes'].strip()
        
        db.session.commit()
        return professor
    
    @staticmethod
    def delete_professor(id):
        """Exclui um professor (exclusão física)"""
        professor = Professor.query.get_or_404(id)
        
        # Verificar se o professor tem turmas atribuídas
        if professor.turmas:
            raise ValueError("Não é possível excluir professor com turmas atribuídas. Transfira as turmas primeiro.")
        
        db.session.delete(professor)
        db.session.commit()
        return professor
    
    @staticmethod
    def get_quantidade_turmas(professor_id):
        """Retorna a quantidade de turmas de um professor"""
        professor = Professor.query.get_or_404(professor_id)
        return len(professor.turmas) if professor.turmas else 0