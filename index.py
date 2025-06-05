#Importação de bibliotecas
from sentence_transformers import SentenceTransformer, util
from comandos import *

#Carregando modelo de linguagem (substituir por um próprio no futuro)
print("Carregando modelo...")
modelo = SentenceTransformer('all-MiniLM-L6-v2') #mais rapido: " all-MiniLM-L6-v2 "// mais preciso: " all-mpnet-base-v2 "
print("Modelo carregado!")

#Transformando as frases-base em embeddings
frases_lista = list(base_frases.keys())
embeddings_base = modelo.encode(frases_lista, convert_to_tensor=True)

#Interpretando o input
def interpretar_comando(frase_usuario, threshold=0.6):
    embedding_entrada = modelo.encode(frase_usuario, convert_to_tensor=True)
    similaridades = util.cos_sim(embedding_entrada, embeddings_base)
    indice = similaridades.argmax().item()
    similaridade_valor = similaridades[0][indice].item()
    
    if (similaridade_valor >= threshold):
        frase_mais_proxima = frases_lista[indice]
        print(f"\n🔍 Interpretação: '{frase_usuario}' parece com '{frase_mais_proxima}'")
        base_frases[frase_mais_proxima]()  # Executa a função
    else:
        print(f"\n🤔 Não entendi o que você quis dizer. (similaridade: {similaridade_valor:.2f})")

#Execução e interação com o usuário
while True:
    entrada = input("\nDigite um comando (ou 'sair'): ")
    if entrada.lower() == "sair":
        break
    interpretar_comando(entrada)
