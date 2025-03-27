from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with a white background
size = (256, 256)
image = Image.new('RGB', size, 'white')
draw = ImageDraw.Draw(image)

# Draw a clock-like circle
circle_bbox = (20, 20, 236, 236)
draw.ellipse(circle_bbox, outline='#007bff', width=10)

# Draw clock hands
center = (128, 128)
# Hour hand
draw.line((center[0], center[1], center[0] + 50, center[1] - 50), fill='#007bff', width=8)
# Minute hand
draw.line((center[0], center[1], center[0] - 70, center[1] + 20), fill='#007bff', width=8)

# Save as PNG first
if not os.path.exists('assets'):
    os.makedirs('assets')
png_path = 'assets/app_icon.png'
image.save(png_path)

# Convert to ICO
ico_path = 'assets/app_icon.ico'
image.save(ico_path, format='ICO', sizes=[(256, 256)]) 