import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
    
class Background(Widget):
    def addTask(self):
        if (self.ids.name.text == "" or not int(self.ids.time.text)):
            print("ITEM SEM CONFIGURAÇÕES CORRETAS")
            return
        self.ids.box.add_widget(Button(text = "X", size_hint_x = None, width = 55, height = 55, size_hint_y = None))
        self.ids.box.add_widget(Label(text = self.ids.name.text, size_hint_y = None, height = 55))    
        self.ids.box.add_widget(Label(text = str(self.ids.time.text), size_hint_y = None, height = 55))
        self.ids.name.text = ""
        self.ids.time.text = ""
        
    pass     
    
class Tarefa(Widget):
    pass

class Inicializer(App):
    def build(self):
        background = Background()
        return background
        
        
if __name__ == "__main__":
    Inicializer().run()