import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class Item:
    def __init__(self, name, tempo):
        self.name = name
        self.time = int(tempo)
        
Ciclo = []
    
class Background(Widget):
    def addTask(self):
        if (self.ids.name.text == "" or self.ids.time.text == "" or not self.ids.time.text.isdigit()):
            return
            
        self.ids.box.add_widget(Button(text = "X", size_hint_x = None, width = 55, height = 55, size_hint_y = None))
        self.ids.box.add_widget(Label(text = self.ids.name.text, size_hint_y = None, height = 55))    
        self.ids.box.add_widget(Label(text = str(self.ids.time.text), size_hint_y = None, height = 55))
        
        Ciclo.append(Item(self.ids.name.text, self.ids.time.text))
        
        print("Item adicionado: " + self.ids.name.text + " por " + str(self.ids.time.text) + " minutos, total de itens existentes: " + str(len(Ciclo)))
        
        self.ids.name.text = ""
        self.ids.time.text = ""
        
    pass     
    
class Tarefa(Widget):
    pass
    
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Ciclo de Estudos e Técnica Pomodoro"
        BoxLayout:
            size_hint_y: None
            size_hint_x: None
            height: 100
            width: 100
            spacing: 6
            orientation: 'vertical'
            Button:
                text: 'Start'
                on_press: 
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'pomodoro'
            Button:
                text: 'Edit'
                on_press: 
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'settings'
            
<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        Button:
            text: 'Back to Menu'
            size_hint_y: None
            height: 55
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'
            
        Background:
            size: root.width, root.height

<PomodoroScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Pomodoro"
        GridLayout:
            size_hint_y: None
            height: 55
            cols: 2
            Button:
                text: 'My settings button'
            Button:
                text: 'Back to menu'
                on_press: 
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'menu'
""")

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class PomodoroScreen(Screen):
    pass

class Inicializer(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(PomodoroScreen(name='pomodoro'))
        return sm
        
        
if __name__ == "__main__":
    Inicializer().run()