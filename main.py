# Programa principal — Índice Remissivo usando Árvore AVL
# Autor: Gustavo Borges Rodrigues Costa
# Curso: Gestão da Informação — UFU
#
# Este script:
#   1. Lê um arquivo de texto (texto_de_origem.txt) (dom_casmurro.txt nesse caso)
#   2. Extrai todas as palavras, linha por linha, ignorando
#      pontuação e diferenças entre maiúsculas/minúsculas
#   3. Insere cada palavra na árvore AVL, junto da linha em
#      que ela ocorreu
#   4. Demonstra as operações de busca, busca por prefixo,
#      medidor de equilíbrio, palavra mais frequente e remoção
#   5. Gera o arquivo final indice_remissivo.txt

import re
import time

from avl import AVL


ARQUIVO_ENTRADA = 'dom_casmurro.txt'
ARQUIVO_SAIDA = 'indice_remissivo.txt'

# Expressão regular que captura sequências de letras (incluindo
# acentuação em português), ignorando números e pontuação.
PADRAO_PALAVRA = re.compile(r"[^\W\d_]+", re.UNICODE)
# ^:negar \W:qualquer caractere que não seja número ou "_" \d:querquer número _:"_" aqui a gente inclui ele ja que \W não inclui +: uma ou mais ocorrências


def extrai_palavras(linha_texto):
    """Recebe uma linha de texto bruta e retorna a lista de
    palavras encontradas, já convertidas para minúsculas e
    sem nenhum símbolo de pontuação."""
    return PADRAO_PALAVRA.findall(linha_texto.lower())


def constroi_indice(caminho_arquivo):
    """Lê o arquivo de texto linha por linha e constrói a árvore
    AVL com todas as palavras encontradas. Retorna a árvore
    pronta e o tempo total gasto na construção."""
    arvore = AVL()

    inicio = time.perf_counter()

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            palavras_da_linha = extrai_palavras(linha)
            for palavra in palavras_da_linha:
                arvore.inserePalavra(palavra, numero_linha)

    tempo_total = time.perf_counter() - inicio
    return arvore, tempo_total


def imprime_separador(titulo):
    print(f'\n{"=" * 60}') #apenas para deixar o terminal mais "bonito"
    print(f'  {titulo}')
    print(f'{"=" * 60}')


def main():
    imprime_separador('CONSTRUÇÃO DO ÍNDICE REMISSIVO')

    arvore, tempo_construcao = constroi_indice(ARQUIVO_ENTRADA)

    print(f'Número total de palavras: {arvore.totalPalavras()}')
    print(f'Número de palavras distintas: {arvore.palavrasDistintas()}')
    print(f'Número de palavras descartadas (repetidas): '
          f'{arvore.totalPalavras() - arvore.palavrasDistintas()}')
    print(f'Tempo de construção do índice usando árvore AVL: '
          f'{tempo_construcao:.4f}s.')
    print(f'Total de rotações executadas: {arvore.totalRotacoes()}')


    # Demonstração: busca simples
    
    imprime_separador('BUSCA SIMPLES')

    palavras_teste = ['arvore', 'algoritmo', 'inexistente']
    for palavra in palavras_teste:
        resultado = arvore.busca(palavra)
        if resultado:
            print(f'"{palavra}" encontrada nas linhas: {sorted(resultado)}')
        else:
            print(f'"{palavra}" não foi encontrada no texto.')


    # Demonstração: busca por prefixo

    imprime_separador('BUSCA APROXIMADA POR PREFIXO')

    prefixos_teste = ['arv', 'pra', 'estr']
    for prefixo in prefixos_teste:
        resultado = arvore.buscaPrefixo(prefixo)
        print(f'Prefixo "{prefixo}": {resultado}')


    # Demonstração: medidor de equilíbrio (ME)

    imprime_separador('MEDIDOR DE EQUILÍBRIO (ME)')

    palavras_me = ['casa', 'planta', 'naoexisteestapalavra']
    for palavra in palavras_me:
        resultado = arvore.medidorEquilibrio(palavra)

        if resultado == -1:
            print(f'"{palavra}": palavra não encontrada no índice.') #não existe
        elif resultado == 0:
            print(f'"{palavra}": ponto da árvore perfeitamente equilibrado (ME = 0).')
        else:
            print(f'"{palavra}": ponto da árvore desequilibrado (ver valor de ME acima).')


    # Demonstração: palavra mais frequente

    imprime_separador('PALAVRA MAIS FREQUENTE')

    palavra, qtd_linhas = arvore.palavraMaisFrequente()
    print(f'A palavra mais frequente é "{palavra}", '
          f'presente em {qtd_linhas} linha(s) diferentes.')

    # Demonstração: remoção
    
    imprime_separador('REMOÇÃO DE OCORRÊNCIAS')

    linhas_antes = arvore.busca('arvore')
    print(f'Antes da remoção, "arvore" aparece nas linhas: {sorted(linhas_antes)}')

    primeira_linha = sorted(linhas_antes)[0]
    arvore.removePalavra('arvore', primeira_linha)

    linhas_depois = arvore.busca('arvore')
    print(f'Após remover a linha {primeira_linha}, '
          f'"arvore" aparece nas linhas: {sorted(linhas_depois)}')


    # Geração do aquivo final do índice

    imprime_separador('GERANDO ARQUIVO DE ÍNDICE')

    arquivo_gerado = arvore.imprimeIndice(ARQUIVO_SAIDA, tempo_construcao)
    print(f'Índice remissivo completo salvo em: {arquivo_gerado}')


if __name__ == '__main__': #para reutilizar as funções do arquivo sem rodar o programa inteiro
    main()
