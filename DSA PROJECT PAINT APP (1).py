from tkinter import*
from tkinter import colorchooser
import PIL.ImageGrab as ImageGrab
from tkinter import filedialog
from tkinter import messagebox 

#windowKey+alt+r for recording
root=Tk()
root.title("Paintify")
root.geometry("1000x600")

#-----------------Variables---------------------------

#size of pencil
options=[1,2,3,4,5,10,20,30,40,50,100]

stroke_size=IntVar()
stroke_size.set(1)

stroke_color=StringVar()
stroke_color.set("black")

previousColor = StringVar()
previousColor.set("White")
previousColor2 = StringVar()
previousColor2.set("White")

#variables for pencil 
prevPoint = [0,0]
currentPoint = [0,0]

#variable for text
textValue=StringVar()

undo_stack=[]
redo_stack = []

#-----------------Functions------------------------------

# yeh is liye ke jb pencil pr click hu tw icon aye pencil ka
def usePencil():
    stroke_color.set("black")
    canvas["cursor"]="arrow"

def useEraser():
     stroke_color.set("white")
     canvas["cursor"]="dotbox"

def selectColor():
    selectedColor = colorchooser.askcolor( "blue" , title= "Select Color")
    if selectedColor[1] == None:
        stroke_color.set("black")
    else:
        stroke_color.set(selectedColor[1])
        previousColor2.set(previousColor.get())
        previousColor.set(selectedColor[1])

        previousColorButton["bg"] = previousColor.get()
        previousColor2Button["bg"] = previousColor2.get()
def saveAction(item_id, item_type, *coords):
    """Save the action with its ID, type, and coordinates for redo/undo."""
    undo_stack.append((item_id, item_type, coords))
    redo_stack.clear()  # Clear redo stack on any new action

    
def paint(event):
    global prevPoint
    x, y = event.x, event.y
    currentPoint = [x, y]
    if prevPoint != [0, 0]:
        polygon = canvas.create_polygon(prevPoint[0], prevPoint[1], x, y, fill=stroke_color.get(),
                                        outline=stroke_color.get() , width=stroke_size.get()) 
        saveAction(polygon, "polygon", prevPoint[0], prevPoint[1], x, y)  # Save the line action with coordinates
    prevPoint = currentPoint
    if event.type == "5":  # Reset on mouse release
        prevPoint = [0, 0]

def paintRight(event):
    x, y = event.x, event.y
    arc = canvas.create_arc(x, y, x + stroke_size.get(), y + stroke_size.get(),
                            fill=stroke_color.get(), outline=stroke_color.get(), width=stroke_size.get())
    saveAction(arc, "arc", x, y, x + stroke_size.get(), y + stroke_size.get())  # Save the arc action with coordinates
def saveImage():
    try:
       fileLocation = filedialog.asksaveasfilename(defaultextension="jpg")
       x=root.winfo_rootx()
       y=root.winfo_rooty()+100

       img=ImageGrab.grab(bbox=(x,y,x+1000,y+500))
       img.save(fileLocation)
       showImage = messagebox.askyesno("Paint App","Do you want to open image?")
       if showImage:
          img.show()
    except Exception as e:
        messagebox.showinfo("Paint App","Error occured")
        

def clear():
    if messagebox.askokcancel("PaintApp","Do you want to clear everything?"):
         canvas.delete("all")
         undo_stack.clear()
         redo_stack.clear()
def createNew():
    if messagebox.askyesno("PaintApp","Do you want to save before you clear everything?"):
        saveImage()
    clear()

def undo():
    if undo_stack:
        item_id, item_type, coords = undo_stack.pop()
        canvas.delete(item_id)  # Remove the item from the canvas
        redo_stack.append((item_id,item_type, coords))  # Save the type and coords for redo


def redo():
    if redo_stack:
        item_id, item_type, coords = redo_stack.pop()  # Unpack the last action from the redo stack
        
        if item_type == "polygon":
            # Create a new polygon with the saved coordinates
            new_item = canvas.create_polygon(*coords, fill=stroke_color.get(), outline=stroke_color.get(), width=stroke_size.get())
        elif item_type == "arc":
            # Recreate the arc using the saved coordinates
            new_item = canvas.create_arc(coords[0], coords[1], coords[2], coords[3], fill=stroke_color.get(), outline=stroke_color.get(), width=stroke_size.get())
        elif item_type == "text":
            new_item = canvas.create_text(coords[0], coords[1], text=textValue.get(), fill=stroke_color.get())
        else:
            return  # If an unknown item_type is encountered, skip

        # Save the new item in the undo stack
        undo_stack.append((new_item, item_type, coords))

def help():
    helpText="1. Draw by holding right button of mouse to create dotted lines.\n2.Click scroll well to put text on Canvas\n3. Click on Select Color Option to select specific color\n4. Click on Clear to clear entire canvas"
    messagebox.showinfo("Help",helpText)
def settings():
    messagebox.showwarning("Settings","Not Available")
def about():
    messagebox.showinfo("About","Paintify \nVersion 1.0\n\nDeveloped by: Zoha, Anum, Fizza\n"
                            + "This is a simple paint application with basic drawing and coloring features.")
def writeText(event):
      text_item = canvas.create_text(event.x, event.y, text=textValue.get())
      saveAction(text_item, "text", event.x, event.y)
#----------------User Interface--------------------------

# frame -1 : Tools

frame1=Frame(root, height=100,width=1100)
frame1.grid(row=0,column=0,sticky=NW)

# toolsFrame

