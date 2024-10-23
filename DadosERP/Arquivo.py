import sqlite3

conector = sqlite3.connect('banco.db')
cursor = conector.cursor()

def criaTabela(tipos, arq, pk, notnull):
    
    entrada = open(arq, 'r')
    dado = []

    campo = entrada.readline().rstrip()
    
    campo = campo.split(";")
    
    nome = arq.split(".csv")
    nome = nome[0]

    # criação banco de dados

    try:
        sql = "drop table " + nome
        cursor.execute(sql)
    except sqlite3.OperationalError:
        pass

    sql = "CREATE TABLE " + nome + " ("
    criado = False
    for item in range(len(tipos)):
        
        if item != (len(tipos) - 1):
            if pk == "(NUMPED, NUMITEM)" and criado != True:
                sql += campo[item] + " " + tipos[item] + ","
                sql += campo[item+1] + " " + tipos[item+1] + ","
                criado = True
                for item in range(len(tipos) - 2):
                    if notnull[item + 2] == 1:
                        sql += campo[item + 2] + " " + tipos[item + 2] + " NOT NULL, "
                    else:
                        sql += campo[item + 2] + " " + tipos[item + 2] + ", "
                sql += "PRIMARY KEY " + pk + ")"
            if campo[item] == pk:
                sql += campo[item] + " " + tipos[item] + " PRIMARY KEY,"
            elif criado == True:
                pass
            else:
                if notnull[item] == 1:
                    sql += campo[item] + " " + tipos[item] + " NOT NULL, "
                else:
                    sql += campo[item] + " " + tipos[item] + ", "
        elif criado == False:
            if notnull[item] == 1:
                sql += campo[item] + " " + tipos[item] + " NOT NULL)"
            else:
                sql += campo[item] + " " + tipos[item] + ")"

    cursor.execute(sql)

    #insert

    registro = entrada.readline().rstrip()

    while registro != '':
        registro = registro.split(';')
        dado.append(registro)
        registro = entrada.readline().rstrip()

    entrada.close()

    for dados in dado:
        sql = "INSERT INTO " + nome + " ("
        for item in range(len(tipos)):
            if item != (len(tipos) - 1):
                sql += campo[item] + ", "
            else:
                sql += campo[item] + ")"
        sql += " VALUES ("
        for item in range(len(tipos)):
            if item != (len(tipos) - 1):
                sql += "?, "
            else:
                sql += "?)"

        cursor.execute(sql, dados)

    conector.commit()
    
#=====================MAIN==========================#
#Tipos de dados

tp = ["INTEGER","NUMERIC","STRING"]
forn = [tp[0], tp[0], tp[0],
        tp[2], tp[2], tp[2],
        tp[0], tp[0], tp[0],
        tp[0]]
ped = [tp[0], tp[2], tp[2],
       tp[0], tp[2], tp[0],
       tp[0], tp[1], tp[0],
       tp[1], tp[1], tp[1],
       tp[1], tp[1], tp[1]]
prod = [tp[0], tp[2], tp[0],
        tp[0], tp[0], tp[1],
        tp[1], tp[0], tp[1],
        tp[0], tp[2], tp[1],
        tp[1]]
pedItem = [tp[0], tp[0], tp[0],
           tp[1], tp[1], tp[2],
           tp[0], tp[1], tp[0],
           tp[0], tp[1]]
repres = [tp[0], tp[2], tp[2],
          tp[1]]

#Chaves Primárias
pkForn = "CODCLIFOR"
pkPed = "NUMPED"
pkProd = "CODPROD"
pkPedItem = "(NUMPED, NUMITEM)"
pkRepres = "CODREPRES"

#NOT NULL
nForn = [1, 1, 0, 1, 0, 0, 0, 1, 1, 0]
nPed = [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
nProd = [1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0]
nPedItem = [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1]
nRepres = [1, 1, 1, 1]

# criando as tabelas

criaTabela(forn, "FornClien.csv", pkForn, nForn)
criaTabela(ped, "Pedidos.csv", pkPed, nPed)
criaTabela(prod, "Produtos.csv", pkProd, nProd)
criaTabela(pedItem, "PedidosItem.csv", pkPedItem, nPedItem)
criaTabela(repres, "Repres.csv", pkRepres, nRepres)

cursor.close()
conector.close()
