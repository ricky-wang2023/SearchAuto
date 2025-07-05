#!/usr/bin/env python3
"""
Create a simple icon for SearchAuto
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Create a 256x256 icon
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw background circle
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=(52, 152, 219), outline=(41, 128, 185), width=5)
    
    # Draw search magnifying glass
    center_x, center_y = size // 2, size // 2
    glass_radius = 60
    handle_length = 40
    handle_width = 8
    
    # Magnifying glass circle
    draw.ellipse([center_x-glass_radius, center_y-glass_radius, 
                  center_x+glass_radius, center_y+glass_radius], 
                 fill=(255, 255, 255), outline=(41, 128, 185), width=3)
    
    # Handle
    handle_start_x = center_x + glass_radius - 10
    handle_start_y = center_y + glass_radius - 10
    handle_end_x = handle_start_x + handle_length
    handle_end_y = handle_start_y + handle_length
    
    draw.line([(handle_start_x, handle_start_y), (handle_end_x, handle_end_y)], 
              fill=(41, 128, 185), width=handle_width)
    
    # Add AI symbol (circuit board pattern)
    for i in range(0, 40, 10):
        draw.line([(center_x-30+i, center_y-20), (center_x-30+i, center_y+20)], 
                  fill=(255, 255, 255), width=2)
    
    # Save as ICO
    img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("✅ Created icon.ico")
    
except ImportError:
    print("⚠️  PIL not available, creating placeholder icon")
    # Create a simple text-based icon
    with open('icon.ico', 'w') as f:
        f.write('placeholder')
    print("✅ Created placeholder icon.ico")
except Exception as e:
    print(f"⚠️  Error creating icon: {e}")
    # Create a simple text-based icon
    with open('icon.ico', 'w') as f:
        f.write('placeholder')
    print("✅ Created placeholder icon.ico") 