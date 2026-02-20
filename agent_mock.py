"""
Versão mock da classe ConversationContext para testes sem créditos da OpenAI
"""
import random
import os
from csv_reader import GerenciadorCSV


class MockConversationContext:
    """Versão simulada que não faz chamadas reais à API"""
    
    def __init__(self, model="gpt-4o-mini", system_message=None, conversation_id=None):
        self.model = model
        self.system_message = system_message
        self.messages = []
        self.interaction_count = 0
        self.conversation_id = conversation_id
        self.context = GerenciadorCSV('dados.csv')  # Será criado em data/dados.csv
        
        # Adicionar system message primeiro
        if system_message:
            self.messages.append({"role": "system", "content": system_message})
        
        # Carregar conversa anterior se conversation_id foi fornecido
        if conversation_id:
            self._load_conversation(conversation_id)
    
    def add_user_message(self, content):
        """Adiciona uma mensagem do usuário ao contexto"""
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content):
        """Adiciona uma mensagem do assistente ao contexto"""
        self.messages.append({"role": "assistant", "content": content})
    
    def _generate_mock_response(self, user_message):
        """Gera uma resposta simulada baseada na mensagem do usuário"""
        self.interaction_count += 1
        user_lower = user_message.lower()
        
        # Detectar pedido de feedback
        if "feedback" in user_lower or "avaliação" in user_lower or "análise" in user_lower:
            return self._generate_feedback()
        
        # Primeira interação - resposta de interesse inicial com reservas
        if self.interaction_count == 1:
            responses = [
                "Olá! Sim, estou buscando algo nessa área. Mas preciso entender melhor se realmente atende minhas necessidades. O que exatamente você está oferecendo?",
                "Oi! Tenho interesse, mas já avaliei outras opções no mercado. O que torna sua solução diferente?",
                "Bom dia! Estou pesquisando sim, mas meu orçamento é um pouco limitado. Me conta mais sobre o que você oferece?"
            ]
            return random.choice(responses)
        
        # Perguntas sobre preço
        if any(word in user_lower for word in ["preço", "valor", "custa", "custo", "investimento", "r$", "reais"]):
            responses = [
                "Hmm, esse valor está um pouco acima do que eu tinha em mente. Existe alguma forma de tornar mais acessível? Talvez parcelamento ou desconto?",
                "Entendo... Mas vi concorrentes oferecendo algo similar por menos. Como você justifica esse preço?",
                "É um investimento considerável. Como posso ter certeza de que vou ter retorno sobre isso?"
            ]
            return random.choice(responses)
        
        # Perguntas sobre benefícios/características
        if any(word in user_lower for word in ["benefício", "vantagem", "característica", "funcionalidade", "diferencial"]):
            responses = [
                "Interessante... Mas como isso resolve especificamente o meu problema de [otimizar processos/aumentar vendas]? Tem casos de sucesso?",
                "Ok, essas características são legais. Mas qual o benefício prático disso no dia a dia?",
                "E comparando com [concorrente X], o que vocês oferecem de melhor?"
            ]
            return random.choice(responses)
        
        # Objeção de urgência
        if self.interaction_count == 3:
            responses = [
                "Estou gostando da conversa, mas não sei se é o momento ideal para decidir. Posso pensar mais alguns dias?",
                "Parece bom, mas preciso conversar com o time/sócio antes de tomar essa decisão.",
            ]
            return random.choice(responses)
        
        # Objeção de comparação
        if self.interaction_count == 4:
            responses = [
                "Você citou vários pontos positivos, mas como seu produto se compara ao [concorrente]? Eles têm uma proposta parecida...",
                "Entendi suas vantagens. Mas preciso ser sincero: estou avaliando outras 2 empresas também. Por que devo escolher vocês?",
            ]
            return random.choice(responses)
        
        # Respostas gerais positivas (mostrando interesse)
        if any(word in user_lower for word in ["garantia", "suporte", "treinamento", "implementação", "prazo"]):
            return "Isso é importante para mim. E quanto tempo leva para implementar? Vocês dão suporte depois?"
        
        # Progressão natural - ficando mais interessado
        if self.interaction_count >= 5:
            responses = [
                "Você apresentou bem os pontos. Estou considerando seriamente, mas ainda tenho uma dúvida: e se não funcionar como esperado?",
                "Gostei da abordagem. Mas preciso ver isso funcionando na prática. Tem algum trial ou demonstração?",
                "Ok, você está me convencendo. Quais seriam os próximos passos se eu decidir seguir em frente?"
            ]
            return random.choice(responses)
        
        # Resposta padrão
        default_responses = [
            "Certo, entendi isso. E quanto ao prazo de entrega? É algo rápido?",
            "Interessante. Mas me fale mais sobre como funciona na prática.",
            "Ok, mas e o suporte? Como funciona se eu tiver problemas?",
            "Entendo. Tem garantia ou período de teste?",
            "Você pode dar exemplos concretos de resultados que seus clientes obtiveram?"
        ]
        return random.choice(default_responses)
    
    def _generate_feedback(self):
        """Gera um feedback realista baseado nas interações"""
        feedback = f"""**FEEDBACK DO PROCESSO DE VENDA**

**PONTOS FORTES:**
- Demonstrou interesse genuíno em entender minhas necessidades
- Comunicação clara e objetiva durante a conversa
- Manteve um tom profissional e cordial
- Apresentou informações de forma estruturada

**PONTOS DE MELHORIA:**
- Poderia ter feito mais perguntas de descoberta no início para entender melhor meu contexto
- Tratamento de objeções poderia ser mais profundo, com exemplos concretos
- Fechamento poderia ser mais direto, com call-to-action clara

**AVALIAÇÃO POR CRITÉRIO (nota de 0 a 10):**
- Rapport e conexão inicial: 7/10
- Identificação de necessidades: 6/10
- Apresentação de benefícios: 7/10
- Tratamento de objeções: 6/10
- Fechamento e call-to-action: 5/10
- Comunicação geral: 7/10

**NOTA GERAL: 6.3/10**

**RECOMENDAÇÕES ESPECÍFICAS:**
1. Inicie com perguntas abertas tipo "Qual seu maior desafio hoje?" antes de apresentar soluções
2. Use a técnica "Feel, Felt, Found" ao tratar objeções: "Entendo como se sente, outros clientes se sentiram assim, e descobriram que..."
3. Termine sempre com uma ação concreta: "Posso enviar uma proposta até amanhã?" ou "Podemos agendar uma demo na terça?"
4. Apresente mais casos de sucesso e dados concretos (números, resultados, ROI)

**Prática faz o mestre! Continue treinando e aplicando essas técnicas.** 🎯"""
        return feedback
    
    def send_message(self, user_message):
        """Simula envio de mensagem e resposta"""
        self.add_user_message(user_message)
        assistant_message = self._generate_mock_response(user_message)
        self.add_assistant_message(assistant_message)
        return assistant_message
    
    def get_messages(self):
        """Retorna todas as mensagens da conversa"""
        return self.messages.copy()
    
    def clear_context(self, keep_system=True):
        """Limpa o contexto da conversa"""
        if keep_system and self.messages and self.messages[0]["role"] == "system":
            system_msg = self.messages[0]
            self.messages = [system_msg]
        else:
            self.messages = []
        self.interaction_count = 0
    
    def get_context_size(self):
        """Retorna o número de mensagens no contexto"""
        return len(self.messages)
    
    def _load_conversation(self, conversation_id):
        """
        Carrega mensagens de uma conversa anterior do CSV
        
        Args:
            conversation_id: ID da conversa a ser carregada
        """
        # Buscar todas as mensagens com o conversation_id fornecido
        messages_data = self.context.search_data({'conversation_id': conversation_id})
        
        if not messages_data:
            print(f"\n⚠️ Nenhuma conversa encontrada com ID: {conversation_id}")
            return
        
        # Ordenar por data para manter a ordem correta
        messages_data.sort(key=lambda x: x.get('data', ''))
        
        print(f"\n📂 Carregando conversa {conversation_id} (MODO MOCK)...")
        print("=" * 60)
        
        # Reconstruir histórico de mensagens
        for msg_data in messages_data:
            user_msg = msg_data.get('message', '')
            assistant_msg = msg_data.get('response', '')
            
            # Adicionar mensagens ao histórico
            self.messages.append({"role": "user", "content": user_msg})
            self.messages.append({"role": "assistant", "content": assistant_msg})
            self.interaction_count += 1
            
            # Exibir mensagem carregada
            print(f"\n[{msg_data.get('data', 'N/A')}]")
            print(f"Vendedor: {user_msg[:80]}..." if len(user_msg) > 80 else f"Vendedor: {user_msg}")
            print(f"Comprador: {assistant_msg[:80]}..." if len(assistant_msg) > 80 else f"Comprador: {assistant_msg}")
        
        print("\n" + "=" * 60)
        print(f"✓ {len(messages_data)} mensagens carregadas")
        print(f"Interações: {self.interaction_count}")
        print("=" * 60 + "\n")
