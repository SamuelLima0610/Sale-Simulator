"""
Módulo para gravação e transcrição de áudio
"""
import sounddevice as sd
import numpy as np
import wave
import os
from openai import OpenAI
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class AudioRecorder:
    """Classe para gravar e transcrever áudio"""
    
    def __init__(self, sample_rate=16000):
        """
        Inicializa o gravador de áudio
        
        Args:
            sample_rate: Taxa de amostragem do áudio (16kHz é ideal para Whisper)
        """
        self.sample_rate = sample_rate
        self.client = OpenAI(api_key=os.environ.get('OPEN'))
        print("✓ AudioRecorder inicializado.")
    
    def record_audio(self, duration=5, filename='audio_temp.wav'):
        """
        Grava áudio do microfone
        
        Args:
            duration: Duração da gravação em segundos
            filename: Nome do arquivo para salvar o áudio
            
        Returns:
            Caminho do arquivo de áudio gravado
        """
        print(f"🎤 Gravando por {duration} segundos...")
        
        # Grava áudio
        recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.int16
        )
        sd.wait()  # Espera a gravação terminar
        
        print("✓ Gravação concluída!")
        
        # Salva o áudio em arquivo WAV
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16 bits
            wf.setframerate(self.sample_rate)
            wf.writeframes(recording.tobytes())
        
        return filename
    
    def transcribe_audio(self, audio_file):
        """
        Transcreve áudio usando Whisper da OpenAI
        
        Args:
            audio_file: Caminho do arquivo de áudio
            
        Returns:
            Texto transcrito
        """
        print("📝 Transcrevendo áudio...")
        
        with open(audio_file, 'rb') as f:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="pt"
            )
        
        print("✓ Transcrição concluída!")
        return transcript.text
    
    def record_and_transcribe(self, duration=5):
        """
        Grava e transcreve áudio em uma única operação
        
        Args:
            duration: Duração da gravação em segundos
            
        Returns:
            Texto transcrito
        """
        audio_file = self.record_audio(duration)
        transcription = self.transcribe_audio(audio_file)
        
        # Remove o arquivo temporário
        try:
            os.remove(audio_file)
        except:
            pass
        
        return transcription


class MockAudioRecorder:
    """Versão mock para testes sem API"""
    
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
    
    def record_audio(self, duration=5, filename='audio_temp.wav'):
        """Simula gravação de áudio"""
        print(f"🎤 [MODO TESTE] Simulando gravação por {duration} segundos...")
        import time
        time.sleep(1)  # Simula o tempo de gravação
        print("✓ Gravação simulada concluída!")
        return filename
    
    def transcribe_audio(self, audio_file):
        """Simula transcrição"""
        print("📝 [MODO TESTE] Simulando transcrição...")
        
        # Retorna frases de exemplo para teste
        examples = [
            "Olá, bom dia! Estou interessado no seu produto.",
            "Qual é o preço desse serviço?",
            "Gostaria de saber mais sobre os benefícios.",
            "Tem desconto para pagamento à vista?",
            "Preciso pensar melhor sobre isso."
        ]
        import random
        return random.choice(examples)
    
    def record_and_transcribe(self, duration=5):
        """Simula gravação e transcrição"""
        audio_file = self.record_audio(duration)
        transcription = self.transcribe_audio(audio_file)
        return transcription
