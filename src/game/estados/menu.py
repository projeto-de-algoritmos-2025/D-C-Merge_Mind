"""
Estado do menu principal
"""
import pygame
import math
from ..estado_manager import Estado
from ...ui.componentes import Botao, Texto
from ...utils.config import CORES, FONTES, LARGURA, ALTURA, VISUAL


class EstadoMenu(Estado):
    """Menu principal do jogo"""
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.particulas = []
        self.tempo_animacao = 0
        self.inicializar_ui()
        self.inicializar_particulas()
        
    def inicializar_ui(self):
        """Inicializa elementos da interface"""
        # Título
        self.titulo = Texto(
            LARGURA // 2, 150,
            "MERGE MIND",
            FONTES['TITULO'],
            CORES['DESTAQUE'],
            centralizado=True
        )
        
        self.subtitulo = Texto(
            LARGURA // 2, 200,
            "Aprenda Merge Sort de forma interativa",
            FONTES['SUBTITULO'],
            CORES['TEXTO'],
            centralizado=True
        )
        
        # Botões do menu
        largura_botao = 300
        altura_botao = 60
        espaco_botao = 20
        x_botao = (LARGURA - largura_botao) // 2
        y_inicial = 300
        
        self.botoes = [
            Botao(
                x_botao, y_inicial,
                largura_botao, altura_botao,
                "🎮 Jogar",
                self.iniciar_jogo,
                CORES['PRINCIPAL']
            ),
            Botao(
                x_botao, y_inicial + (altura_botao + espaco_botao),
                largura_botao, altura_botao,
                "📚 Tutorial",
                self.abrir_tutorial,
                CORES['SUCESSO']
            ),
            Botao(
                x_botao, y_inicial + 2 * (altura_botao + espaco_botao),
                largura_botao, altura_botao,
                "🏆 Ranking",
                self.abrir_ranking,
                CORES['AVISO']
            ),
            Botao(
                x_botao, y_inicial + 3 * (altura_botao + espaco_botao),
                largura_botao, altura_botao,
                "⚙️ Configurações",
                self.abrir_configuracoes,
                CORES['HOVER']
            ),
            Botao(
                x_botao, y_inicial + 4 * (altura_botao + espaco_botao),
                largura_botao, altura_botao,
                "❌ Sair",
                self.sair_jogo,
                CORES['SECUNDARIA']
            )
        ]
        
        # Texto de créditos
        self.creditos = Texto(
            LARGURA // 2, ALTURA - 50,
            "Desenvolvido por Davi Vieira & Henrique Neves - UnB 2024",
            FONTES['PEQUENA'],
            CORES['HOVER'],
            centralizado=True
        )
        
    def inicializar_particulas(self):
        """Inicializa sistema de partículas de fundo"""
        import random
        for _ in range(50):
            particula = {
                'x': random.randint(0, LARGURA),
                'y': random.randint(0, ALTURA),
                'velocidade': random.uniform(0.5, 2.0),
                'tamanho': random.randint(2, 5),
                'cor': (*CORES['PRINCIPAL'], random.randint(50, 150))
            }
            self.particulas.append(particula)
            
    def iniciar_jogo(self):
        """Inicia o jogo"""
        self.game_manager.audio.tocar_som('clique')
        self.game_manager.gerenciador_estados.mudar_estado('selecao_nivel')
        
    def abrir_tutorial(self):
        """Abre o tutorial"""
        self.game_manager.audio.tocar_som('clique')
        self.game_manager.gerenciador_estados.mudar_estado('tutorial')
        
    def abrir_ranking(self):
        """Abre o ranking"""
        self.game_manager.audio.tocar_som('clique')
        self.game_manager.gerenciador_estados.mudar_estado('ranking')
        
    def abrir_configuracoes(self):
        """Abre as configurações"""
        self.game_manager.audio.tocar_som('clique')
        self.game_manager.gerenciador_estados.mudar_estado('configuracoes')
        
    def sair_jogo(self):
        """Sai do jogo"""
        self.game_manager.audio.tocar_som('clique')
        self.game_manager.rodando = False
        
    def processar_eventos(self, eventos):
        """Processa eventos do menu"""
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.game_manager.rodando = False
                
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.game_manager.rodando = False
                elif evento.key == pygame.K_RETURN:
                    self.iniciar_jogo()
                    
            # Processar eventos dos botões
            for botao in self.botoes:
                if botao.processar_evento(evento):
                    self.game_manager.audio.tocar_som('hover')
                    
    def atualizar(self, dt):
        """Atualiza o menu"""
        self.tempo_animacao += dt
        
        # Atualizar botões
        for botao in self.botoes:
            botao.atualizar(dt)
            
        # Atualizar partículas
        for particula in self.particulas:
            particula['y'] += particula['velocidade']
            if particula['y'] > ALTURA:
                particula['y'] = -particula['tamanho']
                
    def renderizar(self):
        """Renderiza o menu"""
        # Fundo gradiente
        self.desenhar_fundo_gradiente()
        
        # Partículas de fundo
        self.renderizar_particulas()
        
        # Título com efeito
        self.renderizar_titulo_animado()
        
        # Subtítulo
        self.subtitulo.renderizar(self.tela)
        
        # Botões
        for botao in self.botoes:
            botao.renderizar(self.tela)
            
        # Créditos
        self.creditos.renderizar(self.tela)
        
    def desenhar_fundo_gradiente(self):
        """Desenha um fundo gradiente"""
        for y in range(ALTURA):
            # Interpolar entre as cores do fundo
            fator = y / ALTURA
            r = int(CORES['FUNDO'][0] * (1 - fator) + CORES['CARD'][0] * fator)
            g = int(CORES['FUNDO'][1] * (1 - fator) + CORES['CARD'][1] * fator)
            b = int(CORES['FUNDO'][2] * (1 - fator) + CORES['CARD'][2] * fator)
            
            pygame.draw.line(self.tela, (r, g, b), (0, y), (LARGURA, y))
            
    def renderizar_particulas(self):
        """Renderiza partículas de fundo"""
        for particula in self.particulas:
            # Aplicar transparência baseada no tempo
            alpha = int(128 + 127 * math.sin(self.tempo_animacao * 2 + particula['x'] * 0.01))
            cor_com_alpha = (*particula['cor'][:3], alpha)
            
            # Criar surface temporária para transparência
            superficie = pygame.Surface((particula['tamanho'] * 2, particula['tamanho'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(superficie, cor_com_alpha, 
                             (particula['tamanho'], particula['tamanho']), 
                             particula['tamanho'])
            
            self.tela.blit(superficie, (int(particula['x']), int(particula['y'])))
            
    def renderizar_titulo_animado(self):
        """Renderiza o título com efeito de animação"""
        # Efeito de flutuação
        offset_y = int(10 * math.sin(self.tempo_animacao * 3))
        
        # Efeito de brilho
        brilho = int(50 + 25 * math.sin(self.tempo_animacao * 4))
        cor_brilho = tuple(min(255, c + brilho) for c in CORES['DESTAQUE'])
        
        # Renderizar título com posição animada
        titulo_animado = Texto(
            LARGURA // 2, 150 + offset_y,
            "MERGE MIND",
            FONTES['TITULO'],
            cor_brilho,
            centralizado=True
        )
        titulo_animado.renderizar(self.tela)
        
    def entrar(self):
        """Chamado ao entrar no estado"""
        # Iniciar música de menu se disponível
        self.game_manager.audio.tocar_musica()
        
    def sair(self):
        """Chamado ao sair do estado"""
        pass
