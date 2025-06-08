def ligar_luz(comodo=None):
    print(f"💡 Ligando luz no(a): {comodo or 'desconhecido'}")

def mostrar_hora():
    from datetime import datetime
    print("⏰ Agora são", datetime.now().strftime("%H:%M"))

#Dicionário de ações possíveis
acoes = {
    "ligue a luz": ligar_luz,
    "que horas são?": mostrar_hora
}

#Dicionário de parâmetros possíveis
parametros = {
    "cozinha": {"comodo": "cozinha"},
    "sala": {"comodo": "sala"},
    "banheiro": {"comodo": "banheiro"}
}


#funções (separar depois)
#Tenta buscar os parametros antes de passar pelo modelo, pra otimizar processamento, sla é um teste ae kkkkk
def extrair_parametro(frase_usuario):
        palavras = frase_usuario.lower().split()
        for palavra in palavras:
            if palavra in parametros:
                return parametros[palavra]
        return {}
