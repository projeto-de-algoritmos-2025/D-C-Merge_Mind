"""
Sistema de pontuação e estatísticas do jogo
"""
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class EstatisticasPartida:
    """Estatísticas de uma partida individual"""
    nivel: str
    elementos: int
    tempo_total: float
    acertos: int
    erros: int
    pontuacao: int
    data: str
    completa: bool
    
    @property
    def precisao(self) -> float:
        """Calcula a precisão da partida"""
        total = self.acertos + self.erros
        return (self.acertos / total * 100) if total > 0 else 0.0
        
    @property
    def pontos_por_segundo(self) -> float:
        """Calcula pontos por segundo"""
        return self.pontuacao / self.tempo_total if self.tempo_total > 0 else 0.0


class SistemaPontuacao:
    """Gerencia pontuação e estatísticas do jogo"""
    
    def __init__(self):
        self.arquivo_stats = "stats.json"
        self.pontuacao_atual = 0
        self.acertos_atual = 0
        self.erros_atual = 0
        self.tempo_inicio = 0
        self.nivel_atual = "FACIL"
        self.elementos_atual = 0
        
        # Multiplicadores de pontuação
        self.multiplicadores = {
            'FACIL': 1.0,
            'MEDIO': 1.5,
            'DIFICIL': 2.0,
            'EXPERT': 3.0
        }
        
        # Bônus
        self.bonus_tempo = 1000  # Bônus por tempo rápido
        self.bonus_perfeito = 2000  # Bônus por não errar
        self.bonus_consecutivo = 100  # Bônus por acertos consecutivos
        
        self.historico: List[EstatisticasPartida] = []
        self.carregar_estatisticas()
        
    def iniciar_partida(self, nivel: str, elementos: int) -> None:
        """Inicia uma nova partida"""
        self.pontuacao_atual = 0
        self.acertos_atual = 0
        self.erros_atual = 0
        self.tempo_inicio = time.time()
        self.nivel_atual = nivel
        self.elementos_atual = elementos
        
    def registrar_acerto(self, tempo_resposta: float = 0) -> int:
        """Registra um acerto e calcula pontos"""
        self.acertos_atual += 1
        
        # Pontuação base
        pontos_base = 100
        
        # Multiplicador do nível
        multiplicador = self.multiplicadores.get(self.nivel_atual, 1.0)
        
        # Bônus por tempo de resposta rápido (máximo 3 segundos)
        bonus_tempo_resposta = max(0, (3.0 - tempo_resposta) * 50) if tempo_resposta > 0 else 0
        
        # Bônus por acertos consecutivos
        bonus_consecutivo = min(self.acertos_atual * self.bonus_consecutivo, 1000)
        
        pontos = int((pontos_base + bonus_tempo_resposta + bonus_consecutivo) * multiplicador)
        self.pontuacao_atual += pontos
        
        return pontos
        
    def registrar_erro(self) -> int:
        """Registra um erro e aplica penalidade"""
        self.erros_atual += 1
        
        # Penalidade por erro
        penalidade = min(self.pontuacao_atual // 10, 200)
        self.pontuacao_atual = max(0, self.pontuacao_atual - penalidade)
        
        return -penalidade
        
    def finalizar_partida(self, completa: bool = True) -> EstatisticasPartida:
        """Finaliza a partida e calcula pontuação final"""
        tempo_total = time.time() - self.tempo_inicio
        
        # Bônus final
        if completa:
            # Bônus por completar
            bonus_completo = 500 * self.multiplicadores.get(self.nivel_atual, 1.0)
            self.pontuacao_atual += int(bonus_completo)
            
            # Bônus por não errar
            if self.erros_atual == 0:
                self.pontuacao_atual += self.bonus_perfeito
                
            # Bônus por tempo (se tempo < 30s para níveis fáceis, escala para outros)
            tempo_limite_bonus = 30 * self.multiplicadores.get(self.nivel_atual, 1.0)
            if tempo_total < tempo_limite_bonus:
                bonus_tempo = int((tempo_limite_bonus - tempo_total) / tempo_limite_bonus * self.bonus_tempo)
                self.pontuacao_atual += bonus_tempo
        
        # Criar estatísticas da partida
        stats = EstatisticasPartida(
            nivel=self.nivel_atual,
            elementos=self.elementos_atual,
            tempo_total=tempo_total,
            acertos=self.acertos_atual,
            erros=self.erros_atual,
            pontuacao=self.pontuacao_atual,
            data=datetime.now().isoformat(),
            completa=completa
        )
        
        # Adicionar ao histórico
        self.historico.append(stats)
        self.salvar_estatisticas()
        
        return stats
        
    def obter_ranking(self, limite: int = 10) -> List[EstatisticasPartida]:
        """Obtém o ranking das melhores pontuações"""
        partidas_completas = [p for p in self.historico if p.completa]
        return sorted(partidas_completas, key=lambda x: x.pontuacao, reverse=True)[:limite]
        
    def obter_estatisticas_gerais(self) -> Dict[str, Any]:
        """Obtém estatísticas gerais do jogador"""
        if not self.historico:
            return {
                'total_partidas': 0,
                'partidas_completas': 0,
                'pontuacao_maxima': 0,
                'precisao_media': 0.0,
                'tempo_medio': 0.0,
                'nivel_favorito': 'FACIL'
            }
            
        partidas_completas = [p for p in self.historico if p.completa]
        
        # Estatísticas básicas
        total_partidas = len(self.historico)
        total_completas = len(partidas_completas)
        pontuacao_maxima = max(p.pontuacao for p in self.historico) if self.historico else 0
        
        # Precisão média
        if self.historico:
            precisao_media = sum(p.precisao for p in self.historico) / len(self.historico)
        else:
            precisao_media = 0.0
            
        # Tempo médio das partidas completas
        if partidas_completas:
            tempo_medio = sum(p.tempo_total for p in partidas_completas) / len(partidas_completas)
        else:
            tempo_medio = 0.0
            
        # Nível mais jogado
        contagem_niveis = {}
        for partida in self.historico:
            contagem_niveis[partida.nivel] = contagem_niveis.get(partida.nivel, 0) + 1
        nivel_favorito = max(contagem_niveis.items(), key=lambda x: x[1])[0] if contagem_niveis else 'FACIL'
        
        return {
            'total_partidas': total_partidas,
            'partidas_completas': total_completas,
            'pontuacao_maxima': pontuacao_maxima,
            'precisao_media': precisao_media,
            'tempo_medio': tempo_medio,
            'nivel_favorito': nivel_favorito,
            'taxa_conclusao': (total_completas / total_partidas * 100) if total_partidas > 0 else 0.0
        }
        
    def salvar_estatisticas(self) -> bool:
        """Salva estatísticas no arquivo"""
        try:
            dados = {
                'historico': [asdict(partida) for partida in self.historico]
            }
            
            with open(self.arquivo_stats, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar estatísticas: {e}")
            return False
            
    def carregar_estatisticas(self) -> bool:
        """Carrega estatísticas do arquivo"""
        try:
            if os.path.exists(self.arquivo_stats):
                with open(self.arquivo_stats, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    
                self.historico = [
                    EstatisticasPartida(**partida) 
                    for partida in dados.get('historico', [])
                ]
                return True
            return False
        except Exception as e:
            print(f"Erro ao carregar estatísticas: {e}")
            self.historico = []
            return False
            
    def resetar_estatisticas(self) -> bool:
        """Reseta todas as estatísticas"""
        self.historico = []
        try:
            if os.path.exists(self.arquivo_stats):
                os.remove(self.arquivo_stats)
            return True
        except Exception as e:
            print(f"Erro ao resetar estatísticas: {e}")
            return False
