import os
import pyautogui
import time
from datetime import datetime
from tkinter import ttk
import tkinter as tk
import subprocess
import threading
from threading import Thread
#SCHEDULER
#task class


screenW, screenH = pyautogui.size()
currMouseX, currMouseY = pyautogui.position()

def convertToMin(time):
    #convert time to minutes
    #current time
    now = datetime.now()
    currTime = now.strftime("%H:%M:%S")
    currHour = int(currTime[:2])
    currMin = int(currTime[3:5])
    currTotalMin = currHour * 60 + currMin

    #scheduled time
    print(time)
    hour = int(time[:2])
    minutes = int(time[2:])
    totalMin = hour * 60 + minutes
    return totalMin - currTotalMin

class Task():
    def __init__(self, time, title, description):
        self.time = convertToMin(time)
        self.title = title
        self.description = description
    
    def __eq__(self, other):
        return self.title == other.title
  
    def __hash__(self):
        return hash(self.title)

    def __repr__(self):
        return f"{self.time}, {self.title}"

#schedule class
class Schedule():
    def __init__(self):
        #self.timer = time.time()
        self.tasks = []

    def updateTime(self):
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            task.time -= 1
            if (task.time == 0):
                self.deleteTask(task)
                makePopup()
                typeInPop()
                #pyautogui.alert(text="its time", title="TASK")
    
    def makeNewTask(self,time, title, description):
        newTask = Task(time, title, description)
        if (len(self.tasks) == 0): self.tasks.append(newTask)
        else:
            for i in range(len(self.tasks)):
                task = self.tasks[i]
                if (task.time > newTask.time):
                    self.tasks.insert(i, newTask)
                    break
                elif (task.time == newTask.time):
                    break
            if i == len(self.tasks) - 1: self.tasks.append(newTask)
        print(self.tasks)
        return
    
    def deleteTask(self,task):
        for i in range(len(self.tasks)): 
            cmpTask = self.tasks[i]
            if (task.__eq__(cmpTask)):
                self.tasks.remove(task)
                break
    
LARGEFONT =("Verdana", 35) 
schedule = Schedule()
class tkinterApp(tk.Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, *args, **kwargs):  
          
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs) 
          
        # creating a container 
        container = tk.Frame(self)   
        container.pack(side = "top", fill = "both", expand = True)  
        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 

        # initializing frames to an empty array 
        self.frames = {}   

        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (StartPage, MakeTask): 

            frame = F(container, self) 

            # initializing frame of that object from 
            # startpage, page1, page2 respectively with  
            # for loop 
            self.frames[F] = frame  

            frame.grid(row = 0, column = 0, sticky ="nsew") 

        self.show_frame(StartPage) 

    # to display the current frame passed as 
    # parameter 
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.tkraise()

