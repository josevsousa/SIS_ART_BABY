# -*- coding: utf-8 -*-

# @auth.requires_login()
def cadastrarFuncionarios():
  	return dict(formCadastro=crud.create(db.funcionarios))

# @auth.requires_login()
def listarFuncionarios():
	funcionarios = db(db.funcionarios.id>0).select()
	#return dict(livros=livros)

	#virtaul fields
	class Virtual(object):
		def botoes(self):
			#admin
			if auth.has_membership('admin'):   #URL('Funcionarios','deletar',args=[self.Funcionarios.id])
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('funcionarios','select',args=[self.funcionarios.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href=URL('funcionarios','update',args=[self.funcionarios.id]),_class='btn btn-default Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_id=self.funcionarios.id,_href='#',_class='btn btn-default fechar Jview btn-xs')),_class='btn-group JpositionA')
			#user qualquer
			else:
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('funcionarios','select',args=[self.funcionarios.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href=URL('funcionarios','update',args=[self.funcionarios.id]),_class='btn btn-default Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_href='#',_class='btn btn-default Jview btn-xs',_disabled='disabled')),_class='btn-group JpositionA')
			return bts

	funcionarios.setvirtualfields(campos_virtual = Virtual())		
	
	return dict(formListar=funcionarios,d=funcionarios)



# ===================================================
#select
def select():
	table = db(db.funcionarios.id==request.args[0]).select()
	return dict(table=table)
#insert
def inserir():
	return dict(form=crud.create(db.funcionarios))
#update
def update():
	return dict(formUpdate=crud.update(db.funcionarios,request.args(0),_class="formEditar"))
#delete
@auth.requires_membership('admin')
def deletar():
	db(db.funcionarios.id == request.vars.cod).delete()
	return ''



