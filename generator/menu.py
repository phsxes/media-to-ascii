from tkinter import *
from tkinter import filedialog
import generator.utilities

root = Tk()
root.title("Media to ASCII")
root.geometry("825x450")
root.resizable(width=False, height=False)
src, res = None, None


def open_file():
    filename = filedialog.askopenfilename(title='open')
    return filename


def open_img():
    img_path = open_file()
    image = generator.utilities.TkImage(img_path)
    preview = image.get_preview(h=300)
    update_panels(preview, preview)


def update_panels(preview, result):
    global src, res

    if src is None or res is None:
        src = Label(image=preview)
        src.image = preview
        src.pack(side="left", padx=20, pady=20)

        res = Label(image=result)
        res.image = result
        res.pack(side="right", padx=20, pady=20)

    else:
        src.configure(image=preview)
        res.configure(image=result)
        src.image = preview
        res.image = result


btn = Button(root, text='Select Image', command=open_img)
btn.pack(side="top", fill="none", expand=0, padx="10", pady="10")
root.mainloop()
