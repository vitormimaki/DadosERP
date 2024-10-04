import sqlite3

conector = sqlite3.connect('banco.db')
cursor = conector.cursor()

def criaTabela(tipos, arq):
    
    entrada = open(arq, 'r')
    dado = []

    campo = entrada.readline().rstrip()

    campo = campo.split('ï»¿')
    campo = campo[1]
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
    for item in range(len(tipos)):
        if item != (len(tipos) - 1):
            sql += campo[item] + " " + tipos[item] + ", "
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

tp = ["INTEGER","FLOAT","STRING"]
forn = [tp[0], tp[0], tp[0],
        tp[2], tp[2], tp[2],
        tp[0], tp[0], tp[0],
        tp[0]]
ped = [tp[1], tp[2], tp[2],
       tp[1], tp[2], tp[0],
       tp[0], tp[1], tp[0],
       tp[1], tp[1], tp[1],
       tp[1], tp[1], tp[1]]
prod = [tp[0], tp[2], tp[0],
        tp[0], tp[1], tp[1],
        tp[1], tp[1], tp[1],
        tp[0], tp[2], tp[1],
        tp[1]]
pedItem = [tp[1], tp[0], tp[0],
           tp[1], tp[1], tp[2],
           tp[1], tp[1], tp[0],
           tp[0], tp[1]]
repres = [tp[0], tp[2], tp[2],
          tp[1]]



# criando as tabelas

criaTabela(forn, "FornClien.csv")
criaTabela(ped, "Pedidos.csv")
criaTabela(prod, "Produtos.csv")
criaTabela(pedItem, "PedidosItem.csv")
criaTabela(repres, "Repres.csv")

cursor.close()
conector.close()
