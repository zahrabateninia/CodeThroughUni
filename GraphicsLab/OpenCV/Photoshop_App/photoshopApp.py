import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Scale, Button, Label, Frame, colorchooser, Toplevel
from PIL import Image, ImageTk

class ToolTip:
    """Create a tooltip for a given widget"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        # Bind hover events
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        """Display the tooltip"""
        if self.tooltip_window or not self.text:
            return
        
        # Get widget position
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty() + self.widget.winfo_height() // 2
        
        # Create tooltip window
        self.tooltip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove window decorations
        tw.wm_geometry(f"+{x}+{y}")
        
        # Create tooltip label with styling
        label = Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("Arial", 9), padx=5, pady=3)
        label.pack()
    
    def hide_tooltip(self, event=None):
        """Hide the tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class SimplePhotoshop:
    def __init__(self, root):
        """Initialize the Photoshop application with GUI components"""
        self.root = root
        self.root.title("Photo Editor - OpenCV")
        self.root.configure(bg='#2b2b2b')
        
        # Store the original and current image
        self.original_image = None
        self.current_image = None
        self.display_image = None
        
        # History stack for undo functionality (stores up to 10 previous states)
        self.history = []
        self.history_limit = 10 
        
        # Drawing variables
        self.drawing_mode = None 
        self.start_point = None
        self.drawing_color = (255, 0, 0)
        
        # Create GUI layout
        self.create_widgets()
        
        # Bind resize event to automatically redraw image
        self.root.bind('<Configure>', lambda e: self.display_on_canvas() if self.current_image is not None else None)
        
    def save_state(self):
        """Saves the current image state to the history stack before an operation."""
        if self.current_image is not None:
            # Check if current image is different from the last saved state to avoid duplicates
            if not self.history or not np.array_equal(self.current_image, self.history[-1]):
                if len(self.history) >= self.history_limit:
                    self.history.pop(0) # Remove the oldest state
                self.history.append(self.current_image.copy())

    def undo_step(self):
        """Resets image to the previous step in history."""
        if len(self.history) > 1:
            self.history.pop() # Remove the most recent state (the one we want to undo)
            self.current_image = self.history[-1].copy() 
            self.display_on_canvas()
            self.update_status(f"Undo successful. History: {len(self.history)} states left.")
            self.reset_adjustment_sliders() # Reset sliders as their effect is now part of the image
        elif len(self.history) == 1:
            self.update_status("Cannot undo further (at original state).")
        else:
            self.update_status("No history available to undo.")

    def reset_adjustment_sliders(self):
        """Resets the brightness, contrast, and blur sliders."""
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.blur_slider.set(0)

    def create_widgets(self):
        """Create all GUI buttons, sliders, and canvas"""
        
        # Left toolbar frame (vertical button panel)
        toolbar_frame = Frame(self.root, bg='#3c3c3c', width=60) # Smaller width as no text
        toolbar_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Tool buttons with improved icons and descriptive text
        
        # File Operations
        self.create_tool_button(toolbar_frame, "📁", self.load_image, "Load New Image")
        self.create_tool_button(toolbar_frame, "💾", self.save_image, "Save Current Image")
        
        Label(toolbar_frame, text="─────", bg='#3c3c3c', fg='#666').pack(pady=5)
        
        # History & Reset Operations
        self.create_tool_button(toolbar_frame, "↩", self.undo_step, "Revert to Previous Edit (max 10 steps)")
        self.create_tool_button(toolbar_frame, "⟲", self.reset_image, "Reset Image to Original State")
        
        Label(toolbar_frame, text="─────", bg='#3c3c3c', fg='#666').pack(pady=5)
        
        # Drawing tools
        self.create_tool_button(toolbar_frame, "☐", lambda: self.set_drawing_mode('rectangle'), "Draw Rectangle")
        self.create_tool_button(toolbar_frame, "◯", lambda: self.set_drawing_mode('circle'), "Draw Circle")
        self.create_tool_button(toolbar_frame, "━", lambda: self.set_drawing_mode('line'), "Draw Line")
        self.create_tool_button(toolbar_frame, "🖹", lambda: self.set_drawing_mode('text'), "Add Text Annotation")
        self.create_tool_button(toolbar_frame, "🎨", self.choose_color, "Select Drawing Color")
        
        Label(toolbar_frame, text="─────", bg='#3c3c3c', fg='#666').pack(pady=5)
        
        # Filters and Adjustments
        self.create_tool_button(toolbar_frame, "⚫", self.apply_grayscale, "Apply Grayscale Filter")
        self.create_tool_button(toolbar_frame, "⚡", self.apply_edge_detection, "Detect Edges (Canny)")
        self.create_tool_button(toolbar_frame, "✨", self.apply_sharpen, "Apply Sharpen Filter")

        Label(toolbar_frame, text="─────", bg='#3c3c3c', fg='#666').pack(pady=5)
        
        # Transformation buttons
        self.create_tool_button(toolbar_frame, "⇄", self.flip_horizontal, "Flip Image Horizontally")
        self.create_tool_button(toolbar_frame, "⇅", self.flip_vertical, "Flip Image Vertically")
        self.create_tool_button(toolbar_frame, "↻", self.rotate_90, "Rotate 90° Clockwise")

        # Right panel for controls
        control_frame = Frame(self.root, bg='#2b2b2b')
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Adjustments section
        Label(control_frame, text="ADJUSTMENTS", bg='#2b2b2b', fg='white', 
              font=('Arial', 10, 'bold')).pack(pady=(0, 10))
        
        # Brightness slider
        Label(control_frame, text="Brightness", bg='#2b2b2b', fg='white').pack()
        self.brightness_slider = Scale(control_frame, from_=-100, to=100, orient=tk.HORIZONTAL, 
                                       command=self.apply_filters, bg='#3c3c3c', fg='white',
                                       highlightthickness=0, length=200)
        self.brightness_slider.set(0)
        self.brightness_slider.pack(pady=5)
        
        # Contrast slider
        Label(control_frame, text="Contrast", bg='#2b2b2b', fg='white').pack()
        self.contrast_slider = Scale(control_frame, from_=0.5, to=3.0, resolution=0.1, 
                                       orient=tk.HORIZONTAL, command=self.apply_filters,
                                       bg='#3c3c3c', fg='white', highlightthickness=0, length=200)
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(pady=5)
        
        # Blur slider
        Label(control_frame, text="Blur", bg='#2b2b2b', fg='white').pack()
        self.blur_slider = Scale(control_frame, from_=0, to=50, orient=tk.HORIZONTAL, 
                                 command=self.apply_filters, bg='#3c3c3c', fg='white',
                                 highlightthickness=0, length=200)
        self.blur_slider.set(0)
        self.blur_slider.pack(pady=5)
        
        # Shape thickness slider
        Label(control_frame, text="Shape Thickness", bg='#2b2b2b', fg='white').pack(pady=(20, 0))
        self.thickness_slider = Scale(control_frame, from_=1, to=20, orient=tk.HORIZONTAL,
                                       bg='#3c3c3c', fg='white', highlightthickness=0, length=200)
        self.thickness_slider.set(3)
        self.thickness_slider.pack(pady=5)
        
        # Status label
        self.status_label = Label(control_frame, text="Ready", bg='#2b2b2b', 
                                 fg='#888', wraplength=180)
        self.status_label.pack(pady=20)
        
        # Canvas for image display
        self.canvas = tk.Canvas(self.root, bg='#1e1e1e', highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind mouse events for drawing
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_canvas_release)
    
    def create_tool_button(self, parent, icon, command, tooltip):
        """Create a styled tool button with hover tooltip (icon only)"""
        btn = Button(parent, text=icon, command=command, 
                     bg='#3c3c3c', fg='white', activebackground='#5a5a5a',
                     width=3, # Fixed width for uniform icons
                     height=2, 
                     relief=tk.FLAT, bd=0,
                     font=('Arial', 18)) # Even larger font for icon visibility
        btn.pack(pady=3, padx=5, fill=tk.X) 
        # Create tooltip using the ToolTip class
        ToolTip(btn, tooltip)
        # Also update status bar
        btn.bind('<Enter>', lambda e: self.update_status(tooltip))
        btn.bind('<Leave>', lambda e: self.update_status("Ready"))
        return btn
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
    
    def set_drawing_mode(self, mode):
        """Set the current drawing mode"""
        self.drawing_mode = mode
        self.update_status(f"Drawing mode: {mode}")
    
    def choose_color(self):
        """Open color picker dialog"""
        color = colorchooser.askcolor(title="Choose shape color")
        if color[0]:  # color[0] is RGB tuple
            self.drawing_color = tuple(int(c) for c in color[0])
            self.update_status(f"Color selected: RGB{self.drawing_color}")
    
    def on_canvas_click(self, event):
        """Handle mouse click on canvas"""
        if self.current_image is None or self.drawing_mode is None:
            return
        self.start_point = (event.x, event.y)
    
    def on_canvas_drag(self, event):
        """Handle mouse drag on canvas - placeholder for potential live preview"""
        pass
    
    def on_canvas_release(self, event):
        """Handle mouse release - draw the shape"""
        if self.current_image is None or self.drawing_mode is None or self.start_point is None:
            return
        
        self.save_state() # Save state before applying drawing
        
        end_point = (event.x, event.y)
        
        # Convert canvas coordinates to image coordinates
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_height, img_width = self.current_image.shape[:2]
        
        # Calculate the scale and offset used in display
        scale = min(canvas_width / img_width, canvas_height / img_height, 1.0)
        scaled_width = int(img_width * scale)
        scaled_height = int(img_height * scale)
        offset_x = (canvas_width - scaled_width) // 2
        offset_y = (canvas_height - scaled_height) // 2
        
        # Convert to image coordinates
        img_x1 = int((self.start_point[0] - offset_x) / scale)
        img_y1 = int((self.start_point[1] - offset_y) / scale)
        img_x2 = int((end_point[0] - offset_x) / scale)
        img_y2 = int((end_point[1] - offset_y) / scale)
        
        # Get thickness from slider
        thickness = self.thickness_slider.get()
        
        # Draw on the actual image
        if self.drawing_mode == 'rectangle':
            cv2.rectangle(self.current_image, (img_x1, img_y1), (img_x2, img_y2), 
                          self.drawing_color, thickness)
        elif self.drawing_mode == 'circle':
            center = ((img_x1 + img_x2) // 2, (img_y1 + img_y2) // 2)
            radius = int(np.sqrt((img_x2 - img_x1)**2 + (img_y2 - img_y1)**2) / 2)
            cv2.circle(self.current_image, center, radius, self.drawing_color, thickness)
        elif self.drawing_mode == 'line':
            cv2.line(self.current_image, (img_x1, img_y1), (img_x2, img_y2), 
                     self.drawing_color, thickness)
        elif self.drawing_mode == 'text':
            # Prompt for text input
            text = tk.simpledialog.askstring("Input", "Enter text:")
            if text:
                # Use img_x1, img_y1 as the start point for the text
                cv2.putText(self.current_image, text, (img_x1, img_y1),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, self.drawing_color, thickness)
        
        self.display_on_canvas()
        self.start_point = None
        
    def load_image(self):
        """Open file dialog to load an image"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            # Read image using cv2
            self.original_image = cv2.imread(file_path)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.current_image = self.original_image.copy()
            
            # --- History management: Clear old history and save the original state ---
            self.history = [] 
            self.save_state() 
            # ------------------------------------------------------------------------
            
            self.reset_adjustment_sliders()
            
            self.display_on_canvas()
            self.update_status("Image loaded successfully")
            self.drawing_mode = None
            
    def save_image(self):
        """Save the current edited image"""
        if self.current_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if file_path:
                # Convert RGB back to BGR for cv2.imwrite
                image_to_save = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(file_path, image_to_save)
                self.update_status("Image saved successfully")
        else:
            self.update_status("No image to save")
                
    def reset_image(self):
        """Reset image to original state and clear history (except for the initial state)"""
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            
            # Reset history to contain only the original state
            self.history = [self.original_image.copy()] 
            
            self.reset_adjustment_sliders()
            self.display_on_canvas()
            self.update_status("Image reset to original")
            self.drawing_mode = None
        else:
            self.update_status("No image loaded")
            
    def apply_filters(self, event=None):
        """Apply brightness, contrast, and blur adjustments"""
        if self.original_image is None:
            return
        
        # Start with original image (float conversion for calculations)
        image = self.original_image.copy().astype(np.float32)
        
        # Apply contrast adjustment (multiply pixel values)
        contrast = self.contrast_slider.get()
        image = image * contrast
        
        # Apply brightness adjustment (add to pixel values)
        brightness = self.brightness_slider.get()
        image = image + brightness
        
        # Clip values to valid range [0, 255]
        image = np.clip(image, 0, 255).astype(np.uint8)
        
        # Apply blur if slider value > 0
        blur_amount = self.blur_slider.get()
        if blur_amount > 0:
            # Blur kernel size must be odd
            kernel_size = blur_amount * 2 + 1
            image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        
        self.current_image = image
        self.display_on_canvas()
        
    def apply_grayscale(self):
        """Convert image to grayscale"""
        if self.current_image is not None:
            self.save_state() # Save state before operation
            # Convert to grayscale
            gray = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
            # Convert back to RGB format for consistency (3 channels)
            self.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
            self.display_on_canvas()
            self.update_status("Grayscale applied")
        else:
            self.update_status("No image loaded")
            
    def apply_edge_detection(self):
        """Apply Canny edge detection"""
        if self.current_image is not None:
            self.save_state() # Save state before operation
            # Convert to grayscale first
            gray = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
            # Apply Canny edge detection
            edges = cv2.Canny(gray, 100, 200)
            # Convert to RGB for display
            self.current_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            self.display_on_canvas()
            self.update_status("Edge detection applied")
        else:
            self.update_status("No image loaded")
            
    def apply_sharpen(self):
        """Apply sharpening filter using a kernel"""
        if self.current_image is not None:
            self.save_state() # Save state before operation
            # Define sharpening kernel
            kernel = np.array([[-1, -1, -1],
                               [-1,  9, -1],
                               [-1, -1, -1]])
            # Apply kernel to image
            self.current_image = cv2.filter2D(self.current_image, -1, kernel)
            self.display_on_canvas()
            self.update_status("Sharpening applied")
        else:
            self.update_status("No image loaded")
            
    def flip_horizontal(self):
        """Flip image horizontally"""
        if self.current_image is not None:
            self.save_state() # Save state before operation
            self.current_image = cv2.flip(self.current_image, 1)
            self.display_on_canvas()
            self.update_status("Flipped horizontally")
        else:
            self.update_status("No image loaded")
            
    def flip_vertical(self):
        """Flip image vertically"""
        if self.current_image is not None:
            self.save_state() # Save state before operation
            self.current_image = cv2.flip(self.current_image, 0)
            self.display_on_canvas()
            self.update_status("Flipped vertically")
        else:
            self.update_status("No image loaded")
            
    def rotate_90(self):
        """Rotate image 90 degrees clockwise"""
        if self.current_image is not None:
            self.save_state() # Save state before operation
            self.current_image = cv2.rotate(self.current_image, cv2.ROTATE_90_CLOCKWISE)
            self.display_on_canvas()
            self.update_status("Rotated 90° clockwise")
        else:
            self.update_status("No image loaded")
            
    def display_on_canvas(self):
        """Display the current image on the canvas, resized to fit"""
        if self.current_image is None:
            return
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Get image dimensions
        img_height, img_width = self.current_image.shape[:2]
        
        # Calculate scaling factor to fit image in canvas
        scale = min(canvas_width / img_width, canvas_height / img_height, 1.0)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Resize image for display
        display_img = cv2.resize(self.current_image, (new_width, new_height), 
                                 interpolation=cv2.INTER_AREA)
        
        # Convert to PIL format for tkinter
        img_pil = Image.fromarray(display_img)
        self.display_image = ImageTk.PhotoImage(img_pil)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, 
                                 image=self.display_image, anchor=tk.CENTER)

# Main program execution
if __name__ == "__main__":
    root = tk.Tk()
    app = SimplePhotoshop(root)
    # Start the main loop after all setup
    root.mainloop()