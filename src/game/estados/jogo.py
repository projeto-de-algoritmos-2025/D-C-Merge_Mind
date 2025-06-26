"""
Estado principal do jogo - Merge Sort Interativo
"""
import pygame
import random
import time
from typing import List, Optional, Tuple
from ..estado_manager import Estado
from ...ui.componentes import BlocoNumero, Texto, BarraProgresso, Botao
from ...utils.config import CORES, FONTES, LARGURA, ALTURA, VISUAL, NIVEIS, JOGO
from ..pontuacao import SistemaPontuacao


class EstadoJogo(Estado):
    """Estado principal do jogo com Merge Sort interativo"""
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.pontuacao_sistema = SistemaPontuacao()
        self.resetar_jogo()
        
    def resetar_jogo(self):
        """Reseta o estado do jogo"""
        self.lista_original = []
        self.sublistas = []
        self.resultado_atual = []
        self.fase_atual = 0
        self.subfase_atual = 0
        self.aguardando_resposta = False
        self.elementos_comparacao = []
        self.tempo_resposta_inicio = 0
        self.blocos_numeros = []
        self.nivel = 'FACIL'
        self.animando = False
        self.jogo_concluido = False
        self.jogo_pausado = False
        
        # UI
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """Inicializa elementos da interface do jogo"""
        # Textos informativos
        self.texto_instrucao = Texto(
            LARGURA // 2, 50,
            "Clique no MENOR número para ordenar:",
            FONTES['NORMAL'],
            CORES['TEXTO'],
            centralizado=True
        )
        
        self.texto_pontuacao = Texto(
            50, 30,
            "Pontos: 0",
            FONTES['NORMAL'],
            CORES['DESTAQUE']
        )
        
        self.texto_nivel = Texto(
            LARGURA - 200, 30,
            "Nível: Fácil",
            FONTES['NORMAL'],
            CORES['TEXTO']
        )
        
        # Barra de progresso
        self.barra_progresso = BarraProgresso(
            LARGURA // 2 - 200, 100,
            400, 20,
            100
        )
        
        # Botões de controle
        self.botao_pausa = Botao(
            LARGURA - 120, 70,
            100, 40,
            "⏸ Pausa",
            self.pausar_jogo,
            CORES['AVISO']
        )
        
        self.botao_reiniciar = Botao(
            LARGURA - 240, 70,
            100, 40,
            "🔄 Novo",
            self.reiniciar_jogo,
            CORES['SECUNDARIA']
        )
        
    def iniciar_novo_jogo(self, nivel: str):
        """Inicia um novo jogo com o nível especificado"""
        self.nivel = nivel
        config_nivel = NIVEIS[nivel]
        
        # Gerar lista aleatória
        quantidade = config_nivel['elementos']
        self.lista_original = random.sample(range(JOGO['MIN_VALOR'], JOGO['MAX_VALOR']), quantidade)
        
        # Inicializar sublistas (cada elemento em sua própria lista)
        self.sublistas = [[num] for num in self.lista_original]
        self.fase_atual = 0
        self.subfase_atual = 0
        self.jogo_concluido = False
        self.jogo_pausado = False
        
        # Inicializar sistema de pontuação
        self.pontuacao_sistema.iniciar_partida(nivel, quantidade)
        
        # Atualizar UI
        self.texto_nivel.definir_texto(f"Nível: {config_nivel['nome']}")
        self.atualizar_pontuacao_ui()
        self.atualizar_progresso()
        
        # Preparar primeira fusão
        self.preparar_proxima_fusao()
        
    def preparar_proxima_fusao(self):
        """Prepara a próxima operação de fusão"""
        if len(self.sublistas) <= 1:
            self.concluir_jogo()
            return
            
        # Encontrar próximo par para fusão
        if self.subfase_atual >= len(self.sublistas) // 2:
            # Passar para próxima fase
            self.fase_atual += 1
            self.subfase_atual = 0
            self.atualizar_progresso()
            
        # Se há listas ímpares, mover a última para próxima rodada
        nova_lista = []
        for i in range(0, len(self.sublistas) - 1, 2):
            # Fusão das listas i e i+1 será feita interativamente
            pass
            
        if len(self.sublistas) % 2 == 1:
            # Lista ímpar vai direto para próxima rodada
            pass
            
        self.iniciar_fusao_interativa()
        
    def iniciar_fusao_interativa(self):
        """Inicia o processo de fusão interativa"""
        if self.subfase_atual * 2 + 1 >= len(self.sublistas):
            # Não há mais pares para fusão nesta fase
            self.finalizar_fase()
            return
            
        # Pegar as duas sublistas para fusão
        idx1 = self.subfase_atual * 2
        idx2 = self.subfase_atual * 2 + 1
        
        self.lista1 = self.sublistas[idx1].copy()
        self.lista2 = self.sublistas[idx2].copy()
        self.resultado_fusao = []
        self.i = 0  # Índice para lista1
        self.j = 0  # Índice para lista2
        
        self.aguardando_resposta = True
        self.apresentar_comparacao()
        
    def apresentar_comparacao(self):
        """Apresenta os dois elementos para comparação"""
        if self.i >= len(self.lista1):
            # Terminou lista1, adicionar resto da lista2
            self.resultado_fusao.extend(self.lista2[self.j:])
            self.finalizar_fusao()
            return
            
        if self.j >= len(self.lista2):
            # Terminou lista2, adicionar resto da lista1
            self.resultado_fusao.extend(self.lista1[self.i:])
            self.finalizar_fusao()
            return
            
        # Apresentar elementos para comparação
        self.elementos_comparacao = [
            (self.lista1[self.i], 'lista1'),
            (self.lista2[self.j], 'lista2')
        ]
        
        self.tempo_resposta_inicio = time.time()
        self.atualizar_blocos_visuais()
        
        # Atualizar instrução
        self.texto_instrucao.definir_texto(
            f"Clique no MENOR número: {self.lista1[self.i]} ou {self.lista2[self.j]}"
        )
        
    def processar_escolha(self, valor_escolhido: int) -> bool:
        """Processa a escolha do jogador"""
        if not self.aguardando_resposta:
            return False
            
        valor1, valor2 = self.lista1[self.i], self.lista2[self.j]
        escolha_correta = min(valor1, valor2)
        tempo_resposta = time.time() - self.tempo_resposta_inicio
        
        if valor_escolhido == escolha_correta:
            # Resposta correta
            pontos = self.pontuacao_sistema.registrar_acerto(tempo_resposta)
            self.mostrar_feedback(f"+{pontos} pontos!", CORES['SUCESSO'])
            self.game_manager.audio.tocar_som('acerto')
            
            # Adicionar elemento correto ao resultado
            self.resultado_fusao.append(valor_escolhido)
            
            # Avançar índices
            if valor_escolhido == valor1:
                self.i += 1
            else:
                self.j += 1
                
        else:
            # Resposta incorreta
            penalidade = self.pontuacao_sistema.registrar_erro()
            self.mostrar_feedback(f"{penalidade} pontos", CORES['SECUNDARIA'])
            self.game_manager.audio.tocar_som('erro')
            
        self.atualizar_pontuacao_ui()
        
        # Continuar com próxima comparação
        self.apresentar_comparacao()
        return True
        
    def finalizar_fusao(self):
        """Finaliza a fusão atual"""
        self.aguardando_resposta = False
        
        # Substituir as duas sublistas pelo resultado
        idx = self.subfase_atual * 2
        self.sublistas[idx:idx+2] = [self.resultado_fusao]
        
        # Próxima subfase
        self.subfase_atual += 1
        
        # Mostrar resultado da fusão
        self.mostrar_resultado_fusao()
        
        # Preparar próxima fusão após delay
        pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # 1.5 segundos
        
    def finalizar_fase(self):
        """Finaliza a fase atual"""
        # Reorganizar sublistas para próxima fase
        novas_sublistas = []
        for i in range(0, len(self.sublistas), 2):
            if i + 1 < len(self.sublistas):
                # Par será fundido na próxima fase
                novas_sublistas.extend([self.sublistas[i], self.sublistas[i+1]])
            else:
                # Lista ímpar passa direto
                novas_sublistas.append(self.sublistas[i])
                
        self.sublistas = novas_sublistas
        self.subfase_atual = 0
        self.preparar_proxima_fusao()
        
    def concluir_jogo(self):
        """Conclui o jogo"""
        self.jogo_concluido = True
        self.aguardando_resposta = False
        
        # Finalizar pontuação
        stats = self.pontuacao_sistema.finalizar_partida(True)
        
        # Tocar som de sucesso
        self.game_manager.audio.tocar_som('sucesso')
        
        # Mostrar resultado final
        self.texto_instrucao.definir_texto(
            f"🎉 Parabéns! Lista ordenada! Pontuação final: {stats.pontuacao}"
        )
        
        # Atualizar progresso para 100%
        self.barra_progresso.definir_valor(100)
        
    def mostrar_feedback(self, texto: str, cor: Tuple[int, int, int]):
        """Mostra feedback visual temporário"""
        # Implementação simples - poderia ser mais elaborada
        self.feedback_texto = Texto(
            LARGURA // 2, 180,
            texto,
            FONTES['NORMAL'],
            cor,
            centralizado=True
        )
        
    def mostrar_resultado_fusao(self):
        """Mostra o resultado da fusão atual"""
        resultado_str = " ".join(map(str, self.resultado_fusao))
        self.texto_instrucao.definir_texto(f"Resultado da fusão: [{resultado_str}]")
        
    def atualizar_blocos_visuais(self):
        """Atualiza a representação visual dos blocos"""
        self.blocos_numeros.clear()
        
        if not self.elementos_comparacao:
            return
            
        # Posicionar blocos para comparação
        largura_total = 2 * VISUAL['BLOCO_LARGURA'] + VISUAL['ESPACO_BLOCO']
        x_inicial = (LARGURA - largura_total) // 2
        y = 250
        
        for i, (valor, origem) in enumerate(self.elementos_comparacao):
            x = x_inicial + i * (VISUAL['BLOCO_LARGURA'] + VISUAL['ESPACO_BLOCO'])
            cor = CORES['SUCESSO'] if origem == 'lista1' else CORES['SECUNDARIA']
            
            bloco = BlocoNumero(x, y, valor, cor)
            bloco.destacar(True)
            self.blocos_numeros.append(bloco)
            
    def atualizar_pontuacao_ui(self):
        """Atualiza a exibição da pontuação"""
        self.texto_pontuacao.definir_texto(f"Pontos: {self.pontuacao_sistema.pontuacao_atual}")
        
    def atualizar_progresso(self):
        """Atualiza a barra de progresso"""
        if not self.lista_original:
            return
            
        # Calcular progresso baseado no número de sublistas restantes
        total_elementos = len(self.lista_original)
        sublistas_restantes = len(self.sublistas)
        
        if sublistas_restantes <= 1:
            progresso = 100
        else:
            # Progresso baseado na redução do número de sublistas
            progresso = ((total_elementos - sublistas_restantes) / (total_elementos - 1)) * 100
            
        self.barra_progresso.definir_valor(progresso)
        
    def pausar_jogo(self):
        """Pausa/despausa o jogo"""
        self.jogo_pausado = not self.jogo_pausado
        texto_botao = "▶ Continuar" if self.jogo_pausado else "⏸ Pausa"
        self.botao_pausa.texto = texto_botao
        self.botao_pausa.superficie_texto = self.botao_pausa.fonte.render(texto_botao, True, self.botao_pausa.cor_texto)
        
    def reiniciar_jogo(self):
        """Reinicia o jogo com o mesmo nível"""
        self.game_manager.audio.tocar_som('clique')
        self.iniciar_novo_jogo(self.nivel)
        
    def processar_eventos(self, eventos):
        """Processa eventos do jogo"""
        if self.jogo_pausado:
            # Apenas processar despause
            for evento in eventos:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    self.pausar_jogo()
                elif self.botao_pausa.processar_evento(evento):
                    self.game_manager.audio.tocar_som('clique')
            return
            
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.game_manager.rodando = False
                
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.game_manager.gerenciador_estados.mudar_estado('menu')
                elif evento.key == pygame.K_SPACE:
                    self.pausar_jogo()
                elif evento.key == pygame.K_r:
                    self.reiniciar_jogo()
                    
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1 and self.aguardando_resposta:
                    # Verificar clique nos blocos
                    mouse_pos = evento.pos
                    for bloco in self.blocos_numeros:
                        if bloco.rect.collidepoint(mouse_pos):
                            self.processar_escolha(bloco.numero)
                            break
                            
            elif evento.type == pygame.USEREVENT + 1:
                # Timer para próxima fusão
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancelar timer
                self.preparar_proxima_fusao()
                
            # Processar eventos dos botões
            if self.botao_pausa.processar_evento(evento):
                self.game_manager.audio.tocar_som('clique')
            if self.botao_reiniciar.processar_evento(evento):
                pass  # Já processado no callback
                
    def atualizar(self, dt):
        """Atualiza o estado do jogo"""
        if self.jogo_pausado:
            return
            
        # Atualizar componentes UI
        self.barra_progresso.atualizar(dt)
        self.botao_pausa.atualizar(dt)
        self.botao_reiniciar.atualizar(dt)
        
        # Atualizar blocos
        for bloco in self.blocos_numeros:
            bloco.atualizar(dt)
            
    def renderizar(self):
        """Renderiza o estado do jogo"""
        # Fundo
        self.tela.fill(CORES['FUNDO'])
        
        # Overlay de pausa
        if self.jogo_pausado:
            # Escurecer tela
            overlay = pygame.Surface((LARGURA, ALTURA))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.tela.blit(overlay, (0, 0))
            
            # Texto de pausa
            texto_pausa = Texto(
                LARGURA // 2, ALTURA // 2,
                "JOGO PAUSADO\nPressione ESPAÇO para continuar",
                FONTES['TITULO'],
                CORES['TEXTO'],
                centralizado=True
            )
            texto_pausa.renderizar(self.tela)
            self.botao_pausa.renderizar(self.tela)
            return
            
        # UI do jogo
        self.texto_instrucao.renderizar(self.tela)
        self.texto_pontuacao.renderizar(self.tela)
        self.texto_nivel.renderizar(self.tela)
        self.barra_progresso.renderizar(self.tela)
        self.botao_pausa.renderizar(self.tela)
        self.botao_reiniciar.renderizar(self.tela)
        
        # Blocos de números
        for bloco in self.blocos_numeros:
            bloco.renderizar(self.tela)
            
        # Feedback temporário
        if hasattr(self, 'feedback_texto'):
            self.feedback_texto.renderizar(self.tela)
            
        # Sublistas atuais (visualização do estado)
        self.renderizar_sublistas()
        
        # Instruções
        if not self.jogo_concluido:
            instrucoes = Texto(
                LARGURA // 2, ALTURA - 50,
                "ESC: Menu | ESPAÇO: Pausa | R: Reiniciar",
                FONTES['PEQUENA'],
                CORES['HOVER'],
                centralizado=True
            )
            instrucoes.renderizar(self.tela)
            
    def renderizar_sublistas(self):
        """Renderiza as sublistas atuais em formato visual"""
        if not self.sublistas:
            return
            
        y_base = 400
        max_sublistas_por_linha = 6
        
        for linha_idx in range((len(self.sublistas) + max_sublistas_por_linha - 1) // max_sublistas_por_linha):
            y = y_base + linha_idx * 80
            inicio_idx = linha_idx * max_sublistas_por_linha
            fim_idx = min(inicio_idx + max_sublistas_por_linha, len(self.sublistas))
            sublistas_linha = self.sublistas[inicio_idx:fim_idx]
            
            # Calcular largura total necessária
            largura_total = 0
            for sublista in sublistas_linha:
                largura_sublista = len(sublista) * (VISUAL['BLOCO_LARGURA'] + 5) + 20
                largura_total += largura_sublista
                
            x_inicial = (LARGURA - largura_total) // 2
            x_atual = x_inicial
            
            for sublista in sublistas_linha:
                # Desenhar cada sublista
                for i, num in enumerate(sublista):
                    x = x_atual + i * (VISUAL['BLOCO_LARGURA'] + 5)
                    bloco = BlocoNumero(x, y, num, CORES['CARD'])
                    bloco.renderizar(self.tela)
                    
                x_atual += len(sublista) * (VISUAL['BLOCO_LARGURA'] + 5) + 20
                
    def entrar(self):
        """Chamado ao entrar no estado"""
        # Iniciar jogo com nível selecionado
        nivel = getattr(self.game_manager, 'nivel_selecionado', 'FACIL')
        self.iniciar_novo_jogo(nivel)
        
    def sair(self):
        """Chamado ao sair do estado"""
        # Cancelar timers
        pygame.time.set_timer(pygame.USEREVENT + 1, 0)
