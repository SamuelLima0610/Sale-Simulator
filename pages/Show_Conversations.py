import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Visualizar Conversas",
    page_icon="📋",
    layout="wide"
)

# ===== FUNÇÕES AUXILIARES =====
def carregar_conversas():
    """Carrega as conversas do arquivo CSV"""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dados.csv')
    if not os.path.exists(csv_path):
        return None
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return None

def formatar_data(data_str):
    """Formata a data para exibição"""
    try:
        dt = datetime.fromisoformat(data_str)
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except:
        return data_str

def deletar_conversa(conversation_id):
    """Deleta uma conversa específica do arquivo CSV"""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dados.csv')
    
    try:
        # Carregar dados atuais
        df = pd.read_csv(csv_path)
        
        # Filtrar dados removendo a conversa específica
        df_filtrado = df[df['conversation_id'] != conversation_id]
        
        # Salvar arquivo atualizado
        df_filtrado.to_csv(csv_path, index=False)
        
        return True, f"Conversa {conversation_id} deletada com sucesso!"
    except Exception as e:
        return False, f"Erro ao deletar conversa: {str(e)}"

def obter_resumo_conversas(df):
    """Obtém um resumo de todas as conversas"""
    # Obter primeira mensagem de cada conversa
    primeira_mensagem = df.groupby('conversation_id')['message'].first().reset_index()
    primeira_mensagem.columns = ['conversation_id', 'primeira_mensagem']
    
    resumo = df.groupby('conversation_id').agg({
        'data': 'first',
        'message': 'count',
        'total_tokens': 'sum',
        'input_cost_usd': 'sum',
        'output_cost_usd': 'sum'
    }).reset_index()
    
    # Juntar com primeira mensagem
    resumo = resumo.merge(primeira_mensagem, on='conversation_id')
    
    resumo.columns = ['conversation_id', 'Data', 'Num. Mensagens', 'Total Tokens', 'Custo Input (USD)', 'Custo Output (USD)', 'Primeira Mensagem']
    resumo['Custo Total (USD)'] = resumo['Custo Input (USD)'] + resumo['Custo Output (USD)']
    resumo['Data'] = resumo['Data'].apply(formatar_data)
    
    # Truncar primeira mensagem se muito longa
    resumo['Primeira Mensagem'] = resumo['Primeira Mensagem'].apply(
        lambda x: x[:100] + '...' if len(x) > 100 else x
    )
    
    return resumo

def exibir_conversa(df, conversation_id):
    """Exibe as mensagens de uma conversa específica"""
    conversa = df[df['conversation_id'] == conversation_id].sort_index()
    
    # Cabeçalho com título e botão de deletar
    col_titulo, col_deletar = st.columns([3, 1])
    with col_titulo:
        st.subheader(f"Conversa: {conversation_id}")
    with col_deletar:
        if st.button("🗑️ Deletar Conversa", key=f"delete_single_{conversation_id}", type="secondary"):
            st.session_state.conversa_para_deletar = conversation_id
            st.rerun()
    
    # Informações da conversa
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Mensagens", len(conversa))
    with col2:
        st.metric("Total Tokens", int(conversa['total_tokens'].sum()))
    with col3:
        custo_total = conversa['input_cost_usd'].sum() + conversa['output_cost_usd'].sum()
        st.metric("Custo Total", f"${custo_total:.6f}")
    with col4:
        data_primeira = conversa['data'].iloc[0]
        st.metric("Data", formatar_data(data_primeira))
    
    st.markdown("---")
    
    # Exibir mensagens
    st.subheader("📝 Histórico de Mensagens")
    
    for idx, row in conversa.iterrows():
        # Mensagem do vendedor (usuário)
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**Vendedor:**")
            st.markdown(row['message'])
        
        # Resposta do comprador (assistente)
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(f"**Comprador:**")
            st.markdown(row['response'])
        
        # Informações técnicas (expansível)
        with st.expander(f"ℹ️ Detalhes técnicos da mensagem #{idx+1}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Tokens:** {int(row['total_tokens'])}")
            with col2:
                st.write(f"**Custo Input:** ${row['input_cost_usd']:.6f}")
            with col3:
                st.write(f"**Custo Output:** ${row['output_cost_usd']:.6f}")

# ===== INTERFACE PRINCIPAL =====
st.title("💬 Visualizador de Conversas de Vendas")
st.markdown("---")

# Inicializar session state para controle da exclusão
if 'dados_atualizados' not in st.session_state:
    st.session_state.dados_atualizados = False

df = carregar_conversas()

