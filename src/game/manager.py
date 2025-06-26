"""
Gerenciador principal do jogo Merge_Mind
"""
import pygame
import sys
from .estado_manager import GerenciadorEstados
from .estados.menu import EstadoMenu
from .estados.selecao_nivel import EstadoSelecaoNivel
from .estados.jogo import EstadoJogo
from .estados.ranking import EstadoRanking
from ..utils.config import LARGURA, ALTURA, FPS, TITULO, CORES
from ..utils.audio import GerenciadorAudio


class GameManager:
    """Classe principal que gerencia todo o jogo"""
    
    def __init__(self):
        # Inicializar Pygame
        pygame.init()
        
        # Configurar tela
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        
        # Clock para controle de FPS
        self.clock = pygame.time.Clock()
        
        # Estado do jogo
        self.rodando = True
        self.nivel_selecionado = 'FACIL'
        
        # Sistemas
        self.audio = GerenciadorAudio()
        self.gerenciador_estados = GerenciadorEstados(self)
        
        # Inicializar estados
        self.inicializar_estados()
        
        # Configurar ícone (se disponível)
        self.configurar_icone()
        
    def inicializar_estados(self):
        """Inicializa todos os estados do jogo"""
        # Criar estados
        estado_menu = EstadoMenu(self)
        estado_selecao = EstadoSelecaoNivel(self)
        estado_jogo = EstadoJogo(self)
        estado_ranking = EstadoRanking(self)
        
        # Adicionar estados ao gerenciador
        self.gerenciador_estados.adicionar_estado('menu', estado_menu)
        self.gerenciador_estados.adicionar_estado('selecao_nivel', estado_selecao)
        self.gerenciador_estados.adicionar_estado('jogo', estado_jogo)
        self.gerenciador_estados.adicionar_estado('ranking', estado_ranking)
        
        # Iniciar no menu
        self.gerenciador_estados.mudar_estado('menu')
        
    def configurar_icone(self):
        """Configura o ícone da janela"""
        try:
            # Tentar carregar ícone personalizado
            import os
            if os.path.exists('assets/icon.png'):
                icone = pygame.image.load('assets/icon.png')
                pygame.display.set_icon(icone)
            else:
                # Criar ícone simples se não existir
                self.criar_icone_simples()
        except Exception as e:
            print(f"Aviso: Não foi possível carregar ícone: {e}")
            
    def criar_icone_simples(self):
        """Cria um ícone simples usando Pygame"""
        try:
            # Criar surface de 32x32 para o ícone
            icone = pygame.Surface((32, 32))
            icone.fill(CORES['FUNDO'])
            
            # Desenhar um símbolo simples
            pygame.draw.rect(icone, CORES['PRINCIPAL'], (4, 4, 24, 24), border_radius=4)
            pygame.draw.rect(icone, CORES['DESTAQUE'], (8, 8, 16, 16), border_radius=2)
            
            pygame.display.set_icon(icone)
        except Exception as e:
            print(f"Aviso: Não foi possível criar ícone: {e}")
            
    def processar_eventos(self):
        """Processa eventos globais do jogo"""
        eventos = pygame.event.get()
        
        # Eventos globais
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                # Atalhos globais
                if evento.key == pygame.K_F11:
                    self.alternar_tela_cheia()
                elif evento.key == pygame.K_F4 and pygame.key.get_pressed()[pygame.K_LALT]:
                    self.rodando = False
                    
        # Passar eventos para o estado atual
        self.gerenciador_estados.processar_eventos(eventos)
        
    def alternar_tela_cheia(self):
        """Alterna entre tela cheia e janela"""
        try:
            flags = self.tela.get_flags()
            if flags & pygame.FULLSCREEN:
                # Sair da tela cheia
                self.tela = pygame.display.set_mode((LARGURA, ALTURA))
            else:
                # Entrar em tela cheia
                self.tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
        except Exception as e:
            print(f"Erro ao alternar tela cheia: {e}")
            
    def atualizar(self, dt: float):
        """Atualiza a lógica do jogo"""
        self.gerenciador_estados.atualizar(dt)
        
    def renderizar(self):
        """Renderiza o jogo"""
        # Limpar tela
        self.tela.fill(CORES['FUNDO'])
        
        # Renderizar estado atual
        self.gerenciador_estados.renderizar()
        
        # Atualizar display
        pygame.display.flip()
        
    def executar(self):
        """Loop principal do jogo"""
        print(f"Iniciando {TITULO}...")
        print("Controles:")
        print("- ESC: Voltar/Sair")
        print("- F11: Tela cheia")
        print("- ESPAÇO: Pausar (durante o jogo)")
        print("- R: Reiniciar (durante o jogo)")
        print()
        
        tempo_anterior = pygame.time.get_ticks()
        
        try:
            while self.rodando:
                # Calcular delta time
                tempo_atual = pygame.time.get_ticks()
                dt = (tempo_atual - tempo_anterior) / 1000.0  # Converter para segundos
                tempo_anterior = tempo_atual
                
                # Limitar delta time para evitar saltos grandes
                dt = min(dt, 1.0/30.0)  # Máximo 30 FPS para evitar problemas
                
                # Processar eventos
                self.processar_eventos()
                
                # Atualizar
                if self.rodando:  # Verificar novamente após eventos
                    self.atualizar(dt)
                    
                # Renderizar
                self.renderizar()
                
                # Controlar FPS
                self.clock.tick(FPS)
                
        except KeyboardInterrupt:
            print("\nJogo interrompido pelo usuário.")
        except Exception as e:
            print(f"Erro durante execução: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.finalizar()
            
    def finalizar(self):
        """Finaliza o jogo e libera recursos"""
        print("Finalizando jogo...")
        
        try:
            # Limpar áudio
            self.audio.limpar()
            
            # Finalizar Pygame
            pygame.quit()
        except Exception as e:
            print(f"Erro ao finalizar: {e}")
        finally:
            sys.exit(0)


def main():
    """Função principal para executar o jogo"""
    try:
        game = GameManager()
        game.executar()
    except Exception as e:
        print(f"Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
