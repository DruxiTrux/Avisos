# 🤖 Bot Notificador de YouTube para Discord

Un bot ligero desarrollado en Python que supervisa un canal de YouTube específico mediante RSS y notifica automáticamente en tu servidor de Discord cuando se publica un **nuevo video** (filtrando los YouTube Shorts) o cuando el canal inicia un **directo**.

El sistema está diseñado para ejecutarse de forma **24/7 de manera totalmente gratuita** utilizando **GitHub Actions**.

---

## 🚀 Características
- **Notificaciones de Videos:** Envía una alerta con mención `@everyone` cuando se publica un video nuevo[cite: 1].
- **Filtro de Shorts:** Omite automáticamente los YouTube Shorts para evitar notificaciones innecesarias.
- **Notificaciones de Directos:** Detecta cuando el canal comienza una transmisión en vivo y avisa al instante.
- **Sin Costes:** Corre en la nube usando GitHub Actions cada 10 minutos sin necesidad de mantener tu PC encendida[cite: 1].
- **Control de Historial:** Guarda registros locales (`vh_videos.json` y `vh_streams.json`) para no repetir alertas de contenidos ya anunciados[cite: 1].

---

## 📁 Estructura del Proyecto
```text
📦 NotificadorYouTube
 ┣ 📂 .github
 ┃ ┗ 📂 workflows
 ┃   ┗ 📜 bot.yml
 ┣ 📜 bot.py
 ┣ 📜 requirements.txt
 ┣ 📜 vh_videos.json (Se genera automáticamente)
 ┗ 📜 vh_streams.json (Se generan automáticamente)
