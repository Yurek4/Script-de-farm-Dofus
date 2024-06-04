import cv2
import numpy as np
import pyautogui as pg
import time
from PIL import ImageGrab  # Usar para capturar a tela

# Carregar as imagens do template dos recursos
templates = [
    cv2.imread("Lupulo.PNG", 0),
    cv2.imread("Lupulo2.PNG", 0),
    cv2.imread("Lupulo3.PNG", 0),
    cv2.imread("Lupulo4.PNG", 0)
]

# Definir um limiar para a correspondência
threshold = 0.7

def checkImage(template):
    template_w, template_h = template.shape[::-1]

    # Capturar a tela inteira
    screenshot = ImageGrab.grab()
    ImagemMaior = np.array(screenshot)

    # Converter a imagem para escala de cinza
    ImagemMaior_gray = cv2.cvtColor(ImagemMaior, cv2.COLOR_BGR2GRAY)

    # Realizar a correspondência de templates
    match = cv2.matchTemplate(ImagemMaior_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(match >= threshold)

    # Desenhar retângulos ao redor das correspondências encontradas
    for pt in zip(*loc[::-1]):
        cv2.rectangle(ImagemMaior, pt, (pt[0] + template_w, pt[1] + template_h), (0, 255, 0), 2)

    # Salvar a imagem com as correspondências
    cv2.imwrite('detected.png', ImagemMaior)

    # Se encontrar correspondências, clicar nelas
    found = False
    for pt in zip(*loc[::-1]):
        center_x = pt[0] + template_w // 2
        center_y = pt[1] + template_h // 2
        pg.click(center_x, center_y)
        time.sleep(1)
        found = True
        break  # Clique apenas na primeira correspondência encontrada

    if not found:
        print("Não encontrou o recurso.")

# Executar a função para verificar e clicar nos recursos
while True:
    for template in templates:
        checkImage(template)
    time.sleep(2)  # Esperar 2 segundos antes de verificar novamente
