from models.atividade import Atividade, Nota
from datetime import datetime
import requests

# Mock database
atividades_db = []
notas_db = []
current_id = 1
nota_current_id = 1

class AtividadeService:
    

    
    @staticmethod
    def get_all_atividades():
        """Retorna todas as atividades ordenadas por data de entrega"""
        atividades_ordenadas = sorted(atividades_db, key=lambda x: x.data_entrega)
        return [atividade.to_dict() for atividade in atividades_ordenadas], 200
    
    @staticmethod
    def get_atividade_by_id(id):
        """Busca atividade por ID"""
        atividade = next((a for a in atividades_db if a.id == id), None)
        if atividade:
            return atividade.to_dict(), 200
        return {'error': 'Atividade não encontrada'}, 404
    
    @staticmethod
    def get_atividades_por_professor(professor_id):
        """Retorna atividades de um professor específico"""
        atividades = [a for a in atividades_db if a.professor_id == professor_id]
        atividades_ordenadas = sorted(atividades, key=lambda x: x.data_entrega)
        return [atividade.to_dict() for atividade in atividades_ordenadas], 200
    
    @staticmethod
    def get_atividades_por_turma(turma_id):
        """Retorna atividades de uma turma específica"""
        atividades = [a for a in atividades_db if a.turma_id == turma_id]
        atividades_ordenadas = sorted(atividades, key=lambda x: x.data_entrega)
        return [atividade.to_dict() for atividade in atividades_ordenadas], 200
    
    @staticmethod
    def create_atividade(data):
        """Cria uma nova atividade"""
        global current_id
        
        # Validar dependências externas
        if not AtividadeService._validar_turma_existe(data['turma_id']):
            return {'error': 'Turma não encontrada no sistema'}, 400
        
        if not AtividadeService._validar_professor_existe(data['professor_id']):
            return {'error': 'Professor não encontrado no sistema'}, 400
        
        nova_atividade = Atividade(
            id=current_id,
            nome_atividade=data['nome_atividade'],
            descricao=data['descricao'],
            peso_porcento=data['peso_porcento'],
            data_entrega=data['data_entrega'],
            turma_id=data['turma_id'],
            professor_id=data['professor_id'],
            status=data.get('status', 'pendente')
        )
        atividades_db.append(nova_atividade)
        current_id += 1
        return nova_atividade.to_dict(), 201
    
    @staticmethod
    def update_atividade(id, data):
        """Atualiza uma atividade existente"""
        atividade = next((a for a in atividades_db if a.id == id), None)
        if not atividade:
            return {'error': 'Atividade não encontrada'}, 404
        
        # Atualizar campos se fornecidos
        if 'nome_atividade' in data:
            atividade.nome_atividade = data['nome_atividade']
        if 'descricao' in data:
            atividade.descricao = data['descricao']
        if 'peso_porcento' in data:
            atividade.peso_porcento = data['peso_porcento']
        if 'data_entrega' in data:
            atividade.data_entrega = data['data_entrega']
        if 'status' in data:
            atividade.status = data['status']
        if 'turma_id' in data:
            atividade.turma_id = data['turma_id']
        
        return atividade.to_dict(), 200
    
    @staticmethod
    def delete_atividade(id):
        """Exclui uma atividade e suas notas relacionadas"""
        global atividades_db, notas_db
        
        # Remover atividade
        atividade = next((a for a in atividades_db if a.id == id), None)
        if not atividade:
            return {'error': 'Atividade não encontrada'}, 404
        
        # Remover notas relacionadas à atividade
        notas_db = [n for n in notas_db if n.atividade_id != id]
        atividades_db = [a for a in atividades_db if a.id != id]
        
        return {'message': 'Atividade e notas relacionadas excluídas com sucesso'}, 200
    
    
    @staticmethod
    def get_notas_by_atividade(atividade_id):
        """Retorna todas as notas de uma atividade específica"""
        notas = [n for n in notas_db if n.atividade_id == atividade_id]
        notas_ordenadas = sorted(notas, key=lambda x: x.aluno_id)
        return [nota.to_dict() for nota in notas_ordenadas], 200
    
    @staticmethod
    def get_notas_by_aluno(aluno_id):
        """Retorna todas as notas de um aluno específico"""
        notas = [n for n in notas_db if n.aluno_id == aluno_id]
        notas_ordenadas = sorted(notas, key=lambda x: x.atividade_id)
        return [nota.to_dict() for nota in notas_ordenadas], 200
    
    @staticmethod
    def create_nota(data):
        """Cria uma nova nota"""
        global nota_current_id
        
        # Verificar se a atividade existe
        atividade = next((a for a in atividades_db if a.id == data['atividade_id']), None)
        if not atividade:
            return {'error': 'Atividade não encontrada'}, 404
        
        # Verificar se já existe nota para este aluno nesta atividade
        nota_existente = next((n for n in notas_db if n.aluno_id == data['aluno_id'] and n.atividade_id == data['atividade_id']), None)
        if nota_existente:
            return {'error': 'Já existe uma nota para este aluno nesta atividade'}, 400
        
        nova_nota = Nota(
            id=nota_current_id,
            nota=data['nota'],
            aluno_id=data['aluno_id'],
            atividade_id=data['atividade_id']
        )
        notas_db.append(nova_nota)
        nota_current_id += 1
        return nova_nota.to_dict(), 201
    
    @staticmethod
    def get_nota_by_id(id):
        """Busca nota por ID"""
        nota = next((n for n in notas_db if n.id == id), None)
        if nota:
            return nota.to_dict(), 200
        return {'error': 'Nota não encontrada'}, 404
    
    @staticmethod
    def update_nota(id, data):
        """Atualiza uma nota existente"""
        nota = next((n for n in notas_db if n.id == id), None)
        if not nota:
            return {'error': 'Nota não encontrada'}, 404
        
        if 'nota' in data:
            nota.nota = data['nota']
        
        return nota.to_dict(), 200
    
    @staticmethod
    def delete_nota(id):
        """Exclui uma nota"""
        global notas_db
        notas_db = [n for n in notas_db if n.id != id]
        return {'message': 'Nota excluída com sucesso'}, 200
    
    
    @staticmethod
    def _validar_turma_existe(turma_id):
        """Valida se a turma existe no microsserviço de Gerenciamento"""
        try:
            response = requests.get(f'http://app:5000/api/v1/turmas/{turma_id}', timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    @staticmethod
    def _validar_professor_existe(professor_id):
        """Valida se o professor existe no microsserviço de Gerenciamento"""
        try:
            response = requests.get(f'http://app:5000/api/v1/professores/{professor_id}', timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    @staticmethod
    def _validar_aluno_existe(aluno_id):
        """Valida se o aluno existe no microsserviço de Gerenciamento"""
        try:
            response = requests.get(f'http://app:5000/api/v1/alunos/{aluno_id}', timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False