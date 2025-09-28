import numpy as np
import wave
import struct


def gerar_som(filename, freq=440.0, duracao=0.2, volume=0.5, tipo="senoidal"):
    taxa = 44100  # Hz
    n_amostras = int(taxa * duracao)
    t = np.linspace(0, duracao, n_amostras, False)

    if tipo == "quadrada":  # som retrô estilo 8-bit
        onda = np.sign(np.sin(freq * t * 2 * np.pi)) * volume
    else:  # padrão senoidal
        onda = np.sin(freq * t * 2 * np.pi) * volume

    # converte para 16-bit PCM
    onda = np.int16(onda * 32767)

    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(1)  # mono
        wav_file.setsampwidth(2)  # 2 bytes = 16 bits
        wav_file.setframerate(taxa)
        wav_file.writeframes(onda.tobytes())


# === Sons do jogo ===
# Comer -> beep curto agudo (quadrado para ficar retrô)
gerar_som("comer.wav", freq=800.0, duracao=0.1, volume=0.6, tipo="quadrada")

# Morrer -> beep grave longo
gerar_som("morrer.wav", freq=200.0, duracao=0.4, volume=0.6, tipo="senoidal")

# Trilha sonora -> loop simples 8-bit (mistura de notas)
def gerar_trilha(filename="trilha.wav"):
    notas = [440, 660, 550, 880, 660, 440, 550, 330]  # escala simples
    duracao_nota = 0.25
    taxa = 44100
    trilha = np.array([], dtype=np.int16)

    for freq in notas * 4:  # repete 4x
        t = np.linspace(0, duracao_nota, int(taxa * duracao_nota), False)
        onda = np.sign(np.sin(freq * t * 2 * np.pi)) * 0.4  # onda quadrada
        onda = np.int16(onda * 32767)
        trilha = np.concatenate((trilha, onda))

    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(taxa)
        wav_file.writeframes(trilha.tobytes())

gerar_trilha()

print("Sons gerados com sucesso:🎶comer.wav e 🎶morrer.wav e 🎶trilha.wav")
