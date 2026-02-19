import streamlit as st
from agent import ConversationContext
from agent_mock import MockConversationContext

# System message otimizado para simular um comprador realista
SYSTEM_MESSAGE = """
Você é um comprador potencial interessado em avaliar produtos ou serviços. Seu papel é participar de uma simulação de venda realista.

## SEU PERFIL E COMPORTAMENTO:
- Você é um comprador criterioso, mas aberto a ofertas convincentes
- Tem necessidades e dúvidas genuínas sobre o produto/serviço
- Seu orçamento é limitado, mas está disposto a investir se ver valor
- Faz perguntas relevantes sobre características, benefícios, preço e condições
- Apresenta objeções realistas quando apropriado (preço, concorrência, necessidade, urgência)
- Responde de forma natural e conversacional, como um cliente real
- Sua decisão de compra depende de quão bem o vendedor atende suas necessidades
- Só fornece feedback quando solicitado explicitamente (digitando "FEEDBACK")

## DURANTE A CONVERSA:
1. Comece demonstrando interesse inicial, mas com reservas
2. Faça perguntas sobre características, benefícios e diferenciais
3. Apresente 2-3 objeções ao longo da conversa (escolha entre: preço alto, falta de urgência, comparação com concorrentes, dúvidas sobre ROI)
4. Avalie como o vendedor lida com suas objeções
5. Observe se o vendedor: escuta ativamente, identifica suas necessidades, apresenta soluções, cria rapport, usa técnicas de vendas
6. Mantenha o tom realista - nem muito fácil nem impossível de convencer

## QUANDO O VENDEDOR PEDIR FEEDBACK:
Forneça uma análise estruturada em português com as seguintes seções:

**PONTOS FORTES:**
- Liste 3-4 aspectos positivos específicos do processo de venda

**PONTOS DE MELHORIA:**
- Identifique 2-3 áreas que podem ser aprimoradas

**AVALIAÇÃO POR CRITÉRIO (nota de 0 a 10):**
- Rapport e conexão inicial
- Identificação de necessidades (perguntas de descoberta)
- Apresentação de benefícios (não apenas características)
- Tratamento de objeções
- Fechamento e call-to-action
- Comunicação geral

**NOTA GERAL:** X/10

**RECOMENDAÇÕES ESPECÍFICAS:**
- Dê 2-3 sugestões práticas e acionáveis

Seja construtivo, específico e baseie seu feedback em exemplos concretos da conversa.
"""

