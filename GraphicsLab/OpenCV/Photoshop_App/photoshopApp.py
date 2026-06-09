import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Scale, Button, Label, Frame, colorchooser, simpledialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class WelcomeScreen:
    """Welcome screen with modern design"""
    def __init__(self, root, start_callback):
        self.root = root
        self.start_callback = start_callback
        
        # Configure window
        self.root.title("Professional Photo Editor")
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create gradient background
        self.canvas = tk.Canvas(root, width=window_width, height=window_height, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create gradient effect
        for i in range(window_height):
            color_value = int(26 + (i / window_height) * 80)
            color = f'#{color_value:02x}{color_value + 30:02x}{color_value + 60:02x}'
            self.canvas.create_line(0, i, window_width, i, fill=color)
        
        # Title
        self.canvas.create_text(400, 180, text="Professional Photo Editor", 
                               font=('Arial', 36, 'bold'), fill='white')
        
        # Subtitle
        self.canvas.create_text(400, 230, text="OpenCV Image Processing Studio", 
                               font=('Arial', 16), fill='#b8c5d6')
        
        # Features text
        features = "✓ Advanced Filters  ✓ Face Detection  ✓ Drawing Tools  ✓ Image Merge"
        self.canvas.create_text(400, 280, text=features, 
                               font=('Arial', 12), fill='#8fa3b8')
        
        # Start button with modern style
        btn_frame = Frame(root, bg='#4a69bd', relief=tk.FLAT, bd=0)
        btn_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER, width=200, height=60)
        
        start_btn = Button(btn_frame, text="START EDITING", command=self.start_app,
                          bg='#4a69bd', fg='white', font=('Arial', 14, 'bold'),
                          relief=tk.FLAT, bd=0, cursor='hand2',
                          activebackground='#3c5aa6', activeforeground='white')
        start_btn.pack(fill=tk.BOTH, expand=True)
        
        # Hover effects
        start_btn.bind('<Enter>', lambda e: start_btn.config(bg='#5a7dd6'))
        start_btn.bind('<Leave>', lambda e: start_btn.config(bg='#4a69bd'))
        
        # Credits
        self.canvas.create_text(400, 550, text="Powered by OpenCV & Python", 
                               font=('Arial', 10), fill='#6c7a89')
    
    def start_app(self):
        self.canvas.destroy()
        self.start_callback()


