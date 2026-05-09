import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Scale, Button, Label, Frame, colorchooser, simpledialog
from PIL import Image, ImageTk

class SimplePhotoshop:
    def __init__(self, root):
        """Initialize the Photoshop application"""
        self.root = root
        self.root.title("Photo Editor - OpenCV")
        self.root.configure(bg='#2b2b2b')
        
        # Renamed from original_image to base_image: the result of the last permanent edit/drawing
        self.base_image = None
        self.current_image = None
        self.display_image = None
        self.history = []
        self.history_limit = 10 
        self.drawing_mode = None 
        self.start_point = None
        self.drawing_color = (255, 0, 0)
        
        self.create_widgets()
        
        self.root.bind('<Configure>', lambda e: self.display_on_canvas() if self.current_image is not None else None)
        
    def save_state(self):
        """Saves the current base image state to the history stack."""
        if self.base_image is not None:
            if not self.history or not np.array_equal(self.base_image, self.history[-1]):
                if len(self.history) >= self.history_limit:
                    self.history.pop(0)
                self.history.append(self.base_image.copy())

    def undo_step(self):
        """Resets image to the previous step in history."""
        if len(self.history) > 1:
            self.history.pop()
            self.base_image = self.history[-1].copy()
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status(f"Undo successful. History: {len(self.history)} states left.")
            self.reset_adjustment_sliders()
        elif len(self.history) == 1:
            self.update_status("Cannot undo further (at original state).")
        else:
            self.update_status("No history available to undo.")

    def reset_adjustment_sliders(self):
        """Resets the brightness, contrast, and blur sliders."""
        if hasattr(self, 'brightness_slider'): self.brightness_slider.set(0)
        if hasattr(self, 'contrast_slider'): self.contrast_slider.set(1.0)
        if hasattr(self, 'blur_slider'): self.blur_slider.set(0)

    def create_widgets(self):
        """Create all GUI buttons, sliders, and canvas (maximized for code brevity)"""
        
        # Button styling dictionary for compactness
        btn_style = dict(bg='#3c3c3c', fg='white', activebackground='#5a5a5a', width=3, 
                         height=2, relief=tk.FLAT, bd=0, font=('Arial', 18))
        
        toolbar_frame = Frame(self.root, bg='#3c3c3c', width=60)
        toolbar_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # File Operations
        Button(toolbar_frame, text="📁", command=self.load_image, **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        Button(toolbar_frame, text="💾", command=self.save_image, **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        
        Label(toolbar_frame, text="─────", bg='#3c3c3c', fg='#666').pack(pady=5)
        
        # History & Reset Operations
        Button(toolbar_frame, text="↩", command=self.undo_step, **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        Button(toolbar_frame, text="⟲", command=self.reset_image, **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        
        Label(toolbar_frame, text="─────", bg='#3c3c3c', fg='#666').pack(pady=5)
        
        # Drawing tools
        Button(toolbar_frame, text="☐", command=lambda: self.set_drawing_mode('rectangle'), **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        Button(toolbar_frame, text="◯", command=lambda: self.set_drawing_mode('circle'), **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        Button(toolbar_frame, text="━", command=lambda: self.set_drawing_mode('line'), **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        Button(toolbar_frame, text="🖹", command=lambda: self.set_drawing_mode('text'), **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        Button(toolbar_frame, text="🎨", command=self.choose_color, **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        
        Label(toolbar_frame, text="─────", bg='#3c3c3c', fg='#666').pack(pady=5)
        
        # Filters and Adjustments
        Button(toolbar_frame, text="⚫", command=self.apply_grayscale, **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        Button(toolbar_frame, text="⚡", command=self.apply_edge_detection, **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        Button(toolbar_frame, text="✨", command=self.apply_sharpen, **btn_style).pack(pady=3, padx=5, fill=tk.X); 

        Label(toolbar_frame, text="─────", bg='#3c3c3c', fg='#666').pack(pady=5)
        
        # Transformation buttons
        Button(toolbar_frame, text="⇄", command=self.flip_horizontal, **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        Button(toolbar_frame, text="⇅", command=self.flip_vertical, **btn_style).pack(pady=3, padx=5, fill=tk.X); 
        Button(toolbar_frame, text="↻", command=self.rotate_90, **btn_style).pack(pady=3, padx=5, fill=tk.X); 

        # Right panel for controls
        control_frame = Frame(self.root, bg='#2b2b2b')
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        Label(control_frame, text="ADJUSTMENTS", bg='#2b2b2b', fg='white', font=('Arial', 10, 'bold')).pack(pady=(0, 10))
        
        # Brightness slider
        Label(control_frame, text="Brightness", bg='#2b2b2b', fg='white').pack();
        self.brightness_slider = Scale(control_frame, from_=-100, to=100, orient=tk.HORIZONTAL, command=self.apply_filters, bg='#3c3c3c', fg='white', highlightthickness=0, length=200);
        self.brightness_slider.set(0); self.brightness_slider.pack(pady=5);
        
        # Contrast slider
        Label(control_frame, text="Contrast", bg='#2b2b2b', fg='white').pack();
        self.contrast_slider = Scale(control_frame, from_=0.5, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.apply_filters, bg='#3c3c3c', fg='white', highlightthickness=0, length=200);
        self.contrast_slider.set(1.0); self.contrast_slider.pack(pady=5);
        
        # Blur slider
        Label(control_frame, text="Blur", bg='#2b2b2b', fg='white').pack();
        self.blur_slider = Scale(control_frame, from_=0, to=50, orient=tk.HORIZONTAL, command=self.apply_filters, bg='#3c3c3c', fg='white', highlightthickness=0, length=200);
        self.blur_slider.set(0); self.blur_slider.pack(pady=5);
        
        # Shape thickness slider
        Label(control_frame, text="Shape Thickness", bg='#2b2b2b', fg='white').pack(pady=(20, 0));
        self.thickness_slider = Scale(control_frame, from_=1, to=20, orient=tk.HORIZONTAL, bg='#3c3c3c', fg='white', highlightthickness=0, length=200);
        self.thickness_slider.set(3); self.thickness_slider.pack(pady=5);
        
        # Status label (only hover effect removed, message is still useful)
        self.status_label = Label(control_frame, text="Ready", bg='#2b2b2b', fg='#888', wraplength=180);
        self.status_label.pack(pady=20);
        
        # Canvas for image display
        self.canvas = tk.Canvas(self.root, bg='#1e1e1e', highlightthickness=0);
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10);
        
        # Bind mouse events for drawing
        self.canvas.bind('<Button-1>', self.on_canvas_click);
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag);
        self.canvas.bind('<ButtonRelease-1>', self.on_canvas_release);
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
    
    def set_drawing_mode(self, mode):
        """Set the current drawing mode"""
        self.drawing_mode = mode
        self.update_status(f"Drawing mode selected: {mode}. Click and drag on the image.")
    
    def choose_color(self):
        """Open color picker dialog"""
        color = colorchooser.askcolor(title="Choose shape color")
        if color[0]:
            self.drawing_color = tuple(int(c) for c in color[0])
            self.update_status(f"Color selected: RGB{self.drawing_color}")
    
    def on_canvas_click(self, event):
        """Handle mouse click on canvas"""
        if self.current_image is None or self.drawing_mode is None: return
        self.start_point = (event.x, event.y)
    
    def on_canvas_drag(self, event):
        """Handle mouse drag on canvas - placeholder for potential live preview"""
        pass
    
    def on_canvas_release(self, event):
        """Handle mouse release - draw the shape"""
        if self.current_image is None or self.drawing_mode is None or self.start_point is None: return
        
        self.save_state()
        end_point = (event.x, event.y)
        
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        img_height, img_width = self.current_image.shape[:2]
        
        scale_w, scale_h = canvas_width / img_width, canvas_height / img_height
        scale = min(scale_w, scale_h); scale = min(scale, 1.0);
            
        scaled_width, scaled_height = int(img_width * scale), int(img_height * scale)
        offset_x, offset_y = (canvas_width - scaled_width) // 2, (canvas_height - scaled_height) // 2
        
        if scale == 1.0 and (img_width < canvas_width or img_height < canvas_height):
            img_x1, img_y1 = int(self.start_point[0] - offset_x), int(self.start_point[1] - offset_y)
            img_x2, img_y2 = int(end_point[0] - offset_x), int(end_point[1] - offset_y)
        else:
            img_x1, img_y1 = int((self.start_point[0] - offset_x) / scale), int((self.start_point[1] - offset_y) / scale)
            img_x2, img_y2 = int((end_point[0] - offset_x) / scale), int((end_point[1] - offset_y) / scale)
        
        img_x1, img_y1 = np.clip(img_x1, 0, img_width - 1), np.clip(img_y1, 0, img_height - 1)
        img_x2, img_y2 = np.clip(img_x2, 0, img_width - 1), np.clip(img_y2, 0, img_height - 1)
        
        thickness = self.thickness_slider.get()
        
        if self.drawing_mode == 'rectangle':
            cv2.rectangle(self.current_image, (img_x1, img_y1), (img_x2, img_y2), self.drawing_color, thickness)
        elif self.drawing_mode == 'circle':
            center = ((img_x1 + img_x2) // 2, (img_y1 + img_y2) // 2)
            radius = int(np.sqrt((img_x2 - img_x1)**2 + (img_y2 - img_y1)**2) / 2)
            cv2.circle(self.current_image, center, radius, self.drawing_color, thickness)
        elif self.drawing_mode == 'line':
            cv2.line(self.current_image, (img_x1, img_y1), (img_x2, img_y2), self.drawing_color, thickness)
        elif self.drawing_mode == 'text':
            text = tk.simpledialog.askstring("Input", "Enter text:")
            if text:
                cv2.putText(self.current_image, text, (img_x1, img_y1), cv2.FONT_HERSHEY_SIMPLEX, 1, self.drawing_color, thickness)
        
        # CRITICAL FIX: The drawing becomes the new base for future slider adjustments
        self.base_image = self.current_image.copy()
        
        self.display_on_canvas()
        self.start_point = None
        
    def load_image(self):
        """Open file dialog to load an image"""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
        if file_path:
            image = cv2.imread(file_path)
            if image is None:
                self.update_status("Error: Could not load image file."); return

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.base_image = image.copy() # Set the base image
            self.current_image = image.copy()
            self.history = []; self.save_state(); 
            self.reset_adjustment_sliders()
            self.display_on_canvas()
            self.update_status("Image loaded successfully")
            self.drawing_mode = None
            
    def save_image(self):
        """Save the current edited image"""
        if self.current_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                image_to_save = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(file_path, image_to_save)
                self.update_status("Image saved successfully")
        else:
            self.update_status("No image to save")
                
    def reset_image(self):
        """Reset image to original state (first state in history)"""
        if self.base_image is not None:
            # Revert to the absolute first state in history (the original load)
            original_state = self.history[0].copy() if self.history else self.base_image.copy()
            
            self.base_image = original_state
            self.current_image = original_state.copy()
            self.history = [original_state] # Reset history to only contain the original
            
            self.reset_adjustment_sliders()
            self.display_on_canvas()
            self.update_status("Image reset to original")
            self.drawing_mode = None
        else:
            self.update_status("No image loaded")
            
    def apply_filters(self, event=None):
        """Apply brightness, contrast, and blur adjustments based on the base_image"""
        if self.base_image is None: return
        
        # CRITICAL FIX: Start filtering from the permanent base image (which contains drawings)
        image = self.base_image.copy().astype(np.float32)
        contrast = self.contrast_slider.get(); image = image * contrast
        brightness = self.brightness_slider.get(); image = image + brightness
        image = np.clip(image, 0, 255).astype(np.uint8)
        
        blur_amount = self.blur_slider.get()
        if blur_amount > 0:
            kernel_size = blur_amount * 2 + 1; image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        
        self.current_image = image
        self.display_on_canvas()
        
    def apply_grayscale(self):
        """Convert image to grayscale"""
        if self.current_image is not None:
            self.save_state()
            gray = cv2.cvtColor(self.base_image, cv2.COLOR_RGB2GRAY)
            self.base_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB) # Update base
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Grayscale applied")
        else:
            self.update_status("No image loaded")
            
    def apply_edge_detection(self):
        """Apply Canny edge detection"""
        if self.current_image is not None:
            self.save_state()
            gray = cv2.cvtColor(self.base_image, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            self.base_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB) # Update base
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Edge detection applied")
        else:
            self.update_status("No image loaded")
            
    def apply_sharpen(self):
        """Apply sharpening filter using a kernel"""
        if self.current_image is not None:
            self.save_state()
            kernel = np.array([[-1, -1, -1], [-1,  9, -1], [-1, -1, -1]])
            self.base_image = cv2.filter2D(self.base_image, -1, kernel) # Update base
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Sharpening applied")
        else:
            self.update_status("No image loaded")
            
    def flip_horizontal(self):
        """Flip image horizontally"""
        if self.current_image is not None:
            self.save_state()
            self.base_image = cv2.flip(self.base_image, 1) # Update base
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Flipped horizontally")
        else:
            self.update_status("No image loaded")
            
    def flip_vertical(self):
        """Flip image vertically"""
        if self.current_image is not None:
            self.save_state()
            self.base_image = cv2.flip(self.base_image, 0) # Update base
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Flipped vertically")
        else:
            self.update_status("No image loaded")
            
    def rotate_90(self):
        """Rotate image 90 degrees clockwise"""
        if self.current_image is not None:
            self.save_state()
            self.base_image = cv2.rotate(self.base_image, cv2.ROTATE_90_CLOCKWISE) # Update base
            self.current_image = self.base_image.copy()
            self.display_on_canvas()
            self.update_status("Rotated 90° clockwise")
        else:
            self.update_status("No image loaded")
            
    def display_on_canvas(self):
        """Display the current image on the canvas, resized to fit"""
        if self.current_image is None: return
        
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        img_height, img_width = self.current_image.shape[:2]
        
        scale = min(canvas_width / img_width, canvas_height / img_height); scale = min(scale, 1.0);
        new_width, new_height = int(img_width * scale), int(img_height * scale)
        
        if new_width < img_width or new_height < img_height:
             display_img = cv2.resize(self.current_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        else:
            display_img = self.current_image
            
        img_pil = Image.fromarray(display_img)
        self.display_image = ImageTk.PhotoImage(img_pil)
        
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.display_image, anchor=tk.CENTER)

# Main program execution
if __name__ == "__main__":
    root = tk.Tk()
    app = SimplePhotoshop(root)
    root.mainloop()