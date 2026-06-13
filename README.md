# Simulador de Vendas com IA

Sistema de treinamento de vendas usando IA que simula um comprador realista e fornece feedback detalhado através de uma interface web moderna.

## 🚀 Funcionalidades

- **Interface Web Moderna**: Aplicação Streamlit com interface intuitiva
- **Modo Real**: Usa GPT-4o-mini da OpenAI para conversas realistas
- **Modo Teste**: Simulações GRATUITAS sem necessidade de API
- **Feedback Detalhado**: Receba avaliação completa do seu processo de venda
- **Histórico de Contexto**: A IA lembra toda a conversa durante a sessão
- **Visualização de Conversas**: Acompanhe histórico completo de todas as sessões
- **Armazenamento de Dados**: Sistema de persistência em CSV para análise posterior

## 📋 Pré-requisitos

- Python 3.8+
- Chave de API da OpenAI (apenas para modo real)

## 🔧 Instalação

1. **Clone ou baixe o projeto**

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Configure a chave da OpenAI (apenas para modo real):**

Crie um arquivo `.env` na pasta raiz do projeto:
```env
OPEN=sua-chave-api-aqui
```

**Alternativa:** Use variáveis de ambiente:

Windows (PowerShell):
```powershell
$env:OPEN="sua-chave-aqui"
```

Linux/Mac:
```bash
export OPEN="sua-chave-aqui"
```

## 🎯 Como Usar

Execute o simulador:
```bash
streamlit run Conversation.py
```

A aplicação abrirá automaticamente no seu navegador (geralmente em `http://localhost:8501`).

### Opções na interface web:

1. **Sidebar (Configurações):**
   - **Modo Teste**: Respostas simuladas gratuitas
   - **Modo Real**: Usa API da OpenAI (requer configuração)
   - **Nova Conversa**: Reinicia a sessão de treinamento

2. **Chat Principal:**
   - Digite suas mensagens de venda normalmente
   - **Digite "FEEDBACK"**: Recebe avaliação completa do processo
   - **Visualizar Conversas**: Acesse o histórico na sidebar

### Navegação:

- **Página Principal**: Simulador de vendas interativo
- **Visualizar Conversas**: Histórico completo de todas as sessões com métricas

## 📁 Estrutura do Projeto

```
sales-simulator/
├── Conversation.py           # Interface principal Streamlit
├── agent.py                  # Classe de conversa com API OpenAI
├── agent_mock.py            # Classe simulada (modo gratuito)
├── csv_reader.py            # Gerenciador de dados CSV
├── requirements.txt         # Dependências do projeto
├── data/
│   └── dados.csv           # Armazenamento das conversas
└── pages/
    └── Show_Conversations.py # Visualização do histórico
```

## 🎓 Dicas de Treinamento

O comprador IA foi programado para:
- Demonstrar interesse inicial com reservas
- Fazer perguntas sobre características e benefícios
- Apresentar objeções realistas (preço, urgência, concorrência)
- Avaliar suas técnicas de vendas
- Fornecer feedback estruturado

**Pratique:**
- Rapport e conexão inicial
- Perguntas de descoberta
- Apresentação de benefícios (não apenas características)
- Tratamento de objeções
- Fechamento com call-to-action

## 🐛 Solução de Problemas

**Erro ao iniciar o Streamlit:**
- Verifique se todas as dependências foram instaladas: `pip install -r requirements.txt`
- Certifique-se de estar na pasta correta do projeto

**Erro de API OpenAI (Modo Real):**
- Verifique se a variável de ambiente `OPEN` está configurada no arquivo `.env`
- Use o Modo Teste para treinar sem custos
- Confirme se sua chave API está válida e tem créditos

**Erro de carregamento de dados:**
- O arquivo `dados.csv` será criado automaticamente na pasta `data/`
- Verifique se o usuário tem permissões de escrita na pasta do projeto

**Interface não abre no navegador:**
- Acesse manualmente: `http://localhost:8501`
- Verifique se a porta 8501 não está sendo usada por outra aplicação

## 💰 Custos

- **Modo Teste**: Gratuito (respostas simuladas)
- **Modo Real**: 
  - GPT-4o-mini: ~$0.15 / 1M tokens de entrada, ~$0.60 / 1M tokens de saída
  - Custo típico por sessão de treinamento: $0.01 - $0.05

## ℹ️ Funcionalidades

### Sistema de Feedback Inteligente
O comprador IA avalia automaticamente:
- Rapport e conexão inicial
- Identificação de necessidades
- Apresentação de benefícios
- Tratamento de objeções
- Técnicas de fechamento
- Comunicação geral

### Armazenamento de Dados
- Todas as conversas são salvas automaticamente
- Métricas de uso de tokens e custos (modo real)
- Histórico completo acessível na interface web

## 📝 Licença

Projeto educacional para treinamento de vendas.

## 🔮 Próximas Funcionalidades

Funcionalidades planejadas para futuras versões:
- Gravação e transcrição de áudio com Whisper
- Dashboard analítico com métricas de performance
- Múltiplos personas de compradores
- Integração com CRM
- Relatórios detalhados de progresso

---

*Desenvolvido para aprimorar técnicas de vendas através de simulações realistas com IA*
