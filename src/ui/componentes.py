"""
Componentes avançados de interface do usuário para Merge_Mind
Sistema moderno e profissional de UI
"""
import pygame
import math
from typing import Callable, Optional, Tuple, List, Any, Dict
from enum import Enum
from ..utils.config import CORES, FONTES, VISUAL, ANIMACAO


class EstadoComponente(Enum):
    """Estados possíveis de um componente"""
    NORMAL = "normal"
    HOVER = "hover"
    PRESSIONADO = "pressionado"
    DESABILITADO = "desabilitado"
    FOCADO = "focado"


class TipoAnimacao(Enum):
    """Tipos de animação disponíveis"""
    FADE = "fade"
    SLIDE = "slide"
    BOUNCE = "bounce"
    SCALE = "scale"
    ROTATE = "rotate"


class ComponenteUI:
    """Classe base para componentes de UI com sistema de animação"""
    
    def __init__(self, x: int, y: int, largura: int, altura: int):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.visivel = True
        self.ativo = True
        self.estado = EstadoComponente.NORMAL
        
        # Sistema de animação
        self.animacoes = {}
        self.alpha = 255
        self.escala = 1.0
        self.rotacao = 0.0
        self.offset_x = 0
        self.offset_y = 0
        
        # Eventos e callbacks
        self.callbacks = {}
        
    def adicionar_animacao(self, tipo: TipoAnimacao, duracao: int, 
                          valor_inicial: float, valor_final: float,
                          callback: Optional[Callable] = None) -> None:
        """Adiciona uma animação ao componente"""
        self.animacoes[tipo] = {
            'duracao': duracao,
            'tempo_atual': 0,
            'valor_inicial': valor_inicial,
            'valor_final': valor_final,
            'callback': callback,
            'ativa': True
        }
    
    def atualizar_animacoes(self, dt: float) -> None:
        """Atualiza todas as animações ativas"""
        for tipo, anim in list(self.animacoes.items()):
            if not anim['ativa']:
                continue
                
            anim['tempo_atual'] += dt
            progresso = min(anim['tempo_atual'] / anim['duracao'], 1.0)
            
            # Aplicar easing
            progresso_suave = self._aplicar_easing(progresso)
            
            # Calcular valor atual
            valor_atual = anim['valor_inicial'] + (anim['valor_final'] - anim['valor_inicial']) * progresso_suave
            
            # Aplicar ao componente
            if tipo == TipoAnimacao.FADE:
                self.alpha = int(valor_atual)
            elif tipo == TipoAnimacao.SCALE:
                self.escala = valor_atual
            elif tipo == TipoAnimacao.ROTATE:
                self.rotacao = valor_atual
            elif tipo == TipoAnimacao.SLIDE:
                self.offset_x = valor_atual
            
            # Verificar se terminou
            if progresso >= 1.0:
                anim['ativa'] = False
                if anim['callback']:
                    anim['callback']()
    
    def _aplicar_easing(self, t: float) -> float:
        """Aplica função de easing para animações suaves"""
        # Ease out cubic
        return 1 - (1 - t) ** 3
    
    def processar_evento(self, evento: pygame.event.Event) -> bool:
        """Processa eventos. Retorna True se o evento foi consumido"""
        if not self.visivel or not self.ativo:
            return False
            
        return False
        
    def atualizar(self, dt: float) -> None:
        """Atualiza o componente"""
        self.atualizar_animacoes(dt)
        
    def renderizar(self, tela: pygame.Surface) -> None:
        """Renderiza o componente"""
        if not self.visivel:
            return
    
    def definir_callback(self, evento: str, callback: Callable) -> None:
        """Define callback para evento específico"""
        self.callbacks[evento] = callback
    
    def disparar_callback(self, evento: str, *args, **kwargs) -> None:
        """Dispara callback se existir"""
        if evento in self.callbacks:
            self.callbacks[evento](*args, **kwargs)


