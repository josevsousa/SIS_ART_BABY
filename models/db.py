# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager, Crud, Mail, Storage

mail = Mail()
auth = Auth(db)
service = Service()
plugins = PluginManager()
crud = Crud(db)


## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email: 'logging' or
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'mail.seusite.com.br:587'
mail.settings.sender = 'user'
mail.settings.login = 'senha'



## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True


## configura a data
# from datetime import datetime
# codigoVenda =  str(datetime.now()).replace('-','').replace(':','').replace('.','').replace(' ','')
# datetime.now().day
# datetime.now().hour
# datetime.now().minute
# datetime.now().second

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

#tabela produtos
db.define_table('produtos',
    Field('codigo_produto',label="Código"), #unique = nao repetir
    Field('nome_produto', requires = IS_NOT_EMPTY(error_message="Nome obrigatório"), label="Nome" ),
    Field('preco_produto_lojinha','double', label="R$"),
    Field('dataGravado','datetime', default=request.now, label="Data", writable=False),
    Field('foto_produto','upload', label="Foto"),
    migrate ='produtos.table'   
    )
db.produtos.codigo_produto.requires = IS_NOT_EMPTY(error_message="Codigo obrigatório")
db.produtos.codigo_produto.requires = IS_NOT_IN_DB(db, db.produtos.codigo_produto, error_message = 'Codigo inválido!')

# db.define_table('autoCompletProdutos',
#         Field('nome_produto'),
#         Field('codigo_produto'),
#         migrate = 'autoCompletProdutos.table'
#     )
# db.autoCompletProdutos.nome_produto.widget = SQLFORM.widgets.autocomplete(request, db.produtos.nome_produto, limitby=(0,5), min_length=2)

OPERADORA = (' - ','TIM','OI','VIVO','CLARO','FIXO','NENHUMA')
UF = ( " - ","AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RO", "RS", "RR", "SC", "SE", "SP", "TO" )

Clientes = db.define_table('clientes',
    Field('nome',label='Nome'), 
    Field('celular', label='Cel..'),
    Field('operadora', default=' - '),
    Field('fixo', label='Tel:..'),
    Field('email',label='E-mail'),
    Field('cnpj', label='CNPJ'),
    Field('insc', label='INSC'),
    Field('cep', label='CEP'),
    Field('endereco', label='Endereço'),
    Field('numero' ,label='Número'),
    Field('cidade', label='Cidade'),
    Field('uf', label='UF', default=' - '),
    Field('bairro', label='Bairro'),
    Field('apelido', label='Apelido'),
    Field('dataGravado','datetime', default=request.now, label="Data"),
    Field('foto_cliente','upload', label='Foto'),
    migrate = "clientes.table"
    )
db.clientes.nome.requires = IS_NOT_IN_DB(db, db.clientes.nome, error_message = 'Usuario invalido')
db.clientes.uf.requires = IS_IN_SET(UF, error_message="UF invalido!!!")
db.clientes.operadora.requires = IS_IN_SET(OPERADORA, error_message="Operadora invalida!!!")

Funcionarios = db.define_table('funcionarios',
    Field('matricula', label='Matrícula'),
    Field('nome',label='Nome'), 
    Field('celular', label='Celulares'),
    # Field('Cel',"list:string"),
    Field('operadora', default=' - '),
    Field('fixo', label='Tel:..'),
    Field('email',label='E-mail'),
    Field('cpf', label='CPF'),
    Field('cep', label='CEP'),
    Field('endereco', label='Endereço'),
    Field('numero' ,label='Número'),
    Field('cidade', label='Cidade'),
    Field('uf', label='UF', default=' - '),
    Field('bairro', label='Bairro'),
    Field('dataGravado','datetime', default=request.now, label="Data"),
    Field('foto_funcionario','upload', label='Foto'),
    migrate = "funcionarios.table"
    )
