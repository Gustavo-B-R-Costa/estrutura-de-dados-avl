# Classe AVL — árvore binária de busca balanceada (AVL),
# adaptada para armazenar PALAVRAS em ordem alfabética e suas
# respectivas linhas de ocorrência num texto.
#
# A organização desta classe segue o mesmo padrão visto em
# aula para árvores AVL numéricas (rotações LL, RR, LR, RL,
# fator de balanceamento e altura), mas comparando PALAVRAS
# (strings) ao invés de números.

from no import NO


class AVL:
    def __init__(self):
        self.__raiz = None

        # Estatísticas do índice, atualizadas durante a construção
        self.__total_palavras = 0       # total de tokens processados (token:palavra processada pelo programa, inclui palavras repetidas)
        self.__palavras_distintas = 0   # total de nós (palavras únicas)
        self.__rotacoes = 0             # total de rotações realizadas

        # Flag interna usada para saber se a última inserção criou
        # um nó novo (palavra distinta) ou apenas atualizou um nó
        # já existente (palavra repetida).
        self.__nova_palavra = False

    def totalPalavras(self):
        return self.__total_palavras

    def palavrasDistintas(self):
        return self.__palavras_distintas

    def totalRotacoes(self):
        return self.__rotacoes

    def vazia(self):
        return self.__raiz is None

    def __altura(self, no):
        if no is None:
            return -1
        return no.altura

    def __maior(self, x, y):
        return x if x > y else y

    def __fatorBalanceamento(self, no):
        """Fator de balanceamento COM SINAL:
          > 0  -> lado esquerdo mais alto
          < 0  -> lado direito mais alto
          == 0 -> perfeitamente equilibrado"""
        return self.__altura(no.esq) - self.__altura(no.dir)

    def __atualizaAltura(self, no):
        no.altura = self.__maior(self.__altura(no.esq), self.__altura(no.dir)) + 1

    # Rotações da árvore AVL
    # (mesmo princípio das rotações vistas em aula: LL, RR, LR, RL)

    def __rotacaoLL(self, A):
        self.__rotacoes += 1
        B = A.esq
        A.esq = B.dir
        B.dir = A
        self.__atualizaAltura(A)
        self.__atualizaAltura(B)
        return B

    def __rotacaoRR(self, A):
        self.__rotacoes += 1
        B = A.dir
        A.dir = B.esq
        B.esq = A
        self.__atualizaAltura(A)
        self.__atualizaAltura(B)
        return B

    def __rotacaoLR(self, A):
        A.esq = self.__rotacaoRR(A.esq)
        return self.__rotacaoLL(A)

    def __rotacaoRL(self, A):
        A.dir = self.__rotacaoLL(A.dir)
        return self.__rotacaoRR(A)

    def __balanceia(self, no):
        """Verifica o fator de balanceamento de um nó e aplica a
        rotação adequada, caso necessário. Essa função é chamada
        após toda inserção e remoção, subindo da folha até a raiz."""
        fb = self.__fatorBalanceamento(no)

        if fb > 1:   # lado esquerdo mais pesado
            if self.__fatorBalanceamento(no.esq) >= 0:
                no = self.__rotacaoLL(no)
            else:
                no = self.__rotacaoLR(no)

        elif fb < -1:   # lado direito mais pesado
            if self.__fatorBalanceamento(no.dir) <= 0:
                no = self.__rotacaoRR(no)
            else:
                no = self.__rotacaoRL(no)

        return no


    # Inserção

    def inserePalavra(self, palavra, linha):
        """Insere uma palavra e a linha em que ela ocorreu na árvore.
        Se a palavra já existir, apenas adiciona a linha à lista
        de ocorrências (sem criar um novo nó)."""
        palavra = palavra.lower()
        self.__total_palavras += 1
        self.__nova_palavra = False

        self.__raiz = self.__insereValor(self.__raiz, palavra, linha)

        if self.__nova_palavra:
            self.__palavras_distintas += 1

    def __insereValor(self, atual, palavra, linha):
        if atual is None:
            self.__nova_palavra = True
            return NO(palavra, linha)

        if palavra < atual.palavra:
            atual.esq = self.__insereValor(atual.esq, palavra, linha)
        elif palavra > atual.palavra:
            atual.dir = self.__insereValor(atual.dir, palavra, linha)
        else:
            # Palavra já existe: apenas registra a nova linha
            atual.adicionaLinha(linha)
            return atual

        self.__atualizaAltura(atual)
        return self.__balanceia(atual)

    # Busca simples

    def busca(self, palavra):
        """Retorna a lista de linhas em que a palavra aparece, ou
        None caso a palavra não exista no índice."""
        palavra = palavra.lower()
        atual = self.__raiz

        while atual is not None:
            if palavra == atual.palavra:
                return atual.linhas
            elif palavra > atual.palavra:
                atual = atual.dir
            else:
                atual = atual.esq

        return None

    def __buscaNo(self, atual, palavra):
        """Retorna o NÓ correspondente à palavra (uso interno)."""
        while atual is not None:
            if palavra == atual.palavra:
                return atual
            elif palavra > atual.palavra:
                atual = atual.dir
            else:
                atual = atual.esq
        return None


    # Busca aproximada por prefixo

    def buscaPrefixo(self, prefixo):
        prefixo = prefixo.lower()
        resultado = []
        self.__buscaPrefixoRec(self.__raiz, prefixo, resultado)
        return resultado

    def __buscaPrefixoRec(self, atual, prefixo, resultado):
        if atual is None:
            return

        # Percurso em ordem garante que o resultado final já
        # venha em ordem alfabética, sem necessidade de sort().
        self.__buscaPrefixoRec(atual.esq, prefixo, resultado)
        if atual.palavra.startswith(prefixo):
            resultado.append(atual.palavra)
        self.__buscaPrefixoRec(atual.dir, prefixo, resultado)


    # Medidor de equilibrio (ME) de uma palavra
    # ME = (nº de nós da subárvore esquerda) - (nº de nós da
    #      subárvore direita), a partir do nó da palavra buscada.
    #
    # Retorno:
    #   -1 -> palavra não encontrada
    #    0 -> palavra encontrada, ME == 0 (equilibrado)
    #    1 -> palavra encontrada, ME != 0 (e imprime o valor de ME)

    def __contaNos(self, no):
        if no is None:
            return 0
        return 1 + self.__contaNos(no.esq) + self.__contaNos(no.dir)

    def medidorEquilibrio(self, palavra):
        palavra = palavra.lower()
        no = self.__buscaNo(self.__raiz, palavra)

        if no is None:
            return -1

        qtd_esq = self.__contaNos(no.esq)
        qtd_dir = self.__contaNos(no.dir)
        me = qtd_esq - qtd_dir

        if me == 0:
            return 0
        else:
            print(f'Medidor de equilíbrio de "{palavra}": {me}')
            return 1


    # Palavra mais frequente (aparece em mais linhas distintas)

    def palavraMaisFrequente(self):
        self.__melhor_palavra = None #palavra que, até aquele instante, apareceu em mais linhas.
        self.__melhor_qtd = -1 #quantidade de linhas dessa palavra, começa em -1 pq a primeira é a melhor até o momento
        self.__palavraMaisFrequenteRec(self.__raiz)
        return self.__melhor_palavra, self.__melhor_qtd

    def __palavraMaisFrequenteRec(self, atual):
        if atual is None:
            return

        self.__palavraMaisFrequenteRec(atual.esq)

        qtd_linhas = len(atual.linhas)
        if qtd_linhas > self.__melhor_qtd:
            self.__melhor_qtd = qtd_linhas
            self.__melhor_palavra = atual.palavra

        self.__palavraMaisFrequenteRec(atual.dir)

    #Remoção
    # A remoção é feita indicando a palavra e a linha a remover.
    # Se, após remover a linha, a lista de ocorrências ficar
    # vazia, o nó inteiro é removido da árvore (com rebalanceamento).
    
    def removePalavra(self, palavra, linha):
        palavra = palavra.lower()
        no = self.__buscaNo(self.__raiz, palavra)

        if no is None:
            return False   # palavra não existe no índice

        if linha not in no.linhas:
            return False   # a palavra não ocorre nessa linha

        ficou_vazio = no.removeLinha(linha)

        if ficou_vazio:
            self.__raiz = self.__removeNo(self.__raiz, palavra)
            self.__palavras_distintas -= 1

        return True

    def __menorNo(self, no):
        """Encontra o nó com a menor palavra de uma subárvore."""
        atual = no
        while atual.esq is not None:
            atual = atual.esq
        return atual

    def __removeNo(self, atual, palavra):
        if atual is None:
            return None

        if palavra < atual.palavra:
            atual.esq = self.__removeNo(atual.esq, palavra)
        elif palavra > atual.palavra:
            atual.dir = self.__removeNo(atual.dir, palavra)
        else:
            # Encontrou o nó a ser removido
            if atual.esq is None:
                return atual.dir
            elif atual.dir is None:
                return atual.esq
            else:
                # Nó com dois filhos: substitui pelo sucessor
                # (menor palavra da subárvore direita)
                sucessor = self.__menorNo(atual.dir)
                atual.palavra = sucessor.palavra
                atual.linhas = sucessor.linhas
                atual.dir = self.__removeNo(atual.dir, sucessor.palavra)

        self.__atualizaAltura(atual)
        return self.__balanceia(atual)


    #percurso em ordem (para depuração e testes)

    def emOrdem(self):
        self.__emOrdem(self.__raiz)
        print()

    def __emOrdem(self, atual):
        if atual is not None:
            self.__emOrdem(atual.esq)
            print(f'{atual.palavra} {sorted(atual.linhas)}', end='  ')
            self.__emOrdem(atual.dir)


    # Geração do índice remissivo em arquivo texto

    def __coletaIndice(self, atual, linhas_saida):
        if atual is None:
            return
        self.__coletaIndice(atual.esq, linhas_saida)
        linhas_ordenadas = ','.join(str(l) for l in sorted(atual.linhas))
        linhas_saida.append(f'{atual.palavra} {linhas_ordenadas}')
        self.__coletaIndice(atual.dir, linhas_saida)

    def imprimeIndice(self, nome_arquivo, tempo_construcao):
        """
        Gera um arquivo .txt com o índice remissivo completo, em
        ordem alfabética, seguido das cinco linhas finais exigidas
        pelo enunciado do projeto.
        """
        linhas_saida = []
        self.__coletaIndice(self.__raiz, linhas_saida)

        descartadas = self.__total_palavras - self.__palavras_distintas

        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            for linha in linhas_saida:
                arquivo.write(linha + '\n')

            arquivo.write('------------------\n') #separador
            arquivo.write(f'Número total de palavras: {self.__total_palavras}\n')
            arquivo.write(f'Número de palavras distintas: {self.__palavras_distintas}\n')
            arquivo.write(f'Número de palavras descartadas (repetidas): {descartadas}\n')
            arquivo.write(f'Tempo de construção do índice usando árvore AVL: {tempo_construcao:.4f}s.\n')
            arquivo.write(f'Total de rotações executadas: {self.__rotacoes}\n')

        return nome_arquivo