class Botao(ComponenteUI):
    """Botão interativo moderno com animações e estados"""
    
    def __init__(self, x: int, y: int, largura: int, altura: int, 
                 texto: str, callback: Optional[Callable] = None,
                 estilo: str = "primario"):
        super().__init__(x, y, largura, altura)
        self.texto = texto
        self.callback = callback
        self.estilo = estilo
        
        # Configurações visuais baseadas no estilo
        self._configurar_estilo()
        
        # Estados visuais
        self.hover = False
        self.pressionado = False
        self.escala_hover = 1.0
        self.brilho_atual = 0
        
        # Fonte e texto
        self.fonte = pygame.font.Font(None, FONTES['BOTAO'])
        self._atualizar_superficie_texto()
        
        # Sombra
        self.sombra_offset = 4
        self.sombra_blur = 8
    
    def _configurar_estilo(self) -> None:
        """Configura cores baseadas no estilo"""
        estilos = {
            "primario": {
                "cor_fundo": CORES['PRINCIPAL'],
                "cor_hover": tuple(min(255, c + 30) for c in CORES['PRINCIPAL']),
                "cor_pressionado": tuple(max(0, c - 30) for c in CORES['PRINCIPAL']),
                "cor_texto": CORES['TEXTO']
            },
            "secundario": {
                "cor_fundo": CORES['SECUNDARIA'],
                "cor_hover": tuple(min(255, c + 30) for c in CORES['SECUNDARIA']),
                "cor_pressionado": tuple(max(0, c - 30) for c in CORES['SECUNDARIA']),
                "cor_texto": CORES['TEXTO']
            },
            "sucesso": {
                "cor_fundo": CORES['SUCESSO'],
                "cor_hover": tuple(min(255, c + 30) for c in CORES['SUCESSO']),
                "cor_pressionado": tuple(max(0, c - 30) for c in CORES['SUCESSO']),
                "cor_texto": CORES['TEXTO']
            },
            "transparente": {
                "cor_fundo": (0, 0, 0, 0),
                "cor_hover": (255, 255, 255, 30),
                "cor_pressionado": (255, 255, 255, 60),
                "cor_texto": CORES['TEXTO']
            }
        }
        
        config = estilos.get(self.estilo, estilos["primario"])
        self.cor_fundo = config["cor_fundo"]
        self.cor_hover = config["cor_hover"]
        self.cor_pressionado = config["cor_pressionado"]
        self.cor_texto = config["cor_texto"]
    
    def _atualizar_superficie_texto(self) -> None:
        """Atualiza a superfície de texto"""
        self.superficie_texto = self.fonte.render(self.texto, True, self.cor_texto)
        self.rect_texto = self.superficie_texto.get_rect(center=self.rect.center)
    
    def processar_evento(self, evento: pygame.event.Event) -> bool:
        """Processa eventos do botão"""
        if not self.visivel or not self.ativo:
            return False
        
        rect_real = pygame.Rect(
            self.rect.x + self.offset_x,
            self.rect.y + self.offset_y,
            self.rect.width * self.escala,
            self.rect.height * self.escala
        )
        
        if evento.type == pygame.MOUSEMOTION:
            novo_hover = rect_real.collidepoint(evento.pos)
            if novo_hover != self.hover:
                self.hover = novo_hover
                if self.hover:
                    self.adicionar_animacao(TipoAnimacao.SCALE, 150, self.escala, 1.05)
                    self.estado = EstadoComponente.HOVER
                else:
                    self.adicionar_animacao(TipoAnimacao.SCALE, 150, self.escala, 1.0)
                    self.estado = EstadoComponente.NORMAL
        
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and rect_real.collidepoint(evento.pos):
                self.pressionado = True
                self.estado = EstadoComponente.PRESSIONADO
                self.adicionar_animacao(TipoAnimacao.SCALE, 100, self.escala, 0.95)
                return True
        
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1 and self.pressionado:
                self.pressionado = False
                if rect_real.collidepoint(evento.pos):
                    self.adicionar_animacao(TipoAnimacao.SCALE, 100, self.escala, 1.05)
                    if self.callback:
                        self.callback()
                    self.disparar_callback('clique')
                else:
                    self.adicionar_animacao(TipoAnimacao.SCALE, 100, self.escala, 1.0)
                self.estado = EstadoComponente.HOVER if self.hover else EstadoComponente.NORMAL
                return True
        
        return False
    
    def renderizar(self, tela: pygame.Surface) -> None:
        """Renderiza o botão com efeitos visuais"""
        if not self.visivel:
            return
        
        # Calcular posição e tamanho com transformações
        x = self.rect.x + self.offset_x
        y = self.rect.y + self.offset_y
        largura = int(self.rect.width * self.escala)
        altura = int(self.rect.height * self.escala)
        
        # Centralizar quando há escala
        x -= (largura - self.rect.width) // 2
        y -= (altura - self.rect.height) // 2
        
        rect_botao = pygame.Rect(x, y, largura, altura)
        
        # Desenhar sombra
        if self.estado != EstadoComponente.PRESSIONADO:
            sombra_rect = pygame.Rect(x + self.sombra_offset, y + self.sombra_offset, largura, altura)
            pygame.draw.rect(tela, (0, 0, 0, 80), sombra_rect, border_radius=VISUAL['RAIO_BORDA'])
        
        # Escolher cor baseada no estado
        if self.estado == EstadoComponente.PRESSIONADO:
            cor_atual = self.cor_pressionado
        elif self.estado == EstadoComponente.HOVER:
            cor_atual = self.cor_hover
        else:
            cor_atual = self.cor_fundo
        
        # Aplicar alpha
        if len(cor_atual) == 3:
            cor_atual = (*cor_atual, self.alpha)
        
        # Desenhar fundo do botão
        pygame.draw.rect(tela, cor_atual, rect_botao, border_radius=VISUAL['RAIO_BORDA'])
        
        # Desenhar borda se estiver focado
        if self.estado == EstadoComponente.FOCADO:
            pygame.draw.rect(tela, CORES['DESTAQUE'], rect_botao, 3, border_radius=VISUAL['RAIO_BORDA'])
        
        # Desenhar texto
        if self.alpha > 0:
            texto_surface = self.superficie_texto.copy()
            if self.alpha < 255:
                texto_surface.set_alpha(self.alpha)
            
            rect_texto_ajustado = self.superficie_texto.get_rect(center=rect_botao.center)
            tela.blit(texto_surface, rect_texto_ajustado)
    
    def definir_texto(self, novo_texto: str) -> None:
        """Atualiza o texto do botão"""
        self.texto = novo_texto
        self._atualizar_superficie_texto()


