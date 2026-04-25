import cv2
import numpy as np
from datetime import datetime
import time
import os


hora_abertura = 8
hora_fechamento = 18

tempo_suspeito_segundos = 4 * 60 

intervalo_minimo_alerta = 10

PASTA_ALERTAS = "capturas_alerta"


def garantir_pasta_alertas():
    if not os.path.exists(PASTA_ALERTAS):
        os.makedirs(PASTA_ALERTAS)


def fora_do_horario_atual():
    hora_atual = datetime.now().hour
    return hora_atual < hora_abertura or hora_atual >= hora_fechamento


def salvar_frame_alerta(frame):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho_arquivo = os.path.join(PASTA_ALERTAS, f"alerta_{timestamp}.jpg")
    cv2.imwrite(caminho_arquivo, frame)
    print(f"[INFO] Captura salva em: {caminho_arquivo}")


def criar_detector_pessoas():
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    return hog


def detectar_pessoas(hog, frame):
    caixas_detectadas, _ = hog.detectMultiScale(
        frame,
        winStride=(8, 8),
        padding=(8, 8),
        scale=1.05
    )
    return caixas_detectadas


def desenhar_deteccoes(frame, caixas):
    for (x, y, w, h) in caixas:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame


def main():
    garantir_pasta_alertas()
    hog = criar_detector_pessoas()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERRO] Nao foi possivel abrir a webcam.")
        return

    inicio_presenca = None

    ultimo_alerta = 0.0

    print("[INFO] Sistema iniciado.")
    print("[INFO] Pressione 'q' para sair.")

    while True:
        sucesso, frame = cap.read()
        if not sucesso:
            print("[ERRO] Falha ao ler frame da webcam.")
            break

        caixas = detectar_pessoas(hog, frame)
        pessoa_detectada = len(caixas) > 0
        agora = time.time()

        if pessoa_detectada:
            if inicio_presenca is None:
                inicio_presenca = agora
        else:
            inicio_presenca = None

        tempo_presenca = 0
        if inicio_presenca is not None:
            tempo_presenca = agora - inicio_presenca

        alerta_fora_horario = pessoa_detectada and fora_do_horario_atual()
        alerta_permanencia = pessoa_detectada and tempo_presenca >= tempo_suspeito_segundos
        disparar_alerta = alerta_fora_horario or alerta_permanencia

        pode_alertar = (agora - ultimo_alerta) >= intervalo_minimo_alerta
        if disparar_alerta and pode_alertar:
            if alerta_fora_horario:
                print("ALERTA: Pessoa detectada fora do horario!")
            if alerta_permanencia:
                print("ALERTA: Pessoa com permanencia suspeita (mais de 4 minutos)!")
            salvar_frame_alerta(frame)
            ultimo_alerta = agora

        frame = desenhar_deteccoes(frame, caixas)
        status_horario = "FORA DO HORARIO" if fora_do_horario_atual() else "Horario normal"
        texto_tempo = f"Presenca continua: {int(tempo_presenca)}s"

        cv2.putText(frame, status_horario, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, texto_tempo, (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Pressione Q para sair", (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

        cv2.imshow("Camera de Seguranca - MVP", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Sistema encerrado.")


if __name__ == "__main__":
    main()
