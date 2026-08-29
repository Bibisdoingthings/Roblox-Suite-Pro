import ctypes
import os
import random
import sys
import threading
import time
import webbrowser
import customtkinter as ctk
import keyboard
import psutil
import pydirectinput

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class RobloxFocusManager:
    @staticmethod
    def get_roblox_hwnds():
        """Identifica unicamente le finestre del client di gioco tramite Process ID e Class Name."""
        user32 = ctypes.windll.user32
        hwnds = []

        def enum_windows_callback(hwnd, extra):
            if user32.IsWindowVisible(hwnd):
                # 1. Verifica la classe della finestra nativa di Roblox
                class_buff = ctypes.create_unicode_buffer(256)
                user32.GetClassNameW(hwnd, class_buff, 256)
                class_name = class_buff.value

                # 2. Verifica il processo reale proprietario dell'HWND
                pid = ctypes.c_ulong()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                
                try:
                    proc = psutil.Process(pid.value)
                    proc_name = proc.name().lower()
                    
                    # Filtra escludendo Chrome, Edge, Firefox, Explorer e tool di editing
                    if "robloxplayer" in proc_name and class_name == "WINDOWSCLIENT":
                        hwnds.append(hwnd)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
        user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)
        return hwnds

    @staticmethod
    def bring_to_front(hwnd):
        user32 = ctypes.windll.user32
        if user32.IsIconic(hwnd):
            user32.ShowWindow(hwnd, 9)  # SW_RESTORE
        user32.SetForegroundWindow(hwnd)