class Modal(ComponenteUI):
    """Modal/diálogo moderno com overlay"""
    
    def __init__(self, largura: int, altura: int, titulo: str = ""):
        # Centralizar na tela
        from ..utils.config import LARGURA, ALTURA
        x = (LARGURA - largura) // 2
        y = (ALTURA - altura) // 2
        
        super().__init__(x, y, largura, altura)
        self.titulo = titulo
        self.elementos = []
        self.overlay_alpha = 128
        self.fechavel = True
        
        # Configurar título se fornecido
        if titulo:
            self.texto_titulo = Texto(
                self.rect.x + 20, self.rect.y + 20,
                titulo, FONTES['SUBTITULO'], CORES['TEXTO']
            )
    
    def adicionar_elemento(self, elemento: ComponenteUI) -> None:
        """Adiciona elemento ao modal"""
        self.elementos.append(elemento)
    
    def processar_evento(self, evento: pygame.event.Event) -> bool:
        """Processa eventos do modal"""
        if not self.visivel or not self.ativo:
            return False
        
        # Processar elementos filhos
        for elemento in self.elementos:
            if elemento.processar_evento(evento):
                return True
        
        # Clique fora do modal para fechar
        if evento.type == pygame.MOUSEBUTTONDOWN and self.fechavel:
            if not self.rect.collidepoint(evento.pos):
                self.fechar()
                return True
        
        # Impedir que eventos passem para trás do modal
        return True
    
    def fechar(self) -> None:
        """Fecha o modal"""
        self.adicionar_animacao(TipoAnimacao.FADE, 200, self.alpha, 0, 
                               callback=lambda: setattr(self, 'visivel', False))
    
    def abrir(self) -> None:
        """Abre o modal"""
        self.visivel = True
        self.alpha = 0
        self.adicionar_animacao(TipoAnimacao.FADE, 200, 0, 255)
    
    def atualizar(self, dt: float) -> None:
        """Atualiza modal e elementos"""
        super().atualizar(dt)
        for elemento in self.elementos:
            elemento.atualizar(dt)
    
    def renderizar(self, tela: pygame.Surface) -> None:
        """Renderiza o modal"""
        if not self.visivel:
            return
        
        # Overlay
        overlay = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.overlay_alpha))
        tela.blit(overlay, (0, 0))
        
        # Fundo do modal
        pygame.draw.rect(tela, CORES['CARD'], self.rect, border_radius=VISUAL['RAIO_BORDA'])
        pygame.draw.rect(tela, CORES['PRINCIPAL'], self.rect, 3, border_radius=VISUAL['RAIO_BORDA'])
        
        # Título
        if hasattr(self, 'texto_titulo'):
            self.texto_titulo.renderizar(tela)
        
        # Elementos filhos
        for elemento in self.elementos:
            elemento.renderizar(tela)


