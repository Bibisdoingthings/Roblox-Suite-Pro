<div align="center">

# ⚡ Roblox Suite Pro

**High-Performance Multi-Instance Automation, Anti-AFK & Discord Community Infrastructure**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%2F%2011-0078D6.svg?logo=windows&logoColor=white)](https://www.microsoft.com/)
[![Anti-Cheat](https://img.shields.io/badge/Byfron%2FHyperion-Safe%20%E2%9C%93-brightgreen.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2.svg?logo=discord&logoColor=white)](https://discord.gg/YOUR_INVITE_LINK)

<br />

<p align="center">
  <a href="#-panoramica">Panoramica</a> •
  <a href="#-architettura-del-software">Architettura</a> •
  <a href="#-anti-cheat-compliance--crash-prevention">Sicurezza Byfron</a> •
  <a href="#-guida-allinstallazione--requisiti">Installazione</a> •
  <a href="#-compilazione-eseguibile-exe">Compilazione EXE</a> •
  <a href="#-generatore-icone-multi-layer">Asset Grafici</a> •
  <a href="#-infrastruttura-server-discord">Bot Discord</a> •
  <a href="#-risoluzione-problemi-troubleshooting">Risoluzione Problemi</a> •
  <a href="#-community--supporto">Community</a>
</p>

</div>

---

## 📌 Panoramica

**Roblox Suite Pro** è una suite desktop open-source sviluppata in Python con interfaccia grafica moderna ad alte prestazioni basata su `CustomTkinter`. È progettata per gestire automazioni anti-AFK, routine macro e sessioni multi-account simultanee senza incorrere in crash, freeze o violazioni dei meccanismi di integrità di sistema.

A differenza dei tool convenzionali che tentano memory injection o manipolazioni a livello kernel, Roblox Suite Pro impiega una pipeline basata su **Window Focus Cycling** e **DirectInput hardware scan codes**, garantendo piena conformità e stabilità operativa.

---

## 🚀 Architettura del Software

### 1. Hub Multi-Account & Window Cycling
* **Identificazione Finestre Native:** Riconosce esclusivamente i client di gioco attivi analizzando il processo proprietario (`RobloxPlayerBeta.exe`) e la classe di finestra nativa (`WINDOWSCLIENT`), escludendo schede del browser (Chrome, Edge, Firefox) e strumenti ausiliari.
* **Window Cycling Engine:** Esegue a turno il focus mirato di ciascuna istanza attiva per trasmettere scan code hardware reali via `pydirectinput`, evitando che i messaggi in background vengano ignorati dal motore di rendering Direct3D.
* **Process Manager & Fast Kill:** Monitora costantemente i PID attivi e consente sia la chiusura mirata di un singolo client sia la terminazione forzata simultanea di tutte le sessioni aperte.

### 2. Core Anti-AFK & Instant Auto-Pause
* **Input Hardware a Basso Livello:** Invio di keystroke realistici con pattern di movimento casuale (WASD), salti cadenzati e auto-clicker ausiliario.
* **Interruptible Sleep (10ms):** Il worker thread esegue micro-controlli ogni 0.01 secondi, consentendo la messa in pausa immediata senza dover attendere il completamento dei cooldown di intervallo.
* **Rilascio Forzato Tasti:** All'attivazione della pausa, tutti i tasti premuti (`keyUp`) e i pulsanti del mouse vengono rilasciati a zero millisecondi per bloccare l'inerzia del personaggio.
* **Hook Tastiera Globale:** Rileva la digitazione manuale dell'utente e sospende automaticamente il bot per non interferire con il gameplay.

---

## 🛡️ Anti-Cheat Compliance & Crash Prevention

Roblox adotta la protezione a livello kernel **Byfron (Hyperion)**. Roblox Suite Pro previene crash silenziosi, freeze e sanzioni rispettando i seguenti vincoli architetturali:

* **Zero Memory Injection:** Nessuna DLL o codice iniettato nello spazio di memoria del client di gioco.
* **Nessuna Manipolazione Mutex:** Il software non altera handle del kernel di Windows (`ROBLOX_singletonMutex`), operazione che provocherebbe la terminazione immediata del processo da parte dell'anti-cheat.
* **Nessun Buffer Scraping Invasivo:** Evita screenshot continui ad alta frequenza che saturano il rendering Direct3D.

---

## ⚙️ Guida all'Installazione & Requisiti

### 1. Requisiti di Sistema
* **Sistema Operativo:** Windows 10 o Windows 11 (64-bit).
* **Python:** Versione **3.10** o successiva ([Scarica da python.org](https://www.python.org/downloads/)).
  * ⚠️ *Durante l'installazione di Python, seleziona obbligatoriamente la casella **"Add python.exe to PATH"**.*
* **Privilegi:** Account con permessi di **Amministratore** (necessari per consentire la simulazione degli scan code hardware DirectInput).

---

### 2. File Dipendenze (`requirements.txt`)

Crea un file denominato `requirements.txt` nella cartella principale del progetto con il seguente contenuto:

```text
customtkinter>=5.2.0
pydirectinput>=1.0.4
keyboard>=0.13.5
psutil>=5.9.0
Pillow>=10.0.0
discord.py>=2.3.0
pyinstaller>=6.0.0
