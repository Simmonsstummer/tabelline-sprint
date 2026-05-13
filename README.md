# 🎮 Tabelline Sprint

Una webapp veloce e colorata per imparare le tabelline divertendosi. Quante ne indovini in 60 secondi?

👉 **[Gioca ora](https://simmonsstummer.github.io/tabelline-sprint/)**

## 🎯 Caratteristiche

- ⏱️ Sfida da 60 secondi
- ❌ Penalità di 3 secondi per ogni errore (e mostra la risposta corretta)
- 🏆 Record persistente salvato sul dispositivo
- 🔥 Sistema combo con coriandoli ogni 5 risposte corrette di fila
- ✨ Selettore di tabelline (2-10) per concentrarsi su quelle più ostiche
- 🔊 Suoni generati con Web Audio API (nessun file esterno)
- 📱 Mobile-first, installabile sulla home come PWA (funziona anche offline)
- 🎨 Design colorato e tattile, pensato per bambini

## 📁 Struttura dei file

```
├── index.html          # L'app vera e propria (HTML + CSS + JS in un solo file)
├── manifest.json       # Manifest PWA (per installazione su home)
├── service-worker.js   # Service Worker (caching offline)
├── favicon.ico         # Favicon per il tab del browser
├── icon-180.png        # Icona Apple touch (iOS)
├── icon-192.png        # Icona PWA (Android)
└── icon-512.png        # Icona PWA grande
```

## 📲 Installazione sulla home screen

**iOS (Safari):**
1. Apri il sito su Safari
2. Tocca il pulsante "Condividi" (quadrato con freccia)
3. Scorri e tocca "Aggiungi a Home"

**Android (Chrome):**
1. Apri il sito su Chrome
2. Apparirà un banner "Installa app", oppure dal menu (⋮) scegli "Aggiungi a schermata Home"

L'app si avvia a schermo intero, senza barre del browser, e funziona anche senza connessione (dopo il primo caricamento).

## 🛠️ Personalizzazione rapida

Tutto è in `index.html`. Cose facili da cambiare:

- **Durata del gioco**: cerca `gameTime: 60` e cambia il valore
- **Penalità per errore**: cerca `penalty: 3` 
- **Colori**: cerca `:root {` all'inizio del CSS — tutti i colori sono variabili
- **Tabelline disponibili**: la generazione domande è nella funzione `newQuestion()`

## 📜 Licenza

Rilasciato sotto licenza [Creative Commons BY-NC 4.0](LICENSE) — libero per uso personale, didattico e per condivisione/modifica, **purché non a scopo commerciale** e con attribuzione. Per usi commerciali contattare l'autore.
