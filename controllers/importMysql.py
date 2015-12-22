def produtos(): 
    path = request.folder+"static/mysqlImport/produtos.csv"
    f = file(path,'r')

    # linha = f.readline().split(',')
    
    for l in f.readlines():
    	linha = l.split(',')
        db.produtos.insert(codigo_produto=linha[1],nome_produto=linha[2],preco_produto_lojinha=linha[3],dataGravado=linha[4])
        # print (codigo_produto=linha[1],nome_produto=linha[2],preco_produto_lojinha=linha[5],dataGravado=linha[4])
    
    f.close()

    return dict()

def clientes(): 
    path = request.folder+"static/mysqlImport/clientes.csv"
    f = file(path,'r')

    # linha = f.readline().split(',')

    for l in f.readlines():
        linha = l.split(',')
        db.clientes.insert(nome=linha[1],celular=linha[10],operadora='*',fixo=linha[9],email=linha[11],cnpj=linha[2],insc=linha[3],cep=linha[4],endereco=linha[5],numero=linha[6],cidade=linha[8],uf=linha[7],bairro=linha[13],apelido='')
        
	# db.clientes.insert(nome="josede",celular="ddddddd",operadora="kkdkk",email="jose@jsodev",dataGravado="2014-10-01 02:20:10")
    return dict()

    