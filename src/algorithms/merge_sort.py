"""
Implementação educativa do algoritmo Merge Sort
Com visualização e interação para fins didáticos
"""

import copy
from typing import List, Tuple, Optional, Callable
from enum import Enum


class FaseMergeSort(Enum):
    """Fases do algoritmo Merge Sort"""
    INICIALIZACAO = "inicializacao"
    DIVISAO = "divisao"
    CONQUISTA = "conquista"
    FUSAO = "fusao"
    FINALIZACAO = "finalizacao"


class EstadoFusao(Enum):
    """Estados possíveis durante a fusão"""
    AGUARDANDO_ESCOLHA = "aguardando_escolha"
    PROCESSANDO = "processando"
    COMPLETADA = "completada"


class MergeSortEducativo:
    """
    Implementação educativa do Merge Sort com suporte a visualização
    e interação do usuário durante o processo de fusão
    """
    
    def __init__(self, lista_original: List[int], callback_visual: Optional[Callable] = None):
        self.lista_original = copy.deepcopy(lista_original)
        self.callback_visual = callback_visual
        
        # Estado atual do algoritmo
        self.fase_atual = FaseMergeSort.INICIALIZACAO
        self.sublistas = []
        self.nivel_atual = 0
        self.fusoes_realizadas = 0
        self.comparacoes_realizadas = 0
        self.decisoes_corretas = 0
        self.tempo_inicio = None
        
        # Estado da fusão atual
        self.estado_fusao = EstadoFusao.COMPLETADA
        self.lista_esquerda = []
        self.lista_direita = []
        self.indice_esquerda = 0
        self.indice_direita = 0
        self.resultado_fusao = []
        
        # Histórico para análise
        self.historico_divisoes = []
        self.historico_fusoes = []
        self.historico_comparacoes = []
        
    def inicializar(self) -> None:
        """Inicializa o processo do Merge Sort"""
        self.fase_atual = FaseMergeSort.DIVISAO
        # Criar sublistas individuais
        self.sublistas = [[elemento] for elemento in self.lista_original]
        self.nivel_atual = 0
        self.fusoes_realizadas = 0
        self.comparacoes_realizadas = 0
        self.decisoes_corretas = 0
        
        # Registrar divisão inicial
        self.historico_divisoes.append({
            'nivel': 0,
            'sublistas': copy.deepcopy(self.sublistas)
        })
        
        if self.callback_visual:
            self.callback_visual('divisao_inicial', {
                'sublistas': self.sublistas,
                'nivel': self.nivel_atual
            })
    
    def proximo_passo(self) -> bool:
        """
        Executa o próximo passo do algoritmo
        Retorna True se ainda há passos a executar
        """
        if self.fase_atual == FaseMergeSort.INICIALIZACAO:
            self.inicializar()
            return True
            
        elif self.fase_atual == FaseMergeSort.DIVISAO:
            if len(self.sublistas) <= 1:
                self.fase_atual = FaseMergeSort.FINALIZACAO
                return False
            else:
                self.fase_atual = FaseMergeSort.CONQUISTA
                return True
                
        elif self.fase_atual == FaseMergeSort.CONQUISTA:
            return self._processar_nivel_atual()
            
        elif self.fase_atual == FaseMergeSort.FUSAO:
            return self._continuar_fusao()
            
        return False
    
    def _processar_nivel_atual(self) -> bool:
        """Processa todas as fusões do nível atual"""
        novas_sublistas = []
        i = 0
        
        while i < len(self.sublistas):
            if i + 1 < len(self.sublistas):
                # Iniciar fusão entre sublistas[i] e sublistas[i+1]
                self._iniciar_fusao(self.sublistas[i], self.sublistas[i+1])
                return True
            else:
                # Sublista ímpar, passa para o próximo nível
                novas_sublistas.append(self.sublistas[i])
                i += 1
        
        self.sublistas = novas_sublistas
        self.nivel_atual += 1
        
        if len(self.sublistas) <= 1:
            self.fase_atual = FaseMergeSort.FINALIZACAO
            return False
        
        return True
    
    def _iniciar_fusao(self, lista_esq: List[int], lista_dir: List[int]) -> None:
        """Inicia o processo de fusão entre duas sublistas"""
        self.fase_atual = FaseMergeSort.FUSAO
        self.estado_fusao = EstadoFusao.AGUARDANDO_ESCOLHA
        
        self.lista_esquerda = copy.deepcopy(lista_esq)
        self.lista_direita = copy.deepcopy(lista_dir)
        self.indice_esquerda = 0
        self.indice_direita = 0
        self.resultado_fusao = []
        
        if self.callback_visual:
            self.callback_visual('iniciar_fusao', {
                'lista_esquerda': self.lista_esquerda,
                'lista_direita': self.lista_direita,
                'nivel': self.nivel_atual
            })
    
    def fazer_escolha(self, escolher_esquerda: bool) -> Tuple[bool, str]:
        """
        Usuário faz uma escolha durante a fusão
        
        Args:
            escolher_esquerda: True para escolher da lista esquerda, False para direita
            
        Returns:
            Tuple[bool, str]: (escolha_correta, mensagem_feedback)
        """
        if (self.fase_atual != FaseMergeSort.FUSAO or 
            self.estado_fusao != EstadoFusao.AGUARDANDO_ESCOLHA):
            return False, "Não é possível fazer escolha neste momento"
        
        # Verificar se ainda há elementos para comparar
        if (self.indice_esquerda >= len(self.lista_esquerda) or 
            self.indice_direita >= len(self.lista_direita)):
            return self._finalizar_fusao_automatica()
        
        elemento_esq = self.lista_esquerda[self.indice_esquerda]
        elemento_dir = self.lista_direita[self.indice_direita]
        
        escolha_correta = (escolher_esquerda and elemento_esq <= elemento_dir) or \
                         (not escolher_esquerda and elemento_dir < elemento_esq)
        
        self.comparacoes_realizadas += 1
        
        if escolha_correta:
            self.decisoes_corretas += 1
            if escolher_esquerda:
                self.resultado_fusao.append(elemento_esq)
                self.indice_esquerda += 1
                mensagem = f"Correto! {elemento_esq} é menor que {elemento_dir}"
            else:
                self.resultado_fusao.append(elemento_dir)
                self.indice_direita += 1
                mensagem = f"Correto! {elemento_dir} é menor que {elemento_esq}"
        else:
            # Fazer a escolha correta automaticamente após feedback
            if elemento_esq <= elemento_dir:
                self.resultado_fusao.append(elemento_esq)
                self.indice_esquerda += 1
                mensagem = f"Ops! {elemento_esq} é menor que {elemento_dir}"
            else:
                self.resultado_fusao.append(elemento_dir)
                self.indice_direita += 1
                mensagem = f"Ops! {elemento_dir} é menor que {elemento_esq}"
        
        # Registrar comparação
        self.historico_comparacoes.append({
            'elemento_esq': elemento_esq,
            'elemento_dir': elemento_dir,
            'escolha_usuario': escolher_esquerda,
            'escolha_correta': escolha_correta,
            'nivel': self.nivel_atual
        })
        
        if self.callback_visual:
            self.callback_visual('escolha_feita', {
                'escolha_correta': escolha_correta,
                'mensagem': mensagem,
                'resultado_parcial': copy.deepcopy(self.resultado_fusao),
                'elemento_escolhido': self.resultado_fusao[-1]
            })
        
        # Verificar se a fusão está completa
        if (self.indice_esquerda >= len(self.lista_esquerda) and 
            self.indice_direita >= len(self.lista_direita)):
            return self._finalizar_fusao()
        elif (self.indice_esquerda >= len(self.lista_esquerda) or 
              self.indice_direita >= len(self.lista_direita)):
            return self._finalizar_fusao_automatica()
        
        return escolha_correta, mensagem
    
    def _finalizar_fusao_automatica(self) -> Tuple[bool, str]:
        """Finaliza a fusão automaticamente quando uma lista se esgota"""
        # Adicionar elementos restantes
        self.resultado_fusao.extend(self.lista_esquerda[self.indice_esquerda:])
        self.resultado_fusao.extend(self.lista_direita[self.indice_direita:])
        
        return self._finalizar_fusao()
    
    def _finalizar_fusao(self) -> Tuple[bool, str]:
        """Finaliza o processo de fusão atual"""
        self.estado_fusao = EstadoFusao.COMPLETADA
        self.fusoes_realizadas += 1
        
        # Registrar fusão no histórico
        self.historico_fusoes.append({
            'lista_esquerda': copy.deepcopy(self.lista_esquerda),
            'lista_direita': copy.deepcopy(self.lista_direita),
            'resultado': copy.deepcopy(self.resultado_fusao),
            'nivel': self.nivel_atual
        })
        
        # Atualizar sublistas com o resultado
        self._atualizar_sublistas_com_resultado()
        
        if self.callback_visual:
            self.callback_visual('fusao_completa', {
                'resultado': copy.deepcopy(self.resultado_fusao),
                'sublistas_atualizadas': copy.deepcopy(self.sublistas),
                'nivel': self.nivel_atual
            })
        
        # Voltar para fase de conquista
        self.fase_atual = FaseMergeSort.CONQUISTA
        
        return True, "Fusão completada!"
    
    def _atualizar_sublistas_com_resultado(self) -> None:
        """Atualiza as sublistas com o resultado da fusão"""
        novas_sublistas = []
        encontrou_fusao = False
        
        i = 0
        while i < len(self.sublistas):
            if (not encontrou_fusao and 
                i + 1 < len(self.sublistas) and
                self.sublistas[i] == self.lista_esquerda and
                self.sublistas[i + 1] == self.lista_direita):
                # Substituir as duas sublistas pelo resultado
                novas_sublistas.append(copy.deepcopy(self.resultado_fusao))
                encontrou_fusao = True
                i += 2
            else:
                novas_sublistas.append(self.sublistas[i])
                i += 1
        
        self.sublistas = novas_sublistas
    
    def obter_proxima_comparacao(self) -> Optional[Tuple[int, int]]:
        """
        Retorna os próximos elementos a serem comparados
        
        Returns:
            Tuple[int, int] ou None se não há comparação pendente
        """
        if (self.fase_atual == FaseMergeSort.FUSAO and 
            self.estado_fusao == EstadoFusao.AGUARDANDO_ESCOLHA and
            self.indice_esquerda < len(self.lista_esquerda) and
            self.indice_direita < len(self.lista_direita)):
            
            return (self.lista_esquerda[self.indice_esquerda], 
                   self.lista_direita[self.indice_direita])
        
        return None
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas do processo de ordenação"""
        total_comparacoes = len(self.historico_comparacoes)
        precisao = (self.decisoes_corretas / total_comparacoes * 100 
                   if total_comparacoes > 0 else 0)
        
        return {
            'fase_atual': self.fase_atual.value,
            'nivel_atual': self.nivel_atual,
            'fusoes_realizadas': self.fusoes_realizadas,
            'comparacoes_realizadas': self.comparacoes_realizadas,
            'decisoes_corretas': self.decisoes_corretas,
            'precisao': round(precisao, 2),
            'elementos_restantes': sum(len(sublista) for sublista in self.sublistas),
            'sublistas_restantes': len(self.sublistas),
            'esta_completo': len(self.sublistas) <= 1
        }
    
    def obter_resultado_final(self) -> Optional[List[int]]:
        """Retorna o resultado final se a ordenação estiver completa"""
        if len(self.sublistas) == 1:
            return copy.deepcopy(self.sublistas[0])
        return None
    
    def reiniciar(self) -> None:
        """Reinicia o algoritmo para uma nova execução"""
        self.__init__(self.lista_original, self.callback_visual)
