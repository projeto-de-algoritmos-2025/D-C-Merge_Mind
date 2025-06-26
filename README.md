# 🧩 Merge_Mind

*Projeto da disciplina Projeto de Algoritmos, sobre o algoritmo Merge Sort — Aplicação prática com visualização interativa em Pygame*

## 👥 Alunos
| Matrícula | Nome |
|----------|------|
| 222006641 | Davi de Aguiar Vieira |
| 222006801 | Henrique Carvalho Neves |

## 📝 Entregas
| D&C - Merge_Mind |
|------------------|
| ✅ Jogo educativo sobre Merge Sort com interface gráfica |
| ✅ Visualização interativa usando Pygame |
| ✅ Código comentado e estruturado para fins didáticos |
| ✅ README explicativo com instruções |

---

## 🎯 Sobre o Projeto

**MergeMind** é um jogo educativo que ensina de forma interativa e visual como funciona o algoritmo de ordenação **Merge Sort**, utilizando a estratégia de *Dividir e Conquistar*.  
Neste jogo, o jogador participa da etapa de fusão do algoritmo, escolhendo manualmente o menor elemento entre dois blocos em destaque, simulando a ordenação feita pelo Merge Sort.

É uma forma lúdica de consolidar o entendimento do funcionamento interno do algoritmo, tornando o processo mais acessível e intuitivo.

---

## 🧠 Como este projeto se relaciona com o algoritmo Merge Sort?

Este jogo é, essencialmente, uma *representação visual interativa de um Merge Sort* com as seguintes características:

- O vetor original é dividido em sublistas até que todas tenham apenas um elemento (fase de **divisão** do Merge Sort).
- A fase de **conquista (fusão)** é executada com a ajuda do jogador, que escolhe o menor valor entre dois blocos apresentados.
- A cada fusão realizada, uma nova lista ordenada é gerada e mostrada visualmente na tela.
- A ordenação completa ocorre quando todos os elementos são fundidos em uma única lista final ordenada.
- A interação força o jogador a refletir sobre as decisões corretas, simulando na prática o comportamento do algoritmo.

---

## 📸 Visualização

Durante a execução do jogo:

- Os números são exibidos como blocos retangulares coloridos.
- O jogador vê dois blocos (um de cada sublista) e deve clicar no **menor valor**.
- A fusão correta das sublistas é mostrada na tela, reforçando a lógica do Merge Sort.
- Ao fim, a lista ordenada é exibida como resultado final do algoritmo.

---

## ⚙️ Instalação

### ✅ Pré-requisitos

- Python 3.x
- Biblioteca [pygame](https://www.pygame.org/)

### 🔧 Instalação do Pygame

```bash
pip install pygame