class RobloxMasterSuite(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Roblox Suite Pro - DirectInput Focus Engine")
        self.geometry("620x680")
        self.minsize(560, 600)
        self.attributes("-topmost", True)

        icon_file = resource_path("icon.ico")
        if os.path.exists(icon_file):
            try:
                self.iconbitmap(icon_file)
            except Exception:
                pass

        self.is_running = True
        self.is_bot_active = False
        self.bot_sending_input = False
        self.roblox_detected = False

        self.current_toggle_key = "f6"
        self.current_exit_key = "f7"
        self.movement_keys = ['w', 'a', 's', 'd']

        self.all_keys = [
            "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
            "num 1", "num 2", "num 3", "num 4", "num 5", "num 6", "num 7", "num 8", "num 9", "num 0",
            "insert", "delete", "home", "end", "page up", "page down", "pause"
        ]

        self.build_ui()
        self.setup_hooks()

        self.bot_thread = threading.Thread(target=self.focus_automation_loop, daemon=True)
        self.bot_thread.start()

        self.monitor_thread = threading.Thread(target=self.process_monitor_loop, daemon=True)
        self.monitor_thread.start()

        self.protocol("WM_DELETE_WINDOW", self.stop_and_close)

    def is_roblox_running(self) -> bool:
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name']
                if name and 'RobloxPlayer' in name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")

        title = ctk.CTkLabel(
            header_frame,
            text="ROBLOX SUITE PRO",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#38bdf8"
        )
        title.pack(side="left")

        self.process_badge = ctk.CTkLabel(
            header_frame,
            text="● Client: Non Rilevato",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ef4444"
        )
        self.process_badge.pack(side="right")

        self.status_banner = ctk.CTkLabel(
            self,
            text="STATO: INATTIVO",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#f87171",
            fg_color="#1e293b",
            corner_radius=8,
            height=38
        )
        self.status_banner.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.tabs = ctk.CTkTabview(self, corner_radius=10)
        self.tabs.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")

        self.tab_afk = self.tabs.add("Anti-AFK")
        self.tab_instances = self.tabs.add("Gestione Istanze")
        self.tab_community = self.tabs.add("Community")

        self.build_afk_tab()
        self.build_instances_tab()
        self.build_community_tab()

        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=3, column=0, padx=20, pady=(5, 15), sticky="ew")
        footer_frame.grid_columnconfigure((0, 1), weight=1)

        self.toggle_btn = ctk.CTkButton(
            footer_frame,
            text=f"AVVIA ({self.current_toggle_key.upper()})",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#22c55e",
            hover_color="#16a34a",
            height=40,
            command=self.toggle_bot
        )
        self.toggle_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.exit_btn = ctk.CTkButton(
            footer_frame,
            text=f"ESCI ({self.current_exit_key.upper()})",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            height=40,
            command=self.stop_and_close
        )
        self.exit_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")

    def build_afk_tab(self):
        self.tab_afk.grid_columnconfigure(1, weight=1)

        self.auto_pause_switch = ctk.CTkSwitch(
            self.tab_afk,
            text="Pausa Automatica alla Digitazione Manuale",
            onvalue=True,
            offvalue=False
        )
        self.auto_pause_switch.select()
        self.auto_pause_switch.grid(row=0, column=0, columnspan=2, padx=15, pady=(12, 6), sticky="w")

        self.jump_switch = ctk.CTkSwitch(
            self.tab_afk,
            text="Includi Salto (Spazio)",
            onvalue=True,
            offvalue=False
        )
        self.jump_switch.select()
        self.jump_switch.grid(row=1, column=0, columnspan=2, padx=15, pady=6, sticky="w")

        ctk.CTkLabel(self.tab_afk, text="Tasto Toggle (Avvio/Pausa):").grid(row=2, column=0, padx=15, pady=8, sticky="w")
        self.toggle_dropdown = ctk.CTkComboBox(self.tab_afk, values=self.all_keys, command=self.on_hotkey_changed, state="readonly")
        self.toggle_dropdown.set(self.current_toggle_key)
        self.toggle_dropdown.grid(row=2, column=1, padx=15, pady=8, sticky="ew")

        ctk.CTkLabel(self.tab_afk, text="Tasto Uscita Rapida:").grid(row=3, column=0, padx=15, pady=8, sticky="w")
        self.exit_dropdown = ctk.CTkComboBox(self.tab_afk, values=self.all_keys, command=self.on_hotkey_changed, state="readonly")
        self.exit_dropdown.set(self.current_exit_key)
        self.exit_dropdown.grid(row=3, column=1, padx=15, pady=8, sticky="ew")

        ctk.CTkLabel(self.tab_afk, text="Intervallo Azioni:").grid(row=4, column=0, padx=15, pady=(10, 2), sticky="w")
        self.interval_slider = ctk.CTkSlider(self.tab_afk, from_=0.5, to=5.0, number_of_steps=45)
        self.interval_slider.set(1.5)
        self.interval_slider.grid(row=5, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

        self.interval_label = ctk.CTkLabel(self.tab_afk, text="1.5s", text_color="#94a3b8")
        self.interval_label.grid(row=4, column=1, padx=15, pady=(10, 2), sticky="e")
        self.interval_slider.configure(command=lambda val: self.interval_label.configure(text=f"{val:.1f}s"))

    def build_instances_tab(self):
        self.tab_instances.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.tab_instances,
            text="Terminazione Processi:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 2))

        kill_frame = ctk.CTkFrame(self.tab_instances, fg_color="transparent")
        kill_frame.pack(fill="x", padx=15, pady=4)
        kill_frame.grid_columnconfigure(0, weight=1)
        kill_frame.grid_columnconfigure(1, weight=1)

        self.kill_all_btn = ctk.CTkButton(
            kill_frame,
            text="CHIUDI TUTTI I CLIENT ROBLOX",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#b91c1c",
            hover_color="#991b1b",
            height=32,
            command=self.kill_all_roblox_instances
        )
        self.kill_all_btn.grid(row=0, column=0, columnspan=2, pady=4, sticky="ew")

        self.pid_entry = ctk.CTkEntry(kill_frame, placeholder_text="PID specifico...", height=30)
        self.pid_entry.grid(row=1, column=0, padx=(0, 5), pady=4, sticky="ew")

        self.kill_pid_btn = ctk.CTkButton(
            kill_frame,
            text="Chiudi PID",
            fg_color="#475569",
            hover_color="#334155",
            height=30,
            command=self.kill_specific_pid
        )
        self.kill_pid_btn.grid(row=1, column=1, padx=(5, 0), pady=4, sticky="ew")

        ctk.CTkLabel(
            self.tab_instances,
            text="Log Attività & Finestre:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 2))

        self.instance_log = ctk.CTkTextbox(self.tab_instances, height=150, activate_scrollbars=True)
        self.instance_log.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        self.instance_log.insert("end", "[SISTEMA] Pronto. DirectInput Engine attivo.\n")
        self.instance_log.configure(state="disabled")

    def build_community_tab(self):
        self.tab_community.grid_columnconfigure((0, 1), weight=1)

        info_box = ctk.CTkLabel(
            self.tab_community,
            text="Roblox Suite Pro - DirectInput Native Engine.",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8",
            justify="center"
        )
        info_box.grid(row=0, column=0, columnspan=2, padx=15, pady=(20, 15))

        discord_btn = ctk.CTkButton(
            self.tab_community,
            text="Discord",
            fg_color="#5865F2",
            hover_color="#4752C4",
            command=lambda: webbrowser.open("https://discord.gg")
        )
        discord_btn.grid(row=1, column=0, padx=10, pady=8, sticky="ew")

        github_btn = ctk.CTkButton(
            self.tab_community,
            text="GitHub",
            fg_color="#24292F",
            hover_color="#1B1F23",
            command=lambda: webbrowser.open("https://github.com")
        )
        github_btn.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

    def kill_all_roblox_instances(self):
        killed = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = proc.info['name']
                if name and 'RobloxPlayer' in name:
                    proc.kill()
                    killed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if killed > 0:
            self.log_event(f"[KILL] Terminate {killed} istanze di Roblox.")
        else:
            self.log_event("[KILL] Nessun client Roblox trovato in esecuzione.")

    def kill_specific_pid(self):
        pid_text = self.pid_entry.get().strip()
        if not pid_text.isdigit():
            self.log_event("[ERRORE] Inserisci un PID numerico valido.")
            return

        target_pid = int(pid_text)
        try:
            target_proc = psutil.Process(target_pid)
            if 'RobloxPlayer' in target_proc.name():
                target_proc.kill()
                self.log_event(f"[KILL] Istanza Roblox PID {target_pid} chiusa.")
                self.pid_entry.delete(0, 'end')
            else:
                self.log_event(f"[AVVISO] Il PID {target_pid} non appartiene a Roblox.")
        except psutil.NoSuchProcess:
            self.log_event(f"[ERRORE] Nessun processo trovato con PID {target_pid}.")
        except psutil.AccessDenied:
            self.log_event(f"[ERRORE] Permessi insufficienti per terminare il PID {target_pid}.")

    def on_hotkey_changed(self, _=None):
        self.current_toggle_key = self.toggle_dropdown.get().lower()
        self.current_exit_key = self.exit_dropdown.get().lower()

        self.toggle_dropdown.configure(values=[k for k in self.all_keys if k != self.current_exit_key])
        self.exit_dropdown.configure(values=[k for k in self.all_keys if k != self.current_toggle_key])

        t_key = self.current_toggle_key.upper()
        self.toggle_btn.configure(text=f"AVVIA ({t_key})" if not self.is_bot_active else f"METTI IN PAUSA ({t_key})")
        self.exit_btn.configure(text=f"ESCI ({self.current_exit_key.upper()})")

    def setup_hooks(self):
        keyboard.hook(self.on_keyboard_event)

    def on_keyboard_event(self, event):
        if event.event_type != 'down' or self.bot_sending_input:
            return

        key = event.name.lower() if event.name else ""

        if key == self.current_toggle_key:
            self.after(0, self.toggle_bot)
        elif key == self.current_exit_key:
            self.after(0, self.stop_and_close)
        elif self.is_bot_active and self.auto_pause_switch.get():
            self.after(0, self.set_bot_state, False)

    def toggle_bot(self):
        if not self.is_bot_active and not self.is_roblox_running():
            self.status_banner.configure(text="ERRORE: APRI ROBLOX PRIMA DI AVVIARE", text_color="#f87171", fg_color="#450a0a")
            self.log_event("[BLOCCO] Avvio annullato: Roblox non è aperto.")
            return
        self.set_bot_state(not self.is_bot_active)

    def release_all_keys(self):
        try:
            for k in self.movement_keys:
                pydirectinput.keyUp(k)
            pydirectinput.keyUp('space')
        except Exception:
            pass

    def set_bot_state(self, active: bool):
        self.is_bot_active = active
        t_key = self.current_toggle_key.upper()

        if self.is_bot_active:
            self.status_banner.configure(text="STATO: ATTIVO", text_color="#4ade80", fg_color="#064e3b")
            self.toggle_btn.configure(text=f"METTI IN PAUSA ({t_key})", fg_color="#eab308", hover_color="#ca8a04")
        else:
            self.release_all_keys()
            self.status_banner.configure(text="STATO: IN PAUSA", text_color="#f87171", fg_color="#1e293b")
            self.toggle_btn.configure(text=f"AVVIA ({t_key})", fg_color="#22c55e", hover_color="#16a34a")

    def interruptible_sleep(self, duration: float) -> bool:
        steps = int(duration / 0.01)
        for _ in range(steps):
            if not self.is_running or not self.is_bot_active:
                return False
            time.sleep(0.01)
        return True

    def focus_automation_loop(self):
        """Cicla solo sulle finestre native di gioco identificate."""
        while self.is_running:
            if not self.is_bot_active:
                time.sleep(0.01)
                continue

            hwnds = RobloxFocusManager.get_roblox_hwnds()
            if not hwnds:
                time.sleep(0.5)
                continue

            for hwnd in hwnds:
                if not self.is_bot_active:
                    break

                RobloxFocusManager.bring_to_front(hwnd)
                time.sleep(0.05)

                self.bot_sending_input = True
                try:
                    chosen_key = random.choice(self.movement_keys)
                    pydirectinput.keyDown(chosen_key)
                    if not self.interruptible_sleep(0.18):
                        pydirectinput.keyUp(chosen_key)
                        break
                    pydirectinput.keyUp(chosen_key)

                    if self.jump_switch.get() and self.is_bot_active:
                        pydirectinput.press('space')
                finally:
                    self.bot_sending_input = False

            cooldown = self.interval_slider.get()
            self.interruptible_sleep(cooldown)

    def process_monitor_loop(self):
        last_count = -1
        while self.is_running:
            try:
                hwnds = RobloxFocusManager.get_roblox_hwnds()
                count = len(hwnds)
                self.roblox_detected = (count > 0)

                if count != last_count:
                    last_count = count
                    if count > 0:
                        self.process_badge.configure(
                            text=f"● Finestre Attive: {count}",
                            text_color="#22c55e"
                        )
                        self.log_event(f"[CLIENT] Rilevate {count} finestre di gioco effettive.")
                    else:
                        self.process_badge.configure(text="● Client: Non Rilevato", text_color="#ef4444")
                        self.log_event("[CLIENT] Nessuna finestra Roblox trovata.")
                        if self.is_bot_active:
                            self.after(0, self.set_bot_state, False)
                            self.after(0, lambda: self.status_banner.configure(
                                text="STATO: FERMATO (ROBLOX CHIUSO)",
                                text_color="#f87171",
                                fg_color="#450a0a"
                            ))
            except Exception:
                pass
            time.sleep(2)

    def log_event(self, msg: str):
        try:
            self.instance_log.configure(state="normal")
            self.instance_log.insert("end", f"{msg}\n")
            self.instance_log.see("end")
            self.instance_log.configure(state="disabled")
        except Exception:
            pass

    def stop_and_close(self):
        self.is_bot_active = False
        self.is_running = False
        self.release_all_keys()
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        self.destroy()

if __name__ == "__main__":
    app = RobloxMasterSuite()
    app.mainloop()
