from openai import OpenAI
import os
from dotenv import load_dotenv

from gerenciador_csv import GerenciadorCSV
from datetime import datetime

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class ConversationContext:
    """Classe responsável por guardar e gerenciar o contexto de uma conversa com OpenAI"""
    
    def __init__(self, model="gpt-4o-mini", system_message=None, conversation_id=None):
        """
        Inicializa uma nova conversa
        
        Args:
            model: Modelo do OpenAI a ser usado
            conversation_id: ID da conversa para manter contexto
            system_message: Mensagem do sistema para definir comportamento do assistente
        """
        self.client = OpenAI(api_key=os.environ.get('OPEN'))
        self.model = model
        self.messages = []
        self.total_tokens_used = 0
        self.total_cost = 0.0
        self.conversation_id = conversation_id if conversation_id else datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Preços por 1M tokens (input/output) em USD
        self.pricing = {
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
            "gpt-4": {"input": 30.00, "output": 60.00},
        }
        self.context = GerenciadorCSV('data/dados.csv')
        
        # Carregar conversa anterior se conversation_id foi fornecido
        if conversation_id:
            self._load_conversation(conversation_id)
        elif system_message:
            self.messages.append({"role": "system", "content": system_message})
    
    def add_user_message(self, content):
        """Adiciona uma mensagem do usuário ao contexto"""
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content):
        """Adiciona uma mensagem do assistente ao contexto"""
        self.messages.append({"role": "assistant", "content": content})
    
    def _calculate_token_usage_and_cost(self, response):
        """
        Calcula o uso de tokens e o custo da chamada à API
        
        Args:
            response: Objeto de resposta da API OpenAI
            
        Returns:
            dict: Dicionário com informações de uso e custo
        """
        usage = response.usage
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens
        
        # Calcula o custo baseado no modelo
        model_key = self.model
        if model_key not in self.pricing:
            # Usa preço padrão do gpt-4o-mini se modelo não encontrado
            model_key = "gpt-4o-mini"
        
        input_cost = (prompt_tokens / 1_000_000) * self.pricing[model_key]["input"]
        output_cost = (completion_tokens / 1_000_000) * self.pricing[model_key]["output"]
        total_cost = input_cost + output_cost
        
        # Atualiza totais acumulados
        self.total_tokens_used += total_tokens
        self.total_cost += total_cost
        
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "input_cost_usd": input_cost,
            "output_cost_usd": output_cost,
            "total_cost_usd": total_cost,
            "cumulative_tokens": self.total_tokens_used,
            "cumulative_cost_usd": self.total_cost
        }
    
    def send_message(self, user_message):
        """
        Envia uma mensagem e recebe resposta, mantendo o contexto
        
        Args:
            user_message: Mensagem do usuário
            
        Returns:
            tuple: (resposta do assistente, informações de uso de tokens e custo)
        """
        self.add_user_message(user_message)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        
        assistant_message = response.choices[0].message.content
        self.add_assistant_message(assistant_message)
        
        # Calcula uso de tokens e custo
        usage_info = self._calculate_token_usage_and_cost(response)
        information_message = {}
        information_message['conversation_id'] = self.conversation_id
        information_message['data'] = datetime.now().isoformat()
        information_message['total_tokens'] = usage_info['total_tokens']
        information_message['input_cost_usd'] = usage_info['input_cost_usd']
        information_message['message'] = user_message
        information_message['response'] = assistant_message
        information_message['output_cost_usd'] = usage_info['output_cost_usd']
        self.context.save_data(information_message)

        return assistant_message
    
    def get_messages(self):
        """Retorna todas as mensagens da conversa"""
        return self.messages.copy()
    
    def clear_context(self, keep_system=True):
        """
        Limpa o contexto da conversa
        
        Args:
            keep_system: Se True, mantém a mensagem do sistema
        """
        if keep_system and self.messages and self.messages[0]["role"] == "system":
            system_msg = self.messages[0]
            self.messages = [system_msg]
        else:
            self.messages = []
    
    def get_context_size(self):
        """Retorna o número de mensagens no contexto"""
        return len(self.messages)
    
    def get_usage_stats(self):
        """
        Retorna estatísticas de uso acumuladas
        
        Returns:
            dict: Dicionário com tokens totais usados e custo total
        """
        return {
            "total_tokens": self.total_tokens_used,
            "total_cost_usd": self.total_cost,
            "model": self.model
        }
    
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
        
        print(f"\n📂 Carregando conversa {conversation_id}...")
        print("=" * 60)
        
        # Reconstruir histórico de mensagens e calcular totais
        for msg_data in messages_data:
            user_msg = msg_data.get('message', '')
            assistant_msg = msg_data.get('response', '')
            tokens = msg_data.get('total_tokens', 0)
            input_cost = msg_data.get('input_cost_usd', 0.0)
            output_cost = msg_data.get('output_cost_usd', 0.0)
            
            # Adicionar mensagens ao histórico
            self.messages.append({"role": "user", "content": user_msg})
            self.messages.append({"role": "assistant", "content": assistant_msg})
            
            # Atualizar totais
            self.total_tokens_used += tokens
            self.total_cost += (input_cost + output_cost)
            
            # Exibir mensagem carregada
            print(f"\n[{msg_data.get('data', 'N/A')}]")
            print(f"Vendedor: {user_msg}")
            print(f"Comprador: {assistant_msg}")
            print(f"Tokens: {tokens} | Custo: ${input_cost + output_cost:.6f}")
        
        print("\n" + "=" * 60)
        print(f"✓ {len(messages_data)} mensagens carregadas")
        print(f"Total de tokens: {self.total_tokens_used}")
        print(f"Custo acumulado: ${self.total_cost:.6f}")
        print("=" * 60 + "\n")

