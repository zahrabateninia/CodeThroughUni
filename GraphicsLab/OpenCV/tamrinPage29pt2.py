import cv2
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# تمرین 1: تشخیص چشم و رسم اشکال روی آن
# ==========================================

def detect_and_draw_shapes_on_eye():
    # خواندن تصویر
    image = cv2.imread('eye_image.jpg')
    
    if image is None:
        print("خطا: تصویر یافت نشد!")
        return
    
    # تبدیل به خاکستری برای تشخیص بهتر
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # بارگذاری Cascade Classifier برای تشخیص چشم
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    # تشخیص چشم‌ها
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    
    # کپی تصویر برای رسم اشکال
    image_with_circle = image.copy()
    image_with_rectangle = image.copy()
    
    for (x, y, w, h) in eyes:
        # محاسبه مرکز و شعاع دایره
        center_x = x + w // 2
        center_y = y + h // 2
        radius = int(min(w, h) * 0.4)
        
        # رسم دایره سبز روی چشم (تصویر اول)
        cv2.circle(image_with_circle, (center_x, center_y), radius, (0, 255, 0), 2)
        
        # رسم مستطیل قرمز روی چشم (تصویر دوم)
        cv2.rectangle(image_with_rectangle, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    # نمایش نتایج
    cv2.imshow('Original Image', image)
    cv2.imshow('Eye with Circle', image_with_circle)
    cv2.imshow('Eye with Rectangle', image_with_rectangle)
    
    # ذخیره تصاویر
    cv2.imwrite('eye_with_circle.jpg', image_with_circle)
    cv2.imwrite('eye_with_rectangle.jpg', image_with_rectangle)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ==========================================
# تمرین 2: رسم شکل قلب با نقاط
# ==========================================

def draw_heart_shape():
    # تعداد نقاط برای رسم قلب
    t = np.linspace(0, 2 * np.pi, 100)
    
    # معادلات پارامتری قلب
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    
    # نرمال‌سازی مختصات برای نمایش بهتر
    x = (x - x.min()) / (x.max() - x.min())
    y = (y - y.min()) / (y.max() - y.min())
    
    # ایجاد figure
    plt.figure(figsize=(8, 8))
    
    # رسم نقاط قلب با خطوط متصل
    plt.plot(x, y, 'ro-', markersize=8, linewidth=2)
    
    # تنظیمات نمودار
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.title('Heart Shape', fontsize=14, fontweight='bold')
    
    # محدود کردن محور‌ها
    plt.xlim(-0.2, 1.2)
    plt.ylim(-0.2, 1.2)
    
    # ذخیره و نمایش
    plt.savefig('heart_shape.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("شکل قلب با موفقیت رسم شد!")


# ==========================================
# روش جایگزین برای رسم قلب با OpenCV
# ==========================================

def draw_heart_with_opencv():
    # ایجاد تصویر سفید
    img_size = 600
    image = np.ones((img_size, img_size, 3), dtype=np.uint8) * 255
    
    # تعداد نقاط
    n_points = 100
    t = np.linspace(0, 2 * np.pi, n_points)
    
    # معادلات قلب
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    
    # تبدیل به مختصات تصویر
    scale = 15
    offset_x = img_size // 2
    offset_y = img_size // 2 - 50
    
    x_img = (x * scale + offset_x).astype(np.int32)
    y_img = (-y * scale + offset_y).astype(np.int32)
    
    # رسم خطوط بین نقاط
    points = np.column_stack((x_img, y_img))
    
    for i in range(len(points) - 1):
        cv2.line(image, tuple(points[i]), tuple(points[i+1]), (255, 0, 0), 2)
    
    # رسم نقاط
    for point in points:
        cv2.circle(image, tuple(point), 5, (0, 0, 255), -1)
    
    # رسم گرید
    for i in range(0, img_size, 50):
        cv2.line(image, (i, 0), (i, img_size), (200, 200, 200), 1)
        cv2.line(image, (0, i), (img_size, i), (200, 200, 200), 1)
    
    cv2.imshow('Heart Shape with OpenCV', image)
    cv2.imwrite('heart_shape_opencv.png', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("=" * 50)
    print("تمرین 1: تشخیص چشم و رسم اشکال")
    print("=" * 50)
    detect_and_draw_shapes_on_eye()
    
    print("\n" + "=" * 50)
    print("تمرین 2: رسم شکل قلب (با Matplotlib)")
    print("=" * 50)
    draw_heart_shape()
    
    print("\n" + "=" * 50)
    print("تمرین 2: رسم شکل قلب (با OpenCV)")
    print("=" * 50)
    draw_heart_with_opencv()
