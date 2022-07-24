import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from tkinter import *
import tkinter as tk
from tkinter import END
from PIL import ImageTk,Image 


window = tk.Tk()
window.title("AutoFill System")
window.geometry("1000x1000")
font=('Times',23,'bold')
inputt=tk.StringVar()
inputbar=tk.Entry(window,font=font,textvariable=inputt)
inputbar.place(x=375, y=350)
listsug=tk.Listbox(window,height=5,font=font, relief='flat',bg='white')
listsug.place(x=375, y=400)



 
canvas = Canvas(window, width = 300, height = 100)  
canvas.place(x=385, y=240)  
img = ImageTk.PhotoImage(Image.open("GoogleLogo.png"))  
canvas.create_image(0, 0, anchor=NW, image=img) 


def autofill(*args):
    hamlet = gutenberg.words('shakespeare-macbeth.txt')
    # print(len(hamlet))
    target=[]
    text=[]
    sep=' '
    punc=['!','"','#','$','%','&','(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[',']','^','_','`','{','|','}','~',"''","``","--","?."] 
    x=sep.join(hamlet)
    w = word_tokenize(x)


    for word in w:
        if word not in punc:
            text.append(word.lower())


    fd=FreqDist()
    for word in text:
        fd[word.lower()]+=1   


    text_bigram=list(nltk.bigrams(text))
    wordinput=inputbar.get()
    wordList = []
    wordList = wordinput.split()
    lastWord = wordList[len(wordList)-1]
    wordinput = lastWord
    for i in range(len(text_bigram)):
        if text_bigram[i][0].lower() == wordinput.lower():
            target.append(text_bigram[i][1]) 


    fb=FreqDist()
    for words in target:
        fb[words]+=1


    for key,value in fb.items():
        fb[key]=fb[key]/fd[wordinput]
        
    fdtop=fb.most_common(5)
    listsug.delete(0,END)

    for word in fdtop:
        if word[0]=="'" :
            ind = text.index(word[0]) 
            
            while text[ind-1].lower() != wordinput.lower():
                ind = text.index(word[0],ind+1) 
            listvar=wordinput + word[0]+ text[ind+1]
            if wordinput.lower() in text:    
                listsug.insert(tk.END,listvar)
        else:
            listvar2=wordinput +' '+ word[0]
            if wordinput.lower() in text:    
                listsug.insert(tk.END,listvar2)


def my_upd(my_widget): 
    my_w = my_widget.widget
    index = int(my_w.curselection()[0]) 
    value = my_w.get(index) 
    inputt.set(value) 
    listsug.delete(0,END)     
def my_down(my_widget): 
    listsug.focus()  
    listsug.selection_set(0) 


inputbar.bind('<Down>', my_down) 
listsug.bind('<Right>', my_upd) 
listsug.bind('<Return>', my_upd)





inputt.trace('w',autofill)
window.mainloop()