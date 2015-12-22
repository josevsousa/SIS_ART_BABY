@auth.requires_membership('admin')
def cadastrarRepresentantes():
	menu = 'representantes'
	return dict(formCadastro=crud.create(db.representantes))

# @auth.requires_login()
def listarRepresentantes():
	representantes = db(db.representantes.id>0).select()
	#return dict(livros=livros)

	#virtaul fields
	class Virtual(object):
		def botoes(self):
			#admin
			if auth.has_membership('admin'):   #URL('representantes','deletar',args=[self.representantes.id])
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('representantes','select',args=[self.representantes.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href=URL('representantes','update',args=[self.representantes.id]),_class='btn btn-default Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_href='#',_class='btn btn-default fechar Jview btn-xs')),_class='btn-group JpositionA')
			#user qualquer
			else:
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('representantes','select',args=[self.representantes.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href='#',_class='btn btn-default Jview btn-xs',_disabled='disabled')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_href='#',_class='btn btn-default Jview btn-xs',_disabled='disabled')),_class='btn-group JpositionA')
			return bts

	representantes.setvirtualfields(campos_virtual = Virtual())		

	return dict(formListar=representantes)

# ============== select insert update ==============
# def selectCrud():
# 	todos = crud.select(db.produtos, db.produtos.id == request.args(0),['codigo_produto','nome_produto','preco_produto_lojinha','dataGravado'])
# 	return dict(form=todos)

#select
def select():
	table = db(db.representantes.id==request.args[0]).select()
	return dict(table=table)
#insert
@auth.requires_membership('admin')
def inserir():
	return dict()
	#return dict(form=crud.create(db.produtos))
#update
@auth.requires_membership('admin')
def update():
	return dict(form=crud.update(db.representantes,request.args(0)))
#delete
def deletar():
	print request.vars.cod
	db(db.representantes.codigo_produto == request.vars.cod).delete()
	return ''


# ===================================================
