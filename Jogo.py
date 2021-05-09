# -*- coding: utf-8 -*-

#Programa   : Jogo.py
#Finalidade : Desafio BrasilPrev
#Data       : 7 de maio de 2021
#Autor      : OmaR
#Obs.       : 


import sys
from pdb import set_trace
import random
from enum import Enum
from time import sleep 
import pandas as pd

#def ##print(*kwargs):
#    return True

#printTab = lambda x : [#print(i, 'Sem Proprietario' if i['Proprietario'] is None else 'Jogador ' + str(i['Proprietario'].Nome) + ' é o dono.' ) for i in x.Casas ]
JogarDado = lambda : random.randrange(1, 7)

#Constantes 
class Const():
    @classmethod
    def SaldoInicial(self):
        return 300.0      

    @classmethod
    def LimiteRodadas(self):
        return 1000

    @classmethod
    def LimiteSimulacoes(self):
        return 300
#FimClass

class Personalidades():
    @classmethod
    def Impulsivo(self, Jogador, Casa):
        return True

    @classmethod
    def Exigente(self, Jogador, Casa):
        if Casa['ValorAluguel'] > 50:
            return True
        return False

    @classmethod
    def Cauteloso(self, Jogador, Casa):
        if Jogador.Saldo - Casa['CustoVenda'] >= 80:            
            return True
        return False

    @classmethod
    def Aleatorio(self, Jogador, Casa):
        if random.randrange(0, 100) >= 50:
            return True
        return False
#FimClass


class Perfis(Enum): 
    Impulsivo = 0 
    Exigente  = 1  
    Cauteloso = 2 
    Aleatorio = 3 


#Constantes pré-definidas
class Tabuleiro():

    def __init__(self, casas=20):
        self.QtdeCasas = casas
        self.Casas = self.Propriedades()
    #FimMethod


    def Propriedades(self):
        lstPropriedades = []
        for i in range(self.QtdeCasas+1):
            Venda = random.randrange(10, 100)
            #print('faixa de randomicos para aluguel = entre 1% e 10% do valor de venda')
            #print(Venda, int(Venda * 0.01), int(Venda * 0.1 ))
            Aluguel = random.randrange(int(Venda * 0.1), int(Venda * 0.2 ) )

            dct = {
                'Index'        : i, 
                'CustoVenda'   : Venda,
                'ValorAluguel' : Aluguel,
                'Proprietario' : None,
            }
            lstPropriedades.append(dct)
        return lstPropriedades
    #FimMethod
    
#FimClasse

class Jogador():
    def __init__(self, Nome, ePerfil, Saldo=Const.SaldoInicial()):
        self.Nome = Nome
        self.Saldo = Saldo
        self.Perfil = ePerfil
        self.PosTab = 0
#FimClasse

