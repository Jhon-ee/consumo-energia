import numpy as np
# Consumo mensal de energia
# Feito por Jonas Santana

class Circuito():
    def __init__(self,nome = '',p = 0.0,h = 0.0,d = 0,c = 0.0,consumo = 0.0,preco = 0.0):
        self.nome = nome
        self.p = p
        self.h = h
        self.d = d
        self.c = c
        self.consumo = consumo
        self.preco = preco

def leitura():
    circuito = Circuito()
    circuito.nome = []
    circuito.p = []
    circuito.h = []
    circuito.d = []
    circuito.c = []
    circuito.consumo = []
    circuito.preco = []

    q = int(input('INFORME A QUANTIDADE DE APARELHOS ELÉTRICOS: '))
    val = float(input('DIGITE O VALOR DO kWh: '))
    for i in range(0,q):
        circuito.nome.append(input('INFORME O NOME DO APARELHO: '))
        circuito.p.append(float(input('INFORME A POTÊNCIA DO APARELHO: ')))
        circuito.h.append(float(input('INFORME A QUANT. DE HORAS/DIA DO APARELHO LIGADO: ')))
        circuito.d.append(float(input('INFORME A QUANT. DE DIAS DO APARELHO LIGADO: ')))
        print('\n')
        circuito.c.append([(x*y*z)/1000 for x,y,z in zip(circuito.p,circuito.h,circuito.d)])
        circuito.consumo.append(circuito.c[i][i])
        circuito.preco.append(val * np.array(circuito.consumo[i]))
    return (q,circuito)

def escrita(t,dados):
    
    print("{}\t\t\t{}\t\t\t{}".format('APARELHO','kWh','R$\n'))
    for i in range(0,t):
        print("{}\t\t\t{}\t\t\t{}".format(dados.nome[i],dados.consumo[i],round(dados.preco[i],2)))
    print('\nCONSUMO TOTAL(kWh): ',round(sum(dados.consumo),2))
    print('PREÇO TOTAL(R$): ',round(sum(dados.preco),2))

t,dados = leitura()
escrita(t,dados)


