import os
import math
import subprocess
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def build_flawless_reel():
    print("=== BUILDING FLAWLESS DAHI VADA DIWALI REEL (NO TOFU / CLEAN GRAPHICS) ===")
    
    w, h = 1080, 1920
    fps = 60
    total_frames = 1680 # 28.00 seconds
    
    c1 = 'Raw footage/WhatsApp Video 2026-11-10 at 3.29.41 PM.mp4'
    c2 = 'Raw footage/WhatsApp Video 2026-11-10 at 3.29.52 PM.mp4'
    os.makedirs('voice/temp_render', exist_ok=True)
    
    # Helper to draw beautiful 4-point golden sparkle stars
    def draw_star(draw_target, cx, cy, r, color=(243, 201, 62, 255)):
        pts = [
            (cx, cy - r), (cx + int(r*0.28), cy - int(r*0.28)),
            (cx + r, cy), (cx + int(r*0.28), cy + int(r*0.28)),
            (cx, cy + r), (cx - int(r*0.28), cy + int(r*0.28)),
            (cx - r, cy), (cx - int(r*0.28), cy - int(r*0.28))
        ]
        draw_target.polygon(pts, fill=color)

    # Helper to draw warm glowing Diya
    def draw_diya_warm(draw_target, overlay_img, cx, cy, scale=1.0, flicker=1.0):
        glow_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow_layer)
        for r in range(int(150*scale), int(15*scale), -int(15*scale)):
            alpha = int(150 * (1.0 - r/(150.0*scale))**1.5 * flicker)
            gdraw.ellipse([cx - r, cy - int(45*scale) - r, cx + r, cy - int(45*scale) + r], fill=(255, 175, 45, alpha))
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(int(18*scale)))
        overlay_img.alpha_composite(glow_layer)
        
        bw = int(140 * scale)
        bh = int(80 * scale)
        draw_target.ellipse([cx - bw, cy, cx + bw, cy + bh], fill=(195, 130, 30, 255), outline=(255, 220, 80, 255), width=int(4*scale))
        draw_target.ellipse([cx - int(115*scale), cy + int(6*scale), cx + int(115*scale), cy + int(50*scale)], fill=(140, 80, 15, 255), outline=(230, 180, 50, 255), width=int(2*scale))
        draw_target.ellipse([cx - int(85*scale), cy + int(15*scale), cx + int(85*scale), cy + int(42*scale)], fill=(85, 45, 10, 255))
        
        flame_h = int(120 * scale * flicker)
        fw = int(30 * scale)
        flame_pts = [
            (cx, cy - flame_h),
            (cx + fw, cy - flame_h//2),
            (cx + int(fw*0.65), cy - int(8*scale)),
            (cx - int(fw*0.65), cy - int(8*scale)),
            (cx - fw, cy - flame_h//2)
        ]
        draw_target.polygon(flame_pts, fill=(255, 205, 50, 255))
        inner_pts = [
            (cx, cy - flame_h + int(24*scale)),
            (cx + int(fw*0.48), cy - flame_h//2 + int(10*scale)),
            (cx + int(fw*0.25), cy - int(8*scale)),
            (cx - int(fw*0.25), cy - int(8*scale)),
            (cx - int(fw*0.48), cy - flame_h//2 + int(10*scale))
        ]
        draw_target.polygon(inner_pts, fill=(255, 255, 220, 255))

    # --- STEP 1: Re-render Scene 3 Diwali Cutaway Plate with clean text ---
    print("Rendering Scene 3 Diwali Cutaway Plate with vector stars...")
    font_title = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 54, index=1)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 36, index=0)
    font_badge = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 38, index=1)
    
    np.random.seed(42)
    s3_particles = [{'x': np.random.uniform(50, w-50), 'y': np.random.uniform(100, h-100), 'speed': np.random.uniform(1.5, 3.8), 'size': np.random.uniform(3, 8), 'phase': np.random.uniform(0, math.pi*2)} for _ in range(40)]
    
    bg_arr = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        factor = abs(y - h//2) / (h//2)
        bg_arr[y, :, 0] = int(35 * (1 - factor*0.3))
        bg_arr[y, :, 1] = int(14 * (1 - factor*0.3))
        bg_arr[y, :, 2] = int(5 * (1 - factor*0.3))
    base_bg = Image.fromarray(bg_arr, mode='RGB')
    
    cmd_b3 = ['ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-s', f'{w}x{h}', '-pix_fmt', 'rgb24', '-r', str(fps), '-i', '-', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', 'voice/temp_render/b3.mp4']
    proc_b3 = subprocess.Popen(cmd_b3, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for f in range(180):
        img = base_bg.copy()
        draw = ImageDraw.Draw(img)
        
        # Rotating Rangoli Mandala
        cx, cy = 540, 960
        rot = f * 0.4
        rad = 320
        for a in range(0, 360, 30):
            ang = math.radians(a + rot)
            px = cx + rad * math.cos(ang)
            py = cy + rad * math.sin(ang)
            draw.line([cx, cy, px, py], fill=(120, 80, 20), width=2)
            draw.ellipse([px-12, py-12, px+12, py+12], fill=(180, 130, 30))
        draw.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], outline=(160, 110, 25), width=3)
        draw.ellipse([cx-rad//2, cy-rad//2, cx+rad//2, cy+rad//2], outline=(200, 150, 40), width=2)
        
        # Glowing Diya in center
        flicker = 1.0 + 0.08 * math.sin(f * 0.35)
        diya_y = 1100
        for gr in range(180, 20, -20):
            intensity = int(120 * (1.0 - gr/180.0) * flicker)
            draw.ellipse([cx - gr, diya_y - 70 - gr, cx + gr, diya_y - 70 + gr], fill=(min(255, 40+intensity), min(255, 18+intensity//2), 6))
            
        draw.ellipse([cx - 150, diya_y, cx + 150, diya_y + 90], fill=(195, 130, 30), outline=(255, 220, 80), width=4)
        draw.ellipse([cx - 125, diya_y + 8, cx + 125, diya_y + 55], fill=(140, 80, 15), outline=(230, 180, 50), width=2)
        
        flame_h = int(120 * flicker)
        flame_pts = [(cx, diya_y - flame_h), (cx + 30, diya_y - flame_h//2), (cx + 20, diya_y - 10), (cx - 20, diya_y - 10), (cx - 30, diya_y - flame_h//2)]
        draw.polygon(flame_pts, fill=(255, 200, 50))
        inner_flame = [(cx, diya_y - flame_h + 25), (cx + 15, diya_y - flame_h//2 + 10), (cx + 10, diya_y - 10), (cx - 10, diya_y - 10), (cx - 15, diya_y - flame_h//2 + 10)]
        draw.polygon(inner_flame, fill=(255, 255, 210))
        
        # Sparkles
        for p in s3_particles:
            py = (p['y'] - f * p['speed']) % (h - 100) + 50
            px = p['x'] + 15 * math.sin(f * 0.05 + p['phase'])
            sz = p['size'] * (0.8 + 0.3 * math.sin(f * 0.2 + p['phase']))
            draw.ellipse([px-sz, py-sz, px+sz, py+sz], fill=(255, 225, 110))
            
        # Card 1: Urad Dal
        card_w, card_h = 760, 160
        cx_card = (w - card_w) // 2
        prog = min(1.0, f / 20.0)
        cy_card = int(240 + 80 * (1.0 - math.exp(-prog * 5.0) * math.cos(prog * math.pi)))
        draw.rounded_rectangle([cx_card, cy_card, cx_card+card_w, cy_card+card_h], radius=28, fill=(20, 16, 14), outline=(243, 201, 62), width=3)
        draw.text((cx_card + 45, cy_card + 28), 'उड़द दाल (Urad Dal)', font=font_title, fill=(243, 201, 62))
        draw.text((cx_card + 45, cy_card + 95), 'धुली उड़द दाल का फूला हुआ बैटर', font=font_sub, fill=(245, 240, 235))
        
        # Tip Badge with vector star
        if f >= 30:
            prog_t = min(1.0, (f - 30) / 20.0)
            tip_w = 880
            tip_h = 100
            tx = (w - tip_w) // 2
            ty = int(520 + 40 * (1.0 - math.exp(-prog_t * 5.0)))
            draw.rounded_rectangle([tx, ty, tx+tip_w, ty+tip_h], radius=24, fill=(40, 25, 12), outline=(255, 215, 60), width=3)
            # Vector sparkle star on left
            draw_star(draw, tx + 45, ty + tip_h//2, 16, color=(255, 225, 110))
            draw.text((tx + 75, ty + 24), 'प्रो टिप: गुनगुने पानी में 10 मिनट भिगोएं', font=font_badge, fill=(255, 235, 140))
            
        proc_b3.stdin.write(img.tobytes())
        
    proc_b3.stdin.close()
    proc_b3.wait()
    print("Scene 3 Diwali Cutaway Plate regenerated cleanly!")
    
    # --- STEP 2: Concatenate base cuts ---
    segments = ['b1.mp4', 'b2.mp4', 'b3.mp4', 'b4.mp4', 'b5a.mp4', 'b5b.mp4', 'b5c.mp4', 'b6.mp4']
    with open('voice/temp_render/concat_list.txt', 'w') as f:
        for s in segments:
            f.write('file ' + s + '\n')
            
    cmd_cat = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'voice/temp_render/concat_list.txt', '-c', 'copy', 'voice/temp_render/base_28s.mp4']
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # --- STEP 3: Composite final overlays & audio ---
    print("Compositing all 28s frames with clean typography and audio...")
    font_badge = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 38, index=1)
    font_card_title = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 52, index=1)
    font_card_sub = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 34, index=0)
    font_cap = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 54, index=1)
    font_outro_title = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 68, index=1)
    font_outro_sub = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 42, index=0)
    
    master_audio = 'voice/temp_render/master_audio_28s.wav'
    out_mp4 = 'Exports/Dahi_Vada_Recipe_Diwali_Reel.mp4'
    
    caption_cues = [
        (0.20, 1.80, [(0.20, 0.70, "दिवाली"), (0.70, 1.00, "आ"), (1.00, 1.45, "रही"), (1.45, 1.80, "है,")]),
        (1.80, 3.78, [(1.80, 2.25, "मिठाइयों"), (2.25, 2.45, "के"), (2.45, 2.80, "साथ"), (2.80, 3.05, "कुछ"), (3.05, 3.45, "चटपटा"), (3.45, 3.65, "बनता"), (3.65, 3.78, "है!")]),
        (4.20, 6.20, [(4.20, 4.55, "आज"), (4.55, 4.95, "बनाते"), (4.95, 5.25, "हैं"), (5.25, 5.70, "नरम,"), (5.70, 6.20, "मुलायम")]),
        (6.20, 8.59, [(6.20, 6.60, "दही"), (6.60, 7.10, "वड़ा,"), (7.10, 7.60, "थाली"), (7.60, 7.85, "की"), (7.85, 8.30, "शान"), (8.30, 8.59, "है।")]),
        (9.20, 11.20, [(9.20, 9.60, "उड़द"), (9.60, 10.00, "दाल"), (10.00, 10.25, "के"), (10.25, 10.70, "वड़े"), (10.70, 11.20, "तलिए,")]),
        (11.20, 13.00, [(11.20, 11.75, "गुनगुने"), (11.75, 12.15, "पानी"), (12.15, 12.40, "में"), (12.40, 13.00, "भिगोइए,")]),
        (13.00, 14.70, [(13.00, 13.30, "फिर"), (13.30, 13.70, "फेंटा"), (13.70, 14.00, "हुआ"), (14.00, 14.35, "दही"), (14.35, 14.70, "डालिए।")]),
        (16.50, 18.80, [(16.50, 16.85, "ऊपर"), (16.85, 17.15, "से"), (17.15, 17.65, "मीठी"), (17.65, 18.20, "इमली"), (18.20, 18.80, "चटनी,")]),
        (18.80, 20.80, [(18.80, 19.40, "तीखी"), (19.40, 20.00, "हरी"), (20.00, 20.80, "चटनी,")]),
        (20.80, 22.48, [(20.80, 21.20, "भुना"), (21.20, 21.55, "जीरा"), (21.55, 21.75, "और"), (21.75, 22.10, "चाट"), (22.10, 22.48, "मसाला!")]),
        (23.50, 25.40, [(23.50, 23.75, "इस"), (23.75, 24.25, "दिवाली"), (24.25, 24.80, "मेहमानों"), (24.80, 25.00, "को"), (25.00, 25.40, "खिलाइए!")]),
        (25.40, 27.29, [(25.40, 25.75, "दही"), (25.75, 26.10, "वड़ा"), (26.10, 26.50, "रेसिपी"), (26.50, 26.80, "सेव"), (26.80, 27.00, "कर"), (27.00, 27.29, "लीजिए!")])
    ]
    
    np.random.seed(108)
    particles = [{'x': np.random.uniform(40, w - 40), 'y': np.random.uniform(50, h - 50), 'speed': np.random.uniform(1.2, 3.5), 'size': np.random.uniform(3, 7), 'phase': np.random.uniform(0, math.pi * 2)} for _ in range(50)]

    read_cmd = ['ffmpeg', '-i', 'voice/temp_render/base_28s.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-']
    pipe_in = subprocess.Popen(read_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    write_cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{w}x{h}',
        '-pix_fmt', 'rgba',
        '-r', str(fps),
        '-i', '-',
        '-i', master_audio,
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-c:a', 'aac',
        '-b:a', '256k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        out_mp4
    ]
    pipe_out = subprocess.Popen(write_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    frame_bytes_len = w * h * 4
    
    for f in range(total_frames):
        t = f / fps
        raw_base = pipe_in.stdout.read(frame_bytes_len)
        if len(raw_base) < frame_bytes_len:
            break
            
        base_img = Image.frombytes('RGBA', (w, h), raw_base)
        overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # 1. Floating Golden Sparkles (active outside scene 3 cutaway)
        if t < 9.0 or t > 12.0:
            for p in particles:
                py = (p['y'] - f * p['speed']) % (h - 60) + 30
                px = p['x'] + 14 * math.sin(f * 0.04 + p['phase'])
                sz = p['size'] * (0.8 + 0.3 * math.sin(f * 0.15 + p['phase']))
                alpha = int(180 + 75 * math.sin(f * 0.1 + p['phase']))
                draw.ellipse([px-sz, py-sz, px+sz, py+sz], fill=(255, 225, 110, alpha))
                
        # 2. Scene 1 Overlay (1.0s – 3.3s): Diya & "दीवाली स्पेशल" Badge
        if 1.0 <= t < 3.3:
            fade_in = min(1.0, (t - 1.0) / 0.5)
            alpha_val = int(255 * fade_in)
            
            badge_text = 'दीवाली स्पेशल'
            bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            bw = tw + 120
            bh = th + 28
            bx = (w - bw) // 2
            by = 160
            draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=24, fill=(28, 18, 12, int(220 * fade_in)), outline=(243, 201, 62, alpha_val), width=3)
            # Vector stars flanking text
            draw_star(draw, bx + 35, by + bh//2, 16, color=(243, 201, 62, alpha_val))
            draw.text((bx + 60, by + 10), badge_text, font=font_badge, fill=(243, 201, 62, alpha_val))
            draw_star(draw, bx + bw - 35, by + bh//2, 16, color=(243, 201, 62, alpha_val))
            
            # Bottom Glowing Diya
            flicker = 1.0 + 0.08 * math.sin(f * 0.3)
            draw_diya_warm(draw, overlay, 540, 1530, scale=0.88, flicker=flicker)
            
        # 3. Scene 2 (3.8s – 8.8s): Soft Vada Badge
        if 3.8 <= t < 8.8:
            fade_in = min(1.0, (t - 3.8) / 0.4)
            alpha_val = int(255 * fade_in)
            vada_text = 'नरम और स्पंजी दही वड़ा'
            bbox = draw.textbbox((0, 0), vada_text, font=font_badge)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            bw = tw + 110
            bh = th + 28
            bx = (w - bw) // 2
            by = 160
            draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=24, fill=(24, 18, 14, int(220 * fade_in)), outline=(243, 201, 62, alpha_val), width=3)
            draw_star(draw, bx + 32, by + bh//2, 14, color=(243, 201, 62, alpha_val))
            draw.text((bx + 55, by + 10), vada_text, font=font_badge, fill=(243, 201, 62, alpha_val))
            draw_star(draw, bx + bw - 32, by + bh//2, 14, color=(243, 201, 62, alpha_val))
            
        # 4. Scene 4 (12.3s – 16.2s): Curd Card (when curd line plays!)
        if 12.3 <= t < 16.2:
            card_prog = min(1.0, (t - 12.3) / 0.35)
            cw, ch = 740, 160
            cx = (w - cw) // 2
            cy = int(220 + 40 * (1.0 - math.exp(-card_prog * 5.0)))
            draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=28, fill=(20, 16, 14, 230), outline=(243, 201, 62, 230), width=3)
            draw.text((cx + 40, cy + 26), 'दही (Sweet Beaten Curd)', font=font_card_title, fill=(243, 201, 62, 255))
            draw.text((cx + 40, cy + 96), 'गाढ़ा और मीठा फेंटा हुआ दही', font=font_card_sub, fill=(245, 240, 235, 240))
            
        # 5. Scene 5 Toppings Cards
        # 5A: Tamarind Chutney (16.5s – 18.7s)
        if 16.5 <= t < 18.7:
            card_prog = min(1.0, (t - 16.5) / 0.3)
            cw, ch = 700, 160
            cx = (w - cw) // 2
            cy = int(220 + 30 * (1.0 - math.exp(-card_prog * 5.0)))
            draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=28, fill=(24, 16, 12, 230), outline=(243, 201, 62, 230), width=3)
            draw.text((cx + 40, cy + 26), 'इमली चटनी', font=font_card_title, fill=(243, 201, 62, 255))
            draw.text((cx + 40, cy + 96), 'खट्टी-मीठी गाढ़ी सोंठ चटनी', font=font_card_sub, fill=(245, 240, 235, 240))
            
        # 5B: Mint Chutney (18.8s – 21.0s)
        elif 18.8 <= t < 21.0:
            card_prog = min(1.0, (t - 18.8) / 0.3)
            cw, ch = 700, 160
            cx = (w - cw) // 2
            cy = int(220 + 30 * (1.0 - math.exp(-card_prog * 5.0)))
            draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=28, fill=(16, 24, 14, 230), outline=(243, 201, 62, 230), width=3)
            draw.text((cx + 40, cy + 26), 'हरी चटनी', font=font_card_title, fill=(243, 201, 62, 255))
            draw.text((cx + 40, cy + 96), 'ताज़ा धनिया-पुदीना चटनी', font=font_card_sub, fill=(245, 240, 235, 240))
            
        # 5C: Roasted Cumin & Chaat Masala (21.1s – 23.3s)
        elif 21.1 <= t < 23.3:
            card_prog = min(1.0, (t - 21.1) / 0.3)
            cw, ch = 740, 160
            cx = (w - cw) // 2
            cy = int(220 + 30 * (1.0 - math.exp(-card_prog * 5.0)))
            draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=28, fill=(24, 18, 12, 230), outline=(243, 201, 62, 230), width=3)
            draw.text((cx + 40, cy + 26), 'भुना जीरा और चाट मसाला', font=font_card_title, fill=(243, 201, 62, 255))
            draw.text((cx + 40, cy + 96), 'शाही स्वाद और खुशबूदार मसाले', font=font_card_sub, fill=(245, 240, 235, 240))
            
        # 6. Scene 6 (25.2s – 28.0s): Festive Diwali Outro Card with vector stars
        if 25.2 <= t <= 28.0:
            prog_outro = min(1.0, (t - 25.2) / 0.4)
            ow, oh = 860, 240
            ox = (w - ow) // 2
            oy = int(240 + 40 * (1.0 - math.exp(-prog_outro * 5.0)))
            draw.rounded_rectangle([ox, oy, ox+ow, oy+oh], radius=32, fill=(28, 16, 10, int(235 * prog_outro)), outline=(255, 215, 60, int(255 * prog_outro)), width=4)
            
            t1 = 'शुभ दीपावली'
            b1 = draw.textbbox((0, 0), t1, font=font_outro_title)
            t1_w = b1[2] - b1[0]
            t1_x = ox + (ow - t1_w)//2
            draw_star(draw, t1_x - 45, oy + 70, 22, color=(255, 220, 80, 255))
            draw.text((t1_x, oy + 32), t1, font=font_outro_title, fill=(255, 220, 80, 255))
            draw_star(draw, t1_x + t1_w + 45, oy + 70, 22, color=(255, 220, 80, 255))
            
            t2 = 'दही वड़ा रेसिपी | सेव करें'
            b2 = draw.textbbox((0, 0), t2, font=font_outro_sub)
            t2_w = b2[2] - b2[0]
            draw.text((ox + (ow - t2_w)//2, oy + 135), t2, font=font_outro_sub, fill=(245, 240, 235, 255))
            
        # 7. Word-by-word Karaoke Captions at exactly 62% height (1190px)
        cap_y = 1190
        for cue_start, cue_end, words in caption_cues:
            if cue_start <= t <= cue_end:
                word_strings = [w_item[2] for w_item in words]
                w_widths = [draw.textbbox((0, 0), ws, font=font_cap)[2] - draw.textbbox((0, 0), ws, font=font_cap)[0] for ws in word_strings]
                space_w = draw.textbbox((0, 0), ' ', font=font_cap)[2] - draw.textbbox((0, 0), ' ', font=font_cap)[0]
                total_w = sum(w_widths) + space_w * (len(words) - 1)
                
                start_x = (w - total_w) // 2
                pad_x, pad_y = 28, 14
                
                draw.rounded_rectangle([start_x - pad_x, cap_y - pad_y, start_x + total_w + pad_x, cap_y + 64 + pad_y],
                                       radius=24, fill=(16, 12, 10, 225), outline=(243, 201, 62, 140), width=2)
                
                curr_x = start_x
                for (w_st, w_en, w_str), ww in zip(words, w_widths):
                    is_active = (w_st <= t <= w_en)
                    color = (243, 201, 62, 255) if is_active else (255, 255, 255, 255)
                    draw.text((curr_x + 2, cap_y + 2), w_str, font=font_cap, fill=(0, 0, 0, 230))
                    draw.text((curr_x, cap_y), w_str, font=font_cap, fill=color)
                    curr_x += ww + space_w
                break
                
        # 8. Festive Transitions (Light flare / glow wipes)
        for t_trans in [3.5, 9.0, 12.0, 16.5, 23.5]:
            if abs(t - t_trans) < 0.20:
                prog = 1.0 - abs(t - t_trans) / 0.20
                flare_alpha = int(190 * math.sin(prog * math.pi * 0.5))
                draw.rectangle([0, 0, w, h], fill=(255, 210, 90, flare_alpha))
                
        final_frame = Image.alpha_composite(base_img, overlay)
        pipe_out.stdin.write(final_frame.tobytes())
        
        if f % 240 == 0:
            print(f"Render progress: {f}/{total_frames} frames ({t:.1f}s / 28.0s)")
            
    pipe_in.stdout.close()
    pipe_in.wait()
    pipe_out.stdin.close()
    pipe_out.wait()
    print("ALL DONE: FLAWLESS DAHI VADA DIWALI REEL EXPORTED!")

if __name__ == "__main__":
    build_flawless_reel()
