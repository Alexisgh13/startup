import csv
import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response
import pymysql as MySQLdb

HOST = "lhcp1124.webapps.net"
PORT = 3306
USER = "y72kz6jm_Client"
PASSWORD = "qnrgdPO9*GKL"
DB = "y72kz6jm_wcjdb"

app = Flask(__name__)
connect = MySQLdb.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)


from forms import AddCategory, AddInterests


@app.route('/')
def homepage():
    return render_template('home.html')


# ------- CONTENT
@app.route('/content/new_category', methods=['POST', 'GET'])
def newCategory():
    formCategory = AddCategory(request.form)

    cn = connect.cursor()
    cn.execute("SELECT * from categorie")
    categories = cn.fetchall()

    if request.method == 'POST' and formCategory.validate():
        category = request.form.get('category')

        newCategory = connect.cursor()
        newCategory.execute("INSERT INTO `categorie` (`idCat`) VALUES ('" + category + "')")
        connect.commit()
        newCategory.close()

        return redirect(url_for('newCategory'))

    if request.method == 'GET' and request.args.get('id'):
        category = request.args.get('id')

        deleteCategory = connect.cursor()
        deleteCategory.execute("DELETE FROM `categorie` WHERE idCat='" + category + "'")
        connect.commit()
        deleteCategory.close()

        return redirect(url_for('newCategory'))

    return render_template('content_category.html', categories=categories, formCategory=formCategory)


@app.route('/content/new_interest', methods=['POST', 'GET'])
def newInterest():
    formInterests = AddInterests(request.form)

    cn = connect.cursor()
    cn.execute("SELECT * from centreinterets ORDER BY centreInt ASC")
    centreinterets = cn.fetchall()

    if request.method == 'POST' and formInterests.validate():
        label = request.form.get('category')
        idCat = request.form.get('idCat')

        newInterest = connect.cursor()
        newInterest.execute("INSERT INTO `centreinterets` (`centreInt`, `idCat`) VALUES ('" + label + "', '" + idCat + "')")
        connect.commit()
        newInterest.close()

        return redirect(url_for('newInterest'))

    if request.method == 'GET' and request.args.get('label') and request.args.get('category'):
        label = request.args.get('label')
        category = request.args.get('category')

        deleteInterest = connect.cursor()
        deleteInterest.execute("DELETE FROM `centreinterets` WHERE centreInt='" + label + "' AND idCat='" + category + "'")
        connect.commit()
        deleteInterest.close()
        print("DELETE FROM `centreinterets` WHERE centreInt='" + label + "' AND idCat='" + category + "'")
        return redirect(url_for('newInterest'))

    return render_template('content_interest.html', centreInterest=centreinterets, formInterests=formInterests)


@app.route('/content/avatar')
def newAvatar():
    pass


@app.route('/download/<string:csvName>', methods=['GET'])
def dlCsv(csvName):
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    if request.method == 'GET' and csvName == 'categories':
        cn = connect.cursor()
        cn.execute("SELECT * from categorie")
        categories = cn.fetchall()
        csvName = csvName + str(date) + '.csv'
        with open("generations/" + csvName, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(['idCats'])
            for data in categories:
                filewriter.writerow([data[0]])

        excelDownload = open("generations/" + csvName, 'rb').read()
        return Response(
            excelDownload,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-disposition":
                         "attachment; filename=generations/" + csvName})


# ------- UTILISATEURS
@app.route('/users/')
def users():
    pass


# ------- LOGS
@app.route('/logs/')
def logs():
    pass


if __name__ == '__main__':
    app.run()
