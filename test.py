import customtkinter as ctk

top = ctk.CTk()

testlabel = ctk.CTkLabel(top, text="This is a test label.")
testlabel.configure(font=("Lato", 18))
testlabel.pack(padx=12, pady=15)

testbutton = ctk.CTkButton(
	top, 
	text="This is a test button.", 
	corner_radius=10, 
	fg_color="#2E8B57",  # SeaGreen color
	hover_color="#3CB371",  # MediumSeaGreen color
	text_color="white"
)

testbutton.pack(padx=12, pady=15)

exitbutton = ctk.CTkButton(top, text="Exit", command=top.quit, corner_radius=10, 
    fg_color="#B22222",  # FireBrick color
    hover_color="#CD5C5C",  # IndianRed color
    text_color="white")
exitbutton.pack(padx=12, pady=15)

top.mainloop()