from app import db
from app.models.turma import Turma
from app.models.professor import Professor  # IMPORTAR O MODELO PROFESSOR

class TurmaService:
    @staticmethod
    def get_all_turmas():
        """Retorna todas as turmas ordenadas por descrição"""
        return Turma.query.order_by(Turma.descricao).all()
    
    @staticmethod
    def get_turma_by_id(id):
        """Busca turma por ID, retorna 404 se não encontrada"""
        return Turma.query.get_or_404(id)
    
    @staticmethod
    def get_turmas_ativas():
        """Retorna apenas as turmas ativas"""
        return Turma.query.filter_by(ativo=True).order_by(Turma.descricao).all()
    
    @staticmethod
    def get_turmas_por_professor(professor_id):
        """Retorna turmas de um professor específico"""
        return Turma.query.filter_by(professor_id=professor_id).order_by(Turma.descricao).all()
    
    @staticmethod
    def get_turmas_ativas_por_professor(professor_id):
        """Retorna turmas ativas de um professor específico"""
        return Turma.query.filter_by(professor_id=professor_id, ativo=True).order_by(Turma.descricao).all()
    
    @staticmethod
    def create_turma(data):
        """Cria uma nova turma"""
        # VALIDAÇÃO: Verificar se o professor existe
        professor = Professor.query.get(data['professor_id'])
        if not professor:
            raise ValueError("Professor não encontrado")
        
        turma = Turma(
            descricao=data['descricao'].strip(),
            professor_id=data['professor_id'],
            ativo=data.get('ativo', True)
        )
        db.session.add(turma)
        db.session.commit()
        return turma
    
    @staticmethod
    def update_turma(id, data):
        """Atualiza uma turma existente"""
        turma = Turma.query.get_or_404(id)
        
        # VALIDAÇÃO: Se estiver atualizando o professor_id, verificar se existe
        if 'professor_id' in data:
            professor = Professor.query.get(data['professor_id'])
            if not professor:
                raise ValueError("Professor não encontrado")
            turma.professor_id = data['professor_id']
        
        # Atualizar campos se fornecidos
        if 'descricao' in data:
            turma.descricao = data['descricao'].strip()
        if 'ativo' in data:
            turma.ativo = data['ativo']
        
        db.session.commit()
        return turma
    
    @staticmethod
    def delete_turma(id):
        """Exclui uma turma (exclusão física)"""
        turma = Turma.query.get_or_404(id)
        
        # Verificar se a turma tem alunos matriculados
        if turma.alunos:
            raise ValueError("Não é possível excluir turma com alunos matriculados. Transfira os alunos primeiro.")
        
        db.session.delete(turma)
        db.session.commit()
        return turma
    
    @staticmethod
    def desativar_turma(id):
        """Desativa uma turma (exclusão lógica)"""
        turma = Turma.query.get_or_404(id)
        turma.ativo = False
        db.session.commit()
        return turma
    
    @staticmethod
    def ativar_turma(id):
        """Ativa uma turma"""
        turma = Turma.query.get_or_404(id)
        turma.ativo = True
        db.session.commit()
        return turma
    
    @staticmethod
    def get_quantidade_alunos(turma_id):
        """Retorna a quantidade de alunos em uma turma"""
        turma = Turma.query.get_or_404(turma_id)
        return len(turma.alunos) if turma.alunos else 0
    
    @staticmethod
    def get_quantidade_alunos_ativos(turma_id):
        """Retorna a quantidade de alunos ativos em uma turma"""
        turma = Turma.query.get_or_404(turma_id)
        alunos_ativos = [aluno for aluno in turma.alunos if aluno.ativo] if turma.alunos else []
        return len(alunos_ativos) 