toolsFrame=Frame(frame1, height=100 ,width=100 , relief= SUNKEN , borderwidth= 3)
toolsFrame.grid(row=0,column=0)
pencilButton= Button(toolsFrame,text="Pencil",width=10,command=usePencil)
pencilButton.grid(row=0,column=0)
eraserButton= Button(toolsFrame,text="Eraser",width=10,command= useEraser)
eraserButton.grid(row=1,column=0)
undoButton = Button(toolsFrame, text="Undo", width=10, command=undo)
undoButton.grid(row=2, column=0)
redoButton = Button(toolsFrame, text="Redo", width=10, command=redo)
redoButton.grid(row=3, column=0)


#yeh droplist ke liye hai

# sizeFrame

sizeFrame=Frame(frame1, height=100 ,width=100 ,relief= SUNKEN , borderwidth= 3)
sizeFrame.grid(row=0,column=1)
defaultButton= Button(sizeFrame,text="default",width=10,command=usePencil)
defaultButton.grid(row=0,column=0)
sizeList=OptionMenu(sizeFrame, stroke_size, *options)
sizeList.grid(row=1,column=0)

#colourbox frame
colorBoxFrame = Frame(frame1, height=100, width=100, relief=SUNKEN, borderwidth=3)
colorBoxFrame.grid(row=0, column=2)

colorBoxButton = Button(colorBoxFrame, text="Select Color", width=10, command=selectColor)
colorBoxButton.grid(row=0, column=0)
previousColorButton = Button(colorBoxFrame, text="Previous", width=10, command=lambda: stroke_color.set(previousColor.get()))
previousColorButton.grid(row=1, column=0)
previousColor2Button = Button(colorBoxFrame, text="Previous2", width=10, command=lambda: stroke_color.set(previousColor2.get()))
previousColor2Button.grid(row=2, column=0)
#colors frame
colorsFrame  = Frame(frame1 , height=100 , width=100 , relief= SUNKEN , borderwidth= 3)
colorsFrame.grid(row=0 , column= 3)

redbutton = Button( colorsFrame  ,  text= "Red" , bg="red" , width=10 , command=lambda:stroke_color.set("red"))
redbutton.grid(row=0 , column=0)
greenbutton = Button( colorsFrame  ,  text= "Green" , bg="green" , width=10 , command=lambda:stroke_color.set("green"))
greenbutton.grid(row=1 , column=0)
bluebutton = Button( colorsFrame  ,  text= "Blue" , bg="blue" , width=10 , command=lambda:stroke_color.set("blue"))
bluebutton.grid(row=2 , column=0)
yellowbutton = Button( colorsFrame  ,  text= "Yellow" , bg="yellow" , width=10 , command=lambda:stroke_color.set("yellow"))
yellowbutton.grid(row=0 , column=1)
pinkbutton = Button( colorsFrame  ,  text= "Pink" , bg="pink" , width=10 , command=lambda:stroke_color.set("pink"))
pinkbutton.grid(row=1 , column=1)
orangebutton = Button( colorsFrame  ,  text= "Orange" , bg="orange" , width=10 , command=lambda:stroke_color.set("orange"))
orangebutton.grid(row=2 , column=1)

#saveImageFrame
saveImageFrame  = Frame(frame1 , height=100 , width=100 , relief= SUNKEN , borderwidth= 3)
saveImageFrame.grid(row=0 , column= 4)

saveImagebutton = Button( saveImageFrame  ,  text= "Save" , bg="White" , width=10 , command=saveImage)
saveImagebutton.grid(row=0 , column=0)
newImagebutton = Button( saveImageFrame  ,  text= "New" , bg="White" , width=10 , command=createNew)
newImagebutton.grid(row=1 , column=0)
clearImagebutton = Button( saveImageFrame  ,  text= "Clear" , bg="White" , width=10 , command=clear)
clearImagebutton.grid(row=2 , column=0)

#helpSettingFrame
helpSettingFrame  = Frame(frame1 , height=100 , width=100 , relief= SUNKEN , borderwidth= 3)
helpSettingFrame.grid(row=0 , column= 5)

helpbutton = Button( helpSettingFrame  ,  text= "Help" , bg="White" , width=10 , command=help)
helpbutton.grid(row=0 , column=0)
settingbutton = Button( helpSettingFrame  ,  text= "Settings" , bg="White" , width=10 , command=settings)
settingbutton.grid(row=1 , column=0)
aboutbutton = Button( helpSettingFrame  ,  text= "About" , bg="White" , width=10 , command=about)
aboutbutton.grid(row=2 , column=0)

#TextFrame
TextFrame  = Frame(frame1 , height=100 , width=200 , relief= SUNKEN , borderwidth= 3)
TextFrame.grid(row=0 , column= 6)

textTitleButton = Label( TextFrame  ,  text= "Write your text here:" , bg="White" , width=20)
textTitleButton.grid(row=0 , column=0)
entryButton = Entry( TextFrame ,textvariable=textValue, bg="White" , width=20)
entryButton.grid(row=1 , column=0)
clearButton = Button( TextFrame ,  text= "Clear" , bg="White" , width=20 , command=lambda:textValue.set(""))
clearButton.grid(row=2 , column=0)

#noteFrame
noteFrame  = Frame(frame1 , height=100 , width=200 , relief= SUNKEN , borderwidth= 3)
noteFrame.grid(row=0 , column= 7)

textTitleButton = Text( noteFrame  ,bg="White" , width=40,height=4)
textTitleButton.grid(row=0 , column=0)

# Frame -2- Canvas
frame2=Frame(root, height=500,width=1100,bg="yellow")
frame2.grid(row=1,column=0)

canvas=Canvas(frame2,height=500,width=1100,bg="white")
canvas.grid(row=0, column=0)
 
canvas.bind("<B1-Motion>" , paint)
canvas.bind("<ButtonRelease-1>" , paint)
canvas.bind("<B3-Motion>", paintRight)
canvas.bind("<Button-2>",writeText)
root.resizable(False,False)
root.mainloop()

