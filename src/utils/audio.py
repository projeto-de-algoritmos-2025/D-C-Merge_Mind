"""
Sistema de gerenciamento de áudio
"""
import pygame
import os
from typing import Dict, Optional
from ..utils.config import AUDIO


class GerenciadorAudio:
    """Gerencia música e efeitos sonoros do jogo"""
    
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        self.sons: Dict[str, pygame.mixer.Sound] = {}
        self.volume_master = AUDIO['VOLUME_MASTER']
        self.volume_sfx = AUDIO['VOLUME_SFX']
        self.volume_musica = AUDIO['VOLUME_MUSICA']
        
        self.musica_atual = None
        self.sfx_habilitado = True
        self.musica_habilitada = True
        
        # Carregar sons padrão (se existirem)
        self._carregar_sons_padrao()
        
    def _carregar_sons_padrao(self) -> None:
        """Carrega sons padrão do diretório assets/sounds"""
        try:
            caminho_sons = "assets/sounds"
            if os.path.exists(caminho_sons):
                for arquivo in os.listdir(caminho_sons):
                    if arquivo.endswith(('.wav', '.ogg', '.mp3')):
                        nome = os.path.splitext(arquivo)[0]
                        self.carregar_som(nome, os.path.join(caminho_sons, arquivo))
        except Exception as e:
            print(f"Erro ao carregar sons padrão: {e}")
            
    def carregar_som(self, nome: str, caminho: str) -> bool:
        """Carrega um efeito sonoro"""
        try:
            if os.path.exists(caminho):
                som = pygame.mixer.Sound(caminho)
                som.set_volume(self.volume_sfx * self.volume_master)
                self.sons[nome] = som
                return True
            else:
                print(f"Arquivo de som não encontrado: {caminho}")
                return False
        except Exception as e:
            print(f"Erro ao carregar som '{nome}': {e}")
            return False
            
    def tocar_som(self, nome: str, loop: int = 0) -> bool:
        """Toca um efeito sonoro"""
        if not self.sfx_habilitado:
            return False
            
        if nome in self.sons:
            try:
                self.sons[nome].play(loops=loop)
                return True
            except Exception as e:
                print(f"Erro ao tocar som '{nome}': {e}")
                return False
        else:
            # Se o som não existe, criar um som sintético
            self._criar_som_sintetico(nome)
            return False
            
    def _criar_som_sintetico(self, tipo: str) -> None:
        """Cria sons sintéticos simples para quando não há arquivos de áudio"""
        try:
            # Parâmetros para diferentes tipos de som
            sons_sinteticos = {
                'clique': (440, 0.1),      # Frequência 440Hz, 0.1s
                'acerto': (523, 0.2),      # Dó maior, 0.2s
                'erro': (220, 0.3),        # Lá menor, 0.3s
                'sucesso': (659, 0.4),     # Mi maior, 0.4s
                'hover': (330, 0.05),      # Mi baixo, 0.05s
            }
            
            if tipo in sons_sinteticos:
                freq, duracao = sons_sinteticos[tipo]
                som = self._gerar_beep(freq, duracao)
                if som:
                    self.sons[tipo] = som
                    som.play()
        except Exception as e:
            print(f"Erro ao criar som sintético '{tipo}': {e}")
            
    def _gerar_beep(self, frequencia: int, duracao: float) -> Optional[pygame.mixer.Sound]:
        """Gera um beep sintético"""
        try:
            import numpy as np
            sample_rate = 22050
            frames = int(duracao * sample_rate)
            
            # Gerar onda senoidal
            arr = np.sin(2 * np.pi * frequencia * np.linspace(0, duracao, frames))
            arr = (arr * 32767).astype(np.int16)
            
            # Converter para stereo
            arr_stereo = np.zeros((frames, 2), dtype=np.int16)
            arr_stereo[:, 0] = arr
            arr_stereo[:, 1] = arr
            
            sound = pygame.sndarray.make_sound(arr_stereo)
            sound.set_volume(self.volume_sfx * self.volume_master * 0.3)
            return sound
        except ImportError:
            # Fallback: criar som simples sem numpy
            try:
                sample_rate = 22050
                frames = int(duracao * sample_rate)
                arr = []
                
                for i in range(frames):
                    # Onda quadrada simples
                    value = 16383 if (i * frequencia // sample_rate) % 2 else -16383
                    arr.append([value, value])
                
                import array
                sound_array = array.array('h', [item for sublist in arr for item in sublist])
                sound = pygame.sndarray.make_sound(sound_array.reshape(-1, 2))
                sound.set_volume(self.volume_sfx * self.volume_master * 0.3)
                return sound
            except Exception as e:
                print(f"Erro ao gerar beep: {e}")
                return None
        except Exception as e:
            print(f"Erro ao gerar beep: {e}")
            return None
            
    def carregar_musica(self, caminho: str) -> bool:
        """Carrega música de fundo"""
        try:
            if os.path.exists(caminho):
                pygame.mixer.music.load(caminho)
                self.musica_atual = caminho
                return True
            else:
                print(f"Arquivo de música não encontrado: {caminho}")
                return False
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
            return False
            
    def tocar_musica(self, loop: int = -1) -> bool:
        """Toca música de fundo"""
        if not self.musica_habilitada or not self.musica_atual:
            return False
            
        try:
            pygame.mixer.music.set_volume(self.volume_musica * self.volume_master)
            pygame.mixer.music.play(loops=loop)
            return True
        except Exception as e:
            print(f"Erro ao tocar música: {e}")
            return False
            
    def parar_musica(self) -> None:
        """Para a música"""
        pygame.mixer.music.stop()
        
    def pausar_musica(self) -> None:
        """Pausa a música"""
        pygame.mixer.music.pause()
        
    def continuar_musica(self) -> None:
        """Continua a música pausada"""
        pygame.mixer.music.unpause()
        
    def definir_volume_master(self, volume: float) -> None:
        """Define o volume master (0.0 a 1.0)"""
        self.volume_master = max(0.0, min(1.0, volume))
        self._atualizar_volumes()
        
    def definir_volume_sfx(self, volume: float) -> None:
        """Define o volume dos efeitos sonoros (0.0 a 1.0)"""
        self.volume_sfx = max(0.0, min(1.0, volume))
        self._atualizar_volumes()
        
    def definir_volume_musica(self, volume: float) -> None:
        """Define o volume da música (0.0 a 1.0)"""
        self.volume_musica = max(0.0, min(1.0, volume))
        if self.musica_atual:
            pygame.mixer.music.set_volume(self.volume_musica * self.volume_master)
            
    def _atualizar_volumes(self) -> None:
        """Atualiza o volume de todos os sons carregados"""
        for som in self.sons.values():
            som.set_volume(self.volume_sfx * self.volume_master)
            
    def alternar_sfx(self) -> bool:
        """Alterna os efeitos sonoros on/off"""
        self.sfx_habilitado = not self.sfx_habilitado
        return self.sfx_habilitado
        
    def alternar_musica(self) -> bool:
        """Alterna a música on/off"""
        self.musica_habilitada = not self.musica_habilitada
        if not self.musica_habilitada:
            self.parar_musica()
        return self.musica_habilitada
        
    def limpar(self) -> None:
        """Limpa todos os recursos de áudio"""
        self.parar_musica()
        self.sons.clear()
        pygame.mixer.quit()
