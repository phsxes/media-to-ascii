from tkinter import *
from tkinter import filedialog
import generator.utilities

root = Tk()
root.title("Media to ASCII")
root.geometry("1200x600")
root.resizable(width=True, height=True)
panel1, panel2 = None, None


def open_file():
    filename = filedialog.askopenfilename(title='open')
    return filename


def open_img():
    img_path = open_file()
    image = generator.utilities.TkImage(img_path)
    preview = image.get_preview(h=300)
    update_panels(preview, preview)


def update_panels(preview, result):
    global panel1, panel2

    if panel1 is None or panel2 is None:
        panel1 = Label(image=preview)
        panel1.image = preview
        panel1.pack(side="left", padx=20, pady=20)

        panel2 = Label(image=result)
        panel2.image = result
        panel2.pack(side="right", padx=20, pady=20)

    else:
        panel1.configure(image=preview)
        panel2.configure(image=result)
        panel1.image = preview
        panel2.image = result


btn = Button(root, text='Select Image', command=open_img)
btn.pack(side="top", fill="none", expand=0, padx="10", pady="10")
root.mainloop()
