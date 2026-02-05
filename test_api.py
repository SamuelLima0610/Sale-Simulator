"""
Script para testar se a API key está funcionando
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

api_key = os.environ.get('OPEN')

if not api_key:
    print("❌ Variável de ambiente 'OPEN' não está configurada!")
    print("\nConfigure com:")
    print('$env:OPEN="sua-chave-aqui"')
else:
    print(f"✓ Variável 'OPEN' encontrada: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Testa uma chamada simples
        print("\nTestando API...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Oi"}],
            max_tokens=10
        )
        
        print("✓ API funcionando!")
        print(f"Resposta: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"\n❌ Erro ao acessar API: {e}")
        print("\nPossíveis causas:")
        print("1. Chave API inválida")
        print("2. Sem créditos na conta")
        print("3. Limite de uso atingido")
        print("\nVerifique em: https://platform.openai.com/account/billing/overview")
