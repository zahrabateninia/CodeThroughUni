from fpdf import FPDF
from PIL import Image
import os

def images_to_pdf(image_names, output_pdf):
    base_path = os.path.dirname(os.path.abspath(__file__))

    pdf = FPDF()

    for image_name in image_names:
        image_path = os.path.join(base_path, image_name)

        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            continue

        img = Image.open(image_path)
        width, height = img.size

        # Convert pixels to mm (1px ≈ 0.264583 mm)
        width_mm = width * 0.264583
        height_mm = height * 0.264583

        pdf.add_page()

        # Fit image inside A4 page (210x297 mm)
        max_width = 210
        max_height = 297

        ratio = min(max_width / width_mm, max_height / height_mm)

        new_width = width_mm * ratio
        new_height = height_mm * ratio

        pdf.image(image_path, x=0, y=0, w=new_width, h=new_height)

    output_path = os.path.join(base_path, output_pdf)
    pdf.output(output_path)

    print(f"PDF successfully created at:\n{output_path}")


# if __name__ == "__main__":
    images = [
        "image1.jpg",
        "image2.png"
    ]

    images_to_pdf(images, "output.pdf")
