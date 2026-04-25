# MVP de Câmera de Segurança com OpenCV

Protótipo rápido de monitoramento para pequenos comércios usando webcam local, com foco em prevenção de furtos fora do horário de funcionamento.

## O que foi desenvolvido

Script principal: `camera_seguranca_mvp.py`

Funcionalidades implementadas:
- Captura de vídeo em tempo real pela webcam.
- Detecção de pessoas com método clássico `HOG + SVM` do OpenCV.
- Verificação de horário de funcionamento (`hora_abertura` e `hora_fechamento`).
- Alerta quando houver pessoa detectada fora do horário.
- Alerta por permanência suspeita (mais de 4 minutos contínuos).
- Salvamento automático de imagens de alerta na pasta `capturas_alerta/`.
- Exibição de informações na tela (status de horário e tempo de presença).

## Tecnologias e bibliotecas

- Python 3
- OpenCV (`opencv-python`)
- NumPy (`numpy`)
- `datetime`, `time`, `os` (bibliotecas padrão do Python)

## Instalação

No terminal, dentro da pasta do projeto:

```bash
pip install opencv-python numpy
```

## Como executar

1. Abra o terminal na pasta do projeto.
2. Execute:

```bash
python camera_seguranca_mvp.py
```

3. A janela da câmera será aberta em tempo real.
4. Para encerrar, pressione `q`.

## Como funcionam os alertas

O sistema dispara alerta quando:
- Há pessoa detectada fora do horário configurado.
- Há pessoa detectada continuamente por mais de 4 minutos.

Ao disparar:
- Mostra mensagem no terminal.
- Salva uma imagem com data e hora em `capturas_alerta/`.

Observação: existe um intervalo mínimo entre alertas para evitar repetição excessiva.

## Configuração rápida

No arquivo `camera_seguranca_mvp.py`, você pode ajustar:
- `hora_abertura`
- `hora_fechamento`
- `tempo_suspeito_segundos`
- `intervalo_minimo_alerta`

## Estrutura do projeto

```text
hackton/
├── camera_seguranca_mvp.py
├── capturas_alerta/
└── README.md
```

## Próximas melhorias sugeridas

- Criar log em arquivo `.txt` com histórico de alertas.
- Definir região de interesse (ROI) para monitorar áreas específicas.
- Ajustar parâmetros de detecção para reduzir falsos positivos.
- Adicionar alerta sonoro local.
