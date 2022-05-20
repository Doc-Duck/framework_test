
def new_element(type, value, action):
    if type == 'button':
        file = open(f'Httpapp/templates/viewer.html', 'r')
        old_data = file.read()
        new_data = old_data.replace('<!--- add link --->', f'<a href="{action}" class="btn btn-success">{ value }</a>\n<!--- add link --->')
        with open(f'Httpapp/templates/viewer.html', 'w') as f:
            f.write(new_data)


def new_chart(file_name, name, column_x, column_y):
    with open(f"Httpapp/templates/{file_name}.html", 'r') as f:
        old_data = f.read()
    if name == 'line':
        chart_string = f"<script>const labels = [{{% for el in items %}}'{{{{ el.{column_x} }}}}',{{% endfor %}}];const data = {{labels: labels, datasets: [{{label: 'My First dataset', backgroundColor: 'rgb(255, 99, 132)', borderColor: 'rgb(255, 99, 132)', data: [{{% for el in items %}}'{{{{ el.{column_y} }}}}',{{% endfor %}}],}}]}};const config = {{type: 'line', data: data, options: {{}}}};</script><script>const myChart = new Chart(document.getElementById('{name}'), config);</script>"
        div_string = f'<div><canvas id="{name}"></canvas></div>'+'\n<!--- add div --->'

    if name == 'pie':
        chart_string = f"<script>const data = {{labels: [{{% for el in items %}}'{{{{ el.{column_x} }}}}',{{% endfor %}}], datasets: [{{label: 'My First Dataset', data: [{{% for el in items %}}'{{{{ el.{column_y} }}}}',{{% endfor %}}],backgroundColor: [{{% for el in items %}}'rgb({{{{range(1, 255)|random}}}},{{{{range(1, 255)|random}}}},{{{{range(1, 255)|random}}}})',{{% endfor %}}], hoverOffset: 4}}]}};const config = {{type: 'pie', data: data,}};</script><script>const myChart = new Chart(document.getElementById('{name}'), config);</script>"
        div_string = f'<div><canvas id="{name}"></canvas></div>' + '\n<!--- add div --->'

    new_data = old_data.replace('<!--- add chart --->', chart_string + '\n<!--- add chart --->')
    new_data = new_data.replace('<!--- add div --->', div_string)
    with open(f'Httpapp/templates/{file_name}.html', 'w') as f:
        f.write(new_data)
