# -*- conding: utf-8 -*-
@auth.requires(auth.has_membership('operacional_A') or auth.has_membership('admin'))
def abertos():
	from datetime import datetime
	pedidos = db(db.historicoVendas.id>0 and db.historicoVendas.status_venda!='Finalizada').select()
	return dict(pedidos=pedidos)

def diasCorridos(i):
	return '00.00.00-%s'%i	

def iten():
	cod = request.vars.cod
	data = request.vars.dataSolicitacao
	grid = db(Itens.codigoVenda == cod).select()
	head = H3("COD: [ %s ]  aberto em %s"%(cod, data))


	#pegar lista do historicoVendas.itensVendaPendente e jogar na tela 
	return dict(head=head,grid=grid,cod=cod)

def update_ItenStatus():
	from datetime import datetime
	index = request.vars.transitory
	index = index.split(';')
	db(Itens.id == index[0]).update(status=index[1],data_check_iten=datetime.now())
	#----- checar se todos estao desmarcados --

	total_item = len(db(Itens.codigoVenda == index[2]).select())#quantidade de itens pra separar
	itens_marcados = 0  # quantidade de intes ja separados
	#percorre todos os itens vendo se ja estao todos separados ou não
	for iten in db(Itens.codigoVenda == index[2]).select():
	    if iten.status == True:
	        itens_marcados += 1 #achando um item marcado como separado ele soma esse iten a var itens_marcados
	if itens_marcados == total_item:
	    db(db.historicoVendas.codigoVenda == index[2]).update(status_venda='OK') #se tiver tudo marcado
	elif itens_marcados < 1:
		db(db.historicoVendas.codigoVenda == index[2]).update(status_venda='Pendente') #se tiver nao tiver nenhum marcado
	else:            	
		db(db.historicoVendas.codigoVenda == index[2]).update(status_venda='Separando...') #se tiver so alguns marcados

def update_ItenObs():
    index = request.vars.transitory
    index = index.split(';')
    db(Itens.id == index[0]).update(obs=index[1])



# def updateGrid():
# 	index = request.vars.transitory
# 	index = index.split('&')
# 	cod = index[0]
# 	gridNew = index[1]
# 	# print gridNew	
# 	db(db.historicoVendas.codigoVenda == cod).update(itensVendaPendente=gridNew)
# 	db(db.pendentes.codigo == cod).update(status='Separando')


# def updateFinal():
# 	from datetime import datetime
# 	cod = request.vars.transitory
# 	db(db.pendentes.codigo == cod).update(status='OK',dataSeparado=datetime.now())


# def updateZero():
# 	cod = request.vars.transitory
# 	db(db.pendentes.codigo == cod).update(status='Pendente')


# def updateObs():
# 	cod = request.vars.transitory
# 	db(db.pendentes.codigo == cod).update(status='Separando')
# 	db.commit()