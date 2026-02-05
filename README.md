# Simulador de Vendas com IA

Sistema de treinamento de vendas usando IA que simula um comprador realista e fornece feedback detalhado.

## 🚀 Funcionalidades

- **Modo Real**: Usa GPT-4o-mini da OpenAI para conversas realistas
- **Modo Teste**: Simulações GRATUITAS sem necessidade de API
- **Gravação de Áudio**: Grave sua fala ao invés de digitar (usa Whisper para transcrição)
- **Feedback Detalhado**: Receba avaliação completa do seu processo de venda
- **Histórico de Contexto**: A IA lembra toda a conversa

## 📋 Pré-requisitos

- Python 3.8+
- Chave de API da OpenAI (apenas para modo real)

## 🔧 Instalação

1. **Clone ou baixe o projeto**

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

**Nota:** No Windows, o `sounddevice` pode precisar de configuração adicional. Se tiver problemas, instale:
```bash
pip install sounddevice --upgrade
```

3. **Configure a chave da OpenAI (apenas para modo real):**

Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY="sua-chave-aqui"
```

Linux/Mac:
```bash
export OPENAI_API_KEY="sua-chave-aqui"
```

## 🎯 Como Usar

Execute o simulador:
```bash
python main.py
```

### Opções durante a conversa:

- **Digite normalmente**: Sua mensagem de vendas
- **Digite "VOZ"**: Grava um áudio e transcreve automaticamente
- **Digite "FEEDBACK"**: Recebe avaliação completa do processo

### Exemplo de uso com áudio:

```
Você (vendedor): VOZ
Preparando gravação...
Duração da gravação em segundos (padrão 5): 7
🎤 Gravando por 7 segundos...
✓ Gravação concluída!
📝 Transcrevendo áudio...
✓ Transcrição concluída!

📝 Transcrição: "Olá! Como posso ajudá-lo hoje?"

Comprador: Olá! Estou buscando uma solução para...
```

## 📁 Estrutura do Projeto

```
projeto-ia/
├── agent.py              # Classe principal de conversa (API real)
├── agent_mock.py         # Classe simulada (gratuita)
├── audio_recorder.py     # Gravação e transcrição de áudio
├── main.py              # Interface principal
└── requirements.txt     # Dependências
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

**Erro de microfone no Windows:**
- Verifique se o microfone está conectado e habilitado nas configurações do Windows
- Execute: `pip install sounddevice --upgrade`

**Erro de API OpenAI:**
- Verifique se a variável de ambiente `OPENAI_API_KEY` está configurada
- Use o Modo Teste (opção 2) para treinar sem custos

**Erro de transcrição:**
- O Whisper precisa de áudio claro
- Fale próximo ao microfone
- Evite ambientes ruidosos

## 💰 Custos

- **Modo Teste**: Gratuito (respostas simuladas)
- **Modo Real**: 
  - GPT-4o-mini: ~$0.15 / 1M tokens de entrada, ~$0.60 / 1M tokens de saída
  - Whisper: ~$0.006 / minuto de áudio

## 📝 Licença

Projeto educacional para treinamento de vendas.
