import sqlite3
import pandas as pd
import openpyxl


def new_table(file_name):

    #----------------Добавление таблицы в бд----------------

    con = sqlite3.connect('Httpapp/items.db')
    wb = pd.read_excel(file_name, sheet_name=None)
    for sheet in wb:
        wb[sheet].to_sql(sheet, con, index=False)
    con.commit()
    con.close()


    #----------------Чтение exel файла----------------

    s = str(pd.read_excel(file_name).columns).replace("'", "")
    result = s[s.find('[')+1:s.find(']')]
    result = result.split(', ')
    xl = pd.ExcelFile(file_name).sheet_names[0]
    print(xl)


    #----------------Работа с файлом классов бд----------------

    trash = f'class {xl}(db.Model):\n'
    i = 0
    with open('Httpapp/models.py', 'r') as f:
        old_data = f.read()
    while i < len(result):
        if i == 0:
            trash = trash + '\t' + result[i] + ' = db.Column(primary_key=True)\n'
        else:
            trash = trash + '\t' + result[i] + ' = db.Column()\n'
        i += 1
    with open('Httpapp/models.py', 'w') as f:
        f.write(old_data + trash + '\n')


    #----------------Создание html файла таблицы----------------

    name = 'Httpapp/templates/' + xl + '.html'
    td = ''
    for column in result:
        td = td + f'<td style="text-align: center">{{{{ el.{column} }}}}</td>' + '\n' + '\t\t\t'
        i += 1
    print(td)
    with open(name, 'w') as f:
        f.write(f'{{% extends "base.html" %}}\n\
        \n\
        {{% block body %}}\n\
        \n\
        <table class="table table-striped container">\n\
          <thead>\n\t\
          </thead>\n\t\
          <tbody>\n\t\
          {{% for el in {xl} %}}\n\
            <tr>\n\
                {td}\n\
            </tr>\t\t\n\
          {{% endfor %}}\n\t\
          </tbody>\n\t\
        </table>\n\
        {{% endblock %}}')


    #----------------Создание нового маршрута----------------

    my_file = open('Httpapp/roots.py', 'a+')
    text_for_file = f'\n\n\n@apps.route("/{xl}")\n@login_required\ndef {xl.lower()}():\n\t{xl.lower()} = {xl}.query.all()\n\treturn render_template("{xl}.html", {xl}={xl.lower()})'
    my_file.write(text_for_file)
    my_file.close()

    with open('Httpapp/roots.py', 'r') as f:
        old_data = f.read()
    new_data = old_data.replace('#list_add', f',{xl} #list_add')
    with open('Httpapp/roots.py', 'w') as f:
        f.write(new_data)


    #----------------Добавление нового элемента списка в тэмплейт----------------

    with open('Httpapp/templates/base.html', 'r') as f:
        old_data = f.read()
    new_data = old_data.replace('<!-- 123 -->', '<!-- hi -->\n\t\t\t<!-- 123 -->')
    with open('Httpapp/templates/base.html', 'w') as f:
        f.write(new_data)
