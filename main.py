#!/usr/bin/env python3
"""
Merge_Mind - Jogo Educativo sobre Algoritmos de Dividir e Conquistar
Versão 2.0 - Completa e Profissional

Este é o ponto de entrada principal do jogo que ensina algoritmos
de dividir e conquistar de forma interativa e visual.

Autores:
- Davi de Aguiar Vieira (222006641)
- Henrique Carvalho Neves (222006801)

Disciplina: Projeto de Algoritmos
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path para importações
projeto_root = Path(__file__).parent
src_path = projeto_root / "src"
sys.path.insert(0, str(src_path))

try:
    import pygame
    print("✓ Pygame encontrado")
except ImportError:
    print("❌ Erro: Pygame não encontrado!")
    print("Instale com: pip install pygame")
    sys.exit(1)

try:
    from src.game.manager import GameManager
    from src.utils.config import TITULO, LARGURA, ALTURA
    from src.utils.dados import GerenciadorDados
    print("✓ Módulos do jogo carregados com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar módulos do jogo: {e}")
    print("Verifique se todos os arquivos estão presentes")
    sys.exit(1)


def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    dependencias = [
        ("pygame", "2.0.0"),
        ("sys", None),
        ("os", None),
        ("json", None),
        ("math", None),
        ("pathlib", None),
        ("typing", None),
        ("enum", None),
        ("datetime", None)
    ]
    
    print("🔍 Verificando dependências...")
    
    for nome, versao_min in dependencias:
        try:
            modulo = __import__(nome)
            if versao_min and hasattr(modulo, "__version__"):
                print(f"✓ {nome} v{modulo.__version__}")
            else:
                print(f"✓ {nome}")
        except ImportError:
            print(f"❌ {nome} não encontrado")
            return False
    
    return True


def configurar_ambiente():
    """Configura o ambiente do jogo"""
    print("⚙️  Configurando ambiente...")
    
    # Criar pastas necessárias
    pastas_necessarias = [
        "data",
        "assets/images",
        "assets/sounds", 
        "assets/fonts",
        "assets/music"
    ]
    
    for pasta in pastas_necessarias:
        pasta_path = projeto_root / pasta
        pasta_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Pasta criada/verificada: {pasta}")
    
    # Inicializar sistema de dados
    try:
        dados = GerenciadorDados()
        print("✓ Sistema de persistência inicializado")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar sistema de dados: {e}")
        return False


def exibir_informacoes_sistema():
    """Exibe informações sobre o sistema e o jogo"""
    print("\n" + "="*60)
    print(f"🎮 {TITULO}")
    print("="*60)
    print(f"Resolução: {LARGURA}x{ALTURA}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Pygame: {pygame.version.ver}")
    print(f"Plataforma: {sys.platform}")
    print("="*60)
    print("\n🎯 Algoritmos Disponíveis:")
    print("  • Merge Sort - Aprenda ordenação por divisão e conquista")
    print("  • Quick Sort - Domine o particionamento eficiente")  
    print("  • Binary Search - Entenda busca em arrays ordenados")
    print("\n📚 Recursos do Jogo:")
    print("  • Tutorial interativo para cada algoritmo")
    print("  • Visualização passo a passo do algoritmo")
    print("  • Sistema de pontuação e ranking")
    print("  • Múltiplos níveis de dificuldade")
    print("  • Estatísticas detalhadas de performance")
    print("  • Interface moderna e responsiva")
    print("="*60)


def main():
    """Função principal do jogo"""
    print("\n🚀 Iniciando Merge_Mind...")
    
    # Verificar dependências
    if not verificar_dependencias():
        print("\n❌ Dependências não satisfeitas. Instalação necessária:")
        print("pip install -r requirements.txt")
        return 1
    
    # Configurar ambiente
    if not configurar_ambiente():
        print("\n❌ Falha na configuração do ambiente")
        return 1
    
    # Exibir informações
    exibir_informacoes_sistema()
    
    # Inicializar o jogo
    try:
        print("\n🎮 Iniciando jogo...")
        game = GameManager()
        
        print("✓ Jogo inicializado com sucesso!")
        print("\n🎉 Divirta-se aprendendo algoritmos!\n")
        
        # Executar loop principal
        game.executar()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Jogo interrompido pelo usuário")
        return 0
        
    except Exception as e:
        print(f"\n❌ Erro durante execução do jogo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Cleanup
        try:
            pygame.quit()
            print("✓ Recursos liberados com sucesso")
        except:
            pass
    
    print("\n👋 Obrigado por jogar Merge_Mind!")
    return 0


if __name__ == "__main__":
    # Configurar encoding para output
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    
    # Executar jogo
    exit_code = main()
    sys.exit(exit_code)