### Orientação teórica
Professor: Giovani Bontempo

### Integrantes do Projeto
Jadson Porto

Michael L. Ramos

Tabatha Paola

### Sobre o Projeto
A SCHOOL API é uma solução completa para gestão escolar baseada em microsserviços que permite:

### 🎯 Microsserviço App (Porta 5000)
- Cadastro e gerenciamento de Alunos, Professores e Turmas
- Cálculo automático de médias dos alunos
- Relacionamentos entre entidades
---------------------------------------------> http://localhost:5000/docs/

### 📅 Microsserviço Reservas (Porta 5001)
- Reservas de recursos escolares (laboratórios, salas, etc).
- Controle de conflitos de agendamento.
- Status de reservas (ativa, cancelada, concluída).
---------------------------------------------> http://localhost:5001/docs/

### 📚 Microsserviço Atividades (Porta 5002)
- Gerenciamento de Atividades e Notas.
- Cálculo de médias por aluno e por atividade.
- Controle de prazos e status.
---------------------------------------------> http://localhost:5002/docs/


### 🏗️ Arquitetura
O comando docker-compose up -d --build é essencial para que outros desenvolvedores possam executar sua aplicação facilmente.

### Baixar as dependencias e ligar o Docker Desktop

- 1º: pip install -r requirements.txt
- 2º: docker-compose logs -f  [só se for necessário]
- 3º: docker-compose up -d --build  [caso precise]
- 4º: docker-compose up --build [ou pode usar este]

### EXTRA ###

- Para gerar um relatório de criação de todo o conteúdo siga o passo a passo:

- Execute o arquivo "script.py", ele irá coletar todo o conteúdo existente nos Endpoints online e criará um relatório completo com todas as informações necessárias para facilitar leitura.

- Instale a extensão "vscode-pdf" para fazer a leitura do arquivo PDF criado dentro do VSCODE ou abra a pasta origem do projeto e abra o arquivo PDF que foi gerado com o script.