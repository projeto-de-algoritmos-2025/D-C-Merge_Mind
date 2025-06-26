"""
Sistema de persistência de dados para o jogo Merge_Mind
Gerencia salvamento e carregamento de configurações, progresso e rankings
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class GerenciadorDados:
    """Classe responsável pela persistência de dados do jogo"""
    
    def __init__(self):
        self.pasta_dados = Path("data")
        self.arquivo_config = self.pasta_dados / "config.json"
        self.arquivo_progresso = self.pasta_dados / "progresso.json"
        self.arquivo_ranking = self.pasta_dados / "ranking.json"
        self.arquivo_estatisticas = self.pasta_dados / "estatisticas.json"
        
        # Criar pasta de dados se não existir
        self.pasta_dados.mkdir(exist_ok=True)
        
        # Configurações padrão
        self.config_padrao = {
            "volume_master": 0.7,
            "volume_sfx": 0.8,
            "volume_musica": 0.5,
            "resolucao": [1200, 800],
            "fullscreen": False,
            "alto_contraste": False,
            "tamanho_fonte_aumentado": False,
            "reducao_animacao": False,
            "audio_descritivo": False,
            "legendas": True,
            "idioma": "pt_BR",
            "algoritmo_favorito": "MERGE_SORT",
            "nivel_padrao": "MEDIO"
        }
        
        # Progresso padrão
        self.progresso_padrao = {
            "algoritmos_desbloqueados": ["MERGE_SORT"],
            "niveis_completados": {
                "MERGE_SORT": [],
                "QUICK_SORT": [],
                "BINARY_SEARCH": []
            },
            "tutorial_completo": {
                "MERGE_SORT": False,
                "QUICK_SORT": False,
                "BINARY_SEARCH": False
            },
            "pontuacao_total": 0,
            "tempo_total_jogado": 0,  # em segundos
            "primeira_vez": True
        }
        
        # Inicializar arquivos se não existirem
        self._inicializar_arquivos()
    
    def _inicializar_arquivos(self) -> None:
        """Inicializa arquivos de dados com valores padrão se não existirem"""
        if not self.arquivo_config.exists():
            self.salvar_configuracoes(self.config_padrao)
        
        if not self.arquivo_progresso.exists():
            self.salvar_progresso(self.progresso_padrao)
        
        if not self.arquivo_ranking.exists():
            self.salvar_ranking([])
        
        if not self.arquivo_estatisticas.exists():
            self.salvar_estatisticas({})
    
    def carregar_configuracoes(self) -> Dict[str, Any]:
        """Carrega configurações do arquivo"""
        try:
            with open(self.arquivo_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Mesclar com configurações padrão para novas opções
            config_final = self.config_padrao.copy()
            config_final.update(config)
            
            return config_final
        except (FileNotFoundError, json.JSONDecodeError):
            return self.config_padrao.copy()
    
    def salvar_configuracoes(self, configuracoes: Dict[str, Any]) -> bool:
        """Salva configurações no arquivo"""
        try:
            with open(self.arquivo_config, 'w', encoding='utf-8') as f:
                json.dump(configuracoes, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False
    
    def carregar_progresso(self) -> Dict[str, Any]:
        """Carrega progresso do jogador"""
        try:
            with open(self.arquivo_progresso, 'r', encoding='utf-8') as f:
                progresso = json.load(f)
            
            # Mesclar com progresso padrão para novos campos
            progresso_final = self.progresso_padrao.copy()
            progresso_final.update(progresso)
            
            return progresso_final
        except (FileNotFoundError, json.JSONDecodeError):
            return self.progresso_padrao.copy()
    
    def salvar_progresso(self, progresso: Dict[str, Any]) -> bool:
        """Salva progresso do jogador"""
        try:
            with open(self.arquivo_progresso, 'w', encoding='utf-8') as f:
                json.dump(progresso, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar progresso: {e}")
            return False
    
    def carregar_ranking(self) -> List[Dict[str, Any]]:
        """Carrega ranking de pontuações"""
        try:
            with open(self.arquivo_ranking, 'r', encoding='utf-8') as f:
                ranking = json.load(f)
            return ranking
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def salvar_ranking(self, ranking: List[Dict[str, Any]]) -> bool:
        """Salva ranking de pontuações"""
        try:
            with open(self.arquivo_ranking, 'w', encoding='utf-8') as f:
                json.dump(ranking, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar ranking: {e}")
            return False
    
    def adicionar_pontuacao(self, algoritmo: str, nivel: str, pontuacao: int, 
                           precisao: float, tempo: int, 
                           nome_jogador: str = "Jogador") -> bool:
        """Adiciona nova pontuação ao ranking"""
        ranking = self.carregar_ranking()
        
        nova_entrada = {
            "nome": nome_jogador,
            "algoritmo": algoritmo,
            "nivel": nivel,
            "pontuacao": pontuacao,
            "precisao": round(precisao, 2),
            "tempo": tempo,
            "data": datetime.now().isoformat(),
            "timestamp": datetime.now().timestamp()
        }
        
        ranking.append(nova_entrada)
        
        # Ordenar por pontuação (maior primeiro) e manter top 100
        ranking.sort(key=lambda x: x["pontuacao"], reverse=True)
        ranking = ranking[:100]
        
        return self.salvar_ranking(ranking)
    
    def obter_ranking_por_algoritmo(self, algoritmo: str, limite: int = 10) -> List[Dict[str, Any]]:
        """Obtém ranking filtrado por algoritmo"""
        ranking = self.carregar_ranking()
        ranking_filtrado = [entrada for entrada in ranking if entrada["algoritmo"] == algoritmo]
        return ranking_filtrado[:limite]
    
    def obter_ranking_geral(self, limite: int = 10) -> List[Dict[str, Any]]:
        """Obtém ranking geral"""
        ranking = self.carregar_ranking()
        return ranking[:limite]
    
    def carregar_estatisticas(self) -> Dict[str, Any]:
        """Carrega estatísticas detalhadas"""
        try:
            with open(self.arquivo_estatisticas, 'r', encoding='utf-8') as f:
                estatisticas = json.load(f)
            return estatisticas
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def salvar_estatisticas(self, estatisticas: Dict[str, Any]) -> bool:
        """Salva estatísticas detalhadas"""
        try:
            with open(self.arquivo_estatisticas, 'w', encoding='utf-8') as f:
                json.dump(estatisticas, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar estatísticas: {e}")
            return False
    
    def atualizar_estatisticas(self, algoritmo: str, nivel: str, 
                              resultado: Dict[str, Any]) -> bool:
        """Atualiza estatísticas com resultado de uma partida"""
        estatisticas = self.carregar_estatisticas()
        
        # Inicializar estrutura se não existir
        if algoritmo not in estatisticas:
            estatisticas[algoritmo] = {}
        
        if nivel not in estatisticas[algoritmo]:
            estatisticas[algoritmo][nivel] = {
                "partidas_jogadas": 0,
                "partidas_completadas": 0,
                "pontuacao_total": 0,
                "precisao_media": 0.0,
                "tempo_total": 0,
                "melhor_pontuacao": 0,
                "melhor_precisao": 0.0,
                "melhor_tempo": float('inf')
            }
        
        stats = estatisticas[algoritmo][nivel]
        
        # Atualizar estatísticas
        stats["partidas_jogadas"] += 1
        
        if resultado.get("completada", False):
            stats["partidas_completadas"] += 1
        
        if "pontuacao" in resultado:
            stats["pontuacao_total"] += resultado["pontuacao"]
            stats["melhor_pontuacao"] = max(stats["melhor_pontuacao"], resultado["pontuacao"])
        
        if "precisao" in resultado:
            # Calcular nova média de precisão
            total_partidas = stats["partidas_jogadas"]
            stats["precisao_media"] = ((stats["precisao_media"] * (total_partidas - 1)) + 
                                     resultado["precisao"]) / total_partidas
            stats["melhor_precisao"] = max(stats["melhor_precisao"], resultado["precisao"])
        
        if "tempo" in resultado:
            stats["tempo_total"] += resultado["tempo"]
            if resultado["tempo"] < stats["melhor_tempo"]:
                stats["melhor_tempo"] = resultado["tempo"]
        
        return self.salvar_estatisticas(estatisticas)
    
    def obter_estatisticas_resumo(self) -> Dict[str, Any]:
        """Obtém resumo das estatísticas"""
        estatisticas = self.carregar_estatisticas()
        progresso = self.carregar_progresso()
        
        resumo = {
            "tempo_total_jogado": progresso.get("tempo_total_jogado", 0),
            "pontuacao_total": progresso.get("pontuacao_total", 0),
            "algoritmos_desbloqueados": len(progresso.get("algoritmos_desbloqueados", [])),
            "partidas_por_algoritmo": {},
            "precisao_media_geral": 0.0,
            "melhor_pontuacao_geral": 0
        }
        
        total_partidas = 0
        precisao_total = 0.0
        
        for algoritmo, niveis in estatisticas.items():
            partidas_algoritmo = 0
            for nivel, stats in niveis.items():
                partidas_nivel = stats.get("partidas_jogadas", 0)
                partidas_algoritmo += partidas_nivel
                total_partidas += partidas_nivel
                
                if partidas_nivel > 0:
                    precisao_total += stats.get("precisao_media", 0) * partidas_nivel
                
                resumo["melhor_pontuacao_geral"] = max(
                    resumo["melhor_pontuacao_geral"],
                    stats.get("melhor_pontuacao", 0)
                )
            
            resumo["partidas_por_algoritmo"][algoritmo] = partidas_algoritmo
        
        if total_partidas > 0:
            resumo["precisao_media_geral"] = round(precisao_total / total_partidas, 2)
        
        return resumo
    
    def resetar_dados(self, tipo: str = "tudo") -> bool:
        """
        Reseta dados específicos ou todos
        
        Args:
            tipo: "config", "progresso", "ranking", "estatisticas" ou "tudo"
        """
        try:
            if tipo in ["config", "tudo"]:
                self.salvar_configuracoes(self.config_padrao)
            
            if tipo in ["progresso", "tudo"]:
                self.salvar_progresso(self.progresso_padrao)
            
            if tipo in ["ranking", "tudo"]:
                self.salvar_ranking([])
            
            if tipo in ["estatisticas", "tudo"]:
                self.salvar_estatisticas({})
            
            return True
        except Exception as e:
            print(f"Erro ao resetar dados: {e}")
            return False
    
    def exportar_dados(self, arquivo_destino: str) -> bool:
        """Exporta todos os dados para um arquivo"""
        try:
            dados = {
                "configuracoes": self.carregar_configuracoes(),
                "progresso": self.carregar_progresso(),
                "ranking": self.carregar_ranking(),
                "estatisticas": self.carregar_estatisticas(),
                "data_exportacao": datetime.now().isoformat()
            }
            
            with open(arquivo_destino, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Erro ao exportar dados: {e}")
            return False
    
    def importar_dados(self, arquivo_origem: str) -> bool:
        """Importa dados de um arquivo"""
        try:
            with open(arquivo_origem, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            if "configuracoes" in dados:
                self.salvar_configuracoes(dados["configuracoes"])
            
            if "progresso" in dados:
                self.salvar_progresso(dados["progresso"])
            
            if "ranking" in dados:
                self.salvar_ranking(dados["ranking"])
            
            if "estatisticas" in dados:
                self.salvar_estatisticas(dados["estatisticas"])
            
            return True
        except Exception as e:
            print(f"Erro ao importar dados: {e}")
            return False
