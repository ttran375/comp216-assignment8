from tkinter import *
from tkinter.ttk import *
from tkinter import font
from gmail_smtp import GmailSMTP
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GaugeView(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("Gauge")
        Canvas(self, width=500, height=500).pack(padx=20, pady=20)
        container = Frame(self)
        container.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
        self.create_ui(container)

        style = Style()
        style.theme_use("clam")
        style.configure(".", bd=0, background="white")
        style.configure("CustomButton.TButton", bd=4, background="lightgray")
        style.configure("CustomCombobox.TCombobox", background="lightgray")

    def create_ui(self, parent=None):
        if not parent:
            parent = self

        Label(
            parent,
            text="Lab 8 Gauge",
            font=font.Font(size=32, weight="bold", slant="italic"),
        ).pack(side=TOP, pady=10)

        self.value = DoubleVar()
        self.value.set(0)
        row1 = Frame(parent)
        row1.pack(fill="x", pady=5, padx=5)
        Label(row1, text="Enter New Value:", width=12).pack(side=LEFT)
        Entry(row1, text="Enter New Value:", textvariable=self.value).pack(side=LEFT)
        Button(
            row1, text="Enter", command=self.updateView, style="CustomButton.TButton"
        ).pack(side=LEFT, padx=5)

        self.canvas = Canvas(parent)

        x_center = 270
        y_center = 225
        # center 270 225, radius 200
        self.canvas.create_oval(
            x_center - 200,
            y_center - 200,
            x_center + 200,
            y_center + 200,
            outline="#C0C0C0",
            fill="#C0C0C0",
            width=2,
        )
        self.canvas.create_oval(
            x_center - 190,
            y_center - 190,
            x_center + 190,
            y_center + 190,
            outline="white",
            fill="white",
            width=0,
        )
        self.canvas.create_oval(
            x_center - 15,
            y_center - 15,
            x_center + 15,
            y_center + 15,
            outline="black",
            fill="black",
            width=0,
        )
        self.canvas.create_oval(
            x_center - 10,
            y_center - 10,
            x_center + 10,
            y_center + 10,
            outline="#d4af37",
            fill="#d4af37",
            width=0,
        )

        # center 270 225, radius 120, red marker
        self.canvas.create_arc(
            x_center - 120,
            y_center - 120,
            x_center + 120,
            y_center + 120,
            start=-60,
            extent=300,
            outline="#D23247",
            fill="white",
            width=6,
            style=ARC,
        )

        # canvas.create_line(x_center, y_center, 420, 225)
        r_marker = 132
        r_marker_small = r_marker - 7
        for i in range(9):
            degree_temp = -60 + 37.5 * i
            self.canvas.create_arc(
                x_center - r_marker,
                y_center - r_marker,
                x_center + r_marker,
                y_center + r_marker,
                start=degree_temp,
                extent=1,
                outline="black",
                fill="black",
                width=30,
                style=ARC,
            )
            if i != 8:
                for i in range(9):
                    if i == 4:
                        self.canvas.create_arc(
                            x_center - r_marker_small - 4,
                            y_center - r_marker_small - 4,
                            x_center + r_marker_small + 4,
                            y_center + r_marker_small + 4,
                            start=degree_temp + 3.75 * (i + 1),
                            extent=1,
                            outline="black",
                            fill="black",
                            width=23,
                            style=ARC,
                        )
                    else:
                        self.canvas.create_arc(
                            x_center - r_marker_small,
                            y_center - r_marker_small,
                            x_center + r_marker_small,
                            y_center + r_marker_small,
                            start=degree_temp + 3.75 * (i + 1),
                            extent=1,
                            outline="black",
                            fill="black",
                            width=15,
                            style=ARC,
                        )

        self.canvas.create_text(
            345, 365, anchor=W, font=font.Font(size=20, weight="bold"), text="80"
        )
        self.canvas.create_text(
            410, 290, anchor=W, font=font.Font(size=20, weight="bold"), text="70"
        )
        self.canvas.create_text(
            415, 180, anchor=W, font=font.Font(size=20, weight="bold"), text="60"
        )
        self.canvas.create_text(
            360, 100, anchor=W, font=font.Font(size=20, weight="bold"), text="50"
        )
        self.canvas.create_text(
            255, 65, anchor=W, font=font.Font(size=20, weight="bold"), text="40"
        )
        self.canvas.create_text(
            155, 98, anchor=W, font=font.Font(size=20, weight="bold"), text="30"
        )
        self.canvas.create_text(
            100, 185, anchor=W, font=font.Font(size=20, weight="bold"), text="20"
        )
        self.canvas.create_text(
            108, 285, anchor=W, font=font.Font(size=20, weight="bold"), text="10"
        )
        self.canvas.create_text(
            185, 365, anchor=W, font=font.Font(size=20, weight="bold"), text="0"
        )

        self.canvas.create_text(
            225, 345, anchor=W, font=font.Font(size=20, weight="bold"), text="Pressure"
        )
        self.canvas.create_text(
            235, 370, anchor=W, font=font.Font(size=20, weight="bold"), text="Gaugu"
        )

        # pointer
        r_pointer = 170
        # canvas.create_line(x_center, y_center, 176, 381, width=3)
        self.pointer = self.canvas.create_arc(
            x_center - r_pointer,
            y_center - r_pointer,
            x_center + r_pointer,
            y_center + r_pointer,
            start=240 + 3.75 * self.value.get(),
            extent=1,
            outline="black",
            fill="black",
        )

        self.canvas.pack(fill=BOTH, expand=1)

        # Add label for mouse coordinates
        # self.mouse_label = Label(parent, text='Mouse X: 0, Mouse Y: 0')
        # self.mouse_label.pack(side=BOTTOM)
        # # Bind mouse motion event to update the mouse coordinates label
        # self.canvas.bind('<Motion>', self.update_mouse_coordinates)

    def updateView(self):

        if self.value.get() < 0 or self.value.get() > 80:
            gmail_smtp = GmailSMTP(
                os.getenv("GMAIL_USER"),
                os.getenv("GMAIL_PASSWORD"),
                os.getenv("GMAIL_RECIPIENT"),
            )
            gmail_smtp.setSubject("Warning: Out of bound input value")
            gmail_smtp.setBody(userInput=self.value.get(), normalLow=0, normalHigh=80)
            gmail_smtp.sendemail()

        else:
            if self.pointer is not None:
                self.canvas.delete(self.pointer)
            x_center = 270
            y_center = 225
            r_pointer = 170
            self.pointer = self.canvas.create_arc(
                x_center - r_pointer,
                y_center - r_pointer,
                x_center + r_pointer,
                y_center + r_pointer,
                start=240 - 3.75 * self.value.get(),
                extent=1,
                outline="black",
                fill="black",
            )

    def update_mouse_coordinates(self, event):
        x = event.x
        y = event.y
        self.mouse_label.config(text=f"Mouse X: {x}, Mouse Y: {y}")


if __name__ == "__main__":
    app = GaugeView()
    app.mainloop()