class Jogo():

    def __init__(self, Tabuleiro, *tplJogadores):
        self.Tabuleiro = Tabuleiro
        self.Jogadores = [i for i in tplJogadores]
        self.Vencedor = None
        self.TimeOut = False
        self.Stats = {}##print(self.Jogadores)

    #FimDef    

    def switch_Perfil(self, argument, Jogador, Casa):
        switcher = {
            Perfis.Impulsivo : Personalidades.Impulsivo,
            Perfis.Exigente  : Personalidades.Exigente,
            Perfis.Cauteloso : Personalidades.Cauteloso,
            Perfis.Aleatorio : Personalidades.Aleatorio,
        }
        
        func = switcher.get(argument, lambda:'Personalidade Inexistente!')

        return func(Jogador, Casa)
    #FimDef

    def Jogar(self):
        lstExcluidos = []
        for k in range(Const.LimiteRodadas()):

            for i in self.Jogadores:

                if i in lstExcluidos:
                    continue

                pontos = JogarDado()

                #print('Jogador {} jogou dado e tirou {} pontos.'.format(i.Nome, pontos))

                i.PosTab += pontos

                if i.PosTab > self.Tabuleiro.QtdeCasas:
                    #Concluída volta no Tabuleiro, jogador ganha 100 de saldo
                    i.PosTab -= self.Tabuleiro.QtdeCasas
                    i.Saldo += 100

                try:
                    ret = self.switch_Perfil(i.Perfil, i, self.Tabuleiro.Casas[i.PosTab])
                except Exception as e:
                    #print('Erro posicionamento de casas. Falha na lógica', e) 
                    sys.exit(-1)
                    set_trace()
                    

                #Verdadeiro então compra a propriedade
                if ret and self.Tabuleiro.Casas[i.PosTab]['Proprietario'] == None : 
                    Valor = self.Tabuleiro.Casas[i.PosTab]['CustoVenda'] 
                    self.Tabuleiro.Casas[i.PosTab]['Proprietario'] = i
                    i.Saldo -= Valor
                    #print('Jogador {} comprou a casa {} esta com o saldo de {}'.format(i.Nome, self.Tabuleiro.Casas[i.PosTab]['Index'], i.Saldo))

                else: #Falso então Paga o aluguel se houver proprietário
                    Valor = self.Tabuleiro.Casas[i.PosTab]['ValorAluguel'] 
                    if not self.Tabuleiro.Casas[i.PosTab]['Proprietario'] == None and self.Tabuleiro.Casas[i.PosTab]['Proprietario'] != i :
                        i.Saldo -= Valor
                        #print('Jogador {} pagou aluguel de {} na casa {} esta com o saldo de {}'.format(i.Nome, Valor, self.Tabuleiro.Casas[i.PosTab]['Index'], i.Saldo))
                    else:
                        #print('Jogador {} está na  casa {} e tem saldo de {}'.format(i.Nome, self.Tabuleiro.Casas[i.PosTab]['Index'], i.Saldo))
                        pass
                #EndIf

                if i.Saldo < 0: #Jogador fora da partida
                    lstExcluidos.append(i)
                    for y in self.Tabuleiro.Casas:
                        if y['Proprietario'] == i:
                            y['Proprietario'] = None
                        #EndIf
                    #EndFor

                    if len(set(self.Jogadores).difference(set(lstExcluidos))) == 1:
                        #print('')       
                        cj = set(self.Jogadores).difference(set(lstExcluidos))
                        self.Vencedor = cj.pop()
                        #print("Jogador {} venceu com o saldo de {}".format(self.Vencedor.Nome, self.Vencedor.Saldo))
                        #print("FIM DE JOGO !!!")  
                        break              
                    #EndIf
                #EndIf                                          
                
                #print('')                
                #sleep(.001)
            #FimFor
            if self.Vencedor is not None:
                break            
        #FimFor

        if self.Vencedor is  None:
            self.TimeOut = True
            #print('Jogo finalizado por TIME OUT')
            cj = set(self.Jogadores).difference(set(lstExcluidos))
            lst = [i for i in cj]
            iAux = 0            
            for i in lst:
                if i.Saldo > iAux:
                    iAux = i.Saldo
                    self.Vencedor = i                    
            #FimFor
            #print("Jogador {} venceu com o saldo de {}".format(self.Vencedor.Nome, self.Vencedor.Saldo))
        #FimIf            
            
        #print("*" * 100)
        
        #for i in self.Jogadores:                    
            #print("Saldo {} Jogador {} esta na casa {}".format(i.Saldo, i.Nome, i.PosTab))

        #printTab(self.Tabuleiro)
        dctStat = {
                'TimeOut'      : 'Sim' if self.TimeOut else 'Não',
                'Turnos'       : k,
                'PerfilVencedor': self.Vencedor.Perfil }
        self.Stats = dctStat
    #FimDef
         
#FimClasse

if __name__ == '__main__':
    lstStats = []
    for i in range(Const.LimiteSimulacoes()):
        tab = Tabuleiro()
        
        obj = Jogo( tab, Jogador(1, Perfis.Impulsivo)
                        ,Jogador(2, Perfis.Exigente)
                        ,Jogador(3, Perfis.Cauteloso)
                        ,Jogador(4, Perfis.Aleatorio) )
        
        obj.Jogar()

        lstStats.append(obj.Stats)
    #FimFor
    df = pd.DataFrame(lstStats)

    print('Estatisticas do jogo!')

    TimeOut = df[df['TimeOut'] == 'Sim'].shape[0]
    print('Quantidade de partidas encerradas por TimeOUt : ', TimeOut)

    MediaTurnos = df['Turnos'].mean()
    print('Média de turnos por partida : ', MediaTurnos)

    perc1 = 0
    perc2 = 0
    perc3 = 0 
    perc4 = 0
    for i in lstStats:

        if i['PerfilVencedor'] == Perfis.Impulsivo:
            perc1 += 1

        elif i['PerfilVencedor'] == Perfis.Exigente:
            perc2 += 1

        elif i['PerfilVencedor'] == Perfis.Cauteloso:
            perc3 += 1

        elif i['PerfilVencedor'] == Perfis.Aleatorio:
            perc4 += 1

    print('Percentual vitorias perfil Impulsivo :', perc1 / len(lstStats) * 100 )
    print('Percentual vitorias perfil Exigente  :', perc2 / len(lstStats) * 100 )
    print('Percentual vitorias perfil Cauteloso :', perc3 / len(lstStats) * 100 )
    print('Percentual vitorias perfil Aleatorio :', perc4 / len(lstStats) * 100 )

    MaxPerc = max(perc1, max(perc2, max(perc3, perc4)))

    if perc1 == MaxPerc:
        print('Perfil Impulsivo venceu mais.')

    elif perc2 == MaxPerc:
        print('Perfil Exigente venceu mais.')

    elif perc3 == MaxPerc:
        print('Perfil Cauteloso venceu mais.')

    elif perc4 == MaxPerc:
        print('Perfil Aleatorio venceu mais.')

    sys.exit(-1)