class StartPage(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
          
        # label of frame Layout 2 
        label = ttk.Label(self, text ="Startpage", font = LARGEFONT) 
          
        # putting the grid in its place by using 
        # grid 
        label.grid(row = 0, column = 4, padx = 10, pady = 10)  

        button1 = ttk.Button(self, text ="Make Task", 
        command = lambda : controller.show_frame(MakeTask)) 
      
        # putting the button in its place by 
        # using grid 
        button1.grid(row = 1, column = 1, padx = 10, pady = 10) 

        # putting the button in its place by 
        # using grid 

# second window frame page1  
class MakeTask(tk.Frame): 
    def __init__(self, parent, controller): 
        
        global schedule
        
        tk.Frame.__init__(self, parent) 
        
        label = ttk.Label(self, text ="Schedule", font = LARGEFONT) 
        label.pack()
        #label.grid(row = 0, column = 2, padx = 10, pady = 10) 

        # button to show frame 2 with text 
        # layout2 
        button1 = ttk.Button(self, text ="StartPage", 
                            command = lambda : controller.show_frame(StartPage)) 
        button1.pack()
        # putting the button in its place  
        # by using grid 
        #button1.grid(row = 1, column = 1, padx = 10, pady = 10) 

        # putting the button in its place by  
        # using grid 
        #button2.grid(row = 2, column = 1, padx = 10, pady = 10) 
        
        title = ttk.Entry(self, width = 20)
        title.insert(0,'What do you need to do?')
        title.pack()
        #title.grid(row = 3, column = 1, padx = 10, pady = 10) 
        
        desc = ttk.Entry(self, width = 20)
        desc.insert(0,'Description of task')
        desc.pack()
        #desc.grid(row = 4, column = 1, padx = 10, pady = 10) 
        
        hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
               "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]
        minutes = [ "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", 
                  "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                  "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                  "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
                  "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
                  "51", "52", "53", "54", "55", "56", "57", "58", "59"]

        n1 = tk.StringVar()
        hour = ttk.Combobox(self, textvariable = n1)
        hour['values'] = hours
        hour.pack()
        #hour.grid(row = 5, column = 1, padx = 10, pady = 10) 
        
        n2 = tk.StringVar() 
        n2.set("helo")
        minute = ttk.Combobox(self, textvariable = n2)
        minute['values'] = minutes
        minute.pack()
        #minute.grid(row = 6, column = 1, padx = 10, pady = 10) 
        

        button3 = ttk.Button(self, text = "click to make task", command = 
                            lambda: submit(hour, minute, title, desc, schedule, label2))
        button3.pack()

        #display tasks
        display = tk.StringVar()
        #display.set("Hello world")
        label2 = ttk.Label(self, text = display.get())
        label2.pack()
        #label2.grid(row = 1, column = 2, padx = 10, pady = 10) 

def submit(hour, minute, title, desc, schedule, label2):
    time = str(hour.get() + minute.get())
    if time == "": return
    titleStr = str(title.get())
    if titleStr == "": return
    descStr = str(desc.get())
    if descStr == "": return
    applied = schedule.makeNewTask(time, titleStr, descStr);
    updateSchedule(schedule, label2)

def updateSchedule(schedule, label2):
    #new display
    newDisplay = ""
    for i in range(len(schedule.tasks)):
        task = schedule.tasks[i]
        print(task)
        displayTime = str(task.time)
        displayTitle = task.title
        newDisplay += displayTitle + "\t" + "in " + displayTime + " minutes" + "\n"
    #display.set(newDisplay)
    label2.config(text = newDisplay)


def checkMinute():
    global schedule
    while True:
        now = datetime.now()
        currTime = now.strftime("%H:%M:%S")
        seconds = int(currTime[6:])
        #print(seconds)
        if seconds == 0:
            schedule.updateTime()
            #print("minute has passed")
root = tk.Tk()
app = tkinterApp() 

class check():
    def __init__(self):
        pass
    def run(self):
        print("here")
        checkMinute()

root = tk.Tk()
app = tkinterApp() 

if __name__=='__main__':
    checker = check()
    run1 = Thread(target = app.mainloop)
    run2 = Thread(target = checker.run)
    run1.start()
    run2.start()
    run1.join()
        
class Opener:
    def __init__(self, file_path):
        self.file_path = file_path
        self.process = None

    def start(self):
        sub = subprocess.Popen(['open', self.file_path])
        sub.wait()
        print("closed")

def makePopup():
    new = Opener("inspire.txt")
    new1 = Opener("photo.jpeg")
    t1 = threading.Thread(target=new.start)
    t2 = threading.Thread(target=new1.start)
    t2.start()
    t1.start()

def typeInPop():
    x = 300
    y = 300
    r1 = pyautogui.confirm(text="You have work to do now", title="task2", buttons= ['ok','procrastinate'])
    pyautogui.moveTo(x, y, duration=1)
    pyautogui.click(x, y)
    if r1 == 'procrastinate':
        pyautogui.typewrite('lazy toad')
    else:
        pyautogui.typewrite("as u should kween")

#screenW, screenH = pyautogui.size()
#currMouseX, currMouseY = pyautogui.position()

#alert textbox -> 1 dismissal option
#pyautogui.alert(text="description1", title="task1", button="ok")

#confirm textbox -> 2 dismissal options
#pyautogui.confirm(text="You have work to do now", title="task2", buttons= ['ok','procrastinate'])

#prompt textbox
#response = pyautogui.prompt(text="Start task 3 (y/n)", title="task3", default="STOP PROCRASTINATING")
#print(response) #prints

#if response != y --> screen invasion

# angery = pyautogui.locateOnScreen('anger.png') doesnt work rn try later

#p = pyautogui.password(text='enter passcode to stop', title='are you quitting', default='Loser', mask='*')
#print(p) #prints out the password

#r1 = pyautogui.confirm(text="You have work to do now", title="task2", buttons= ['ok','procrastinate'])
#print(currMouseX, currMouseY)
#pyautogui.moveTo(x, y, duration=1)
#pyautogui.click(x, y)
#if r1 == 'man':
#    pyautogui.typewrite('lazy fuck')
#else:
#    pyautogui.typewrite("as u should kween")

