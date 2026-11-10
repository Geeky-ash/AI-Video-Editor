import os
import math
import subprocess
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def build_final_reel():
    print("=== STARTING FINAL DAHI VADA DIWALI REEL RENDER ===")
    
    w, h = 1080, 1920
    fps = 60
    total_frames = 1680 # exactly 28.00 seconds
    
    # Fonts
    font_badge = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 38, index=1)
    font_card_title = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 52, index=1)
    font_card_sub = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 34, index=0)
    font_cap = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 54, index=1)
    font_outro_title = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 68, index=1)
    font_outro_sub = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 42, index=0)
    
    # 1. Base video: voice/temp_render/base_28s.mp4
    base_video = 'voice/temp_render/base_28s.mp4'
    if not os.path.exists(base_video):
        raise FileNotFoundError(f"Missing base video: {base_video}")
        
    # 2. Master audio: voice/temp_render/master_audio_28s.wav
    master_audio = 'voice/temp_render/master_audio_28s.wav'
    if not os.path.exists(master_audio):
        raise FileNotFoundError(f"Missing master audio: {master_audio}")
        
    # Output file
    os.makedirs('Exports', exist_ok=True)
    out_mp4 = 'Exports/Dahi_Vada_Recipe_Diwali_Reel.mp4'
    
    # Pre-generate 45 floating sparkle particles
    np.random.seed(108)
    particles = []
    for _ in range(50):
        particles.append({
            'x': np.random.uniform(40, w - 40),
            'y': np.random.uniform(50, h - 50),
            'speed': np.random.uniform(1.2, 3.5),
            'size': np.random.uniform(3, 7),
            'phase': np.random.uniform(0, math.pi * 2)
        })
        
    # Define caption cues with word-level start and end times
    caption_cues = [
        # Cue 0A
        (0.20, 1.80, [
            (0.20, 0.70, "दिवाली"),
            (0.70, 1.00, "आ"),
            (1.00, 1.45, "रही"),
            (1.45, 1.80, "है,")
        ]),
        # Cue 0B
        (1.80, 3.78, [
            (1.80, 2.25, "मिठाइयों"),
            (2.25, 2.45, "के"),
            (2.45, 2.80, "साथ"),
            (2.80, 3.05, "कुछ"),
            (3.05, 3.45, "चटपटा"),
            (3.45, 3.65, "बनता"),
            (3.65, 3.78, "है!")
        ]),
        # Cue 1A
        (4.20, 6.20, [
            (4.20, 4.55, "आज"),
            (4.55, 4.95, "बनाते"),
            (4.95, 5.25, "हैं"),
            (5.25, 5.70, "नरम,"),
            (5.70, 6.20, "मुलायम")
        ]),
        # Cue 1B
        (6.20, 8.59, [
            (6.20, 6.60, "दही"),
            (6.60, 7.10, "वड़ा,"),
            (7.10, 7.60, "थाली"),
            (7.60, 7.85, "की"),
            (7.85, 8.30, "शान"),
            (8.30, 8.59, "है।")
        ]),
        # Cue 2A
        (9.20, 11.20, [
            (9.20, 9.60, "उड़द"),
            (9.60, 10.00, "दाल"),
            (10.00, 10.25, "के"),
            (10.25, 10.70, "वड़े"),
            (10.70, 11.20, "तलिए,")
        ]),
        # Cue 2B
        (11.20, 13.00, [
            (11.20, 11.75, "गुनगुने"),
            (11.75, 12.15, "पानी"),
            (12.15, 12.40, "में"),
            (12.40, 13.00, "भिगोइए,")
        ]),
        # Cue 2C
        (13.00, 14.70, [
            (13.00, 13.30, "फिर"),
            (13.30, 13.70, "फेंटा"),
            (13.70, 14.00, "हुआ"),
            (14.00, 14.35, "दही"),
            (14.35, 14.70, "डालिए।")
        ]),
        # Cue 3A
        (16.50, 18.80, [
            (16.50, 16.85, "ऊपर"),
            (16.85, 17.15, "से"),
            (17.15, 17.65, "मीठी"),
            (17.65, 18.20, "इमली"),
            (18.20, 18.80, "चटनी,")
        ]),
        # Cue 3B
        (18.80, 20.80, [
            (18.80, 19.40, "तीखी"),
            (19.40, 20.00, "हरी"),
            (20.00, 20.80, "चटनी,")
        ]),
        # Cue 3C
        (20.80, 22.48, [
            (20.80, 21.20, "भुना"),
            (21.20, 21.55, "जीरा"),
            (21.55, 21.75, "और"),
            (21.75, 22.10, "चाट"),
            (22.10, 22.48, "मसाला!")
        ]),
        # Cue 4A
        (23.50, 25.40, [
            (23.50, 23.75, "इस"),
            (23.75, 24.25, "दिवाली"),
            (24.25, 24.80, "मेहमानों"),
            (24.80, 25.00, "को"),
            (25.00, 25.40, "खिलाइए!")
        ]),
        # Cue 4B
        (25.40, 27.29, [
            (25.40, 25.75, "दही"),
            (25.75, 26.10, "वड़ा"),
            (26.10, 26.50, "रेसिपी"),
            (26.50, 26.80, "सेव"),
            (26.80, 27.00, "कर"),
            (27.00, 27.29, "लीजिए!")
        ])
    ]

    # Pre-render Diya Graphic onto RGBA template
    def draw_diya(draw_target, cx, cy, scale=1.0, flicker=1.0):
        # Base brass diya body
        bw = int(140 * scale)
        bh = int(80 * scale)
        draw_target.ellipse([cx - bw, cy, cx + bw, cy + bh], fill=(195, 130, 30, 255), outline=(255, 220, 80, 255), width=int(4*scale))
        draw_target.ellipse([cx - int(115*scale), cy + int(6*scale), cx + int(115*scale), cy + int(50*scale)], fill=(140, 80, 15, 255), outline=(230, 180, 50, 255), width=int(2*scale))
        
        # Flame
        flame_h = int(105 * scale * flicker)
        fw = int(26 * scale)
        flame_pts = [
            (cx, cy - flame_h),
            (cx + fw, cy - flame_h//2),
            (cx + int(fw*0.7), cy - int(10*scale)),
            (cx - int(fw*0.7), cy - int(10*scale)),
            (cx - fw, cy - flame_h//2)
        ]
        draw_target.polygon(flame_pts, fill=(255, 205, 50, 255))
        inner_pts = [
            (cx, cy - flame_h + int(22*scale)),
            (cx + int(fw*0.5), cy - flame_h//2 + int(8*scale)),
            (cx + int(fw*0.3), cy - int(10*scale)),
            (cx - int(fw*0.3), cy - int(10*scale)),
            (cx - int(fw*0.5), cy - flame_h//2 + int(8*scale))
        ]
        draw_target.polygon(inner_pts, fill=(255, 255, 220, 255))

    # FFmpeg reader for base_video
    read_cmd = [
        'ffmpeg', '-i', base_video,
        '-f', 'rawvideo',
        '-pix_fmt', 'rgba',
        '-'
    ]
    pipe_in = subprocess.Popen(read_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    # FFmpeg writer for final composited video
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
            # End of base stream, stop
            break
            
        base_img = Image.frombytes('RGBA', (w, h), raw_base)
        overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # 1. Floating Diwali Sparkle Particles
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
            
            # Top Badge
            badge_text = '✨ दीवाली स्पेशल ✨'
            bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
            bw = bbox[2] - bbox[0] + 56
            bh = bbox[3] - bbox[1] + 24
            bx = (w - bw) // 2
            by = 160
            draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=24, fill=(28, 18, 12, int(220 * fade_in)), outline=(243, 201, 62, alpha_val), width=3)
            draw.text((bx + 28, by + 10), badge_text, font=font_badge, fill=(243, 201, 62, alpha_val))
            
            # Bottom Glowing Diya
            flicker = 1.0 + 0.08 * math.sin(f * 0.3)
            draw_diya(draw, 540, 1560, scale=0.85, flicker=flicker)
            
        # 3. Scene 2 (3.5s – 8.8s): Soft Vada Badge
        if 3.8 <= t < 8.8:
            fade_in = min(1.0, (t - 3.8) / 0.4)
            alpha_val = int(255 * fade_in)
            vada_text = 'नरम और स्पंजी वड़ा 🪔'
            bbox = draw.textbbox((0, 0), vada_text, font=font_badge)
            bw = bbox[2] - bbox[0] + 54
            bh = bbox[3] - bbox[1] + 24
            bx = (w - bw) // 2
            by = 160
            draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=24, fill=(24, 18, 14, int(220 * fade_in)), outline=(243, 201, 62, alpha_val), width=3)
            draw.text((bx + 27, by + 10), vada_text, font=font_badge, fill=(243, 201, 62, alpha_val))
            
        # 4. Scene 4 (12.3s – 16.2s): Curd Card (when curd line plays!)
        if 12.3 <= t < 16.2:
            card_prog = min(1.0, (t - 12.3) / 0.35)
            cw, ch = 720, 160
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
            
        # 6. Scene 6 (25.2s – 28.0s): Festive Diwali Outro Card
        if 25.2 <= t <= 28.0:
            prog_outro = min(1.0, (t - 25.2) / 0.4)
            ow, oh = 860, 240
            ox = (w - ow) // 2
            oy = int(240 + 40 * (1.0 - math.exp(-prog_outro * 5.0)))
            draw.rounded_rectangle([ox, oy, ox+ow, oy+oh], radius=32, fill=(28, 16, 10, int(235 * prog_outro)), outline=(255, 215, 60, int(255 * prog_outro)), width=4)
            
            # Outro text
            t1 = '✨ शुभ दीपावली! 🪔'
            b1 = draw.textbbox((0, 0), t1, font=font_outro_title)
            t1_w = b1[2] - b1[0]
            draw.text((ox + (ow - t1_w)//2, oy + 32), t1, font=font_outro_title, fill=(255, 220, 80, 255))
            
            t2 = 'दही वड़ा रेसिपी 🔖 सेव करें'
            b2 = draw.textbbox((0, 0), t2, font=font_outro_sub)
            t2_w = b2[2] - b2[0]
            draw.text((ox + (ow - t2_w)//2, oy + 130), t2, font=font_outro_sub, fill=(245, 240, 235, 255))
            
        # 7. Word-by-word Karaoke Captions at exactly 62% height (1190px)
        cap_y = 1190
        for cue_start, cue_end, words in caption_cues:
            if cue_start <= t <= cue_end:
                # Calculate widths of words
                word_strings = [w_item[2] for w_item in words]
                w_widths = [draw.textbbox((0, 0), ws, font=font_cap)[2] - draw.textbbox((0, 0), ws, font=font_cap)[0] for ws in word_strings]
                space_w = draw.textbbox((0, 0), ' ', font=font_cap)[2] - draw.textbbox((0, 0), ' ', font=font_cap)[0]
                total_w = sum(w_widths) + space_w * (len(words) - 1)
                
                start_x = (w - total_w) // 2
                pad_x, pad_y = 28, 14
                
                # Dark pill backdrop
                draw.rounded_rectangle([start_x - pad_x, cap_y - pad_y, start_x + total_w + pad_x, cap_y + 64 + pad_y],
                                       radius=24, fill=(16, 12, 10, 225), outline=(243, 201, 62, 140), width=2)
                
                curr_x = start_x
                for (w_st, w_en, w_str), ww in zip(words, w_widths):
                    # Active word check
                    is_active = (w_st <= t <= w_en)
                    color = (243, 201, 62, 255) if is_active else (255, 255, 255, 255)
                    
                    # Shadow
                    draw.text((curr_x + 2, cap_y + 2), w_str, font=font_cap, fill=(0, 0, 0, 230))
                    draw.text((curr_x, cap_y), w_str, font=font_cap, fill=color)
                    curr_x += ww + space_w
                break # Only one cue at a time
                
        # 8. Transitions (Light flare / glow wipes)
        # T1 @ 3.5s, T2 @ 9.0s, T3 @ 12.0s, T4 @ 16.5s, T5 @ 23.5s
        for t_trans in [3.5, 9.0, 12.0, 16.5, 23.5]:
            if abs(t - t_trans) < 0.20:
                prog = 1.0 - abs(t - t_trans) / 0.20
                flare_alpha = int(190 * math.sin(prog * math.pi * 0.5))
                # Additive golden bloom
                draw.rectangle([0, 0, w, h], fill=(255, 210, 90, flare_alpha))
                
        # Composite overlay onto base frame
        final_frame = Image.alpha_composite(base_img, overlay)
        pipe_out.stdin.write(final_frame.tobytes())
        
        if f % 120 == 0:
            print(f"Render progress: {f}/{total_frames} frames ({t:.1f}s / 28.0s)")
            
    pipe_in.stdout.close()
    pipe_in.wait()
    pipe_out.stdin.close()
    pipe_out.wait()
    print("ALL FRAMES COMPOSITED AND ENCODED!")

if __name__ == "__main__":
    build_final_reel()
