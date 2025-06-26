"""
Estado de seleção de nível de dificuldade
"""
import pygame
from ..estado_manager import Estado
from ...ui.componentes import Botao, Texto
from ...utils.config import CORES, FONTES, LARGURA, ALTURA, NIVEIS


class EstadoSelecaoNivel(Estado):
    """Tela de seleção de nível de dificuldade"""
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """Inicializa elementos da interface"""
        # Título
        self.titulo = Texto(
            LARGURA // 2, 100,
            "Escolha o Nível de Dificuldade",
            FONTES['TITULO'],
            CORES['TEXTO'],
            centralizado=True
        )
        
        # Botões de nível
        self.botoes_nivel = []
        largura_botao = 280
        altura_botao = 120
        espaco_x = 50
        total_largura = 2 * largura_botao + espaco_x
        x_inicial = (LARGURA - total_largura) // 2
        y_inicial = 200
        
        # Linha superior: Fácil e Médio
        niveis_linha1 = ['FACIL', 'MEDIO']
        for i, nivel in enumerate(niveis_linha1):
            config = NIVEIS[nivel]
            x = x_inicial + i * (largura_botao + espaco_x)
            
            botao = Botao(
                x, y_inicial,
                largura_botao, altura_botao,
                f"{config['nome']}\n{config['elementos']} elementos",
                lambda n=nivel: self.selecionar_nivel(n),
                CORES['SUCESSO'] if nivel == 'FACIL' else CORES['AVISO']
            )
            self.botoes_nivel.append(botao)
            
        # Linha inferior: Difícil e Expert
        niveis_linha2 = ['DIFICIL', 'EXPERT']
        y_linha2 = y_inicial + altura_botao + 30
        for i, nivel in enumerate(niveis_linha2):
            config = NIVEIS[nivel]
            x = x_inicial + i * (largura_botao + espaco_x)
            
            botao = Botao(
                x, y_linha2,
                largura_botao, altura_botao,
                f"{config['nome']}\n{config['elementos']} elementos",
                lambda n=nivel: self.selecionar_nivel(n),
                CORES['SECUNDARIA'] if nivel == 'DIFICIL' else CORES['PRINCIPAL']
            )
            self.botoes_nivel.append(botao)
            
        # Descrições dos níveis
        self.descricoes = {
            'FACIL': "Perfeito para iniciantes\nSem limite de tempo\nDicas habilitadas",
            'MEDIO': "Para quem já conhece o básico\nTempo limite: 30s\nDicas habilitadas",
            'DIFICIL': "Para jogadores experientes\nTempo limite: 20s\nSem dicas",
            'EXPERT': "Apenas para experts\nTempo limite: 15s\nSem dicas"
        }
        
        # Botão voltar
        self.botao_voltar = Botao(
            50, ALTURA - 100,
            150, 50,
            "⬅ Voltar",
            self.voltar_menu,
            CORES['HOVER']
        )
        
        # Texto de descrição (será atualizado no hover)
        self.texto_descricao = Texto(
            LARGURA // 2, ALTURA - 150,
            "Passe o mouse sobre um nível para ver detalhes",
            FONTES['NORMAL'],
            CORES['TEXTO'],
            centralizado=True
        )
        
    def selecionar_nivel(self, nivel):
        """Seleciona um nível e inicia o jogo"""
        self.game_manager.audio.tocar_som('clique')
        self.game_manager.nivel_selecionado = nivel
        self.game_manager.gerenciador_estados.mudar_estado('jogo')
        
    def voltar_menu(self):
        """Volta para o menu principal"""
        self.game_manager.audio.tocar_som('clique')
        self.game_manager.gerenciador_estados.mudar_estado('menu')
        
    def processar_eventos(self, eventos):
        """Processa eventos da tela de seleção"""
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.game_manager.rodando = False
                
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.voltar_menu()
                elif evento.key == pygame.K_1:
                    self.selecionar_nivel('FACIL')
                elif evento.key == pygame.K_2:
                    self.selecionar_nivel('MEDIO')
                elif evento.key == pygame.K_3:
                    self.selecionar_nivel('DIFICIL')
                elif evento.key == pygame.K_4:
                    self.selecionar_nivel('EXPERT')
                    
            elif evento.type == pygame.MOUSEMOTION:
                # Atualizar descrição baseada no hover
                mouse_pos = evento.pos
                for i, botao in enumerate(self.botoes_nivel):
                    if botao.rect.collidepoint(mouse_pos):
                        nivel = ['FACIL', 'MEDIO', 'DIFICIL', 'EXPERT'][i]
                        self.texto_descricao.definir_texto(self.descricoes[nivel])
                        break
                else:
                    self.texto_descricao.definir_texto("Passe o mouse sobre um nível para ver detalhes")
                    
            # Processar eventos dos botões
            for botao in self.botoes_nivel:
                if botao.processar_evento(evento):
                    self.game_manager.audio.tocar_som('hover')
                    
            if self.botao_voltar.processar_evento(evento):
                self.game_manager.audio.tocar_som('hover')
                
    def atualizar(self, dt):
        """Atualiza a tela de seleção"""
        # Atualizar botões
        for botao in self.botoes_nivel:
            botao.atualizar(dt)
        self.botao_voltar.atualizar(dt)
        
    def renderizar(self):
        """Renderiza a tela de seleção"""
        # Fundo
        self.tela.fill(CORES['FUNDO'])
        
        # Título
        self.titulo.renderizar(self.tela)
        
        # Botões de nível
        for botao in self.botoes_nivel:
            botao.renderizar(self.tela)
            
        # Botão voltar
        self.botao_voltar.renderizar(self.tela)
        
        # Descrição
        self.texto_descricao.renderizar(self.tela)
        
        # Instruções de teclado
        instrucoes = Texto(
            LARGURA // 2, ALTURA - 50,
            "Use as teclas 1-4 para seleção rápida | ESC para voltar",
            FONTES['PEQUENA'],
            CORES['HOVER'],
            centralizado=True
        )
        instrucoes.renderizar(self.tela)
