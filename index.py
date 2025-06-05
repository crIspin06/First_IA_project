#Importação de bibliotecas
from sentence_transformers import SentenceTransformer, util
from comandos import *

#Carregando modelo de linguagem (substituir por um próprio no futuro)
print("Carregando modelo...")
modelo = SentenceTransformer('all-MiniLM-L6-v2') #mais rapido: " all-MiniLM-L6-v2 "// mais preciso: " all-mpnet-base-v2 "
print("Modelo carregado!")

#Transformando emembeddings
    #Transformando a ação
frases_acoes = list(acoes.keys())
embeddings_acoes = modelo.encode(frases_acoes, convert_to_tensor=True)
    #Transformando os parâmetros
frases_parametros = list(parametros.keys())
embeddings_parametros = modelo.encode(frases_parametros, convert_to_tensor=True)


#Interpretando o input
def interpretar_comando(frase_usuario, threshold=0.55):
    emb_usuario = modelo.encode(frase_usuario, convert_to_tensor=True)  #Transforma o input do usuário em um vetor de números
    
    #Verificando Similaridades
        #Da ação...
    sim_acoes = util.cos_sim(emb_usuario, embeddings_acoes)             #Compara o input do usuário com a lista de ações, pra ver se existe alguma disponível  (comandos.py)
    idx_acao = sim_acoes.argmax().item()                                #Pega o índice da frase mais parecida com a do usuário, dentre as opções
    valor_acao = sim_acoes[0][idx_acao].item()                          #Valor de similaridade com a ação mais próxima, pra tentar identificar se houve um input aleatório
    
        #Dos parâmetros...
    contexto = extrair_parametro(frase_usuario) #Tenta extrair pelo próprio input pra economizar processamento
    #Se não conseguir, tenta ir pela aproximação
    if not contexto:
        sim_params = util.cos_sim(emb_usuario, embeddings_parametros)       #  -=-
        idx_param = sim_params.argmax().item()                              #  Essas três linhas fazem a mesma coisa, mas com os parâmetros.
        valor_param = sim_params[0][idx_param].item()                       #  -=-
        #Se o usuário falou um parâmetro reconhecível, adiciona no contexto
        if valor_param >= .4:
            param_frase = frases_parametros[idx_param]
            contexto = parametros[param_frase]

    #Se a similaridade for menor que um valor mínimo (provavelmente é um input aleatório)
    if (valor_acao < threshold):
        print(f"\n🤔 Não entendi o que você quis dizer.")
        return

    funcao_acao = acoes[frases_acoes[idx_acao]]         #  ==> Pega a função associada à frase

    #Debugg
    if 'idx_param' in locals():         #Ve se "idx_param" existe, se sim, entrou no if da linha 32
        param_texto = frases_parametros[idx_param]
        similaridade_texto = f"{valor_param:.2f}"
    else:
        param_texto = str(contexto)
        similaridade_texto = "N/A"
    print(f"\n👤 Usuário disse: {frase_usuario}")
    print(f"🔍 Ação mais parecida: '{frases_acoes[idx_acao]}' (similaridade: {valor_acao:.2f})")
    print(f"🔍 Parâmetro mais parecido: '{param_texto}' (similaridade: {similaridade_texto})")
    print(f"Contexto: {contexto}")
    print(f"Função à chamar: {funcao_acao}")

    #Tenta chamar a função passando os parametros
    try:
        funcao_acao(**contexto)
    #Se não aceitar, chama sem parametro nenhum mesmo
    except TypeError:
        funcao_acao()


#Execução e interação com o usuário
while True:
    entrada = input("\nDigite um comando (ou 'sair'): ")
    if entrada.lower() == "sair":
        break
    interpretar_comando(entrada)
