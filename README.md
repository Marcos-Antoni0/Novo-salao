# Sistema de Agendamento para Salão de Beleza

Este é um sistema web desenvolvido em Django para gerenciar agendamentos de um salão de beleza. O sistema permite o cadastro de clientes, profissionais, serviços e o controle completo da agenda de atendimentos.

## Funcionalidades

### Gestão de Clientes
- Cadastro, edição e exclusão de clientes
- Busca por nome, email ou telefone
- Paginação para melhor performance
- Controle de status (ativo/inativo)

### Gestão de Serviços e Categorias
- Cadastro de categorias de serviços
- Cadastro de serviços com preço e duração
- Vinculação de serviços às categorias
- Controle de status para categorias e serviços

### Gestão da Equipe
- Cadastro de profissionais
- Especialização por categoria (profissionais só podem executar serviços de sua especialidade)
- Controle de dados contratuais

### Sistema de Agendamentos
- Criação de agendamentos vinculando cliente, profissional e serviço
- Controle de status: Agendado, Em atendimento, Concluído, Cancelado
- Validação de compatibilidade entre profissional e serviço
- Visualização detalhada via modal
- Filtros por status e busca

### Dashboard e Relatórios
- Dashboard com gráfico de linha temporal dos serviços concluídos
- Filtros por período de data
- Estatísticas de performance
- Cards informativos na página inicial com dados do dia

### Página Inicial
- Cards com informações importantes do dia:
  - **Serviços do dia**: Total de agendamentos para hoje
  - **Pendentes**: Serviços ainda não finalizados hoje
  - **Finalizados**: Serviços concluídos hoje
  - **Vendas hoje**: Total de vendas realizadas hoje
- Ações rápidas para navegação
- Resumo dos agendamentos do dia

## Tecnologias Utilizadas

- **Python 3.11+**
- **Django 4.x**
- **SQLite** (banco de dados)
- **Bootstrap 5** (interface)
- **Chart.js** (gráficos)
- **Material Design Icons**

## Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

## Estrutura do Projeto

```
sistema-salao-beleza/
├── app/                    # Configurações principais do Django
├── core/                   # App principal (home, autenticação)
├── client/                 # Gestão de clientes
├── service/                # Gestão de serviços e categorias
├── team/                   # Gestão da equipe/profissionais
├── schedule/               # Sistema de agendamentos
├── dashboard/              # Dashboard e relatórios
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
├── templates/              # Templates base
├── manage.py              # Script de gerenciamento Django
└── requirements.txt       # Dependências do projeto
```

## Uso do Sistema

### Primeiro Acesso
1. Acesse `http://127.0.0.1:8000/`
2. Faça login com as credenciais criadas
3. Comece cadastrando categorias de serviços
4. Cadastre os serviços disponíveis
5. Cadastre os profissionais da equipe
6. Cadastre os clientes
7. Comece a criar agendamentos

### Navegação
- **Home**: Dashboard principal com informações do dia
- **Clientes**: Gestão completa de clientes
- **Serviços**: Gestão de categorias e serviços
- **Equipe**: Gestão de profissionais
- **Agenda**: Controle de agendamentos
- **Dashboard**: Relatórios e gráficos

## Características Técnicas

### Performance
- Uso de cache para consultas frequentes
- Paginação em todas as listagens
- Consultas otimizadas com `select_related`
- Validações no frontend e backend

### Segurança
- Autenticação obrigatória
- Proteção CSRF
- Validação de dados
- Controle de acesso por login

### Usabilidade
- Interface responsiva
- Busca em tempo real
- Modais para visualização rápida
- Feedback visual para ações
- Navegação intuitiva

## Regras de Negócio

1. **Profissionais e Especialidades**: Cada profissional possui uma especialidade (categoria) e só pode executar serviços dessa categoria.

2. **Status de Agendamentos**: 
   - Agendado: Agendamento criado
   - Em atendimento: Serviço sendo executado
   - Concluído: Serviço finalizado (gera receita)
   - Cancelado: Agendamento cancelado

3. **Validações**:
   - Não é possível agendar serviços com profissionais, clientes ou serviços inativos
   - Profissional deve ter especialidade compatível com a categoria do serviço

4. **Relatórios**: Apenas serviços com status "Concluído" são considerados para relatórios de performance e vendas.

## Contribuição

Este projeto foi desenvolvido como parte de um desafio técnico, seguindo as melhores práticas de desenvolvimento Django e priorizando:

- Código limpo e bem documentado
- Arquitetura escalável
- Performance otimizada
- Interface amigável
- Segurança


