import tkinter as tk
from tkinter import ttk
import colorsys

class ColorAdjusterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Adjuster")
        
        # HSV max values (default H: 360, S: 1, V: 1)
        self.h_max = 360
        self.s_max = 100
        self.v_max = 100
        
        # Current color in HSV (colorsys format)
        self.hsv = [0, 0, 1]  # default white color
        
        # Frame for color preview
        self.preview_frame = tk.Frame(self.root, height=50, bg=self.hsv_to_hex(self.hsv))
        self.preview_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Frame for HEX input
        self.hex_frame = tk.Frame(self.root)
        self.hex_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(self.hex_frame, text="HEX:").pack(side=tk.LEFT)
        self.hex_input = tk.Entry(self.hex_frame)
        self.hex_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.hex_input.bind("<Return>", self.on_hex_input)
        
        # Frames for RGB and HSV adjustment
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.rgb_frame = tk.Frame(self.control_frame)
        self.rgb_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.hsv_frame = tk.Frame(self.control_frame)
        self.hsv_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Add RGB and HSV sliders and entries
        self.create_rgb_controls()
        self.create_hsv_controls()

        self.update_ui_from_hsv()

    def create_rgb_controls(self):
        tk.Label(self.rgb_frame, text="RGB Controls").pack()
        
        # R control
        self.r_var = tk.IntVar()
        r_frame = tk.Frame(self.rgb_frame)
        r_frame.pack(fill=tk.X, pady=5)
        tk.Label(r_frame, text="R:").pack(side=tk.LEFT)
        self.r_scale = tk.Scale(r_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.r_var, command=self.on_rgb_change)
        self.r_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.r_entry = tk.Entry(r_frame, textvariable=self.r_var, width=8)
        self.r_entry.pack(side=tk.RIGHT)
        self.r_entry.bind("<Return>", self.on_rgb_entry_change)

        # G control
        self.g_var = tk.IntVar()
        g_frame = tk.Frame(self.rgb_frame)
        g_frame.pack(fill=tk.X, pady=5)
        tk.Label(g_frame, text="G:").pack(side=tk.LEFT)
        self.g_scale = tk.Scale(g_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.g_var, command=self.on_rgb_change)
        self.g_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.g_entry = tk.Entry(g_frame, textvariable=self.g_var, width=8)
        self.g_entry.pack(side=tk.RIGHT)
        self.g_entry.bind("<Return>", self.on_rgb_entry_change)

        # B control
        self.b_var = tk.IntVar()
        b_frame = tk.Frame(self.rgb_frame)
        b_frame.pack(fill=tk.X, pady=5)
        tk.Label(b_frame, text="B:").pack(side=tk.LEFT)
        self.b_scale = tk.Scale(b_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.b_var, command=self.on_rgb_change)
        self.b_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.b_entry = tk.Entry(b_frame, textvariable=self.b_var, width=8)
        self.b_entry.pack(side=tk.RIGHT)
        self.b_entry.bind("<Return>", self.on_rgb_entry_change)

    def create_hsv_controls(self):
        tk.Label(self.hsv_frame, text="HSV Controls").pack()
        
        # H control
        self.h_var = tk.DoubleVar()
        h_frame = tk.Frame(self.hsv_frame)
        h_frame.pack(fill=tk.X, pady=5)
        tk.Label(h_frame, text="H:").pack(side=tk.LEFT)
        self.h_scale = tk.Scale(h_frame, from_=0, to=self.h_max, orient=tk.HORIZONTAL, variable=self.h_var, command=self.on_hsv_change)
        self.h_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.h_entry = tk.Entry(h_frame, textvariable=self.h_var, width=8)
        self.h_entry.pack(side=tk.RIGHT)
        self.h_entry.bind("<Return>", self.on_hsv_entry_change)

        # H max control
        self.h_max_var = tk.DoubleVar(value=self.h_max)
        h_max_entry = tk.Entry(h_frame, textvariable=self.h_max_var, width=8)
        h_max_entry.pack(side=tk.RIGHT)
        h_max_entry.bind("<Return>", self.on_h_max_change)

        # S control
        self.s_var = tk.DoubleVar()
        s_frame = tk.Frame(self.hsv_frame)
        s_frame.pack(fill=tk.X, pady=5)
        tk.Label(s_frame, text="S:").pack(side=tk.LEFT)
        self.s_scale = tk.Scale(s_frame, from_=0, to=self.s_max, orient=tk.HORIZONTAL, variable=self.s_var, command=self.on_hsv_change)
        self.s_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.s_entry = tk.Entry(s_frame, textvariable=self.s_var, width=8)
        self.s_entry.pack(side=tk.RIGHT)
        self.s_entry.bind("<Return>", self.on_hsv_entry_change)

        # S max control
        self.s_max_var = tk.DoubleVar(value=self.s_max)
        s_max_entry = tk.Entry(s_frame, textvariable=self.s_max_var, width=8)
        s_max_entry.pack(side=tk.RIGHT)
        s_max_entry.bind("<Return>", self.on_s_max_change)

        # V control
        self.v_var = tk.DoubleVar()
        v_frame = tk.Frame(self.hsv_frame)
        v_frame.pack(fill=tk.X, pady=5)
        tk.Label(v_frame, text="V:").pack(side=tk.LEFT)
        self.v_scale = tk.Scale(v_frame, from_=0, to=self.v_max, orient=tk.HORIZONTAL, variable=self.v_var, command=self.on_hsv_change)
        self.v_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.v_entry = tk.Entry(v_frame, textvariable=self.v_var, width=8)
        self.v_entry.pack(side=tk.RIGHT)
        self.v_entry.bind("<Return>", self.on_hsv_entry_change)

        # V max control
        self.v_max_var = tk.DoubleVar(value=self.v_max)
        v_max_entry = tk.Entry(v_frame, textvariable=self.v_max_var, width=8)
        v_max_entry.pack(side=tk.RIGHT)
        v_max_entry.bind("<Return>", self.on_v_max_change)

    def on_rgb_change(self, event=None):
        # Convert RGB to HSV and update the color preview and other controls
        r, g, b = self.r_var.get(), self.g_var.get(), self.b_var.get()
        self.hsv = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        self.update_ui_from_hsv()

    def on_rgb_entry_change(self, event=None):
        try:
            r = int(self.r_entry.get())
            g = int(self.g_entry.get())
            b = int(self.b_entry.get())
            self.r_var.set(r)
            self.g_var.set(g)
            self.b_var.set(b)
            self.on_rgb_change()
        except ValueError:
            pass

    def on_hsv_change(self, event=None):
        # Update HSV values from sliders
        h = self.h_var.get() / self.h_max
        s = self.s_var.get() / self.s_max
        v = self.v_var.get() / self.v_max
        self.hsv = (h, s, v)
        self.update_ui_from_hsv()

    def on_hsv_entry_change(self, event=None):
        try:
            h = float(self.h_entry.get())
            s = float(self.s_entry.get())
            v = float(self.v_entry.get())
            self.h_var.set(h)
            self.s_var.set(s)
            self.v_var.set(v)
            self.on_hsv_change()
        except ValueError:
            pass

    def on_h_max_change(self, event=None):
        try:
            self.h_max = float(self.h_max_var.get())
            self.h_scale.config(to=self.h_max)
            if self.h_max < 100:
                self.h_scale.config(resolution=self.h_max / 100)
            self.update_ui_from_hsv()
        except ValueError:
            pass

    def on_s_max_change(self, event=None):
        try:
            self.s_max = float(self.s_max_var.get())
            self.s_scale.config(to=self.s_max)
            if self.s_max < 100:
                self.s_scale.config(resolution=self.s_max / 100)
            self.update_ui_from_hsv()
        except ValueError:
            pass

    def on_v_max_change(self, event=None):
        try:
            self.v_max = float(self.v_max_var.get())
            self.v_scale.config(to=self.v_max)
            if self.v_max < 100:
                self.v_scale.config(resolution=self.v_max / 100)
            self.update_ui_from_hsv()
        except ValueError:
            pass

    def on_hex_input(self, event=None):
        hex_color = self.hex_input.get().strip("#")
        if len(hex_color) == 6:
            try:
                r = int(hex_color[:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:], 16)
                self.r_var.set(r)
                self.g_var.set(g)
                self.b_var.set(b)
                self.on_rgb_change()
            except ValueError:
                pass

    def hsv_to_hex(self, hsv):
        r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(*hsv)]
        return f"#{r:02x}{g:02x}{b:02x}"

    def update_ui_from_hsv(self):
        # Update preview
        self.preview_frame.config(bg=self.hsv_to_hex(self.hsv))
        
        # Update RGB controls
        r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(*self.hsv)]
        self.r_var.set(r)
        self.g_var.set(g)
        self.b_var.set(b)

        # Update HSV controls
        h, s, v = self.hsv
        self.h_var.set(h * self.h_max)
        self.s_var.set(s * self.s_max)
        self.v_var.set(v * self.v_max)

        # Update hex input
        self.hex_input.delete(0, tk.END)
        self.hex_input.insert(0, self.hsv_to_hex(self.hsv))

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorAdjusterApp(root)
    root.mainloop()
