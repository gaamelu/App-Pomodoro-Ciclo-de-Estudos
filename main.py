
import json
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, NumericProperty

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from functools import partial

def convertTimeString(integer):
    integer = int(integer)
    hours = int(integer/60)
    minutes = integer - hours*60
    
    s = ''
    if (hours > 0):
        s = str(hours) + 'h '
    
    if (minutes > 0):
        s = s + str(minutes) + 'm'
        
    return s
    
class Tarefa(BoxLayout):
    taskname = ''
    tasktime = 0
    def __init__(self, newname, newtime ,**kwargs):
        super().__init__(**kwargs)
        
        self.size_hint_y = None
        self.height = 55
        
        self.taskname = newname
        self.tasktime = newtime

        self.add_widget(Button(text = "X", on_release = self.removeExistence, size_hint_x = None, width = 55, height = 55, size_hint_y = None))
        self.add_widget(Label(text = newname, size_hint_y = None, height = 55))    
        self.add_widget(Label(text = convertTimeString(newtime), size_hint_y = None, height = 55)) 
        
    def removeExistence(self, button, *args):
        self.parent.parent.parent.parent.tarefas.remove([self.taskname, self.tasktime])
        self.parent.parent.parent.parent.saveData()
        self.parent.remove_widget(self)
    
class Background(Widget):

    NewName = ObjectProperty(None)
    NewTime = ObjectProperty(None)
    tarefas = []
    
    path = ''
    def saveData(self, *args):
        with open('data.json', 'w') as data:
            json.dump(self.tarefas, data)
            
    def loadData(self, *args):
        try:
            with open(self.path+'data.json', 'r') as data:
                self.tarefas = json.load(data)               
        except FileNotFoundError:
            pass
            
    def addTask(self, *args):  
        
        if (self.NewName.text == "" or self.NewTime.text == "" or not self.NewTime.text.isdigit()):
            return
       
        ItemA = Tarefa(self.NewName.text, self.NewTime.text)
        self.ids.box.add_widget(ItemA)
        self.tarefas.append([self.NewName.text, self.NewTime.text])
        self.saveData()
       
        self.NewName.text = ""
        self.NewTime.text = ""
        
    def AddingLayout(self, *args):
    
        Grid = GridLayout(cols=2, spacing = 2)
        pop = Popup(title='Adicionar item', content=Grid, size_hint = (None, None), height = 175, width = 300 ) 
        
        Grid.add_widget(Label(text='Name:'))
        
        self.NewName = TextInput(multiline=False)
        Grid.add_widget(self.NewName)
        
        Grid.add_widget(Label(text='Tempo:'))
        
        self.NewTime = TextInput(multiline=False)
        Grid.add_widget(self.NewTime)
        
        Grid.add_widget(Button(text='Add', on_release = self.addTask))
        Grid.add_widget(Button(text='Cancelar', on_release= pop.dismiss))
        
        pop.open()
        
    pass
    
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
                
        Image:
            source: 'pomodoro.png'
            
        AnchorLayout:
            canvas.before:
                Color:
                    rgba: 1, 1, 0, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            
            BoxLayout:
                orientation: 'vertical'
                pos: self.width/2, self.height/2
                spacing: 5
                
                Button:                      
                    text: 'Start'
                    size_hint: None, None
                    size: 120, 50
                    on_press: 
                        root.manager.transition.direction = 'left'
                        root.manager.current = 'pomodoro'
                Button:
                    text: 'Edit'
                    size_hint: None, None
                    size: 120, 50
                    on_press: 
                        root.manager.transition.direction = 'left'
                        root.manager.current = 'settings'
                Button:
                    text: 'Quit'
                    size_hint: None, None
                    size: 120, 50
                    on_press: root.ConfirmQuit()
            
<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        ActionBar:
            ActionView:
                ActionPrevious:
                    title: 'Editor'
                    on_press: 
                        root.manager.transition.direction = 'right'
                        root.manager.current = 'menu'
                
        Background:
            id: backID

<PomodoroScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        ActionBar:
            ActionView:
                ActionPrevious:
                    title: 'Pomodoro'
                    on_press: 
                        root.manager.transition.direction = 'right'
                        root.manager.current = 'menu'
                        
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
        
    def ConfirmQuit(self, *args):
        
        Conteudo = BoxLayout(spacing=2)
        pop = Popup(title='Voce deseja mesmo sair?', content=Conteudo, size_hint = (None, None), width = 300, height = 180)
        
        Conteudo.add_widget(Image(source='atention.png'))
        Conteudo.add_widget(Button(text='Sim', on_release= App.get_running_app().stop ))
        Conteudo.add_widget(Button(text='Nao', on_release= pop.dismiss))
        
        pop.open()
    pass

class SettingsScreen(Screen):
    pass

class PomodoroScreen(Screen):
    pass

class Inicializer(App):
    def build(self):
        sm = ScreenManager()
        set = SettingsScreen(name='settings')
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(set)
        sm.add_widget(PomodoroScreen(name='pomodoro'))
        
        # ativar esse comentário somente quando estiver disponível a remoção de widgets
        set.ids.backID.path = App.get_running_app().user_data_dir+'\\'

        set.ids.backID.loadData()
        
        for tarefa in set.ids.backID.tarefas:
            ItemA = Tarefa(tarefa[0], tarefa[1])#BoxLayout(size_hint_y = None, height = 55)
            #ItemA.add_widget(Button(text = "X", on_release = partial(set.ids.backID.ids.box.remove_widget, ItemA), size_hint_x = None, width = 55, height = 55, size_hint_y = None))
            #ItemA.add_widget(Label(text = tarefa[0], size_hint_y = None, height = 55))    
            #ItemA.add_widget(Label(text = convertTimeString(tarefa[1]), size_hint_y = None, height = 55))
            set.ids.backID.ids.box.add_widget(ItemA)       
        
        return sm
        
        
if __name__ == "__main__":
    Inicializer().run()