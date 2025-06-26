"""
Estado do ranking e estatísticas
"""
import pygame
from ..estado_manager import Estado
from ...ui.componentes import Botao, Texto
from ...utils.config import CORES, FONTES, LARGURA, ALTURA
from ..pontuacao import SistemaPontuacao


class EstadoRanking(Estado):
    """Tela de ranking e estatísticas"""
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.pontuacao_sistema = SistemaPontuacao()
        self.scroll_y = 0
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """Inicializa elementos da interface"""
        # Título
        self.titulo = Texto(
            LARGURA // 2, 50,
            "🏆 RANKING & ESTATÍSTICAS",
            FONTES['TITULO'],
            CORES['DESTAQUE'],
            centralizado=True
        )
        
        # Botão voltar
        self.botao_voltar = Botao(
            50, ALTURA - 100,
            150, 50,
            "⬅ Voltar",
            self.voltar_menu,
            CORES['HOVER']
        )
        
        # Botão resetar estatísticas
        self.botao_resetar = Botao(
            LARGURA - 200, ALTURA - 100,
            150, 50,
            "🗑 Resetar",
            self.resetar_estatisticas,
            CORES['SECUNDARIA']
        )
        
        self.atualizar_dados()
        
    def atualizar_dados(self):
        """Atualiza os dados do ranking"""
        self.ranking = self.pontuacao_sistema.obter_ranking(10)
        self.estatisticas_gerais = self.pontuacao_sistema.obter_estatisticas_gerais()
        
    def voltar_menu(self):
        """Volta para o menu principal"""
        self.game_manager.audio.tocar_som('clique')
        self.game_manager.gerenciador_estados.mudar_estado('menu')
        
    def resetar_estatisticas(self):
        """Reseta todas as estatísticas"""
        self.game_manager.audio.tocar_som('clique')
        self.pontuacao_sistema.resetar_estatisticas()
        self.atualizar_dados()
        
    def processar_eventos(self, eventos):
        """Processa eventos do ranking"""
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.game_manager.rodando = False
                
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.voltar_menu()
                elif evento.key == pygame.K_UP:
                    self.scroll_y = max(0, self.scroll_y - 30)
                elif evento.key == pygame.K_DOWN:
                    self.scroll_y = min(500, self.scroll_y + 30)
                    
            elif evento.type == pygame.MOUSEWHEEL:
                self.scroll_y = max(0, min(500, self.scroll_y - evento.y * 30))
                
            # Processar eventos dos botões
            if self.botao_voltar.processar_evento(evento):
                self.game_manager.audio.tocar_som('hover')
            if self.botao_resetar.processar_evento(evento):
                self.game_manager.audio.tocar_som('hover')
                
    def atualizar(self, dt):
        """Atualiza o estado do ranking"""
        self.botao_voltar.atualizar(dt)
        self.botao_resetar.atualizar(dt)
        
    def renderizar(self):
        """Renderiza a tela de ranking"""
        # Fundo
        self.tela.fill(CORES['FUNDO'])
        
        # Título
        self.titulo.renderizar(self.tela)
        
        # Divisão em duas colunas
        coluna_esquerda = LARGURA // 2 - 50
        coluna_direita = LARGURA // 2 + 50
        y_base = 120 - self.scroll_y
        
        # Coluna esquerda: Estatísticas gerais
        self.renderizar_estatisticas_gerais(50, y_base)
        
        # Coluna direita: Top 10
        self.renderizar_top_10(coluna_direita, y_base)
        
        # Botões
        self.botao_voltar.renderizar(self.tela)
        self.botao_resetar.renderizar(self.tela)
        
        # Instruções
        instrucoes = Texto(
            LARGURA // 2, ALTURA - 150,
            "Use ↑↓ ou scroll do mouse para navegar",
            FONTES['PEQUENA'],
            CORES['HOVER'],
            centralizado=True
        )
        instrucoes.renderizar(self.tela)
        
    def renderizar_estatisticas_gerais(self, x: int, y: int):
        """Renderiza estatísticas gerais"""
        # Título da seção
        titulo_stats = Texto(
            x + 150, y,
            "📊 ESTATÍSTICAS GERAIS",
            FONTES['SUBTITULO'],
            CORES['PRINCIPAL'],
            centralizado=True
        )
        titulo_stats.renderizar(self.tela)
        
        y_atual = y + 50
        espacamento = 35
        
        stats = self.estatisticas_gerais
        
        # Criar lista de estatísticas para exibir
        estatisticas = [
            ("Total de Partidas:", f"{stats['total_partidas']}"),
            ("Partidas Completas:", f"{stats['partidas_completas']}"),
            ("Taxa de Conclusão:", f"{stats['taxa_conclusao']:.1f}%"),
            ("Pontuação Máxima:", f"{stats['pontuacao_maxima']:,}"),
            ("Precisão Média:", f"{stats['precisao_media']:.1f}%"),
            ("Tempo Médio:", f"{stats['tempo_medio']:.1f}s"),
            ("Nível Favorito:", stats['nivel_favorito'].title())
        ]
        
        for label, valor in estatisticas:
            # Label
            texto_label = Texto(
                x, y_atual,
                label,
                FONTES['NORMAL'],
                CORES['TEXTO']
            )
            texto_label.renderizar(self.tela)
            
            # Valor
            texto_valor = Texto(
                x + 200, y_atual,
                valor,
                FONTES['NORMAL'],
                CORES['DESTAQUE']
            )
            texto_valor.renderizar(self.tela)
            
            y_atual += espacamento
            
    def renderizar_top_10(self, x: int, y: int):
        """Renderiza o top 10 de pontuações"""
        # Título da seção
        titulo_ranking = Texto(
            x + 150, y,
            "🏆 TOP 10 PONTUAÇÕES",
            FONTES['SUBTITULO'],
            CORES['DESTAQUE'],
            centralizado=True
        )
        titulo_ranking.renderizar(self.tela)
        
        if not self.ranking:
            texto_vazio = Texto(
                x + 150, y + 100,
                "Nenhuma partida completa ainda!\nJogue para aparecer no ranking!",
                FONTES['NORMAL'],
                CORES['HOVER'],
                centralizado=True
            )
            texto_vazio.renderizar(self.tela)
            return
            
        y_atual = y + 60
        espacamento = 45
        
        # Cabeçalho
        cabecalho = ["#", "Pontos", "Nível", "Precisão", "Tempo"]
        x_colunas = [x, x + 40, x + 120, x + 200, x + 270]
        
        for i, texto in enumerate(cabecalho):
            texto_cabecalho = Texto(
                x_colunas[i], y_atual,
                texto,
                FONTES['NORMAL'],
                CORES['TEXTO']
            )
            texto_cabecalho.renderizar(self.tela)
            
        y_atual += 30
        
        # Linha separadora
        pygame.draw.line(self.tela, CORES['HOVER'], 
                        (x, y_atual), (x + 320, y_atual), 2)
        y_atual += 10
        
        # Entradas do ranking
        for i, partida in enumerate(self.ranking):
            if y_atual > ALTURA - 200:  # Não desenhar fora da tela
                break
                
            # Posição
            cor_posicao = CORES['DESTAQUE'] if i < 3 else CORES['TEXTO']
            emoji_posicao = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
            
            texto_posicao = Texto(
                x_colunas[0], y_atual,
                emoji_posicao,
                FONTES['NORMAL'],
                cor_posicao
            )
            texto_posicao.renderizar(self.tela)
            
            # Pontuação
            texto_pontos = Texto(
                x_colunas[1], y_atual,
                f"{partida.pontuacao:,}",
                FONTES['NORMAL'],
                CORES['DESTAQUE']
            )
            texto_pontos.renderizar(self.tela)
            
            # Nível
            texto_nivel = Texto(
                x_colunas[2], y_atual,
                partida.nivel.title(),
                FONTES['NORMAL'],
                self.cor_por_nivel(partida.nivel)
            )
            texto_nivel.renderizar(self.tela)
            
            # Precisão
            texto_precisao = Texto(
                x_colunas[3], y_atual,
                f"{partida.precisao:.0f}%",
                FONTES['NORMAL'],
                CORES['SUCESSO'] if partida.precisao >= 90 else CORES['AVISO']
            )
            texto_precisao.renderizar(self.tela)
            
            # Tempo
            texto_tempo = Texto(
                x_colunas[4], y_atual,
                f"{partida.tempo_total:.1f}s",
                FONTES['NORMAL'],
                CORES['TEXTO']
            )
            texto_tempo.renderizar(self.tela)
            
            y_atual += espacamento
            
    def cor_por_nivel(self, nivel: str) -> tuple:
        """Retorna cor baseada no nível"""
        cores_nivel = {
            'FACIL': CORES['SUCESSO'],
            'MEDIO': CORES['AVISO'],
            'DIFICIL': CORES['SECUNDARIA'],
            'EXPERT': CORES['PRINCIPAL']
        }
        return cores_nivel.get(nivel, CORES['TEXTO'])
        
    def entrar(self):
        """Chamado ao entrar no estado"""
        self.atualizar_dados()