db.funcionarios.nome.requires = IS_NOT_IN_DB(db, db.funcionarios.nome, error_message = 'Usuario invalido')
db.funcionarios.uf.requires = IS_IN_SET(UF, error_message="UF invalido!!!")
db.funcionarios.operadora.requires = IS_IN_SET(OPERADORA, error_message="Operadora invalida!!!")

Historico = db.define_table('historicoVendas',
    Field('codigoVenda', label='Código'),
    Field('representante'),
    Field('clienteEmail', label='Cliente'),
    Field('tipoVenda', label='Tipo de venda'),
    Field('valorVenda','double', label='Total'),
    Field('valorDesconto','double', label='Desconto'),
    Field('vendedor'),
    Field('dataVenda','datetime', default=request.now),
    Field('deletado','boolean', default=False),
    Field('separado','boolean', default=False),
    Field('status_venda',default='Pendente'),
    migrate = "historioVendas.table"
    ) 

Representantes = db.define_table('representantes',
    Field('nome',label='Nome'), 
    Field('celular', label='Celula 1'),
    Field('operadora', label='Operadora 1', default=' - '),
    Field('celular_2', label='Celula 2'),
    Field('operadora_2', label='Operadora 2', default=' - '),
    Field('fixo', label='Tel:..'),
    Field('email',label='E-mail'),
    Field('cnpj', label='CNPJ'),
    Field('insc', label='INSC'),
    Field('cep', label='CEP'),
    Field('endereco', label='Endereço'),
    Field('numero' ,label='Número'),
    Field('cidade', label='Cidade'),
    Field('uf', label='UF', default=' - '),
    Field('bairro', label='Bairro'),
    Field('apelido', label='Apelido'),
    Field('dataGravado','datetime', default=request.now, label="Data"),
    Field('foto_representante','upload', label='Foto'),
    migrate = "representante.table"
    )
db.representantes.uf.requires = IS_IN_SET(UF, error_message="UF invalido!!!")
db.representantes.nome.requires = IS_NOT_EMPTY(error_message="Nome obrigatório")
db.representantes.email.requires = IS_NOT_EMPTY(error_message="E-mail obrigatório")
db.representantes.celular.requires = IS_NOT_EMPTY(error_message="Celular obrigatório")
db.representantes.operadora.requires = IS_IN_SET(OPERADORA, error_message="Operadora invalida!!!")
db.representantes.operadora_2.requires = IS_IN_SET(OPERADORA, error_message="Operadora invalida!!!")

Pendentes = db.define_table('pendentes',
    Field('codigo'),
    Field('cliente'),
    Field('representante'),
    Field('dataSolicitacao', 'datetime', default=request.now),
    Field('status', default='Pendente'),
    Field('dataSeparado','datetime')
    )
# Pendentes.status.requires = IS_IN_SET(STATUS, error_message="Status invalido!!!")

Parcelados = db.define_table('parcelados',
    Field('codigo'),
    Field('tipoVenda'),
    Field('cliente'),
    Field('representante'),
    Field('parcela', label='Parcela'),
    Field('dataVencimento', 'datetime', label='Vencimento'),
    Field('valor', label='Valor'),
    Field('statusPagamento', 'boolean', default=False),
    Field('dataPagamento', 'datetime')
    )

Itens = db.define_table('itens',
    Field('codigoVenda', readable=False),
    Field('codigoIten',label="Código"),
    Field('quantidade',label="Qtde"),
    Field('produto',label="Produto"),
    Field('valorUnidade',label="Valor Unid"),
    Field('valorTotal',label="Valor Total"),
    Field('dataRegistro', 'datetime', default=request.now, readable=False),
    Field('status', 'boolean', default=False),
    Field('data_check_iten'),
    Field('obs', default=" ")
    )

# autocomplit
Caixa_Cliente = db.define_table('caixa_cliente',
    Field('nome'),
    Field('representante')
    )
# Caixa_Cliente.representante.requires = IS_IN_DB(db, Representante.nome, error_message = 'Usuário invalido') 
# Caixa_Cliente.nome.widget = SQLFORM.widgets.autocomplete(
#      request, db.clientes.nome, limitby=(0,10), min_length=2)



