# Exemplo de uso
from agent import ConversationContext
from agent_mock import MockConversationContext
from audio_recorder import AudioRecorder, MockAudioRecorder

if __name__ == "__main__":
    
    # Perguntar qual versão usar
    print("=" * 60)
    print("SIMULADOR DE VENDAS - Treinamento")
    print("=" * 60)
    print("\nEscolha o modo:")
    print("1 - MODO REAL (requer créditos OpenAI)")
    print("2 - MODO TESTE (gratuito, sem API)")
    print("-" * 60)
    
    while True:
        choice = input("\nDigite 1 ou 2: ").strip()
        if choice in ["1", "2"]:
            break
        print("Opção inválida!")
    
    use_mock = (choice == "2")
    
    # System message otimizado para simular um comprador realista
    system_message = """
    Você é um comprador potencial interessado em avaliar produtos ou serviços. Seu papel é participar de uma simulação de venda realista.

    ## SEU PERFIL E COMPORTAMENTO:
    - Você é um comprador criterioso, mas aberto a ofertas convincentes
    - Tem necessidades e dúvidas genuínas sobre o produto/serviço
    - Seu orçamento é limitado, mas está disposto a investir se ver valor
    - Faz perguntas relevantes sobre características, benefícios, preço e condições
    - Apresenta objeções realistas quando apropriado (preço, concorrência, necessidade, urgência)
    - Responde de forma natural e conversacional, como um cliente real
    - Sua decisão de compra depende de quão bem o vendedor atende suas necessidades

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

    # Criar a conversa (real ou mock)
    if use_mock:
        conversation = MockConversationContext(
            model="gpt-4o-mini",
            system_message=system_message
        )
        audio_recorder = MockAudioRecorder()
        print("\n✓ Modo TESTE ativo (sem custo, respostas simuladas)")
    else:
        conversation = ConversationContext(
            model="gpt-4o-mini",
            system_message=system_message
        )
        audio_recorder = AudioRecorder()
        print("\n✓ Modo REAL ativo (usando API OpenAI)")
    
    print("=" * 60)
    print("\nVocê é o VENDEDOR. O comprador está esperando sua apresentação.")
    print("Para encerrar e receber feedback, digite: 'FEEDBACK'")
    print("Para gravar áudio ao invés de digitar, digite: 'VOZ'")
    print("\n" + "-" * 60)
    
    # Loop de conversa
    while True:
        user_input = input("\nVocê (vendedor): ").strip()
        
        if not user_input:
            continue
        
        # Opção para gravar áudio
        if user_input.upper() == "VOZ":
            try:
                print("\nPreparando gravação...")
                duration_input = input("Duração da gravação em segundos (padrão 5): ").strip()
                duration = int(duration_input) if duration_input else 5
                
                user_input = audio_recorder.record_and_transcribe(duration)
                print(f"\n📝 Transcrição: \"{user_input}\"\n")
                
                if not user_input:
                    print("❌ Não foi possível transcrever. Tente novamente.")
                    continue
            except Exception as e:
                print(f"❌ Erro ao gravar/transcrever áudio: {e}")
                print("Você pode digitar sua mensagem normalmente.")
                continue
            
        if user_input.upper() == "FEEDBACK":
            print("\n" + "=" * 60)
            print("SOLICITANDO FEEDBACK DO PROCESSO DE VENDA...")
            print("=" * 60 + "\n")
            feedback = conversation.send_message(
                "Por favor, forneça agora o feedback detalhado sobre o meu processo de venda."
            )
            print(f"FEEDBACK DO COMPRADOR:\n\n{feedback}\n")
            print("=" * 60)
            break
        
        response = conversation.send_message(user_input)
        print(f"\nComprador: {response}")
