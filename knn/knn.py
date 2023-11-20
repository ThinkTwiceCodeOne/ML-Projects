import tkinter as tk
from tkinter import filedialog
import numpy
import matplotlib.pyplot
import math
import statistics
import os
from PIL import Image, ImageTk
root = tk.Tk()
root.title("Menubar in Tk")
root.geometry("800x800")

canvas = tk.Canvas(master=root, width=600, height=600)
canvas.pack()
def genDataSet(filename,queryData):
    queryX, queryY = map(int, queryData.split(','))
    classes=['A','B','C','D']
    colors = ['b', 'g', 'c', 'm', 'y', 'k']
    file=open(filename,'r')
    count=0
    j=0
    all_arrays=[]
    for f in file:
        f=f.strip()
        dataSetFile=open(f,'r')
        tl=len(dataSetFile.readlines())
        i=0
        dataSetFile.seek(0)
        name=numpy.empty((5000,2))
        for line in dataSetFile:
            x,y=line.split()
            arr=numpy.array([[x,y]])
            name[i]=arr
            i+=1
        all_arrays.append(name)
    return knn(all_arrays,colors,queryX,queryY,classes)
def knn(all_arrays,colors,queryX,queryY,classes):
    i=0
    j=0
    distanceList=[]
    tl=0
    for arr in all_arrays:
        x,y=arr.T
        color=colors[i]
        matplotlib.pyplot.scatter(x,y,color=color)
        i+=1
        tl+=len(arr)
        for p in arr:
            xd=abs(p[0]-queryX)
            yd=abs(p[1]-queryY)
            d=math.sqrt(xd**2+yd**2)
            distanceList.append((classes[j],d,p))
        j+=1
    matplotlib.pyplot.plot(queryX,queryY,color='r',marker='o',markersize=15)
    distanceList.sort(key=lambda r:r[1])
    kFactor=int(math.sqrt(tl))
    if kFactor%4==0:
        kFactor+=1
    if kFactor%2==0: 
        kFactor+=1
    topKElements=distanceList[:kFactor]
    classess=list((x[0] for x in topKElements))
    result=statistics.mode(classess)
    matplotlib.pyplot.grid(True)
    matplotlib.pyplot.xlim(10000,1000000)
    matplotlib.pyplot.ylim(10000,1000000)
    matplotlib.pyplot.savefig('knn.png')
    matplotlib.pyplot.close()
    return result
def browse_files():
    global fileName
    home_directory = os.path.expanduser("~")
    fileName = filedialog.askopenfilename(initialdir=home_directory, title="Select a File", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    if fileName:
        label.config(text=fileName)
def runAlgo():
    query_text = queryBox.get("1.0", tk.END)
    result=genDataSet(fileName,query_text.strip())
    print(result)
    resultLabel.config(text="Result is "+result)
    image_path = os.path.abspath('knn.png')
    print(image_path)
    i=tk.PhotoImage(file=image_path)
    canvas.create_image(0,0,image=i,anchor="nw")
def show():
    image_path = os.path.abspath('knn.png')
    i = tk.PhotoImage(file=image_path)
    canvas.create_image(10, 10, image=i, anchor="nw")
    canvas.image = i

menubar = tk.Menu()
file_menu = tk.Menu(menubar, tearoff=False)
file_menu.add_command(label="Open File", command=browse_files)
show_button = tk.Button(root, text='Show Image', command=show)
show_button.pack(side=tk.BOTTOM)
button=tk.Button(root,text='Run',command=runAlgo)
button.pack(side=tk.BOTTOM)
queryBox=tk.Text(root,height=3,width=20)
queryBox.pack(side=tk.BOTTOM)
label1 = tk.Label(root, text="Enter query points separated by comma in text box : ")
label1.pack(side=tk.BOTTOM)
label = tk.Label(root, text="File Name : ")
label.pack(side=tk.BOTTOM)
resultLabel=tk.Label(root,text="Result is : ")
resultLabel.pack(side=tk.BOTTOM)
menubar.add_cascade(menu=file_menu, label="File")
root.config(menu=menubar)
root.mainloop()

