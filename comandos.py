base_frases = {
    "ligue a luz da sala": lambda: ligar_luz("sala"),
    "ligue a luz da cozinha": lambda: ligar_luz("cozinha"),
    "que horas são": lambda: mostrar_hora(),
    "qual é a temperatura": lambda: mostrar_temperatura()
}

def ligar_luz(comodo):
    print(f"🔆 Luz do(a) {comodo} ligada!")

def mostrar_hora():
    from datetime import datetime
    print("⏰ Agora são", datetime.now().strftime("%H:%M"))

def mostrar_temperatura():
    print("🌡️ A temperatura é 25°C (exemplo).")