class ProfessionalPhotoEditor:
    def __init__(self, root):
        """Initialize the Professional Photo Editor"""
        self.root = root
        self.root.title("Professional Photo Editor - OpenCV Studio")
        self.root.state('zoomed')  # Maximize window
        
        # Image variables
        self.base_image = None
        self.current_image = None
        self.display_image = None
        self.second_image = None  # For image merging
        self.history = []
        self.history_limit = 15
        
        # Drawing variables
        self.drawing_mode = None
        self.start_point = None
        self.drawing_color = (255, 100, 100)
        self.roi_selected = None
        
        # Load Haar Cascade for face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        self.create_modern_ui()
        
        self.root.bind('<Configure>', lambda e: self.display_on_canvas() if self.current_image is not None else None)
    
    def save_state(self):
        """Save current state to history"""
        if self.base_image is not None:
            if not self.history or not np.array_equal(self.base_image, self.history[-1]):
                if len(self.history) >= self.history_limit:
                    self.history.pop(0)
                self.history.append(self.base_image.copy())
    
    def undo_step(self):
        """Undo to previous state"""
        if len(self.history) > 1:
            self.history.pop()
            self.base_image = self.history[-1].copy()
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Undo successful")
            self.reset_sliders()
        else:
            self.update_status("No more undo steps available")
    
    def reset_sliders(self):
        """Reset all adjustment sliders"""
        if hasattr(self, 'brightness_slider'): self.brightness_slider.set(0)
        if hasattr(self, 'contrast_slider'): self.contrast_slider.set(1.0)
        if hasattr(self, 'blur_slider'): self.blur_slider.set(0)
        if hasattr(self, 'rotation_slider'): self.rotation_slider.set(0)
    
    def create_modern_ui(self):
        """Create modern UI with beautiful design"""
        
        # Main container with gradient background
        main_frame = Frame(self.root, bg='#f0f3f7')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top toolbar with gradient
        top_toolbar = Frame(main_frame, bg='#4a69bd', height=60)
        top_toolbar.pack(side=tk.TOP, fill=tk.X)
        top_toolbar.pack_propagate(False)
        
        title_label = Label(top_toolbar, text="Professional Photo Editor", 
                           font=('Arial', 18, 'bold'), bg='#4a69bd', fg='white')
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Left sidebar container (fixed), inside it a scrollable area
        sidebar_container = Frame(main_frame, bg='white', width=80, relief=tk.FLAT, bd=1)
        sidebar_container.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 5), pady=10)
        sidebar_container.pack_propagate(False)

        # Canvas + Scrollbar for scrollable sidebar
        sidebar_canvas = tk.Canvas(sidebar_container, bg='white', highlightthickness=0)
        sidebar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sidebar_scrollbar = tk.Scrollbar(sidebar_container, orient=tk.VERTICAL,
                                  command=sidebar_canvas.yview)
        sidebar_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)

        # Real sidebar frame INSIDE the canvas
        left_sidebar = Frame(sidebar_canvas, bg='white')
        sidebar_canvas.create_window((0, 0), window=left_sidebar, anchor='nw')

        # Update scrollregion when content changes
        def _on_sidebar_configure(event):
            sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))

        left_sidebar.bind("<Configure>", _on_sidebar_configure)

        # Optional: scroll with mouse wheel (Windows)
        def _on_mousewheel(event):
            sidebar_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        sidebar_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        
        # Button style
        btn_config = {
            'bg': 'white',
            'fg': '#4a69bd',
            'activebackground': '#e8f0fe',
            'activeforeground': '#3c5aa6',
            'relief': tk.FLAT,
            'bd': 0,
            'cursor': 'hand2',
            'font': ('Arial', 20),
            'width': 3,
            'height': 2
        }
        
        # File operations
        Label(left_sidebar, text="FILE", bg='white', fg='#6c7a89', font=('Arial', 8, 'bold')).pack(pady=(10, 5))
        
        self.create_tool_button(left_sidebar, "📁", self.load_image, "Load Image", btn_config)
        self.create_tool_button(left_sidebar, "💾", self.save_image, "Save Image", btn_config)
        self.create_tool_button(left_sidebar, "🖼️", self.load_second_image, "Load 2nd Image", btn_config)
        
        self.create_separator(left_sidebar)
        
        # History
        Label(left_sidebar, text="EDIT", bg='white', fg='#6c7a89', font=('Arial', 8, 'bold')).pack(pady=(5, 5))
        
        self.create_tool_button(left_sidebar, "↩️", self.undo_step, "Undo", btn_config)
        self.create_tool_button(left_sidebar, "⟲", self.reset_image, "Reset", btn_config)
        
        self.create_separator(left_sidebar)
        
        # Drawing tools
        Label(left_sidebar, text="DRAW", bg='white', fg='#6c7a89', font=('Arial', 8, 'bold')).pack(pady=(5, 5))
        
        self.create_tool_button(left_sidebar, "▭", lambda: self.set_drawing_mode('rectangle'), "Rectangle", btn_config)
        self.create_tool_button(left_sidebar, "◯", lambda: self.set_drawing_mode('circle'), "Circle", btn_config)
        self.create_tool_button(left_sidebar, "⬭", lambda: self.set_drawing_mode('ellipse'), "Ellipse", btn_config)
        self.create_tool_button(left_sidebar, "━", lambda: self.set_drawing_mode('line'), "Line", btn_config)
        self.create_tool_button(left_sidebar, "✏️", lambda: self.set_drawing_mode('polygon'), "Polygon", btn_config)
        self.create_tool_button(left_sidebar, "T", lambda: self.set_drawing_mode('text'), "Text", btn_config)
        self.create_tool_button(left_sidebar, "🎨", self.choose_color, "Color", btn_config)
        
        self.create_separator(left_sidebar)
        
        # Filters
        Label(left_sidebar, text="FILTERS", bg='white', fg='#6c7a89', font=('Arial', 8, 'bold')).pack(pady=(5, 5))
        
        self.create_tool_button(left_sidebar, "⚫", self.apply_grayscale, "Grayscale", btn_config)
        self.create_tool_button(left_sidebar, "⚡", self.apply_edge_detection, "Edges", btn_config)
        self.create_tool_button(left_sidebar, "✨", self.apply_sharpen, "Sharpen", btn_config)
        
        self.create_separator(left_sidebar)
        
        # Transform
        Label(left_sidebar, text="TRANSFORM", bg='white', fg='#6c7a89', font=('Arial', 8, 'bold')).pack(pady=(5, 5))
        
        self.create_tool_button(left_sidebar, "⇄", self.flip_horizontal, "Flip H", btn_config)
        self.create_tool_button(left_sidebar, "⇅", self.flip_vertical, "Flip V", btn_config)
        self.create_tool_button(left_sidebar, "↻", self.rotate_90, "Rotate 90°", btn_config)
        
        self.create_separator(left_sidebar)
        
        # Advanced features
        Label(left_sidebar, text="ADVANCED", bg='white', fg='#6c7a89', font=('Arial', 8, 'bold')).pack(pady=(5, 5))
        
        self.create_tool_button(left_sidebar, "😊", self.detect_faces, "Detect Faces", btn_config)
        self.create_tool_button(left_sidebar, "📍", self.detect_corners, "Find Corners", btn_config)
        self.create_tool_button(left_sidebar, "✂️", self.select_roi, "Select ROI", btn_config)
        self.create_tool_button(left_sidebar, "🔗", self.merge_images_menu, "Merge Images", btn_config)
        self.create_tool_button(left_sidebar, "🎭", self.remove_color_channel, "Remove Channel", btn_config)
        self.create_tool_button(left_sidebar, "📹", self.detect_faces_camera, "Face Camera", btn_config)

        
        # Right panel for adjustments
        right_panel = Frame(main_frame, bg='white', width=300, relief=tk.FLAT, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 10), pady=10)
        right_panel.pack_propagate(False)
        
        # Adjustments header
        adj_header = Label(right_panel, text="ADJUSTMENTS", bg='white', fg='#4a69bd', 
                          font=('Arial', 12, 'bold'))
        adj_header.pack(pady=(15, 10))
        
        # Brightness
        self.create_modern_slider(right_panel, "☀️ Brightness", -100, 100, 0, 'brightness_slider')
        
        # Contrast
        self.create_modern_slider(right_panel, "🔆 Contrast", 0.5, 3.0, 1.0, 'contrast_slider', resolution=0.1)
        
        # Gaussian Blur
        self.create_modern_slider(right_panel, "🌫️ Gaussian Blur", 0, 50, 0, 'blur_slider')
        
        # Median Blur
        self.create_modern_slider(right_panel, "💫 Median Blur", 0, 25, 0, 'median_blur_slider')
        
        # Rotation angle
        self.create_modern_slider(right_panel, "🔄 Rotation Angle", -180, 180, 0, 'rotation_slider')
        
        # Shape thickness
        self.create_modern_slider(right_panel, "✏️ Line Thickness", 1, 20, 3, 'thickness_slider')
        
        # Apply button
        apply_btn = Button(right_panel, text="Apply Adjustments", command=self.apply_filters,
                          bg='#4a69bd', fg='white', font=('Arial', 11, 'bold'),
                          relief=tk.FLAT, cursor='hand2', bd=0, pady=10)
        apply_btn.pack(fill=tk.X, padx=20, pady=10)
        
        # Status label
        self.status_label = Label(right_panel, text="Ready to edit", bg='white', 
                                 fg='#6c7a89', font=('Arial', 9), wraplength=260, justify=tk.LEFT)
        self.status_label.pack(pady=20, padx=10)
        
        # Canvas for image display
        canvas_frame = Frame(main_frame, bg='#e8ecf0', relief=tk.FLAT)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg='#ffffff', highlightthickness=1, 
                               highlightbackground='#c8d0d8')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind mouse events
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_canvas_release)
    
    def create_tool_button(self, parent, icon, command, tooltip, config):
        """Create a modern tool button with hover effect"""
        btn = Button(parent, text=icon, command=command, **config)
        btn.pack(pady=2, padx=5, fill=tk.X)
        
        # Hover effects
        def on_enter(e):
            btn.config(bg='#e8f0fe')
        def on_leave(e):
            btn.config(bg='white')
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def create_separator(self, parent):
        """Create a visual separator"""
        sep = Frame(parent, bg='#e0e0e0', height=1)
        sep.pack(fill=tk.X, padx=10, pady=10)
    
    def create_modern_slider(self, parent, label_text, from_, to, default, var_name, resolution=1):
        """Create a modern slider with label and value display"""
        container = Frame(parent, bg='white')
        container.pack(fill=tk.X, padx=20, pady=10)
        
        label = Label(container, text=label_text, bg='white', fg='#2c3e50', 
                     font=('Arial', 10, 'bold'))
        label.pack(anchor=tk.W)
        
        value_label = Label(container, text=str(default), bg='white', fg='#4a69bd', 
                           font=('Arial', 9))
        value_label.pack(anchor=tk.E)
        
        slider = Scale(container, from_=from_, to=to, orient=tk.HORIZONTAL,
                      resolution=resolution, command=lambda v: value_label.config(text=f"{float(v):.1f}"),
                      bg='white', fg='#4a69bd', highlightthickness=0, 
                      troughcolor='#e8f0fe', activebackground='#4a69bd',
                      showvalue=False, length=240, sliderlength=20)
        slider.set(default)
        slider.pack(fill=tk.X)
        
        setattr(self, var_name, slider)
    
    def update_status(self, message):
        """Update status message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def set_drawing_mode(self, mode):
        """Set drawing mode"""
        self.drawing_mode = mode
        self.update_status(f"Drawing mode: {mode}. Click and drag on image.")
    
    def choose_color(self):
        """Choose drawing color"""
        color = colorchooser.askcolor(title="Choose Color")
        if color[0]:
            self.drawing_color = tuple(int(c) for c in color[0])
            self.update_status(f"Color selected: RGB{self.drawing_color}")
    
    def on_canvas_click(self, event):
        """Handle canvas click"""
        if self.current_image is None or self.drawing_mode is None:
            return
        
        if self.drawing_mode == 'polygon':
            # For polygon, collect multiple points
            if not hasattr(self, 'polygon_points'):
                self.polygon_points = []
            
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            img_height, img_width = self.current_image.shape[:2]
            
            scale = min(canvas_width / img_width, canvas_height / img_height, 1.0)
            scaled_width = int(img_width * scale)
            scaled_height = int(img_height * scale)
            offset_x = (canvas_width - scaled_width) // 2
            offset_y = (canvas_height - scaled_height) // 2
            
            img_x = int((event.x - offset_x) / scale)
            img_y = int((event.y - offset_y) / scale)
            img_x = np.clip(img_x, 0, img_width - 1)
            img_y = np.clip(img_y, 0, img_height - 1)
            
            self.polygon_points.append([img_x, img_y])
            self.update_status(f"Polygon: {len(self.polygon_points)} points. Right-click to finish.")
        else:
            self.start_point = (event.x, event.y)
    
    def on_canvas_drag(self, event):
        """Handle canvas drag"""
        pass
    
    def on_canvas_release(self, event):
        """Handle canvas release - draw shape"""
        if self.current_image is None or self.drawing_mode is None or self.start_point is None:
            return
        
        if self.drawing_mode == 'polygon':
            return  # Handled separately
        
        self.save_state()
        end_point = (event.x, event.y)
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_height, img_width = self.current_image.shape[:2]
        
        scale = min(canvas_width / img_width, canvas_height / img_height, 1.0)
        scaled_width = int(img_width * scale)
        scaled_height = int(img_height * scale)
        offset_x = (canvas_width - scaled_width) // 2
        offset_y = (canvas_height - scaled_height) // 2
        
        img_x1 = int((self.start_point[0] - offset_x) / scale)
        img_y1 = int((self.start_point[1] - offset_y) / scale)
        img_x2 = int((end_point[0] - offset_x) / scale)
        img_y2 = int((end_point[1] - offset_y) / scale)
        
        img_x1 = np.clip(img_x1, 0, img_width - 1)
        img_y1 = np.clip(img_y1, 0, img_height - 1)
        img_x2 = np.clip(img_x2, 0, img_width - 1)
        img_y2 = np.clip(img_y2, 0, img_height - 1)
        
        thickness = self.thickness_slider.get()
        
        if self.drawing_mode == 'rectangle':
            cv2.rectangle(self.current_image, (img_x1, img_y1), (img_x2, img_y2), 
                         self.drawing_color, thickness)
        elif self.drawing_mode == 'circle':
            center = ((img_x1 + img_x2) // 2, (img_y1 + img_y2) // 2)
            radius = int(np.sqrt((img_x2 - img_x1)**2 + (img_y2 - img_y1)**2) / 2)
            cv2.circle(self.current_image, center, radius, self.drawing_color, thickness)
        elif self.drawing_mode == 'ellipse':
            center = ((img_x1 + img_x2) // 2, (img_y1 + img_y2) // 2)
            axes = (abs(img_x2 - img_x1) // 2, abs(img_y2 - img_y1) // 2)
            cv2.ellipse(self.current_image, center, axes, 0, 0, 360, self.drawing_color, thickness)
        elif self.drawing_mode == 'line':
            cv2.line(self.current_image, (img_x1, img_y1), (img_x2, img_y2), 
                    self.drawing_color, thickness)
        elif self.drawing_mode == 'text':
            text = simpledialog.askstring("Input", "Enter text:")
            if text:
                cv2.putText(self.current_image, text, (img_x1, img_y1), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, self.drawing_color, thickness)
        
        self.base_image = self.current_image.copy()
        self.display_on_canvas()
        self.start_point = None
        self.update_status("Shape drawn successfully")
    
    def load_image(self):
        """Load an image"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
        if file_path:
            image = cv2.imread(file_path)
            if image is None:
                self.update_status("Error: Could not load image")
                return
            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.base_image = image.copy()
            self.current_image = image.copy()
            self.history = []
            self.save_state()
            self.reset_sliders()
            self.display_on_canvas()
            self.update_status("Image loaded successfully")
            self.drawing_mode = None
    
    def load_second_image(self):
        """Load second image for merging"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
        if file_path:
            image = cv2.imread(file_path)
            if image is None:
                self.update_status("Error: Could not load second image")
                return
            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.second_image = image
            self.update_status("Second image loaded - use Merge Images button")
    
    def save_image(self):
        """Save the current image"""
        if self.current_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if file_path:
                image_to_save = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(file_path, image_to_save)
                self.update_status("Image saved successfully")
        else:
            self.update_status("No image to save")
    
    def reset_image(self):
        """Reset to original image"""
        if self.base_image is not None:
            original_state = self.history[0].copy() if self.history else self.base_image.copy()
            self.base_image = original_state
            self.current_image = original_state.copy()
            self.history = [original_state]
            self.reset_sliders()
            self.display_on_canvas()
            self.update_status("Image reset to original")
            self.drawing_mode = None
        else:
            self.update_status("No image loaded")
    
    def apply_filters(self):
        """Apply all adjustments"""
        if self.base_image is None:
            return
        
        image = self.base_image.copy().astype(np.float32)
        
        # Contrast
        contrast = self.contrast_slider.get()
        image = image * contrast
        
        # Brightness
        brightness = self.brightness_slider.get()
        image = image + brightness
        
        image = np.clip(image, 0, 255).astype(np.uint8)
        
        # Gaussian Blur
        blur_amount = self.blur_slider.get()
        if blur_amount > 0:
            kernel_size = blur_amount * 2 + 1
            image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        
        # Median Blur
        median_blur = self.median_blur_slider.get()
        if median_blur > 0:
            kernel = median_blur * 2 + 1
            image = cv2.medianBlur(image, kernel)
        
        # Rotation
        angle = self.rotation_slider.get()
        if angle != 0:
            h, w = image.shape[:2]
            center = (w // 2, h // 2)
            matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            image = cv2.warpAffine(image, matrix, (w, h))
        
        self.current_image = image
        self.display_on_canvas()
        self.update_status("Adjustments applied")
    
    def apply_grayscale(self):
        """Convert to grayscale"""
        if self.current_image is not None:
            self.save_state()
            gray = cv2.cvtColor(self.base_image, cv2.COLOR_RGB2GRAY)
            self.base_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Grayscale applied")
    
    def apply_edge_detection(self):
        """Apply Canny edge detection"""
        if self.current_image is not None:
            self.save_state()
            gray = cv2.cvtColor(self.base_image, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            self.base_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Edge detection applied")
    
    def apply_sharpen(self):
        """Apply sharpening filter"""
        if self.current_image is not None:
            self.save_state()
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            self.base_image = cv2.filter2D(self.base_image, -1, kernel)
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Sharpening applied")
    
    def flip_horizontal(self):
        """Flip horizontally"""
        if self.current_image is not None:
            self.save_state()
            self.base_image = cv2.flip(self.base_image, 1)
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Flipped horizontally")
    
    def flip_vertical(self):
        """Flip vertically"""
        if self.current_image is not None:
            self.save_state()
            self.base_image = cv2.flip(self.base_image, 0)
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Flipped vertically")
    
    def rotate_90(self):
        """Rotate 90 degrees"""
        if self.current_image is not None:
            self.save_state()
            self.base_image = cv2.rotate(self.base_image, cv2.ROTATE_90_CLOCKWISE)
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Rotated 90° clockwise")
    
    def detect_faces(self):
        """Detect faces using Haar Cascade"""
        if self.current_image is not None:
            self.save_state()
            gray = cv2.cvtColor(self.base_image, cv2.COLOR_RGB2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            result = self.base_image.copy()
            for (x, y, w, h) in faces:
                cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(result, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.9, (0, 255, 0), 2)
            
            self.base_image = result
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status(f"Detected {len(faces)} face(s)")
        else:
            self.update_status("No image loaded")
            
    def detect_faces_camera(self):
        """Detect faces from webcam video (separate OpenCV window)"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.update_status("Cannot open camera")
            return

        self.update_status("Camera running - press 'q' to quit")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Face", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow("Face Detection - Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyWindow("Face Detection - Camera")
        self.update_status("Camera face detection finished")

    
    def detect_corners(self):
        """Detect corners using goodFeaturesToTrack"""
        if self.current_image is not None:
            self.save_state()
            gray = cv2.cvtColor(self.base_image, cv2.COLOR_RGB2GRAY)
            corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
            
            result = self.base_image.copy()
            if corners is not None:
                corners = np.int0(corners)
                for corner in corners:
                    x, y = corner.ravel()
                    cv2.circle(result, (x, y), 5, (255, 0, 0), -1)
            
            self.base_image = result
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status(f"Detected {len(corners) if corners is not None else 0} corners")
        else:
            self.update_status("No image loaded")
    
    def select_roi(self):
        """Select Region of Interest"""
        if self.current_image is not None:
            self.update_status("Select ROI in the popup window (press SPACE or ENTER to confirm, ESC to cancel)")
            
            # Create a temporary window for ROI selection
            temp_image = cv2.cvtColor(self.base_image, cv2.COLOR_RGB2BGR)
            roi = cv2.selectROI("Select ROI", temp_image, fromCenter=False, showCrosshair=True)
            cv2.destroyWindow("Select ROI")
            
            if roi[2] > 0 and roi[3] > 0:  # Valid ROI
                x, y, w, h = roi
                self.save_state()
                
                # Crop the image to ROI
                cropped = self.base_image[y:y+h, x:x+w].copy()
                
                self.base_image = cropped
                self.current_image = self.base_image.copy()
                self.display_on_canvas()
                self.update_status(f"ROI selected: {w}x{h} pixels")
            else:
                self.update_status("ROI selection cancelled")
        else:
            self.update_status("No image loaded")
    
    def merge_images_menu(self):
        """Show menu for different merge options"""
        if self.current_image is None:
            self.update_status("Load first image first")
            return
        
        if self.second_image is None:
            self.update_status("Load second image first (🖼️ button)")
            return
        
        # Create menu dialog
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Merge Images")
        menu_window.geometry("300x400")
        menu_window.configure(bg='white')
        menu_window.transient(self.root)
        menu_window.grab_set()
        
        Label(menu_window, text="Choose Merge Method", font=('Arial', 14, 'bold'), 
              bg='white', fg='#4a69bd').pack(pady=20)
        
        btn_style = {
            'bg': '#4a69bd',
            'fg': 'white',
            'font': ('Arial', 11),
            'relief': tk.FLAT,
            'cursor': 'hand2',
            'pady': 10
        }
        
        Button(menu_window, text="Simple Add (img1 + img2)", 
               command=lambda: [self.merge_images('add'), menu_window.destroy()],
               **btn_style).pack(fill=tk.X, padx=30, pady=5)
        
        Button(menu_window, text="CV2 Add", 
               command=lambda: [self.merge_images('cv2_add'), menu_window.destroy()],
               **btn_style).pack(fill=tk.X, padx=30, pady=5)
        
        Button(menu_window, text="Weighted Blend (50/50)", 
               command=lambda: [self.merge_images('weighted'), menu_window.destroy()],
               **btn_style).pack(fill=tk.X, padx=30, pady=5)
        
        Button(menu_window, text="Bitwise AND", 
               command=lambda: [self.merge_images('and'), menu_window.destroy()],
               **btn_style).pack(fill=tk.X, padx=30, pady=5)
        
        Button(menu_window, text="Bitwise OR", 
               command=lambda: [self.merge_images('or'), menu_window.destroy()],
               **btn_style).pack(fill=tk.X, padx=30, pady=5)
        
        Button(menu_window, text="Bitwise XOR", 
               command=lambda: [self.merge_images('xor'), menu_window.destroy()],
               **btn_style).pack(fill=tk.X, padx=30, pady=5)
        
        Button(menu_window, text="Cancel", command=menu_window.destroy,
               bg='#e74c3c', fg='white', font=('Arial', 11),
               relief=tk.FLAT, cursor='hand2', pady=10).pack(fill=tk.X, padx=30, pady=20)
    
    def merge_images(self, method):
        """Merge two images using different methods"""
        if self.base_image is None or self.second_image is None:
            self.update_status("Need two images to merge")
            return
        
        self.save_state()
        
        # Resize second image to match first image
        h, w = self.base_image.shape[:2]
        img2_resized = cv2.resize(self.second_image, (w, h))
        
        if method == 'add':
            result = self.base_image + img2_resized
        elif method == 'cv2_add':
            result = cv2.add(self.base_image, img2_resized)
        elif method == 'weighted':
            result = cv2.addWeighted(self.base_image, 0.5, img2_resized, 0.5, 0)
        elif method == 'and':
            result = cv2.bitwise_and(self.base_image, img2_resized)
        elif method == 'or':
            result = cv2.bitwise_or(self.base_image, img2_resized)
        elif method == 'xor':
            result = cv2.bitwise_xor(self.base_image, img2_resized)
        else:
            result = self.base_image
        
        self.base_image = result
        self.current_image = self.base_image.copy()
        self.display_on_canvas()
        self.update_status(f"Images merged using {method}")
    
    def remove_color_channel(self):
        """Remove a color channel"""
        if self.current_image is None:
            self.update_status("No image loaded")
            return
        
        # Create menu dialog
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Remove Color Channel")
        menu_window.geometry("300x250")
        menu_window.configure(bg='white')
        menu_window.transient(self.root)
        menu_window.grab_set()
        
        Label(menu_window, text="Choose Channel to Remove", font=('Arial', 14, 'bold'), 
              bg='white', fg='#4a69bd').pack(pady=20)
        
        btn_style = {
            'bg': '#4a69bd',
            'fg': 'white',
            'font': ('Arial', 11),
            'relief': tk.FLAT,
            'cursor': 'hand2',
            'pady': 10
        }
        
        Button(menu_window, text="Remove Red Channel", 
               command=lambda: [self.apply_remove_channel(0), menu_window.destroy()],
               **btn_style).pack(fill=tk.X, padx=30, pady=5)
        
        Button(menu_window, text="Remove Green Channel", 
               command=lambda: [self.apply_remove_channel(1), menu_window.destroy()],
               **btn_style).pack(fill=tk.X, padx=30, pady=5)
        
        Button(menu_window, text="Remove Blue Channel", 
               command=lambda: [self.apply_remove_channel(2), menu_window.destroy()],
               **btn_style).pack(fill=tk.X, padx=30, pady=5)
        
        Button(menu_window, text="Cancel", command=menu_window.destroy,
               bg='#e74c3c', fg='white', font=('Arial', 11),
               relief=tk.FLAT, cursor='hand2', pady=10).pack(fill=tk.X, padx=30, pady=20)
    
    def apply_remove_channel(self, channel):
        """Remove specific color channel (0=Red, 1=Green, 2=Blue in RGB)"""
        self.save_state()
        result = self.base_image.copy()
        result[:, :, channel] = 0
        self.base_image = result
        self.current_image = self.base_image.copy()
        self.display_on_canvas()
        
        channel_names = ['Red', 'Green', 'Blue']
        self.update_status(f"{channel_names[channel]} channel removed")
    
    def display_on_canvas(self):
        """Display image on canvas with proper scaling"""
        if self.current_image is None:
            return
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
        
        img_height, img_width = self.current_image.shape[:2]
        
        scale = min(canvas_width / img_width, canvas_height / img_height, 1.0)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        if new_width < img_width or new_height < img_height:
            display_img = cv2.resize(self.current_image, (new_width, new_height), 
                                    interpolation=cv2.INTER_AREA)
        else:
            display_img = self.current_image
        
        img_pil = Image.fromarray(display_img)
        self.display_image = ImageTk.PhotoImage(img_pil)
        
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, 
                                image=self.display_image, anchor=tk.CENTER)


def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    def start_editor():
        """Start the photo editor after welcome screen"""
        app = ProfessionalPhotoEditor(root)
    
    # Show welcome screen first
    welcome = WelcomeScreen(root, start_editor)
    
    root.mainloop()


if __name__ == "__main__":
    main()