import pygame
import random
import sys

# === Configurações ===
LARGURA, ALTURA = 600, 400
TAMANHO_QUADRADO = 20
FPS = 10

# Cores
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

# === Inicialização ===
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🐍 Snake Game")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("consolas", 30)

# Sons
som_comer = pygame.mixer.Sound("sons/comer.wav")
som_morrer = pygame.mixer.Sound("sons/morrer.wav")

# Música de fundo
pygame.mixer.music.load("sons/trilha.wav")  # coloque sua trilha sonora aqui

# === Funções ===
def desenhar_cobra(cobra):
    for x, y in cobra:
        pygame.draw.rect(tela, VERDE, (x, y, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

def gerar_comida():
    x = random.randrange(0, LARGURA, TAMANHO_QUADRADO)
    y = random.randrange(0, ALTURA, TAMANHO_QUADRADO)
    return x, y

def mostrar_texto(texto, tamanho, cor, y_offset=0):
    fonte_local = pygame.font.SysFont("consolas", tamanho, bold=True)
    render = fonte_local.render(texto, True, cor)
    rect = render.get_rect(center=(LARGURA // 2, ALTURA // 2 + y_offset))
    tela.blit(render, rect)

# === Loop do jogo ===
def jogo():
    cobra = [(100, 100)]
    direcao = (TAMANHO_QUADRADO, 0)  # direita
    direcao_pendente = direcao
    comida = gerar_comida()
    pontos = 0

    # Inicia música de fundo
    pygame.mixer.music.play(-1)  # -1 = loop infinito

    while True:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direcao != (0, TAMANHO_QUADRADO):
                    direcao_pendente = (0, -TAMANHO_QUADRADO)
                elif event.key == pygame.K_DOWN and direcao != (0, -TAMANHO_QUADRADO):
                    direcao_pendente = (0, TAMANHO_QUADRADO)
                elif event.key == pygame.K_LEFT and direcao != (TAMANHO_QUADRADO, 0):
                    direcao_pendente = (-TAMANHO_QUADRADO, 0)
                elif event.key == pygame.K_RIGHT and direcao != (-TAMANHO_QUADRADO, 0):
                    direcao_pendente = (TAMANHO_QUADRADO, 0)

        # Atualizar posição
        direcao = direcao_pendente
        cabeca_x, cabeca_y = cobra[0]
        nova_cabeca = (cabeca_x + direcao[0], cabeca_y + direcao[1])

        # Colisões
        if (nova_cabeca[0] < 0 or nova_cabeca[0] >= LARGURA or 
            nova_cabeca[1] < 0 or nova_cabeca[1] >= ALTURA or 
            nova_cabeca in cobra):
            som_morrer.play()
            pygame.mixer.music.stop()  # para a trilha ao morrer
            return pontos

        # Comer
        if nova_cabeca == comida:
            cobra.insert(0, nova_cabeca)
            pontos += 1
            som_comer.play()
            comida = gerar_comida()
        else:
            cobra.insert(0, nova_cabeca)
            cobra.pop()

        # Desenho
        tela.fill(PRETO)
        desenhar_cobra(cobra)
        pygame.draw.rect(tela, VERMELHO, (comida[0], comida[1], TAMANHO_QUADRADO, TAMANHO_QUADRADO))

        # Pontos
        pontos_txt = fonte.render(f"Pontos: {pontos}", True, BRANCO)
        tela.blit(pontos_txt, (10, 10))

        pygame.display.flip()
        relogio.tick(FPS)

# === Tela inicial ===
def tela_inicial():
    pygame.mixer.music.stop()  # garante que a música não toca aqui
    while True:
        tela.fill(PRETO)
        mostrar_texto("🐍 Snake Game", 50, VERDE, -50)
        mostrar_texto("Pressione ESPAÇO para jogar", 25, BRANCO, 20)
        mostrar_texto("E para sair", 20, BRANCO, 60)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()

# === Tela de game over ===
def tela_game_over(pontos):
    pygame.mixer.music.stop()
    while True:
        tela.fill(PRETO)
        mostrar_texto("GAME OVER!", 50, VERMELHO, -50)
        mostrar_texto(f"Pontuação final: {pontos}", 30, BRANCO, 10)
        mostrar_texto("Pressione R para jogar novamente", 20, VERDE, 60)
        mostrar_texto("E para sair", 20, BRANCO, 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()

# === Execução principal ===
if __name__ == "__main__":
    while True:
        tela_inicial()
        pontos = jogo()
        jogar_novamente = tela_game_over(pontos)
        if not jogar_novamente:
            break