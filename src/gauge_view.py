import os
from tkinter import (
    ARC,
    BOTH,
    LEFT,
    TOP,
    Canvas,
    DoubleVar,
    Entry,
    Frame,
    Label,
    TclError,
    Tk,
    W,
    font,
    messagebox,
)
from tkinter.ttk import Button, Style

from dotenv import load_dotenv
from gmail_service import GmailService

# Load environment variables from a .env file
load_dotenv()


class GaugeView(Tk):
    def __init__(self):

        # Set the window title
        Tk.__init__(self)
        self.title("Gauge")

        # Initialize pointer to None
        self.pointer = None

        # Create a canvas for drawing
        Canvas(self, width=500, height=500).pack(padx=20, pady=20)

        # Create a container frame for UI elements
        container = Frame(self)
        container.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

        # Create the user interface
        self.create_ui(container)

        # Configure the style for the UI elements
        style = Style()
        style.theme_use("clam")
        style.configure(".", bd=0, background="white")
        style.configure("CustomButton.TButton", bd=4, background="lightgray")
        style.configure("CustomCombobox.TCombobox", background="lightgray")

    def create_ui(self, parent=None):

        # Set parent to self if no parent is provided
        if not parent:
            parent = self

        # Create and pack the title label
        Label(
            parent,
            text="Lab 8 Gauge",
            font=font.Font(size=32, weight="bold", slant="italic"),
        ).pack(side=TOP, pady=10)

        # Initialize a DoubleVar to store the gauge value
        self.value = DoubleVar()
        self.value.set(0)

        # Create and pack the input row
        row1 = Frame(parent)
        row1.pack(fill="x", pady=5, padx=5)
        Label(row1, text="Enter New Value:", width=12).pack(side=LEFT)
        Entry(row1, text="Enter New Value:", textvariable=self.value).pack(side=LEFT)
        Button(
            row1, text="Enter", command=self.update_view, style="CustomButton.TButton"
        ).pack(side=LEFT, padx=5)

        # Create the canvas for the gauge
        self.canvas = Canvas(parent)

        # Center coordinates for the gauge
        x_center = 270
        y_center = 225

        # Draw the outer and inner circles of the gauge
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

        # Draw the gauge arc
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

        # Draw the markers on the gauge
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
                for j in range(9):
                    if j == 4:
                        self.canvas.create_arc(
                            x_center - r_marker_small - 4,
                            y_center - r_marker_small - 4,
                            x_center + r_marker_small + 4,
                            y_center + r_marker_small + 4,
                            start=degree_temp + 3.75 * (j + 1),
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
                            start=degree_temp + 3.75 * (j + 1),
                            extent=1,
                            outline="black",
                            fill="black",
                            width=15,
                            style=ARC,
                        )

        # Draw the numbers on the gauge
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

        # Add labels to the gauge
        self.canvas.create_text(
            225, 345, anchor=W, font=font.Font(size=20, weight="bold"), text="Pressure"
        )
        self.canvas.create_text(
            235, 370, anchor=W, font=font.Font(size=20, weight="bold"), text="Gauge"
        )

        # Draw the pointer of the gauge
        r_pointer = 170
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

        # Pack the canvas
        self.canvas.pack(fill=BOTH, expand=1)

    def update_view(self):
        try:
            # Check if the input value is out of bounds
            if self.value.get() < 0 or self.value.get() > 80:
                # Send an email if the value is out of bounds
                gmail_smtp = GmailService(
                    os.getenv("GMAIL_USER"),
                    os.getenv("GMAIL_PASSWORD"),
                    os.getenv("RECIPIENT_EMAIL"),
                )
                gmail_smtp.set_subject("Warning: Out of bound input value")
                gmail_smtp.set_body(
                    user_input=self.value.get(), normal_low=0, normal_high=80
                )
                gmail_smtp.send_email()
                messagebox.showinfo(
                    "Email Sent",
                    "Please check the email!",
                )
            else:
                # Update the pointer position on the gauge
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
        except TclError:
            # Show an error message if the input is invalid
            messagebox.showerror(
                "Invalid Input", "Please enter a valid floating-point number"
            )

    def update_mouse_coordinates(self, event):
        # Update the mouse coordinates label
        x = event.x
        y = event.y
        self.mouse_label.config(text=f"Mouse X: {x}, Mouse Y: {y}")


if __name__ == "__main__":
    app = GaugeView()
    app.mainloop()