# Configuração da página
st.set_page_config(
    page_title="Simulador de Vendas - Treinamento",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar session_state
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.conversation = None
    st.session_state.chat_history = []
    st.session_state.use_mock = True
    st.session_state.conversation_id = None
    st.session_state.feedback_received = False

# Sidebar - Configurações
with st.sidebar:
    st.title("⚙️ Configurações")
    
    st.markdown("---")
    
    # Modo de operação
    mode = st.radio(
        "Modo de Operação:",
        ["Modo Teste (Gratuito)", "Modo Real (OpenAI API)"],
        index=0 if st.session_state.use_mock else 1
    )
    
    st.session_state.use_mock = (mode == "Modo Teste (Gratuito)")
    
    if st.session_state.use_mock:
        st.info("🧪 Modo TESTE ativo\n\nSem custo, respostas simuladas")
    else:
        st.warning("🔴 Modo REAL ativo\n\nRequer créditos OpenAI")
    
    st.markdown("---")
    
    # (Removido) Interface para carregar conversa anterior por ID
    
    if st.button("🔄 Nova Conversa", use_container_width=True):
        st.session_state.initialized = False
        st.session_state.conversation = None
        st.session_state.chat_history = []
        st.session_state.conversation_id = None
        st.session_state.feedback_received = False
        st.rerun()
    
    st.markdown("---")
    
    # Informações da sessão
    if st.session_state.initialized and st.session_state.conversation:
        st.subheader("📊 Informações")
        st.text(f"ID: {st.session_state.conversation.conversation_id}")
        st.text(f"Mensagens: {len(st.session_state.chat_history)}")
        
        if not st.session_state.use_mock and hasattr(st.session_state.conversation, 'total_tokens_used'):
            st.text(f"Tokens: {st.session_state.conversation.total_tokens_used}")
            st.text(f"Custo: ${st.session_state.conversation.total_cost:.4f}")

# Inicializar conversa
if not st.session_state.initialized:
    if st.session_state.use_mock:
        st.session_state.conversation = MockConversationContext(
            model="gpt-4o-mini",
            system_message=SYSTEM_MESSAGE if not st.session_state.conversation_id else None,
            conversation_id=st.session_state.conversation_id
        )
    else:
        st.session_state.conversation = ConversationContext(
            model="gpt-4o-mini",
            system_message=SYSTEM_MESSAGE if not st.session_state.conversation_id else None,
            conversation_id=st.session_state.conversation_id
        )
    
    # Carregar histórico de chat se conversa anterior foi carregada
    if st.session_state.conversation_id:
        # Extrair mensagens do histórico (excluindo system message)
        loaded_count = 0
        for msg in st.session_state.conversation.messages:
            if msg["role"] == "system":
                continue
            st.session_state.chat_history.append({
                "role": msg["role"],
                "content": msg["content"]
            })
            loaded_count += 1
        
        # Verificar se realmente carregou mensagens
        if loaded_count == 0:
            st.warning(f"⚠️ Nenhuma conversa encontrada para o ID: {st.session_state.conversation_id}")
            st.session_state.conversation_id = None
    
    st.session_state.initialized = True

# ===== INTERFACE PRINCIPAL DO SIMULADOR =====
# Header principal
st.title("💼 Simulador de Vendas - Treinamento")
st.markdown("**Você é o VENDEDOR.** O comprador está esperando sua apresentação.")

# Mostrar aviso se conversa foi carregada
if st.session_state.conversation_id and len(st.session_state.chat_history) > 0:
    st.info(f"📂 Conversa carregada: {st.session_state.conversation_id} ({len(st.session_state.chat_history)} mensagens)")

# Área de chat
st.markdown("---")
st.subheader("💬 Conversa")

# Exibir histórico de mensagens
chat_container = st.container()
with chat_container:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**Você (vendedor):** {msg['content']}")
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f"**Comprador:** {msg['content']}")

# Input área
st.markdown("---")

if not st.session_state.feedback_received:
    col1, col2, col3 = st.columns([6, 2, 2])
    
    with col1:
        user_input = st.text_input(
            "Sua mensagem:",
            key="user_input",
            placeholder="Digite sua mensagem aqui...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("📤 Enviar", use_container_width=True)
    
    with col3:
        feedback_button = st.button("📊 Solicitar Feedback", use_container_width=True)
    
    # Processar envio de mensagem
    if send_button and user_input.strip():
        with st.spinner("Aguardando resposta..."):
            # Adicionar mensagem do usuário ao histórico
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Obter resposta do comprador
            response = st.session_state.conversation.send_message(user_input)
            
            # Adicionar resposta ao histórico
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
        
        st.rerun()
    
    # Processar solicitação de feedback
    if feedback_button:
        with st.spinner("Solicitando feedback detalhado..."):
            feedback = st.session_state.conversation.send_message(
                "Por favor, forneça agora o feedback detalhado sobre o meu processo de venda."
            )
            
            st.session_state.chat_history.append({
                "role": "user",
                "content": "FEEDBACK"
            })
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": feedback
            })
            
            st.session_state.feedback_received = True
        
        st.rerun()

else:
    st.success("✅ Feedback recebido! Inicie uma nova conversa para treinar novamente.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "💡 Navegue para 'Visualizar Conversas' na barra lateral para ver seu histórico"
    "</div>",
    unsafe_allow_html=True
)
