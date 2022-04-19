from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from app import start


def print_funk():
    my_file = open('app.py', 'a')
    text_for_file = '@apps.route("/viewer")\ndef viewer():\n\titems = Items.query.order_by(Items.id).all()\n\treturn render_template("viewer.html", items=items)'
    my_file.write(text_for_file + '\n')
    my_file.close()


class Myapp(App):

    def btn_press1(instance):
        start()

    def btn_press2(instance):
        print_funk()

    def build(self):
        btn1 = Button(text='Старт')
        btn2 = Button(text='Добавление страницы товары')
        layout = GridLayout(cols=2)
        layout.add_widget(btn1)
        btn1.bind(on_press=Myapp.btn_press1)
        layout.add_widget(btn2)
        btn2.bind(on_press=Myapp.btn_press2)
        return layout


if __name__ == '__main__':
    Myapp().run()