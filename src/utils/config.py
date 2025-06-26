"""
Configurações globais do jogo Merge_Mind
"""

# Configurações de tela
LARGURA = 1200
ALTURA = 800
FPS = 60
TITULO = "Merge_Mind - Aprenda Merge Sort"

# Cores principais (tema moderno)
CORES = {
    'FUNDO': (15, 16, 53),           # Azul escuro moderno
    'PRINCIPAL': (88, 166, 255),      # Azul claro
    'SECUNDARIA': (255, 107, 107),    # Vermelho suave
    'SUCESSO': (72, 187, 120),        # Verde
    'AVISO': (255, 193, 7),           # Amarelo
    'TEXTO': (255, 255, 255),         # Branco
    'TEXTO_ESCURO': (52, 58, 64),     # Cinza escuro
    'DESTAQUE': (255, 215, 0),        # Dourado
    'CARD': (30, 32, 81),             # Azul escuro card
    'HOVER': (108, 117, 125),         # Cinza hover
    'TRANSPARENTE': (0, 0, 0, 128),   # Preto transparente
}

# Configurações de fontes
FONTES = {
    'TITULO': 48,
    'SUBTITULO': 32,
    'NORMAL': 24,
    'PEQUENA': 18,
    'BOTAO': 20,
}

# Configurações do jogo
JOGO = {
    'MIN_ELEMENTOS': 4,
    'MAX_ELEMENTOS': 12,
    'MIN_VALOR': 1,
    'MAX_VALOR': 99,
    'VELOCIDADE_ANIMACAO': 500,  # ms
    'TEMPO_PAUSA': 1000,         # ms
}

# Configurações de elementos visuais
VISUAL = {
    'BLOCO_LARGURA': 80,
    'BLOCO_ALTURA': 60,
    'ESPACO_BLOCO': 15,
    'RAIO_BORDA': 10,
    'SOMBRA_OFFSET': 3,
    'MARGEM_LATERAL': 50,
    'MARGEM_VERTICAL': 100,
}

# Configurações de áudio
AUDIO = {
    'VOLUME_MASTER': 0.7,
    'VOLUME_SFX': 0.8,
    'VOLUME_MUSICA': 0.5,
}

# Níveis de dificuldade
NIVEIS = {
    'FACIL': {
        'elementos': 4,
        'tempo_limite': None,
        'dicas': True,
        'nome': 'Fácil'
    },
    'MEDIO': {
        'elementos': 6,
        'tempo_limite': 30,
        'dicas': True,
        'nome': 'Médio'
    },
    'DIFICIL': {
        'elementos': 8,
        'tempo_limite': 20,
        'dicas': False,
        'nome': 'Difícil'
    },
    'EXPERT': {
        'elementos': 12,
        'tempo_limite': 15,
        'dicas': False,
        'nome': 'Expert'
    }
}

# Estados do jogo
ESTADOS = {
    'MENU': 'menu',
    'TUTORIAL': 'tutorial',
    'SELECAO_ALGORITMO': 'selecao_algoritmo',
    'SELECAO_NIVEL': 'selecao_nivel',
    'JOGO': 'jogo',
    'PAUSA': 'pausa',
    'CONFIGURACOES': 'configuracoes',
    'RANKING': 'ranking',
    'CREDITOS': 'creditos',
    'ESTATISTICAS': 'estatisticas'
}

# Algoritmos disponíveis
ALGORITMOS = {
    'MERGE_SORT': {
        'nome': 'Merge Sort',
        'descricao': 'Algoritmo de ordenação por divisão e conquista',
        'dificuldade': 'Intermediário',
        'conceitos': ['Divisão e Conquista', 'Recursão', 'Fusão de Arrays'],
        'cor_tema': CORES['PRINCIPAL']
    },
    'QUICK_SORT': {
        'nome': 'Quick Sort',
        'descricao': 'Algoritmo de ordenação por particionamento',
        'dificuldade': 'Avançado',
        'conceitos': ['Divisão e Conquista', 'Particionamento', 'Pivot'],
        'cor_tema': CORES['SECUNDARIA']
    },
    'BINARY_SEARCH': {
        'nome': 'Binary Search',
        'descricao': 'Algoritmo de busca por divisão e conquista',
        'dificuldade': 'Básico',
        'conceitos': ['Divisão e Conquista', 'Busca', 'Arrays Ordenados'],
        'cor_tema': CORES['SUCESSO']
    }
}

# Configurações de animação
ANIMACAO = {
    'DURACAO_FADE': 300,
    'DURACAO_SLIDE': 400,
    'DURACAO_BOUNCE': 600,
    'DURACAO_COMPARACAO': 800,
    'DURACAO_TROCA': 1000,
    'EASING': 'ease_out_cubic'
}

# Configurações de tutorial
TUTORIAL = {
    'VELOCIDADE_TEXTO': 50,  # caracteres por segundo
    'PAUSA_ENTRE_PASSOS': 2000,  # ms
    'DESTACAR_ELEMENTOS': True,
    'SOM_TYPEWRITER': True
}

# Configurações de pontuação
PONTUACAO = {
    'PONTOS_DECISAO_CORRETA': 10,
    'PONTOS_DECISAO_RAPIDA': 5,  # bonus por decisão rápida
    'PONTOS_SEQUENCIA': 2,       # bonus por sequência de acertos
    'MULTIPLICADOR_DIFICULDADE': {
        'FACIL': 1.0,
        'MEDIO': 1.5,
        'DIFICIL': 2.0,
        'EXPERT': 3.0
    },
    'PENALIDADE_ERRO': -2,
    'TEMPO_DECISAO_RAPIDA': 3000  # ms
}

# Configurações de acessibilidade
ACESSIBILIDADE = {
    'ALTO_CONTRASTE': False,
    'TAMANHO_FONTE_AUMENTADO': False,
    'REDUCAO_ANIMACAO': False,
    'AUDIO_DESCRITIVO': False,
    'LEGENDAS': True
}
