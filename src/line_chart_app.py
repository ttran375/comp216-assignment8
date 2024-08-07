import os
import tkinter as tk
from tkinter import messagebox, ttk

from amazon_service import AmazonService
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LineChartApp(tk.Tk):

    # Class variables for minimum and maximum temperature thresholds and email information
    _min_temp = 18
    _max_temp = 27
    _SENDER = os.getenv("AWS_EMAIL")
    _RECIPIENT = os.getenv("RECIPIENT_EMAIL")
    _my_amazon_service = None

    def __init__(self):
        super().__init__()

        # Canvas dimensions for drawing the chart
        self.canvas_temp_width = 600
        self.canvas_temp_height = 300
        self.canvas_width = 800
        self.canvas_height = 300

        # Initialize pointer for temperature indicator
        self.my_pointer = None
        self.x_dist = 20
        self.y_dist = 5

        # Set up the main window
        self.title("Line Chart App")
        self.geometry("800x600")

        # Create a frame for the input and update button
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10)

        # Label and entry for new value input
        self.entry_label = ttk.Label(self.input_frame, text="Enter new value (°C):")
        self.entry_label.grid(row=0, column=0, padx=5)

        self.value_entry = ttk.Entry(self.input_frame)
        self.value_entry.grid(row=0, column=1, padx=5)

        # Button to update the chart with the new value
        self.update_button = ttk.Button(
            self.input_frame, text="Update Chart", command=self.update_chart
        )
        self.update_button.grid(row=0, column=2, padx=5)

        # Canvas for drawing the line chart
        self.canvas = tk.Canvas(
            self, width=self.canvas_width, height=self.canvas_height, bg="white"
        )
        self.canvas.pack(pady=10)

        # Frame for additional information display
        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(pady=10)

        # Labels for displaying units and value ranges
        self.units_label = ttk.Label(self.info_frame, text="Units: °C")
        self.units_label.grid(row=0, column=0, padx=10)

        self.low_value_label = ttk.Label(self.info_frame, text="Low Value: 18°C")
        self.low_value_label.grid(row=0, column=1, padx=10)

        self.normal_range_label = ttk.Label(
            self.info_frame, text="Normal Range: 20°C to 25°C"
        )
        self.normal_range_label.grid(row=0, column=2, padx=10)

        self.high_value_label = ttk.Label(self.info_frame, text="High Value: 27°C")
        self.high_value_label.grid(row=0, column=3, padx=10)

        # Initialize the list of values and draw the initial chart
        self.values = []
        self.draw_chart()
        self.draw_temperature()
        self.draw_temp_pointer(10)

        # Initialize the AmazonService object for sending emails
        self._my_amazon_service = AmazonService(self._SENDER, self._RECIPIENT)
        self._my_amazon_service.set_subject("Warning: Out of bound input value")

    def draw_chart(self):
        """
        Draw the line chart on the canvas.
        This function clears the canvas and redraws the chart with the current values.
        """
        self.canvas.delete("all")

        # Draw the X and Y axes
        self.canvas.create_line(50, 280, 550, 280, arrow=tk.LAST)
        self.canvas.create_line(50, 280, 50, 10, arrow=tk.LAST)

        # Labels for the X and Y axes
        self.canvas.create_text(550, 290, text="Time (s)", anchor=tk.W)
        self.canvas.create_text(15, 50, text="Temperature (°C)", anchor=tk.E, angle=90)

        # Draw the numerical values on the X axis
        for i in range(0, 26, 5):
            x = 50 + (i * self.x_dist)
            self.canvas.create_text(x, 288, text=f"{i}", anchor=tk.N)

        # Draw the numerical values on the Y axis
        for i in range(-10, 41, 10):
            y = 280 - (i + 10) * self.y_dist
            self.canvas.create_text(40, y, text=f"{i}", anchor=tk.E)

    def update_chart(self):
        """
        Update the chart with a new value.
        This function replaces the last value in the list with a new value provided by the user.
        """
        try:
            new_value = int(self.value_entry.get())

            # Check if the new value is out of bounds and send an email if necessary
            if new_value < self._min_temp or new_value > self._max_temp:
                self._my_amazon_service.set_body(
                    new_value, self._min_temp, self._max_temp
                )
                self._my_amazon_service.send_email()
                messagebox.showinfo(
                    "Email Sent",
                    "Please check the email!",
                )

            # Add the new value to the list
            self.values.append(new_value)

            # Calculate the position of the new point on the chart
            new_point = [
                50 + len(self.values) * self.x_dist,
                280 - (new_value + 10) * self.y_dist,
            ]

            # Draw the new point on the chart
            self.canvas.create_oval(
                new_point[0] - 3,
                new_point[1] - 3,
                new_point[0] + 3,
                new_point[1] + 3,
                fill="red",
            )
            self.canvas.create_text(
                new_point[0], new_point[1] - 10, text=str(new_value), fill="black"
            )

            # Draw a line connecting the new point to the previous point
            if len(self.values) > 1:
                pre_point = [
                    50 + (len(self.values) - 1) * self.x_dist,
                    280 - (self.values[-2] + 10) * self.y_dist,
                ]
                self.canvas.create_line(
                    new_point[0],
                    new_point[1],
                    pre_point[0],
                    pre_point[1],
                    fill="blue",
                    width=2,
                )

            # Update the temperature pointer
            self.draw_temp_pointer(new_value)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer")

    def draw_temperature(self):
        """
        Draw the temperature indicator on the canvas.
        This function creates a thermometer-like indicator to show the temperature.
        """
        width = 30
        start_point = [700, 10]
        start_point2 = [start_point[0] + width, start_point[1]]

        cir_top_left = [start_point[0], self.canvas_height - start_point[1] - width]
        cir_bottom_right = [start_point2[0], self.canvas_height - start_point[1]]

        self.temp_start_y = cir_bottom_right[1] - (width / 2)

        # Draw the bulb of the thermometer
        self.canvas.create_oval(
            cir_top_left[0],
            cir_top_left[1],
            start_point2[0],
            cir_bottom_right[1],
            outline="#f11",
            fill="#1f1",
        )

        # Draw the stem of the thermometer
        self.canvas.create_line(
            cir_top_left[0] - 2, start_point[1], cir_top_left[0] - 2, self.temp_start_y
        )

        self.rect_top_left = [cir_top_left[0] + 5, start_point[1]]
        self.rect_bottom_right = [cir_bottom_right[0] - 5, cir_bottom_right[1] - 20]
        self.canvas.create_rectangle(
            self.rect_top_left[0],
            self.rect_top_left[1],
            self.rect_bottom_right[0],
            self.rect_bottom_right[1],
            outline="",
            fill="#1f1",
        )

        # Draw the temperature values on the thermometer
        for i in range(0, 100, 10):
            y = self.temp_start_y - (i * 3)
            self.canvas.create_text(start_point[0] - 5, y, text=f"{i}", anchor=tk.E)

    def draw_temp_pointer(self, i):
        """
        Draw the temperature pointer on the thermometer.
        This function updates the position of the pointer based on the current temperature value.
        """
        if self.my_pointer is not None:
            self.canvas.delete(self.my_pointer)

        new_point = self.temp_start_y - (i * 3)

        new_rect_top_left = [self.rect_top_left[0], new_point]
        new_rect_bottom_right = [self.rect_bottom_right[0], new_point + (5 * 3)]
        self.my_pointer = self.canvas.create_rectangle(
            new_rect_top_left[0],
            new_rect_top_left[1],
            new_rect_bottom_right[0],
            new_rect_bottom_right[1],
            outline="",
            fill="#87cefa",
        )


if __name__ == "__main__":
    app = LineChartApp()
    app.mainloop()
