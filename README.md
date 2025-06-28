# 🧩 Merge_Mind - Versão 2.0

*Jogo educativo completo e profissional sobre algoritmos de Dividir e Conquistar — Aplicação interativa moderna com visualização avançada em Pygame*

## 👥 Alunos
| Matrícula | Nome |
|----------|------|
| 222006641 | Davi de Aguiar Vieira |
| 222006801 | Henrique Carvalho Neves |

## 📝 Entregas
| Dividir e Conquistar |
|----------|
| [Apresentação](https://youtu.be/yfrdvrkAzu0?si=nRzgYpjoxAEbP0WL)
---


## 📝 Versão Atualizada
| **D&C - Merge_Mind 2.0** |
|---------------------------|
| ✅ **Múltiplos Algoritmos**: Merge Sort, Quick Sort e Binary Search |
| ✅ **Interface Moderna**: UI profissional com animações e efeitos |
| ✅ **Sistema de Níveis**: 4 níveis de dificuldade (Fácil, Médio, Difícil, Expert) |
| ✅ **Tutorial Interativo**: Guias passo a passo para cada algoritmo |
| ✅ **Sistema de Pontuação**: Ranking, estatísticas e progressão |
| ✅ **Persistência de Dados**: Salvamento automático de progresso |
| ✅ **Visualização Avançada**: Animações suaves e feedback visual |
| ✅ **Código Estruturado**: Arquitetura modular e bem documentada |

---

## 🎯 Sobre o Projeto

**MergeMind 2.0** é uma plataforma educativa completa que ensina algoritmos de **Dividir e Conquistar** através de experiências interativas e visuais. O jogo oferece:

### 🔬 **Algoritmos Implementados**
- **Merge Sort**: Aprenda ordenação por divisão e conquista
- **Quick Sort**: Domine particionamento e recursão
- **Binary Search**: Entenda busca eficiente em arrays ordenados

### 🎮 **Características do Jogo**
- **Visualização Passo a Passo**: Veja cada etapa do algoritmo em ação
- **Interação Educativa**: Participe das decisões críticas dos algoritmos
- **Feedback Imediato**: Aprenda com seus erros através de dicas visuais
- **Progressão Adaptativa**: Níveis que se adaptam ao seu conhecimento

---

## 🧠 Como Funciona?

### **Merge Sort Interativo**
1. **Divisão Visual**: Veja como o array é dividido em sublistas
2. **Fusão Participativa**: Escolha manualmente os menores elementos
3. **Construção Gradual**: Acompanhe a reconstrução do array ordenado
4. **Análise de Performance**: Estatísticas em tempo real

### **Quick Sort Educativo**
1. **Escolha do Pivot**: Entenda a importância da seleção
2. **Particionamento Interativo**: Participe do processo de divisão
3. **Recursão Visual**: Veja como subproblemas são resolvidos
4. **Otimização Prática**: Aprenda técnicas de melhoria

### **Binary Search Guiado**
1. **Busca Direcionada**: Escolha a direção da busca
2. **Análise de Complexidade**: Compare com busca linear
3. **Casos Limite**: Explore cenários especiais
4. **Eficiência Demonstrada**: Veja O(log n) na prática

---

## 🌟 Novos Recursos - Versão 2.0

### **Interface Moderna**
- Design moderno com animações suaves
- Componentes UI responsivos e profissionais
- Tema escuro com cores acessíveis
- Feedback visual avançado

### **Sistema de Progressão**
- **4 Níveis de Dificuldade**: Fácil → Expert
- **Sistema de Pontuação**: Baseado em precisão e velocidade
- **Ranking Global**: Compare com outros jogadores
- **Estatísticas Detalhadas**: Análise completa de performance

### **Recursos Educativos**
- **Tutorial Interativo**: Aprenda antes de jogar
- **Dicas Contextuais**: Ajuda durante o gameplay
- **Explicações Teóricas**: Fundamentos dos algoritmos
- **Análise Comparativa**: Compare diferentes abordagens

### **Funcionalidades Técnicas**
- **Persistência de Dados**: Progresso salvo automaticamente
- **Sistema de Configurações**: Personalize sua experiência
- **Exportação de Resultados**: Compartilhe seus dados
- **Modo Acessibilidade**: Opções para diferentes necessidades

---

## 📁 Estrutura do Projeto

```
Merge_Mind/
├── main.py                 # Ponto de entrada principal
├── requirements.txt        # Dependências Python
├── README.md              # Documentação
├── data/                  # Dados persistentes
│   ├── config.json       # Configurações do usuário
│   ├── progresso.json    # Progresso do jogador
│   ├── ranking.json      # Rankings e pontuações
│   └── estatisticas.json # Estatísticas detalhadas
├── assets/               # Recursos multimídia
│   ├── images/          # Imagens e ícones
│   ├── sounds/          # Efeitos sonoros
│   ├── music/           # Músicas de fundo
│   └── fonts/           # Fontes personalizadas
└── src/                 # Código fonte
    ├── algorithms/      # Implementações dos algoritmos
    │   ├── merge_sort.py    # Merge Sort educativo
    │   ├── quick_sort.py    # Quick Sort educativo
    │   └── binary_search.py # Binary Search educativo
    ├── game/            # Lógica do jogo
    │   ├── manager.py       # Gerenciador principal
    │   ├── estado_manager.py # Estados do jogo
    │   ├── pontuacao.py     # Sistema de pontuação
    │   └── estados/         # Estados específicos
    │       ├── menu.py          # Menu principal
    │       ├── selecao_nivel.py # Seleção de dificuldade
    │       ├── jogo.py          # Gameplay principal
    │       └── ranking.py       # Visualização de rankings
    ├── ui/              # Interface do usuário
    │   └── componentes.py   # Componentes UI modernos
    └── utils/           # Utilitários
        ├── config.py        # Configurações globais
        ├── dados.py         # Persistência de dados
        └── audio.py         # Sistema de áudio
```

---

## ⚙️ Instalação e Execução

### ✅ **Pré-requisitos**
- Python 3.8 ou superior
- Sistema operacional: Windows, macOS ou Linux

### 🔧 **Instalação Rápida**

1. **Clone o repositório**:
```bash
git clone [url-do-repositorio]
cd Merge_Mind
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Execute o jogo**:
```bash
python main.py
```

### 📦 **Dependências**
```txt
pygame>=2.5.0
pygame-gui>=0.6.9
numpy>=1.24.0
```

---

## 🎮 Como Jogar

### **Primeiro Acesso**
1. **Tutorial**: Complete o tutorial do algoritmo escolhido
2. **Nível**: Selecione sua dificuldade (recomendado: Fácil)
3. **Prática**: Jogue algumas partidas para familiarização

### **Controles**
- **Mouse**: Navegação e seleção
- **Clique Esquerdo**: Interação com elementos
- **Scroll**: Navegação em listas
- **ESC**: Pausa/Menu

### **Dicas para Sucesso**
- 🎯 **Precisão > Velocidade**: Foque em decisões corretas
- 📚 **Use o Tutorial**: Entenda antes de jogar
- 📊 **Analise Estatísticas**: Identifique pontos de melhoria
- 🎚️ **Progrida Gradualmente**: Domine um nível antes do próximo

---

## 🏆 Sistema de Pontuação

### **Pontuação Base**
- ✅ **Decisão Correta**: +10 pontos
- ⚡ **Decisão Rápida**: +5 pontos (bonus)
- 🔥 **Sequência de Acertos**: +2 pontos (multiplicativo)
- ❌ **Erro**: -2 pontos

### **Multiplicadores**
- 🟢 **Fácil**: x1.0
- 🟡 **Médio**: x1.5
- 🟠 **Difícil**: x2.0
- 🔴 **Expert**: x3.0

### **Rankings**
- 🥇 **Global**: Todos os algoritmos
- 🎯 **Por Algoritmo**: Específico para cada um
- 📈 **Progressão**: Histórico de melhoria

---

## 📊 Aspectos Educativos

### **Conceitos Abordados**
- **Dividir e Conquistar**: Estratégia fundamental
- **Análise de Complexidade**: Big O na prática
- **Recursão**: Compreensão através da visualização
- **Otimização**: Técnicas de melhoria de performance

### **Habilidades Desenvolvidas**
- 🧠 **Pensamento Algorítmico**: Decomposição de problemas
- 🔍 **Análise Crítica**: Avaliação de eficiência
- 🎯 **Tomada de Decisão**: Escolhas algorítmicas
- 📐 **Matemática Aplicada**: Logaritmos e exponenciais

---

## 🛠️ Desenvolvimento

### **Arquitetura**
- **Padrão State**: Gerenciamento de estados
- **Component System**: UI modular
- **MVC**: Separação clara de responsabilidades
- **Data Persistence**: Armazenamento eficiente

### **Tecnologias**
- **Python 3.8+**: Linguagem principal
- **Pygame**: Engine gráfica
- **JSON**: Persistência de dados
- **Type Hints**: Código documentado

### **Extensibilidade**
- ➕ **Novos Algoritmos**: Fácil adição
- 🎨 **Temas Visuais**: Sistema de cores configurável
- 🌐 **Internacionalização**: Suporte a múltiplos idiomas
- 📱 **Responsividade**: Adaptação a diferentes resoluções

---

## 📈 Roadmap Futuro

### **Versão 2.1**
- [ ] Sistema de conquistas
- [ ] Modo multiplayer local
- [ ] Mais algoritmos (Heap Sort, Radix Sort)
- [ ] Sistema de dicas inteligentes

### **Versão 3.0**
- [ ] Interface web (pygame-web)
- [ ] Modo online competitivo
- [ ] Editor de problemas customizados
- [ ] Integração com plataformas educacionais

---

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é desenvolvido para fins educacionais como parte da disciplina de Projeto de Algoritmos.

---

## 👨‍💻 Contato

- **Davi de Aguiar Vieira** - 222006641
- **Henrique Carvalho Neves** - 222006801

---

## 🙏 Agradecimentos

- Professor da disciplina Projeto de Algoritmos
- Comunidade Pygame
- Recursos educacionais sobre algoritmos
- Feedback dos usuários beta

---

*"Aprender algoritmos nunca foi tão divertido e visual!"* 🎮✨