if df is not None and not df.empty:
    # Criar abas
    tab1, tab2 = st.tabs(["📋 Lista de Conversas", "💬 Visualizar Conversa"])
    
    with tab1:
        st.subheader("Todas as Conversas Salvas")
        
        # Obter resumo
        resumo = obter_resumo_conversas(df)
        
        # Exibir estatísticas gerais
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Conversas", len(resumo))
        with col2:
            st.metric("Total de Mensagens", int(resumo['Num. Mensagens'].sum()))
        with col3:
            st.metric("Custo Total Acumulado", f"${resumo['Custo Total (USD)'].sum():.6f}")
        
        st.markdown("---")
        
        # Cabeçalho da tabela
        header_cols = st.columns([2, 1.5, 1, 1, 1.2, 2.5, 2])
        with header_cols[0]:
            st.markdown("**ID da Conversa**")
        with header_cols[1]:
            st.markdown("**Data**")
        with header_cols[2]:
            st.markdown("**Mensagens**")
        with header_cols[3]:
            st.markdown("**Tokens**")
        with header_cols[4]:
            st.markdown("**Custo Total**")
        with header_cols[5]:
            st.markdown("**Primeira Mensagem**")
        with header_cols[6]:
            st.markdown("**Ações**")
        
        st.markdown("---")
        
        # Modal de confirmação para deletar conversa
        if 'conversa_para_deletar' in st.session_state:
            conversa_id = st.session_state.conversa_para_deletar
            
            st.warning(f"⚠️ **Confirmação de Exclusão**")
            st.write(f"Tem certeza que deseja deletar a conversa **{conversa_id}**?")
            st.write("Esta ação não pode ser desfeita e todas as mensagens da conversa serão removidas permanentemente.")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("✅ Confirmar", type="primary"):
                    sucesso, mensagem = deletar_conversa(conversa_id)
                    if sucesso:
                        st.success(mensagem)
                        # Limpar session state e marcar dados como atualizados
                        del st.session_state.conversa_para_deletar
                        st.session_state.dados_atualizados = True
                        st.rerun()
                    else:
                        st.error(mensagem)
            
            with col2:
                if st.button("❌ Cancelar"):
                    del st.session_state.conversa_para_deletar
                    st.rerun()
            
            st.markdown("---")
        
        # Exibir cada conversa com botões
        for idx, row in resumo.iterrows():
            cols = st.columns([2, 1.5, 1, 1, 1.2, 2.5, 2])
            
            with cols[0]:
                st.text(row['conversation_id'])
            with cols[1]:
                st.text(row['Data'])
            with cols[2]:
                st.text(str(int(row['Num. Mensagens'])))
            with cols[3]:
                st.text(str(int(row['Total Tokens'])))
            with cols[4]:
                st.text(f"${row['Custo Total (USD)']:.6f}")
            with cols[5]:
                st.text(row['Primeira Mensagem'])
            with cols[6]:
                # Criar duas colunas para os botões
                btn_cols = st.columns(2)
                with btn_cols[0]:
                    if st.button("🔄 Simular", key=f"btn_simular_{row['conversation_id']}"):
                        # Carregar conversa no simulador (página principal)
                        st.session_state.conversation_id = row['conversation_id']
                        st.session_state.initialized = False
                        st.session_state.chat_history = []
                        st.session_state.feedback_received = False
                        st.switch_page("Conversation.py")
                
                with btn_cols[1]:
                    if st.button("🗑️ Deletar", key=f"btn_deletar_{row['conversation_id']}", type="secondary"):
                        # Armazenar ID da conversa para confirmar exclusão
                        st.session_state.conversa_para_deletar = row['conversation_id']
                        st.rerun()
            
            st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Selecione uma Conversa")
        
        # Modal de confirmação para deletar conversa (também na aba 2)
        if 'conversa_para_deletar' in st.session_state:
            conversa_id = st.session_state.conversa_para_deletar
            
            st.warning(f"⚠️ **Confirmação de Exclusão**")
            st.write(f"Tem certeza que deseja deletar a conversa **{conversa_id}**?")
            st.write("Esta ação não pode ser desfeita e todas as mensagens da conversa serão removidas permanentemente.")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("✅ Confirmar", type="primary", key="confirm_tab2"):
                    sucesso, mensagem = deletar_conversa(conversa_id)
                    if sucesso:
                        st.success(mensagem)
                        # Limpar session state e marcar dados como atualizados
                        del st.session_state.conversa_para_deletar
                        st.session_state.dados_atualizados = True
                        st.rerun()
                    else:
                        st.error(mensagem)
            
            with col2:
                if st.button("❌ Cancelar", key="cancel_tab2"):
                    del st.session_state.conversa_para_deletar
                    st.rerun()
            
            st.markdown("---")
        
        # Lista de IDs de conversas
        conversation_ids = df['conversation_id'].unique().tolist()
        conversation_ids.sort(reverse=True)  # Mais recentes primeiro
        
        # Selectbox para escolher a conversa
        selected_id = st.selectbox(
            "Escolha o ID da conversa:",
            options=conversation_ids,
            format_func=lambda x: f"{x} ({formatar_data(df[df['conversation_id']==x]['data'].iloc[0])})"
        )
        
        if selected_id:
            st.markdown("---")
            exibir_conversa(df, selected_id)

else:
    st.warning("⚠️ Nenhuma conversa encontrada no arquivo dados.csv")
    st.info("Execute o simulador de vendas primeiro para gerar conversas.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        💼 Simulador de Vendas - Visualizador de Conversas
    </div>
    """,
    unsafe_allow_html=True
)
