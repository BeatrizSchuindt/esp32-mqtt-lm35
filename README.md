# ESP32 + MQTT + LM35

Projeto de leitura de temperatura com ESP32-S3 e sensor LM35, enviando os dados via MQTT para um notebook e exibindo um gráfico em tempo real com Python.

## Estrutura do projeto

```text
ESP32-MQTT-LM35/
├── .venv/                 # Ambiente virtual Python (Python 3.12)
├── arduino/
│   └── esp_mqtt_lm35.ino  # Código do ESP32 (Arduino IDE)
├── main.py                # Cliente MQTT em Python + gráfico matplotlib
├── .gitignore
└── README.md
```

## Requisitos

### Hardware

- ESP32-S3 (ESP32-S3-N16R8)
- Sensor LM35
- Protoboard e jumpers

### Software

- Python 3.12
- Arduino IDE com suporte ao ESP32 instalado
- Eclipse Mosquitto (broker MQTT)
- Bibliotecas Arduino:
  - `PubSubClient`
- Bibliotecas Python (instaladas na venv):
  - `paho-mqtt`
  - `matplotlib`

## Ambiente virtual (Python 3.12)

Na raiz do projeto:

```bash
py -3.12 -m venv .venv
.\.venv\Scripts\activate  # PowerShell no Windows
pip install --upgrade pip
pip install paho-mqtt matplotlib
```

## Instalação e configuração do Mosquitto

1. Baixar o Mosquitto para Windows em:  
   https://mosquitto.org/download/

2. Instalar o Mosquitto (padrão) e localizar o arquivo `mosquitto.conf`.  
   Normalmente ele fica em algo como:

   ```text
   C:\Program Files\mosquitto\mosquitto.conf
   ```

3. Abrir o `mosquitto.conf` em um editor de texto e adicionar ao final do arquivo:

   ```text
   listener 1883
   allow_anonymous true
   ```

4. No Windows, garantir que a porta TCP 1883 está liberada no Firewall:

   - Abrir o Firewall do Windows.
   - Criar uma regra de entrada permitindo a porta 1883 (TCP) com o nome MQTT

## Código do ESP32

O arquivo `arduino/esp_mqtt_lm35.ino`:

- Conecta o ESP32 à rede Wi-Fi.
- Lê a temperatura do LM35 no pino analógico.
- Envia a temperatura em °C via MQTT para o broker (Mosquitto) no notebook.

Antes de usar o sketch no Arduino IDE, é necessário:

1. Instalar o pacote de placas do ESP32:
   - Menu `Tools > Board > Boards Manager...`
   - Buscar por **"esp32"** (Espressif Systems) e instalar.
2. Selecionar a placa correta:
   - Menu `Tools > Board > ESP32 Arduino > ESP32S3 Dev Module` (ou equivalente à sua placa).
3. Instalar a biblioteca PubSubClient:
   - Menu `Sketch > Include Library > Manage Libraries...`
   - Buscar por **"PubSubClient"** (Nick O'Leary) e instalar.

Em seguida, ajustar no código:

```cpp
const char* ssid       = "NOME_DA_REDE";     // Wi-Fi do roteador
const char* password   = "SENHA_DA_REDE";
const char* mqtt_server = "IP_DO_NOTEBOOK";  // IPv4 obtido com ipconfig
const int   mqtt_port   = 1883;
```

O ESP32 e o notebook devem estar conectados na mesma rede.  
Após configurar, fazer o upload do sketch pelo Arduino IDE (`Sketch > Upload`).

## Script Python (main.py)

O `main.py`:

- Conecta ao broker MQTT (Mosquitto) rodando no notebook.
- Assina o tópico `sensores/temperatura/lm35`.
- Armazena as leituras recebidas.
- Plota em tempo real as temperaturas com o `matplotlib`.

Ajustar o IP do broker, se necessário:

```python
MQTT_SERVER = "IP_DO_NOTEBOOK"  # mesmo IP usado no ESP32
MQTT_PORT   = 1883
MQTT_TOPIC  = "sensores/temperatura/lm35"
```

Com a venv ativa e o Mosquitto rodando:

```bash
python main.py
```

Uma janela do matplotlib será aberta mostrando o gráfico de temperatura em tempo real.

Feito por Ana Beatriz Schuindt, na disciplina de Microcontroladores no período 25/2.
