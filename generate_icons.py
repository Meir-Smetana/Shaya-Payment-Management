"""
Generate all required PWA icons for ShuttleOps.
Run: pip install Pillow --break-system-packages && python generate_icons.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('icons', exist_ok=True)

SIZES = [72, 96, 128, 144, 152, 180, 192, 384, 512]

def create_icon(size):
    # Background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded rect background
    bg_color = (13, 17, 23, 255)      # #0D1117
    accent   = (88, 166, 255, 255)    # #58A6FF
    radius   = int(size * 0.22)

    # Draw rounded background
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=bg_color)

    # Draw shuttle emoji-style icon using geometric shapes
    cx, cy = size // 2, size // 2
    scale = size / 192

    # Body of shuttle (rounded rect)
    bw = int(110 * scale)
    bh = int(52 * scale)
    bx = cx - bw // 2
    by = cy - bh // 2 + int(5 * scale)
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=int(14 * scale), fill=accent)

    # Windshield (darker blue trapezoid approximation)
    ws_color = (30, 60, 100, 255)
    ws_w = int(40 * scale)
    ws_h = int(36 * scale)
    draw.rounded_rectangle([cx - bw // 2 + int(10 * scale), by + int(8 * scale),
                             cx - bw // 2 + int(10 * scale) + ws_w, by + int(8 * scale) + ws_h],
                            radius=int(6 * scale), fill=ws_color)

    # Wheels
    wheel_r = int(12 * scale)
    wheel_color = (33, 38, 45, 255)  # dark
    rim_color   = (139, 148, 158, 255)

    for wx in [cx - int(28 * scale), cx + int(28 * scale)]:
        wy = by + bh - int(4 * scale)
        draw.ellipse([wx - wheel_r, wy - wheel_r, wx + wheel_r, wy + wheel_r], fill=wheel_color)
        draw.ellipse([wx - int(wheel_r * 0.5), wy - int(wheel_r * 0.5),
                      wx + int(wheel_r * 0.5), wy + int(wheel_r * 0.5)], fill=rim_color)

    # Route text area (simplified bar)
    bar_h = int(14 * scale)
    bar_y = by - bar_h - int(10 * scale)
    bar_color = (22, 27, 34, 255)
    draw.rounded_rectangle([cx - int(60 * scale), bar_y,
                             cx + int(60 * scale), bar_y + bar_h],
                            radius=int(4 * scale), fill=bar_color)

    # Small dots to represent route waypoints
    dot_r = int(3 * scale)
    dot_color = accent
    for dot_x in [cx - int(40 * scale), cx, cx + int(40 * scale)]:
        dot_y = bar_y + bar_h // 2
        draw.ellipse([dot_x - dot_r, dot_y - dot_r,
                      dot_x + dot_r, dot_y + dot_r], fill=dot_color)

    return img

for size in SIZES:
    icon = create_icon(size)
    icon.save(f'icons/icon-{size}.png', 'PNG')
    print(f'✅ Generated icon-{size}.png')

# Also create splash screen (1242x2688 - iPhone 11 Pro Max)
splash_w, splash_h = 1242, 2688
splash = Image.new('RGB', (splash_w, splash_h), (13, 17, 23))
draw = ImageDraw.Draw(splash)

# Center logo
icon_512 = create_icon(256)
paste_x = (splash_w - 256) // 2
paste_y = (splash_h - 256) // 2 - 60
splash.paste(icon_512, (paste_x, paste_y), icon_512)

splash.save('icons/splash.png', 'PNG')
print('✅ Generated splash.png')
print('\n🎉 All icons generated in /icons/ directory!')
