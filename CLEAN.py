import re
import json

def carrega_lexico():
    sentilexpt = open('SentiLex-lem-PT02.txt','r')
    dic_palavra_polaridade = {}
    for i in sentilexpt.readlines():
        pos_ponto = i.find('.')
        palavra = (i[:pos_ponto])
        pol_pos = i.find('POL')
        polaridade = (i[pol_pos+7:pol_pos+9]).replace(';','')
        dic_palavra_polaridade[palavra] = polaridade
    return dic_palavra_polaridade

def carrega_pal_proibidas(outrospalavroes_txt, palavroes_txt, palavras_txt, palavroes_json):
    palavras_proibidas = set()
    for arquivo in outrospalavroes_txt, palavroes_txt, palavras_txt, palavroes_json:
        if arquivo.endswith('.txt'):
            with open(arquivo, 'r', encoding='utf-8') as f:
                for linha in f:
                    palavras_proibidas.add(linha.strip().lower())
        elif arquivo.endswith('.json'):
            with open(arquivo, 'r', encoding='utf-8') as f:
                palavras = json.load(f)
                for palavra in palavras:
                    palavras_proibidas.add(palavra.lower())
    return palavras_proibidas

def palavras_proibidas(outrospalavroes_txt, palavroes_txt, palavras_txt, palavroes_json):
    with open('outrospalavroes.txt', 'r') as f:
        outrospalavroes = f.read().splitlines()
    with open('palavroes.txt', 'r') as f:
        palavroes = f.read().splitlines()
    with open('palavras.txt', 'r') as f:
        palavras = f.read().splitlines()
    with open('palavroes.json', 'r') as f:
        palavroes = json.load(f)
    return outrospalavroes, palavroes, palavras, palavroes

def analyze_sentiment():

    comentario = input("Deixe uma lembrança especial: ")

    palavras_proibidas = carrega_pal_proibidas('outrospalavroes.txt', 'palavroes.txt', 'palavras.txt', 'palavroes.json')

    #Verifica se o texto contém palavras probidas e retorna ao input principal
    for palavra in palavras_proibidas:
        if palavra in comentario:
            return "Essa lembraça não pode ser publicada por ferir nossa política de uso. Por favor, tente novamente."

    # Divisão do comentário em palavras
    palavras = re.findall(r'\b\w+\b', comentario.lower())

    sentilex = carrega_lexico()

    # Contagem de palavras positivas, negativas e neutras
    count_positivo = sum(sentilex.get(palavra, 0) == '1' for palavra in palavras)
    count_negativo = sum(sentilex.get(palavra, 0) == '-1' for palavra in palavras)
    count_neutro = sum(sentilex.get(palavra, 0) == '0' for palavra in palavras)

    # Verifica se há mais palavras positivas do que negativas e neutras no comentário. Se essa condição for verdadeira, o comentário é considerado positivo.
    if count_positivo > count_negativo:
        return "Positivo"
    elif count_negativo > count_positivo:
        return "Negativo"
    else:
        return "Neutro" 
    

# Saída esperada
sentimento = analyze_sentiment()
print("Sentimento:", sentimento)
