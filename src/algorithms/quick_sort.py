"""
Implementação educativa do algoritmo Quick Sort
Com visualização e interação para fins didáticos
"""

import copy
from typing import List, Tuple, Optional, Callable
from enum import Enum


class FaseQuickSort(Enum):
    """Fases do algoritmo Quick Sort"""
    INICIALIZACAO = "inicializacao"
    ESCOLHA_PIVOT = "escolha_pivot"
    PARTICAO = "particao"
    RECURSAO = "recursao"
    FINALIZACAO = "finalizacao"


class QuickSortEducativo:
    """
    Implementação educativa do Quick Sort com suporte a visualização
    e interação do usuário durante o processo de particionamento
    """
    
    def __init__(self, lista_original: List[int], callback_visual: Optional[Callable] = None):
        self.lista_original = copy.deepcopy(lista_original)
        self.callback_visual = callback_visual
        self.lista_atual = copy.deepcopy(lista_original)
        
        # Pilha para simular recursão
        self.pilha_recursao = [(0, len(lista_original) - 1)]
        
        # Estado atual
        self.fase_atual = FaseQuickSort.INICIALIZACAO
        self.inicio_atual = 0
        self.fim_atual = 0
        self.pivot_atual = 0
        self.i_atual = 0
        self.j_atual = 0
        
        # Estatísticas
        self.comparacoes_realizadas = 0
        self.trocas_realizadas = 0
        self.decisoes_corretas = 0
        self.nivel_recursao = 0
        
        # Histórico
        self.historico_pivots = []
        self.historico_particoes = []
        self.historico_trocas = []
    
    def inicializar(self) -> None:
        """Inicializa o processo do Quick Sort"""
        if not self.pilha_recursao:
            self.fase_atual = FaseQuickSort.FINALIZACAO
            return
            
        self.inicio_atual, self.fim_atual = self.pilha_recursao.pop()
        
        if self.inicio_atual < self.fim_atual:
            self.fase_atual = FaseQuickSort.ESCOLHA_PIVOT
            self.pivot_atual = self.fim_atual  # Pivot sempre o último elemento
            
            if self.callback_visual:
                self.callback_visual('inicializar_particao', {
                    'lista': copy.deepcopy(self.lista_atual),
                    'inicio': self.inicio_atual,
                    'fim': self.fim_atual,
                    'pivot': self.pivot_atual
                })
        else:
            self.inicializar()  # Pular se início >= fim
    
    def proximo_passo(self) -> bool:
        """Executa o próximo passo do algoritmo"""
        if self.fase_atual == FaseQuickSort.INICIALIZACAO:
            self.inicializar()
            return len(self.pilha_recursao) > 0 or self.inicio_atual < self.fim_atual
            
        elif self.fase_atual == FaseQuickSort.ESCOLHA_PIVOT:
            self._iniciar_particao()
            return True
            
        elif self.fase_atual == FaseQuickSort.PARTICAO:
            return self._continuar_particao()
            
        elif self.fase_atual == FaseQuickSort.RECURSAO:
            self._preparar_recursao()
            return True
            
        return False
    
    def _iniciar_particao(self) -> None:
        """Inicia o processo de particionamento"""
        self.fase_atual = FaseQuickSort.PARTICAO
        self.i_atual = self.inicio_atual
        self.j_atual = self.inicio_atual
        
        # Registrar escolha do pivot
        self.historico_pivots.append({
            'posicao': self.pivot_atual,
            'valor': self.lista_atual[self.pivot_atual],
            'inicio': self.inicio_atual,
            'fim': self.fim_atual
        })
        
        if self.callback_visual:
            self.callback_visual('pivot_escolhido', {
                'pivot_pos': self.pivot_atual,
                'pivot_valor': self.lista_atual[self.pivot_atual],
                'lista': copy.deepcopy(self.lista_atual)
            })
    
    def _continuar_particao(self) -> bool:
        """Continua o processo de particionamento"""
        if self.j_atual >= self.fim_atual:
            # Trocar pivot com elemento na posição i
            self._fazer_troca(self.i_atual, self.pivot_atual)
            self.fase_atual = FaseQuickSort.RECURSAO
            return True
        
        # Comparar elemento atual com pivot
        elemento_atual = self.lista_atual[self.j_atual]
        valor_pivot = self.lista_atual[self.pivot_atual]
        
        if self.callback_visual:
            self.callback_visual('comparar_com_pivot', {
                'elemento_pos': self.j_atual,
                'elemento_valor': elemento_atual,
                'pivot_valor': valor_pivot,
                'i_atual': self.i_atual,
                'lista': copy.deepcopy(self.lista_atual)
            })
        
        self.comparacoes_realizadas += 1
        
        if elemento_atual <= valor_pivot:
            if self.i_atual != self.j_atual:
                self._fazer_troca(self.i_atual, self.j_atual)
            self.i_atual += 1
        
        self.j_atual += 1
        return True
    
    def fazer_decisao_particao(self, elemento_menor_que_pivot: bool) -> Tuple[bool, str]:
        """
        Usuário decide se o elemento atual é menor que o pivot
        
        Args:
            elemento_menor_que_pivot: True se usuário acha que elemento <= pivot
            
        Returns:
            Tuple[bool, str]: (decisao_correta, mensagem_feedback)
        """
        if self.fase_atual != FaseQuickSort.PARTICAO or self.j_atual >= self.fim_atual:
            return False, "Não é possível fazer decisão neste momento"
        
        elemento_atual = self.lista_atual[self.j_atual]
        valor_pivot = self.lista_atual[self.pivot_atual]
        
        decisao_correta = (elemento_menor_que_pivot and elemento_atual <= valor_pivot) or \
                         (not elemento_menor_que_pivot and elemento_atual > valor_pivot)
        
        if decisao_correta:
            self.decisoes_corretas += 1
            mensagem = f"Correto! {elemento_atual} {'<=' if elemento_atual <= valor_pivot else '>'} {valor_pivot}"
        else:
            mensagem = f"Ops! {elemento_atual} {'<=' if elemento_atual <= valor_pivot else '>'} {valor_pivot}"
        
        # Processar decisão independentemente se está correta
        if elemento_atual <= valor_pivot:
            if self.i_atual != self.j_atual:
                self._fazer_troca(self.i_atual, self.j_atual)
            self.i_atual += 1
        
        self.j_atual += 1
        
        if self.callback_visual:
            self.callback_visual('decisao_particao', {
                'decisao_correta': decisao_correta,
                'mensagem': mensagem,
                'lista': copy.deepcopy(self.lista_atual),
                'i_atual': self.i_atual,
                'j_atual': self.j_atual
            })
        
        return decisao_correta, mensagem
    
    def _fazer_troca(self, pos1: int, pos2: int) -> None:
        """Faz troca entre dois elementos"""
        if pos1 != pos2:
            self.lista_atual[pos1], self.lista_atual[pos2] = \
                self.lista_atual[pos2], self.lista_atual[pos1]
            
            self.trocas_realizadas += 1
            
            # Registrar troca
            self.historico_trocas.append({
                'pos1': pos1,
                'pos2': pos2,
                'valores': (self.lista_atual[pos2], self.lista_atual[pos1]),
                'lista_resultante': copy.deepcopy(self.lista_atual)
            })
            
            if self.callback_visual:
                self.callback_visual('troca_realizada', {
                    'pos1': pos1,
                    'pos2': pos2,
                    'lista': copy.deepcopy(self.lista_atual)
                })
    
    def _preparar_recursao(self) -> None:
        """Prepara as chamadas recursivas"""
        posicao_pivot_final = self.i_atual
        
        # Registrar partição
        self.historico_particoes.append({
            'inicio': self.inicio_atual,
            'fim': self.fim_atual,
            'pivot_final': posicao_pivot_final,
            'lista': copy.deepcopy(self.lista_atual)
        })
        
        # Adicionar subproblemas à pilha (direita primeiro para manter ordem)
        if posicao_pivot_final + 1 < self.fim_atual:
            self.pilha_recursao.append((posicao_pivot_final + 1, self.fim_atual))
        
        if self.inicio_atual < posicao_pivot_final - 1:
            self.pilha_recursao.append((self.inicio_atual, posicao_pivot_final - 1))
        
        if self.callback_visual:
            self.callback_visual('particao_completa', {
                'pivot_final': posicao_pivot_final,
                'lista': copy.deepcopy(self.lista_atual),
                'subproblemas': len(self.pilha_recursao)
            })
        
        # Inicializar próxima partição ou finalizar
        if self.pilha_recursao:
            self.nivel_recursao += 1
            self.fase_atual = FaseQuickSort.INICIALIZACAO
        else:
            self.fase_atual = FaseQuickSort.FINALIZACAO
    
    def obter_proxima_comparacao(self) -> Optional[Tuple[int, int]]:
        """Retorna os próximos elementos a serem comparados"""
        if (self.fase_atual == FaseQuickSort.PARTICAO and 
            self.j_atual < self.fim_atual):
            return (self.lista_atual[self.j_atual], self.lista_atual[self.pivot_atual])
        return None
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas do processo de ordenação"""
        total_decisoes = self.comparacoes_realizadas
        precisao = (self.decisoes_corretas / total_decisoes * 100 
                   if total_decisoes > 0 else 0)
        
        return {
            'fase_atual': self.fase_atual.value,
            'nivel_recursao': self.nivel_recursao,
            'comparacoes_realizadas': self.comparacoes_realizadas,
            'trocas_realizadas': self.trocas_realizadas,
            'decisoes_corretas': self.decisoes_corretas,
            'precisao': round(precisao, 2),
            'subproblemas_restantes': len(self.pilha_recursao),
            'esta_completo': self.fase_atual == FaseQuickSort.FINALIZACAO
        }
    
    def obter_resultado_final(self) -> Optional[List[int]]:
        """Retorna o resultado final se a ordenação estiver completa"""
        if self.fase_atual == FaseQuickSort.FINALIZACAO:
            return copy.deepcopy(self.lista_atual)
        return None
    
    def reiniciar(self) -> None:
        """Reinicia o algoritmo para uma nova execução"""
        self.__init__(self.lista_original, self.callback_visual)
