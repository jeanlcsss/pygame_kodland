import pygame
import sys
import random

# Inicialização do PyGame
pygame.init()

# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Definindo as dimensões da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Space Invaders")

global pontuacao
pontuacao = 0

# Funções para desenhar elementos
def desenhar_nave(nave):
    pygame.draw.rect(TELA, BRANCO, nave)

def desenhar_inimigos(inimigos):
    for inimigo in inimigos:
        pygame.draw.rect(TELA, VERMELHO, inimigo)

def desenhar_tiros(tiros):
    for tiro in tiros:
        pygame.draw.rect(TELA, AZUL, tiro)

# Função para atualizar a posição dos tiros
def atualizar_tiros(tiros):
    for tiro in tiros[:]:
        tiro.top -= 10
        if tiro.top < 0:
            tiros.remove(tiro)
    return tiros

# Função para atualizar a posição dos inimigos
def atualizar_inimigos(inimigos):
    for inimigo in inimigos:
        inimigo.top += 5
    return inimigos

# Função para verificar colisões
def verificar_colisoes(tiros, inimigos):
    global pontuacao
    for tiro in tiros[:]:
        for inimigo in inimigos[:]:
            if tiro.colliderect(inimigo):
                tiros.remove(tiro)
                inimigos.remove(inimigo)
                pontuacao +=1
                break

# Função para adicionar inimigos
def adicionar_inimigos(inimigos, numero_inimigos):
    largura_inimigo = 40
    altura_inimigo = 30
    for _ in range(numero_inimigos):
        x = random.randint(0, (LARGURA_TELA - largura_inimigo) // 60) * 60 + 30
        y = 50
        inimigos.append(pygame.Rect(x, y, largura_inimigo, altura_inimigo))

# Função para exibir a tela de Game Over
def tela_game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    jogo()  # Reinicia o jogo
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        TELA.fill(PRETO)
        fonte = pygame.font.SysFont(None, 35)
        texto = fonte.render("Game Over! Pressione [ENTER] para jogar novamente", True, BRANCO)
        texto_rect = texto.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2))
        TELA.blit(texto, texto_rect)

        # Exibe a pontuação
        texto_pontuacao = fonte.render(f"Sua Pontuação: {pontuacao}", True, BRANCO)
        texto_pontuacao_rect = texto_pontuacao.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2 + 50))
        TELA.blit(texto_pontuacao, texto_pontuacao_rect)

        pygame.display.update()

# Função principal do jogo
def jogo():
    global pontuacao
    pontuacao = 0
    # Inicializando variáveis do jogo
    nave = pygame.Rect(LARGURA_TELA // 2 - 25, ALTURA_TELA - 50, 50, 30)
    tiros = []
    inimigos = []
    numero_inimigos = 1
    ciclos_ate_aumentar = 3  # Número de ciclos necessários para aumentar o número de inimigos
    ciclos_atual = 0  # Contador de ciclos atuais
    velocidade_nave = 10  # Velocidade inicial da nave
    incremento_velocidade = 1  # Incremento da velocidade a cada ciclo
    adicionar_inimigos(inimigos, numero_inimigos)
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tiros.append(pygame.Rect(nave.centerx - 5, nave.top - 10, 10, 10))
        
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave.left > 0:
            nave.left -= velocidade_nave
        if teclas[pygame.K_RIGHT] and nave.right < LARGURA_TELA:
            nave.right += velocidade_nave
        
        tiros = atualizar_tiros(tiros)
        inimigos = atualizar_inimigos(inimigos)
        verificar_colisoes(tiros, inimigos)

        # Verifica se algum inimigo alcançou o fundo da tela
        for inimigo in inimigos:
            if inimigo.top > ALTURA_TELA:
                tela_game_over()

        # Adicionar novos inimigos se todos os inimigos forem derrotados
        if not inimigos:
            ciclos_atual += 1
            if ciclos_atual == ciclos_ate_aumentar:
                numero_inimigos += 1  # Aumenta o número de inimigos
                velocidade_nave += incremento_velocidade  # Aumenta a velocidade da nave
                ciclos_atual = 0  # Reseta o contador de ciclos
            adicionar_inimigos(inimigos, numero_inimigos)

        # Limpar a tela e desenhar tudo
        TELA.fill(PRETO)
        desenhar_nave(nave)
        desenhar_inimigos(inimigos)
        desenhar_tiros(tiros)
        pygame.display.update()

        # Controlar o FPS
        clock.tick(30)

# Função principal do menu
def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    jogo()

        TELA.fill(PRETO)
        fonte = pygame.font.SysFont(None, 55)
        texto = fonte.render("Pressione [ENTER] para Iniciar", True, BRANCO)
        texto_rect = texto.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2))
        TELA.blit(texto, texto_rect)
        pygame.display.update()

# Executar o menu
menu()
