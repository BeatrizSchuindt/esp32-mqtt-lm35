import time
from collections import deque

import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

MQTT_SERVER = "10.68.17.102"
MQTT_PORT   = 1883
MQTT_TOPIC  = "sensores/temperatura/lm35"

max_pontos = 100
temperaturas = deque(maxlen=max_pontos)
tempos = deque(maxlen=max_pontos)
start_time = time.time()


def on_connect(client, userdata, flags, rc):
    print("Conectado ao MQTT com código:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global temperaturas, tempos
    try:
        temp = float(msg.payload.decode())
        t = time.time() - start_time
        temperaturas.append(temp)
        tempos.append(t)
        print(f"Recebido: {temp:.2f} °C")
    except ValueError:
        print("Mensagem inválida:", msg.payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, MQTT_PORT, 60)
client.loop_start()



fig, ax = plt.subplots()
linha, = ax.plot([], [], lw=2)
ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Temperatura (°C)")
ax.set_title("LM35 via MQTT (ESP32)")

def init():
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 50)
    linha.set_data([], [])
    return linha,

def update(frame):
    if len(tempos) == 0:
        return linha,
    linha.set_data(list(tempos), list(temperaturas))
    ax.set_xlim(max(0, tempos[0]), max(tempos))
    min_temp = min(temperaturas)
    max_temp = max(temperaturas)
    delta = max(1, (max_temp - min_temp) * 0.2)
    ax.set_ylim(min_temp - delta, max_temp + delta)
    return linha,

ani = animation.FuncAnimation(fig, update, init_func=init,
                              interval=1000, blit=True)

plt.show()

client.loop_stop()
client.disconnect()
