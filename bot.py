import time
import json
import os
import feedparser
import requests

# --- CONFIGURACIÓN ---
WEBHOOK_VIDEOS = "https://discord.com/api/webhooks/1566498219444281394/tcznJWBz4wPnBV5TLmS86_DqCUgKpYyQ6QgOp7JswiOebXnVTiFZ5ulWTfdCmK04Jlyr"
WEBHOOK_STREAMS = "https://discord.com/api/webhooks/1566498273957650514/TT6B0JCkA6qzqeWppBZZFxVRwF1E6W4XHFENmRES_jOFhxB9tRe81FipP67Q7B5A4lZ5"
CHANNEL_ID = "UCWvnoVMxxM6L2kEHHCCArlg"
API_KEY_YOUTUBE = "AQUÍ_TU_API_KEY_DE_YOUTUBE" # Opcional si usas la API para directos

RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

FILE_VIDEOS = "vh_videos.json"
FILE_STREAMS = "vh_streams.json"

def cargar_vistos(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def guardar_vistos(archivo, vistos_set):
    with open(archivo, "w") as f:
        json.dump(list(vistos_set), f)

# --- VERIFICAR VÍDEOS NUEVOS (FILTRANDO SHORTS) ---
def chequear_videos():
    vistos = cargar_vistos(FILE_VIDEOS)
    feed = feedparser.parse(RSS_URL)
    
    if not feed.entries:
        return

    # Buscamos el primer video que NO sea un Short
    latest = None
    for entry in feed.entries:
        link = entry.link
        # Los shorts de YouTube suelen incluir /shorts/ en su enlace en el RSS
        if "/shorts/" not in link:
            latest = entry
            break
            
    if not latest:
        return

    video_id = latest.id
    title = latest.title
    link = latest.link

    if video_id not in vistos:
        mensaje = f"@everyone 🎬 **¡Nuevo video subido!** Vayan a darle mucho amor: **{title}**\n{link}"
        
        payload = {
            "content": mensaje,
            "allowed_mentions": {"parse": ["everyone"]}
        }
        
        requests.post(WEBHOOK_VIDEOS, json=payload)
        
        vistos.add(video_id)
        guardar_vistos(FILE_VIDEOS, vistos)
        print(f"[VIDEO NUEVO NOTIFICADO]: {title}")

# --- VERIFICAR DIRECTOS EN CURSO ---
def chequear_streams():
    vistos = cargar_vistos(FILE_STREAMS)
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&eventType=live&type=video&key={API_KEY_YOUTUBE}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "items" in data and len(data["items"]) > 0:
            stream_item = data["items"][0]
            stream_id = stream_item["id"]["videoId"]
            stream_title = stream_item["snippet"]["title"]
            stream_url = f"https://www.youtube.com/watch?v={stream_id}"
            
            if stream_id not in vistos:
                mensaje = f"@everyone 🔴 **¡Estamos en directo!** Pásense por aquí: **{stream_title}**\n{stream_url}"
                
                payload = {
                    "content": mensaje,
                    "allowed_mentions": {"parse": ["everyone"]}
                }
                
                requests.post(WEBHOOK_STREAMS, json=payload)
                
                vistos.add(stream_id)
                guardar_vistos(FILE_STREAMS, vistos)
                print(f"[STREAM NUEVO NOTIFICADO]: {stream_title}")
                
    except Exception as e:
        print(f"Error al verificar streams: {e}")

# --- BUCLE PRINCIPAL ---
if __name__ == "__main__":
    print("Bot de notificaciones iniciado correctamente...")
    chequear_videos()
    chequear_streams()
