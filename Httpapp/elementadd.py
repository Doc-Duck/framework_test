import codecs
def new_element(type, value, action):
    if type == 'button':
        file = open(f'Httpapp/templates/viewer.html', 'r')
        old_data = file.read()
        new_data = old_data.replace('<!--- add link --->', f'<a href="{action}" class="btn btn-success">{ value }</a>\n<!--- add link --->')
        with open(f'Httpapp/templates/viewer.html', 'w') as f:
            f.write(new_data)


def new_chart(file_name, name, column_x, column_y):
    f = codecs.open(f"Httpapp/templates/{file_name}.html", 'r+', "ISO-8859-1")
    old_data = f.read()
    if name == 'line':
        chart_string = f"<script>var labels = [{{% for el in {file_name} %}}'{{{{ el.{column_x} }}}}',{{% endfor %}}];var data = {{labels: labels, datasets: [{{label: 'My First dataset', backgroundColor: 'rgba({{{{range(1, 255)|random}}}},{{{{range(1, 255)|random}}}},{{{{range(1, 255)|random}}}}, 0.7)', borderColor: 'rgb(255, 99, 132)', data: [{{% for el in {file_name} %}}'{{{{ el.{column_y} }}}}',{{% endfor %}}],}}]}};var config = {{type: 'line', data: data, options: {{}}}};</script><script>var myChart = new Chart(document.getElementById('{name}'), config);</script>"
        div_string = f'<canvas style="width:50%; max-width:700px" id="{name}"></canvas>'+'\n<!--- add div --->'

    if name == 'pie':
        chart_string = f"<script>var data = {{labels: [{{% for el in {file_name} %}}'{{{{ el.{column_x} }}}}',{{% endfor %}}], datasets: [{{label: 'My First Dataset', data: [{{% for el in {file_name} %}}'{{{{ el.{column_y} }}}}',{{% endfor %}}],backgroundColor: [{{% for el in {file_name} %}}'rgba({{{{range(1, 255)|random}}}},{{{{range(1, 255)|random}}}},{{{{range(1, 255)|random}}}}, 0.7)',{{% endfor %}}], hoverOffset: 4}}]}};var config = {{type: 'pie', data: data,}};</script><script>var myChart = new Chart(document.getElementById('{name}'), config);</script>"
        div_string = f'<canvas style="width:50%; max-width:700px" id="{name}"></canvas>' + '\n<!--- add div --->'

    new_data = old_data.replace('<!--- add chart --->', chart_string + '\n<!--- add chart --->')
    new_data = new_data.replace('<!--- add div --->', div_string)
    with codecs.open(f'Httpapp/templates/{file_name}.html', 'w', "ISO-8859-1") as f:
        f.write(new_data)
