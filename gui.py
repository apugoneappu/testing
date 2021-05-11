from otp import OTP
import tkinter as tk
from main_gui import Main

m = Main()

window = tk.Tk()
window.title('BookMySlot')

window.geometry("700x500")

window.rowconfigure([0,1,2,3,4,5], weight=1)
window.rowconfigure(6, weight=2)
window.columnconfigure(0, weight=1)

################ APP NAME #################

frame_app_name = tk.Frame(master=window)
frame_app_name.grid(row=0, column=0, sticky='news')

frame_app_name.rowconfigure(0, weight=1)
frame_app_name.columnconfigure(0, weight=1)

label_app_name = tk.Label(master=window ,text='BookMySlot: Covid Vaccine Booking')
label_app_name.grid(row=0, column=0, sticky='news')

################ MOBILE #################

frame_mobile = tk.Frame(master=window)
frame_mobile.grid(row=1, column=0, sticky='news')

frame_mobile.rowconfigure(0, weight=1)
frame_mobile.columnconfigure(0, weight=2) #label
frame_mobile.columnconfigure(1, weight=5) #entry
frame_mobile.columnconfigure(2, weight=2) #button

label_mobile = tk.Label(master=frame_mobile , text='Mobile number')
label_mobile.grid(row=0, column=0, sticky='news')

entry_mobile = tk.Entry(master=frame_mobile, validate='focusout')
entry_mobile['validatecommand'] = (entry_mobile.register(OTP.check_number_format), '%P')
entry_mobile.grid(row=0, column=1, sticky='news')

button_mobile = tk.Button(master=frame_mobile, text='Get OTP')
button_mobile.grid(row=0, column=2, sticky='news')

################ OTP #################

frame_otp = tk.Frame(master=window)
frame_otp.grid(row=2, column=0, sticky='news')

frame_otp.rowconfigure(0, weight=1)
frame_otp.columnconfigure(0, weight=2) #label
frame_otp.columnconfigure(1, weight=7) #entry

label_otp = tk.Label(master=frame_otp , text='OTP number')
label_otp.grid(row=0, column=0, sticky='news')

entry_otp = tk.Entry(master=frame_otp)
entry_otp.grid(row=0, column=1, sticky='news')

################ Pincode #################

frame_pincode = tk.Frame(master=window)
frame_pincode.grid(row=3, column=0, sticky='news')

frame_pincode.rowconfigure(0, weight=1)
frame_pincode.columnconfigure([0,2,4], weight=2) #labels
frame_pincode.columnconfigure([1,3,5], weight=7) #entries

label_pincode_from = tk.Label(master=frame_pincode , text='Pincode from')
label_pincode_from.grid(row=0, column=0, sticky='news')

entry_pincode_from = tk.Entry(master=frame_pincode)
entry_pincode_from.grid(row=0, column=1, sticky='news')

label_pincode = tk.Label(master=frame_pincode, text='Pincode')
label_pincode.grid(row=0, column=2, sticky='news')

entry_pincode = tk.Entry(master=frame_pincode)
entry_pincode.grid(row=0, column=3, sticky='news')

label_pincode_to = tk.Label(master=frame_pincode , text='Pincode to')
label_pincode_to.grid(row=0, column=4, sticky='news')

entry_pincode_to = tk.Entry(master=frame_pincode)
entry_pincode_to.grid(row=0, column=5, sticky='news')

################ Names #################

frame_names = tk.Frame(master=window)
frame_names.grid(row=4, column=0, sticky='news')

frame_names.rowconfigure(0, weight=1)
frame_names.columnconfigure(0, weight=2) #label
frame_names.columnconfigure(1, weight=7) #entry

label_names = tk.Label(master=frame_names , text='Enter names (comma separated)')
label_names.grid(row=0, column=0, sticky='news')

entry_names = tk.Entry(master=frame_names)
entry_names.grid(row=0, column=1, sticky='news')

################ Captcha #################

frame_captcha = tk.Frame(master=window)
frame_captcha.grid(row=5, column=0, sticky='news')

frame_captcha.rowconfigure([0,1], weight=1) 
frame_captcha.columnconfigure(0, weight=2) # frameleft - label, entry
frame_captcha.columnconfigure(1, weight=7) #label

label_captcha = tk.Label(master=frame_captcha, text='Enter captcha')
label_captcha.grid(row=0, column=0, rowspan=1, columnspan=1)

entry_captcha = tk.Entry(master=frame_captcha)
entry_captcha.grid(row=1, column=0, rowspan=1, columnspan=1)

# Image right
from PIL import ImageTk, Image
load = Image.open("output.png")
img = ImageTk.PhotoImage(load)
label_image = tk.Label(master=frame_captcha, image=img)
label_image.image = img
label_image.grid(row=0, column=1, sticky='news', rowspan=2, columnspan=1)

################ Output #################
frame_output = tk.Frame(master=window)
frame_output.grid(row=6, column=0, sticky='new')

frame_output.rowconfigure(0, weight=1)
frame_output.rowconfigure(1, weight=10)
frame_output.columnconfigure(0, weight=10)

label_output = tk.Label(master=frame_output, text='Output logs', bg='red')
label_output.grid(row=0, column=0)

logs = tk.StringVar()
label_output = tk.Label(master=frame_output, text='', bg='blue')
label_output['textvariable'] = logs
label_output.grid(row=1, column=0)


window.mainloop()