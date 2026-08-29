<div align="center">

# ⚡ Roblox Suite Pro

**High-Performance Multi-Instance Automation & Focus Cycling Engine for Roblox**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%2F%2011-0078D6.svg?logo=windows&logoColor=white)](https://www.microsoft.com/)
[![Anti-Cheat](https://img.shields.io/badge/Byfron%2FHyperion-Safe%20%E2%9C%93-brightgreen.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2.svg?logo=discord&logoColor=white)](https://discord.gg/YOUR_INVITE_LINK)

<br />

<p align="center">
  <a href="#-panoramica">Panoramica</a> •
  <a href="#-caratteristiche-principali">Caratteristiche</a> •
  <a href="#-anti-cheat-compliance">Sicurezza Byfron</a> •
  <a href="#-installazione--avvio">Installazione</a> •
  <a href="#-compilazione-exe">Compilazione</a> •
  <a href="#-community--supporto">Community</a>
</p>

</div>

---

## 📌 Panoramica

**Roblox Suite Pro** è una suite desktop open-source scritta in Python e basata su un'interfaccia moderna in `CustomTkinter`. È progettata per gestire automazioni anti-AFK, cicli macro e sessioni multi-account simultanee senza incorrere in crash o violazioni dell'integrità del processo.

A differenza dei tool convenzionali che tentano hook nella memoria di gioco o modifiche a livello kernel, Roblox Suite Pro impiega una pipeline basata su **Window Focus Cycling** e **DirectInput hardware scan codes**, garantendo totale conformità con i sistemi di protezione del client.

---

## 🚀 Caratteristiche Principali

| Modulo | Descrizione |
|---|---|
| **Multi-Instance Cycling** | Rileva automaticamente tutte le finestre `WINDOWSCLIENT` attive e distribuisce a turno i comandi hardware senza desincronizzazioni. |
| **DirectInput Hardware Engine** | Invio di keystroke nativi a basso livello (`pydirectinput`) compatibili con il rendering DirectX/Direct3D. |
| **Instant Auto-Pause** | Hook tastiera globale (`keyboard`) che sospende immediatamente il bot e azzera l'inerzia dei tasti non appena l'utente digita manualmente. |
| **Process Manager & Fast Kill** | Monitoraggio continuo dei PID con possibilità di terminare istanze singole o forzare la chiusura rapida di tutti i client. |
| **Interfaccia Dark Moderna** | UI modulare ad alto contrasto con personalizzazione a runtime di intervalli, hotkey di attivazione ed esecuzione. |

---

## 🛡️ Anti-Cheat Compliance

Roblox Suite Pro adotta un'architettura rigorosamente **non invasiva**:

* **Zero Memory Injection:** Nessuna DLL iniettata all'interno dello spazio di indirizzamento di `RobloxPlayerBeta.exe`.
* **Nessun Mutex Manipulation:** Non tenta di forzare o dirottare handle del kernel di Windows (`ROBLOX_singletonMutex`), eliminando alla radice i freeze o i crash provocati da Byfron (Hyperion).
* **DirectInput Scan Codes:** I comandi vengono inviati simulando l'hardware fisico tramite le API di input di Windows.

---

## ⚙️ Installazione & Avvio

### Prerequisiti
* **Sistema Operativo:** Windows 10 o Windows 11 (64-bit)
* **Python:** Versione 3.10 o successiva

### Configurazione Rapida

1. **Clona la repository:**
   ```bash
   git clone [https://github.com/TUO_USERNAME/Roblox-Suite-Pro.git](https://github.com/TUO_USERNAME/Roblox-Suite-Pro.git)
   cd Roblox-Suite-Pro
