from PIL import Image, ImageDraw

def create_icon():
    # Create a new image with a transparent background
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Calculate dimensions
    padding = size // 8
    clock_size = size - (2 * padding)
    center = size // 2
    
    # Draw clock circle
    draw.ellipse(
        [padding, padding, padding + clock_size, padding + clock_size],
        outline=(52, 58, 64),  # Dark gray
        fill=(240, 245, 255),  # Light blue background
        width=size // 16
    )
    
    # Draw clock hands
    # Hour hand (pointing to 2)
    draw.line(
        [center, center,
         center + int(clock_size * 0.2), center - int(clock_size * 0.1)],
        fill=(52, 58, 64),
        width=size // 20
    )
    
    # Minute hand (pointing to 10)
    draw.line(
        [center, center,
         center - int(clock_size * 0.3), center + int(clock_size * 0.1)],
        fill=(52, 58, 64),
        width=size // 24
    )
    
    # Center dot
    dot_size = size // 16
    draw.ellipse(
        [center - dot_size, center - dot_size,
         center + dot_size, center + dot_size],
        fill=(52, 58, 64)
    )
    
    # Save in different sizes
    sizes = [16, 32, 48, 64, 128, 256]
    for s in sizes:
        resized = image.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(f'icon_{s}.png')
    
    # Save as ICO file with multiple sizes
    image.save('app_icon.ico', format='ICO', sizes=[(s, s) for s in sizes])

if __name__ == '__main__':
    create_icon() 