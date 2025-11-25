# server.py
import time
from collections import deque

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt

# ====== CONFIG MQTT ======
MQTT_SERVER = "localhost"          # como o Mosquitto roda no mesmo notebook
MQTT_PORT = 1883
MQTT_TOPIC = "sensores/temperatura/lm35"

# ====== ARMAZENAMENTO EM MEMÓRIA ======
max_pontos = 200
dados = deque(maxlen=max_pontos)   # cada item: {"t": ..., "temp": ...}
start_time = time.time()

# ====== FASTAPI ======
app = FastAPI()

# CORS liberado para facilitar o acesso do React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # se quiser, depois pode restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== CALLBACKS MQTT ======
def on_connect(client, userdata, flags, rc, properties=None):
    print("Conectado ao MQTT com código:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global dados
    try:
        temp = float(msg.payload.decode())
        t = time.time() - start_time
        dados.append({"t": t, "temp": temp})
        print(f"MQTT -> {temp:.2f} °C")
    except ValueError:
        print("Payload inválido:", msg.payload)

# ====== CLIENTE MQTT ======
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, MQTT_PORT, 60)
client.loop_start()   # roda o loop MQTT em thread separada

# ====== ROTAS DA API ======
@app.get("/data")
def get_data():
    """Retorna todas as leituras armazenadas."""
    return list(dados)

@app.get("/latest")
def get_latest():
    """Retorna apenas a última leitura."""
    return dados[-1] if dados else {}
