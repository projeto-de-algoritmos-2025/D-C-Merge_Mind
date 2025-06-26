import pygame
import random
import sys
import time

pygame.init()
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo Merge Sort")
FONTE = pygame.font.SysFont(None, 36)
BRANCO = (255, 255, 255)
AZUL = (100, 149, 237)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)
PRETO = (0, 0, 0)

def desenhar_blocos(lista, y, cor=AZUL):
    largura_bloco = 60
    espaco = 10
    x_inicial = (LARGURA - (len(lista) * (largura_bloco + espaco))) // 2
    blocos = []
    for i, num in enumerate(lista):
        x = x_inicial + i * (largura_bloco + espaco)
        pygame.draw.rect(TELA, cor, (x, y, largura_bloco, 50))
        texto = FONTE.render(str(num), True, BRANCO)
        TELA.blit(texto, (x + 20, y + 10))
        blocos.append(pygame.Rect(x, y, largura_bloco, 50))
    return blocos

def esperar_clique(bloco1, bloco2, valor1, valor2):
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if bloco1.collidepoint(evento.pos):
                    return valor1
                elif bloco2.collidepoint(evento.pos):
                    return valor2

def fundir_interativamente(lista1, lista2):
    resultado = []
    i = j = 0
    while i < len(lista1) and j < len(lista2):
        TELA.fill(BRANCO)
        texto = FONTE.render("Clique no menor número:", True, PRETO)
        TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 50))
        blocos1 = desenhar_blocos([lista1[i]], 150, VERDE)
        blocos2 = desenhar_blocos([lista2[j]], 250, VERMELHO)
        pygame.display.flip()

        escolhido = esperar_clique(blocos1[0], blocos2[0], lista1[i], lista2[j])
        if escolhido == lista1[i]:
            resultado.append(lista1[i])
            i += 1
        else:
            resultado.append(lista2[j])
            j += 1

    resultado.extend(lista1[i:])
    resultado.extend(lista2[j:])

    TELA.fill(BRANCO)
    texto = FONTE.render("Resultado da fusão:", True, PRETO)
    TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 350))
    desenhar_blocos(resultado, 400)
    pygame.display.flip()
    time.sleep(1.5)
    return resultado

def merge_sort_jogo(lista):
    sublistas = [[num] for num in lista]

    while len(sublistas) > 1:
        nova_lista = []
        for i in range(0, len(sublistas), 2):
            if i + 1 < len(sublistas):
                fundido = fundir_interativamente(sublistas[i], sublistas[i+1])
                nova_lista.append(fundido)
            else:
                nova_lista.append(sublistas[i])
        sublistas = nova_lista

    TELA.fill(BRANCO)
    texto = FONTE.render("Lista ordenada!", True, PRETO)
    TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 50))
    desenhar_blocos(sublistas[0], 200)
    pygame.display.flip()
    time.sleep(4)

def main():
    lista = random.sample(range(1, 30), 6)
    merge_sort_jogo(lista)
    pygame.quit()

if __name__ == "__main__":
    main()