class ListaScrollavel(ComponenteUI):
    """Lista scrollável de elementos"""
    
    def __init__(self, x: int, y: int, largura: int, altura: int):
        super().__init__(x, y, largura, altura)
        self.elementos = []
        self.scroll_y = 0
        self.velocidade_scroll = 30
        self.altura_conteudo = 0
        
        # Scrollbar
        self.largura_scrollbar = 12
        self.cor_scrollbar = CORES['HOVER']
        self.cor_thumb = CORES['PRINCIPAL']
        self.arrastando_scroll = False
    
    def adicionar_elemento(self, elemento: ComponenteUI) -> None:
        """Adiciona elemento à lista"""
        self.elementos.append(elemento)
        self._calcular_altura_conteudo()
    
    def _calcular_altura_conteudo(self) -> None:
        """Calcula altura total do conteúdo"""
        if not self.elementos:
            self.altura_conteudo = 0
            return
        
        max_y = 0
        for elemento in self.elementos:
            max_y = max(max_y, elemento.rect.bottom)
        
        self.altura_conteudo = max_y - self.rect.y
    
    def processar_evento(self, evento: pygame.event.Event) -> bool:
        """Processa eventos da lista"""
        if not self.visivel or not self.ativo:
            return False
        
        if evento.type == pygame.MOUSEWHEEL and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.scroll_y -= evento.y * self.velocidade_scroll
            self._limitar_scroll()
            return True
        
        # Processar elementos visíveis
        for elemento in self.elementos:
            if self._elemento_visivel(elemento):
                if elemento.processar_evento(evento):
                    return True
        
        return False
    
    def _elemento_visivel(self, elemento: ComponenteUI) -> bool:
        """Verifica se elemento está na área visível"""
        y_elemento = elemento.rect.y - self.scroll_y
        return (y_elemento + elemento.rect.height >= self.rect.y and
                y_elemento <= self.rect.bottom)
    
    def _limitar_scroll(self) -> None:
        """Limita o scroll aos limites do conteúdo"""
        max_scroll = max(0, self.altura_conteudo - self.rect.height)
        self.scroll_y = max(0, min(self.scroll_y, max_scroll))
    
    def atualizar(self, dt: float) -> None:
        """Atualiza lista e elementos"""
        super().atualizar(dt)
        for elemento in self.elementos:
            if self._elemento_visivel(elemento):
                elemento.atualizar(dt)
    
    def renderizar(self, tela: pygame.Surface) -> None:
        """Renderiza a lista com clipping"""
        if not self.visivel:
            return
        
        # Criar superfície para clipping
        clip_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        # Renderizar elementos com offset de scroll
        for elemento in self.elementos:
            if self._elemento_visivel(elemento):
                # Calcular posição relativa ao scroll
                x_rel = elemento.rect.x - self.rect.x
                y_rel = elemento.rect.y - self.rect.y - self.scroll_y
                
                # Criar superfície temporária para o elemento
                elemento_surface = pygame.Surface((elemento.rect.width, elemento.rect.height), pygame.SRCALPHA)
                elemento.renderizar(elemento_surface)
                
                clip_surface.blit(elemento_surface, (x_rel, y_rel))
        
        # Blit superfície com clipping
        tela.blit(clip_surface, self.rect.topleft)
        
        # Renderizar scrollbar se necessário
        if self.altura_conteudo > self.rect.height:
            self._renderizar_scrollbar(tela)
    
    def _renderizar_scrollbar(self, tela: pygame.Surface) -> None:
        """Renderiza a scrollbar"""
        # Posição da scrollbar
        x_scrollbar = self.rect.right - self.largura_scrollbar
        
        # Fundo da scrollbar
        rect_scrollbar = pygame.Rect(x_scrollbar, self.rect.y, self.largura_scrollbar, self.rect.height)
        pygame.draw.rect(tela, self.cor_scrollbar, rect_scrollbar)
        
        # Thumb da scrollbar
        proporcao_visivel = self.rect.height / self.altura_conteudo
        altura_thumb = int(self.rect.height * proporcao_visivel)
        
        proporcao_scroll = self.scroll_y / (self.altura_conteudo - self.rect.height)
        y_thumb = self.rect.y + int((self.rect.height - altura_thumb) * proporcao_scroll)
        
        rect_thumb = pygame.Rect(x_scrollbar, y_thumb, self.largura_scrollbar, altura_thumb)
        pygame.draw.rect(tela, self.cor_thumb, rect_thumb, border_radius=6)


