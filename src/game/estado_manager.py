"""
Sistema de gerenciamento de estados do jogo
"""
from abc import ABC, abstractmethod
import pygame
from typing import Optional, Dict, Any


class Estado(ABC):
    """Classe base abstrata para todos os estados do jogo"""
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.tela = game_manager.tela
        self.clock = game_manager.clock
        
    @abstractmethod
    def processar_eventos(self, eventos: list) -> None:
        """Processa eventos do pygame"""
        pass
    
    @abstractmethod
    def atualizar(self, dt: float) -> None:
        """Atualiza a lógica do estado"""
        pass
    
    @abstractmethod
    def renderizar(self) -> None:
        """Renderiza o estado na tela"""
        pass
    
    def entrar(self) -> None:
        """Chamado quando o estado é ativado"""
        pass
    
    def sair(self) -> None:
        """Chamado quando o estado é desativado"""
        pass


class GerenciadorEstados:
    """Gerencia a transição entre diferentes estados do jogo"""
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.estados: Dict[str, Estado] = {}
        self.estado_atual: Optional[Estado] = None
        self.nome_estado_atual: Optional[str] = None
        self.pilha_estados: list = []
        
    def adicionar_estado(self, nome: str, estado: Estado) -> None:
        """Adiciona um novo estado ao gerenciador"""
        self.estados[nome] = estado
        
    def mudar_estado(self, nome: str) -> bool:
        """Muda para um novo estado"""
        if nome not in self.estados:
            print(f"Estado '{nome}' não encontrado!")
            return False
            
        # Sair do estado atual
        if self.estado_atual:
            self.estado_atual.sair()
            
        # Entrar no novo estado
        self.estado_atual = self.estados[nome]
        self.nome_estado_atual = nome
        self.estado_atual.entrar()
        return True
        
    def empilhar_estado(self, nome: str) -> bool:
        """Empilha um estado (pausa o atual)"""
        if nome not in self.estados:
            return False
            
        if self.estado_atual:
            self.pilha_estados.append(self.nome_estado_atual)
            
        return self.mudar_estado(nome)
        
    def desempilhar_estado(self) -> bool:
        """Volta para o estado anterior na pilha"""
        if not self.pilha_estados:
            return False
            
        estado_anterior = self.pilha_estados.pop()
        return self.mudar_estado(estado_anterior)
        
    def processar_eventos(self, eventos: list) -> None:
        """Processa eventos no estado atual"""
        if self.estado_atual:
            self.estado_atual.processar_eventos(eventos)
            
    def atualizar(self, dt: float) -> None:
        """Atualiza o estado atual"""
        if self.estado_atual:
            self.estado_atual.atualizar(dt)
            
    def renderizar(self) -> None:
        """Renderiza o estado atual"""
        if self.estado_atual:
            self.estado_atual.renderizar()
