from wtforms import Form
from wtforms.fields import StringField, SelectField
from app import connect


class AddCategory(Form):
	category = StringField(render_kw={"placeholder": "Nom de la catégorie"})


class AddInterests(Form):

	cn = connect.cursor()
	cn.execute("SELECT * from categorie")
	interests = cn.fetchall()

	category = StringField(render_kw={"placeholder": "Nom du centre intéret"})
	idCat = SelectField('Select Month', choices=[(x[0], x[0]) for x in interests])
