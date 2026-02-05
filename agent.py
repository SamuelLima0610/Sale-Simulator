from openai import OpenAI
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class ConversationContext:
    """Classe responsável por guardar e gerenciar o contexto de uma conversa com OpenAI"""
    
    def __init__(self, model="gpt-4o-mini", system_message=None):
        """
        Inicializa uma nova conversa
        
        Args:
            model: Modelo do OpenAI a ser usado
            system_message: Mensagem do sistema para definir comportamento do assistente
        """
        self.client = OpenAI(api_key=os.environ.get('OPEN'))
        self.model = model
        self.messages = []
        
        if system_message:
            self.messages.append({"role": "system", "content": system_message})
    
    def add_user_message(self, content):
        """Adiciona uma mensagem do usuário ao contexto"""
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content):
        """Adiciona uma mensagem do assistente ao contexto"""
        self.messages.append({"role": "assistant", "content": content})
    
    def send_message(self, user_message):
        """
        Envia uma mensagem e recebe resposta, mantendo o contexto
        
        Args:
            user_message: Mensagem do usuário
            
        Returns:
            Resposta do assistente
        """
        self.add_user_message(user_message)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        
        assistant_message = response.choices[0].message.content
        self.add_assistant_message(assistant_message)
        
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

