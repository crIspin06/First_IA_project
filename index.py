from sentence_transformers import SentenceTransformer, util
print("Baixando modelo...")

# 1. Carregando o modelo pré-treinado
modelo = SentenceTransformer('all-mpnet-base-v2') #mais rapido: all-MiniLM-L6-v2 // mais preciso: all-mpnet-base-v2
print("Modelo carregado!")

# 2. Define frases-base e funções associadas
base_frases = {
    "ligue a luz da sala": lambda: ligar_luz("sala"),
    "ligue a luz da cozinha": lambda: ligar_luz("cozinha"),
    "que horas são": lambda: mostrar_hora(),
    "qual é a temperatura": lambda: mostrar_temperatura()
}

# 3. Transforma frases-base em embeddings
frases_lista = list(base_frases.keys())
embeddings_base = modelo.encode(frases_lista, convert_to_tensor=True)

# 4. Funções simuladas
def ligar_luz(comodo):
    print(f"🔆 Luz do(a) {comodo} ligada!")

def mostrar_hora():
    from datetime import datetime
    print("⏰ Agora são", datetime.now().strftime("%H:%M"))

def mostrar_temperatura():
    print("🌡️ A temperatura é 25°C (exemplo).")

# 5. Função principal: interpreta e executa
def interpretar_comando(frase_usuario):
    embedding_entrada = modelo.encode(frase_usuario, convert_to_tensor=True)
    similaridades = util.cos_sim(embedding_entrada, embeddings_base)
    indice = similaridades.argmax().item()
    frase_mais_proxima = frases_lista[indice]
    
    print(f"\n🔍 Interpretação: '{frase_usuario}' parece com '{frase_mais_proxima}'")
    base_frases[frase_mais_proxima]()  # Executa a função

# 6. Teste com entradas do usuário
while True:
    entrada = input("\nDigite um comando (ou 'sair'): ")
    if entrada.lower() == "sair":
        break
    interpretar_comando(entrada)