class Tooltip(ComponenteUI):
    """Tooltip para exibir dicas"""
    
    def __init__(self, texto: str, elemento_pai: ComponenteUI):
        self.texto = texto
        self.elemento_pai = elemento_pai
        self.fonte = pygame.font.Font(None, FONTES['PEQUENA'])
        
        # Calcular tamanho do tooltip
        superficie_texto = self.fonte.render(texto, True, CORES['TEXTO'])
        largura = superficie_texto.get_width() + 20
        altura = superficie_texto.get_height() + 12
        
        # Posicionar acima do elemento pai
        x = elemento_pai.rect.centerx - largura // 2
        y = elemento_pai.rect.y - altura - 10
        
        super().__init__(x, y, largura, altura)
        self.superficie_texto = superficie_texto
        self.delay_aparicao = 1000  # ms
        self.tempo_hover = 0
        self.visivel = False
    
    def atualizar(self, dt: float) -> None:
        """Atualiza o tooltip"""
        super().atualizar(dt)
        
        # Verificar se mouse está sobre o elemento pai
        mouse_pos = pygame.mouse.get_pos()
        if self.elemento_pai.rect.collidepoint(mouse_pos):
            self.tempo_hover += dt
            if self.tempo_hover >= self.delay_aparicao:
                self.visivel = True
        else:
            self.tempo_hover = 0
            self.visivel = False
    
    def renderizar(self, tela: pygame.Surface) -> None:
        """Renderiza o tooltip"""
        if not self.visivel:
            return
        
        # Fundo com sombra
        sombra_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width, self.rect.height)
        pygame.draw.rect(tela, (0, 0, 0, 128), sombra_rect, border_radius=6)
        
        # Fundo principal
        pygame.draw.rect(tela, CORES['FUNDO'], self.rect, border_radius=6)
        pygame.draw.rect(tela, CORES['PRINCIPAL'], self.rect, 2, border_radius=6)
        
        # Texto
        pos_texto = (self.rect.x + 10, self.rect.y + 6)
        tela.blit(self.superficie_texto, pos_texto)
        
        # Elementos filhos
        for elemento in self.elementos:
            elemento.renderizar(tela)
        
        self.hover = False
        self.pressionado = False
        self.escala = 1.0
        self.escala_alvo = 1.0
        
    def processar_evento(self, evento: pygame.event.Event) -> bool:
        if not self.ativo or not self.visivel:
            return False
            
        if evento.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(evento.pos)
            self.escala_alvo = 1.05 if self.hover else 1.0
            
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and self.rect.collidepoint(evento.pos):
                self.pressionado = True
                self.escala_alvo = 0.95
                return True
                
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1 and self.pressionado:
                self.pressionado = False
                if self.rect.collidepoint(evento.pos) and self.callback:
                    self.callback()
                self.escala_alvo = 1.05 if self.hover else 1.0
                return True
                
        return False
        
    def atualizar(self, dt: float) -> None:
        # Animação de escala suave
        self.escala += (self.escala_alvo - self.escala) * dt * 8
        
        # Animação de cor
        if self.hover:
            self.cor_atual = self.cor_hover
        else:
            self.cor_atual = self.cor_fundo
            
    def renderizar(self, tela: pygame.Surface) -> None:
        if not self.visivel:
            return
            
        # Calcular rect com escala
        centro = self.rect.center
        largura_escalada = int(self.rect.width * self.escala)
        altura_escalada = int(self.rect.height * self.escala)
        rect_escalado = pygame.Rect(0, 0, largura_escalada, altura_escalada)
        rect_escalado.center = centro
        
        # Desenhar sombra
        sombra_rect = rect_escalado.copy()
        sombra_rect.x += VISUAL['SOMBRA_OFFSET']
        sombra_rect.y += VISUAL['SOMBRA_OFFSET']
        pygame.draw.rect(tela, (0, 0, 0, 100), sombra_rect, border_radius=VISUAL['RAIO_BORDA'])
        
        # Desenhar botão
        pygame.draw.rect(tela, self.cor_atual, rect_escalado, border_radius=VISUAL['RAIO_BORDA'])
        
        # Desenhar borda se hover
        if self.hover:
            pygame.draw.rect(tela, CORES['DESTAQUE'], rect_escalado, 3, border_radius=VISUAL['RAIO_BORDA'])
            
        # Desenhar texto
        rect_texto = self.superficie_texto.get_rect(center=centro)
        tela.blit(self.superficie_texto, rect_texto)


