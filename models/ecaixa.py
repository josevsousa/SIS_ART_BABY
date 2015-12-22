#-*- coding: UTF-8 -*-

db.define_table('category',Field('name'))
db.define_table('product',Field('name'),Field('category'))
db.product.category.widget = SQLFORM.widgets.autocomplete(
     request, db.category.name, limitby=(0,10), min_length=2)