class BlocoNumero(ComponenteUI):
    """Bloco visual para representar números no merge sort"""
    
    def __init__(self, x: int, y: int, numero: int, 
                 cor: Tuple[int, int, int] = CORES['PRINCIPAL']):
        super().__init__(x, y, VISUAL['BLOCO_LARGURA'], VISUAL['BLOCO_ALTURA'])
        self.numero = numero
        self.cor_base = cor
        self.cor_atual = cor
        self.selecionado = False
        self.destacado = False
        
        self.fonte = pygame.font.Font(None, FONTES['NORMAL'])
        self.superficie_texto = self.fonte.render(str(numero), True, CORES['TEXTO'])
        self.rect_texto = self.superficie_texto.get_rect(center=self.rect.center)
        
        self.escala = 1.0
        self.escala_alvo = 1.0
        self.rotacao = 0.0
        self.animando = False
        
    def selecionar(self) -> None:
        """Marca o bloco como selecionado"""
        self.selecionado = True
        self.escala_alvo = 1.1
        
    def desselecionar(self) -> None:
        """Remove a seleção do bloco"""
        self.selecionado = False
        self.escala_alvo = 1.0
        
    def destacar(self, destacar: bool = True) -> None:
        """Destaca ou remove destaque do bloco"""
        self.destacado = destacar
        
    def animar_entrada(self) -> None:
        """Inicia animação de entrada"""
        self.escala = 0.0
        self.escala_alvo = 1.0
        self.animando = True
        
    def processar_evento(self, evento: pygame.event.Event) -> bool:
        if not self.ativo or not self.visivel:
            return False
            
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and self.rect.collidepoint(evento.pos):
                return True
                
        return False
        
    def atualizar(self, dt: float) -> None:
        # Animação de escala
        self.escala += (self.escala_alvo - self.escala) * dt * 10
        
        # Animação de cor
        if self.selecionado:
            self.cor_atual = CORES['DESTAQUE']
        elif self.destacado:
            self.cor_atual = CORES['SUCESSO']
        else:
            self.cor_atual = self.cor_base
            
        # Parar animação quando próximo do alvo
        if abs(self.escala - self.escala_alvo) < 0.01:
            self.animando = False
            
    def renderizar(self, tela: pygame.Surface) -> None:
        if not self.visivel or self.escala <= 0:
            return
            
        # Calcular rect com escala
        centro = self.rect.center
        largura_escalada = int(self.rect.width * self.escala)
        altura_escalada = int(self.rect.height * self.escala)
        rect_escalado = pygame.Rect(0, 0, largura_escalada, altura_escalada)
        rect_escalado.center = centro
        
        # Desenhar sombra
        sombra_rect = rect_escalado.copy()
        sombra_rect.x += VISUAL['SOMBRA_OFFSET']
        sombra_rect.y += VISUAL['SOMBRA_OFFSET']
        pygame.draw.rect(tela, (0, 0, 0, 100), sombra_rect, border_radius=VISUAL['RAIO_BORDA'])
        
        # Desenhar bloco
        pygame.draw.rect(tela, self.cor_atual, rect_escalado, border_radius=VISUAL['RAIO_BORDA'])
        
        # Desenhar borda se selecionado
        if self.selecionado:
            pygame.draw.rect(tela, CORES['TEXTO'], rect_escalado, 3, border_radius=VISUAL['RAIO_BORDA'])
            
        # Desenhar número
        rect_texto = self.superficie_texto.get_rect(center=centro)
        tela.blit(self.superficie_texto, rect_texto)


class BarraProgresso(ComponenteUI):
    """Barra de progresso animada"""
    
    def __init__(self, x: int, y: int, largura: int, altura: int,
                 valor_max: float = 100.0):
        super().__init__(x, y, largura, altura)
        self.valor_max = valor_max
        self.valor_atual = 0.0
        self.valor_alvo = 0.0
        
    def definir_valor(self, valor: float) -> None:
        """Define o valor alvo da barra"""
        self.valor_alvo = max(0, min(valor, self.valor_max))
        
    def atualizar(self, dt: float) -> None:
        # Animação suave do valor
        self.valor_atual += (self.valor_alvo - self.valor_atual) * dt * 5
        
    def renderizar(self, tela: pygame.Surface) -> None:
        if not self.visivel:
            return
            
        # Fundo da barra
        pygame.draw.rect(tela, CORES['CARD'], self.rect, border_radius=VISUAL['RAIO_BORDA'])
        
        # Barra de progresso
        if self.valor_atual > 0:
            largura_progresso = int((self.valor_atual / self.valor_max) * self.rect.width)
            rect_progresso = pygame.Rect(self.rect.x, self.rect.y, largura_progresso, self.rect.height)
            pygame.draw.rect(tela, CORES['SUCESSO'], rect_progresso, border_radius=VISUAL['RAIO_BORDA'])
            
        # Borda
        pygame.draw.rect(tela, CORES['TEXTO'], self.rect, 2, border_radius=VISUAL['RAIO_BORDA'])


class Texto(ComponenteUI):
    """Componente de texto com formatação"""
    
    def __init__(self, x: int, y: int, texto: str, 
                 tamanho_fonte: int = FONTES['NORMAL'],
                 cor: Tuple[int, int, int] = CORES['TEXTO'],
                 centralizado: bool = False):
        self.texto = texto
        self.tamanho_fonte = tamanho_fonte
        self.cor = cor
        self.centralizado = centralizado
        
        self.fonte = pygame.font.Font(None, tamanho_fonte)
        self.superficie = self.fonte.render(texto, True, cor)
        
        if centralizado:
            rect = self.superficie.get_rect(center=(x, y))
            super().__init__(rect.x, rect.y, rect.width, rect.height)
        else:
            super().__init__(x, y, self.superficie.get_width(), self.superficie.get_height())
            
    def definir_texto(self, novo_texto: str) -> None:
        """Atualiza o texto"""
        self.texto = novo_texto
        self.superficie = self.fonte.render(novo_texto, True, self.cor)
        
        if self.centralizado:
            centro_atual = self.rect.center
            self.rect = self.superficie.get_rect(center=centro_atual)
        else:
            self.rect.width = self.superficie.get_width()
            self.rect.height = self.superficie.get_height()
            
    def renderizar(self, tela: pygame.Surface) -> None:
        if not self.visivel:
            return
        tela.blit(self.superficie, self.rect)
