import os
import math
import subprocess
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

def render_final():
    print("=== RENDERING FINAL 1080x1920 DAHI VADA REEL ===")

    w, h = 1080, 1920
    fps = 60
    total_frames = 1680  # 28.00 seconds

    c1 = 'Raw footage/WhatsApp Video 2026-11-10 at 3.29.41 PM.mp4'
    c2 = 'Raw footage/WhatsApp Video 2026-11-10 at 3.29.52 PM.mp4'
    os.makedirs('voice/temp_final', exist_ok=True)
    os.makedirs('Exports', exist_ok=True)

    # Warm color grade — same as preview
    vf_warm = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=60,colorbalance=rm=0.04:gm=0.01:bm=-0.03:rh=0.03:gh=0.01:bh=-0.03,eq=contrast=1.09:brightness=0.01:saturation=1.16,format=yuv420p'
    vf_warm_reframed = 'scale=1280:2276:force_original_aspect_ratio=increase,crop=1080:1920:(in_w-1080)/2:(in_h-1920)*0.18,setsar=1,fps=60,colorbalance=rm=0.04:gm=0.01:bm=-0.03:rh=0.03:gh=0.01:bh=-0.03,eq=contrast=1.09:brightness=0.01:saturation=1.16,format=yuv420p'
    vf_slow_warm = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,setpts=PTS/0.636363,fps=60,colorbalance=rm=0.04:gm=0.01:bm=-0.03:rh=0.03:gh=0.01:bh=-0.03,eq=contrast=1.09:brightness=0.01:saturation=1.16,format=yuv420p'

    print("Step 1: Extracting and grading base cuts at 1080x1920...")
    # 1. Hero 3.5s (from c1 @ 76.0s, reframed to crop phone stand)
    subprocess.run(['ffmpeg', '-y', '-ss', '76.0', '-t', '3.5', '-i', c1,
                    '-vf', vf_warm_reframed,
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    'voice/temp_final/f1.mp4'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  [1/8] Hero plating shot ✓")

    # 2. Vada slow-mo 5.5s (from c2 @ 22.0s, 0.636× speed)
    subprocess.run(['ffmpeg', '-y', '-ss', '22.0', '-t', '3.5', '-i', c2,
                    '-vf', vf_slow_warm,
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    'voice/temp_final/f2.mp4'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  [2/8] Spongy vada slow-mo ✓")

    # 3. Cutaway 3.0s: darkened blurred frame from real footage
    subprocess.run(['ffmpeg', '-y', '-ss', '76.5', '-i', c1,
                    '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                    '-vframes', '1', 'voice/temp_final/plate_raw.jpg'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    raw_plate = Image.open('voice/temp_final/plate_raw.jpg')
    blurred_plate = raw_plate.filter(ImageFilter.GaussianBlur(50))
    darkened_plate = ImageEnhance.Brightness(blurred_plate).enhance(0.38)

    cmd_f3 = ['ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo',
              '-s', '1080x1920', '-pix_fmt', 'rgb24', '-r', '60',
              '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
              '-pix_fmt', 'yuv420p', 'voice/temp_final/f3.mp4']
    proc_f3 = subprocess.Popen(cmd_f3, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    plate_arr = np.array(darkened_plate.convert('RGB'))
    for _ in range(180):  # 3.0s
        proc_f3.stdin.write(plate_arr.tobytes())
    proc_f3.stdin.close()
    proc_f3.wait()
    print("  [3/8] Darkened blurred cutaway ✓")

    # 4. Curd pour 4.5s (from c2 @ 30.0s)
    subprocess.run(['ffmpeg', '-y', '-ss', '30.0', '-t', '4.5', '-i', c2,
                    '-vf', vf_warm,
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    'voice/temp_final/f4.mp4'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  [4/8] Curd pour ✓")

    # 5A. Tamarind 2.3s (from c1 @ 8.0s)
    subprocess.run(['ffmpeg', '-y', '-ss', '8.0', '-t', '2.3', '-i', c1,
                    '-vf', vf_warm,
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    'voice/temp_final/f5a.mp4'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  [5/8] Tamarind drizzle ✓")

    # 5B. Mint 2.3s (from c1 @ 25.5s)
    subprocess.run(['ffmpeg', '-y', '-ss', '25.5', '-t', '2.3', '-i', c1,
                    '-vf', vf_warm,
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    'voice/temp_final/f5b.mp4'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  [6/8] Mint chutney ✓")

    # 5C. Spices 2.4s (from c1 @ 45.0s)
    subprocess.run(['ffmpeg', '-y', '-ss', '45.0', '-t', '2.4', '-i', c1,
                    '-vf', vf_warm,
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    'voice/temp_final/f5c.mp4'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  [7/8] Cumin & chaat masala ✓")

    # 6. Spoon bite 4.5s (from c1 @ 86.5s, reframed)
    subprocess.run(['ffmpeg', '-y', '-ss', '86.5', '-t', '4.5', '-i', c1,
                    '-vf', vf_warm_reframed,
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    'voice/temp_final/f6.mp4'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  [8/8] Hero spoon bite ✓")

    # Concatenate all base cuts
    segments = ['f1.mp4', 'f2.mp4', 'f3.mp4', 'f4.mp4', 'f5a.mp4', 'f5b.mp4', 'f5c.mp4', 'f6.mp4']
    with open('voice/temp_final/concat_list.txt', 'w') as f:
        for s in segments:
            f.write('file ' + s + '\n')
    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                    '-i', 'voice/temp_final/concat_list.txt',
                    '-c', 'copy', 'voice/temp_final/base_1080.mp4'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("\nStep 2: Base 1080x1920 video assembled!")

    # --- STEP 2: Composite typography, cards, captions, light leak ---
    print("\nStep 3: Compositing text overlays and captions at 1080x1920...")

    # Fonts — doubled from 540×960 preview
    font_badge = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 40, index=1)
    font_card_title = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 52, index=1)
    font_card_sub = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 34, index=0)
    font_cap = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 54, index=1)
    font_outro_title = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 68, index=1)
    font_outro_sub = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 42, index=0)

    # Caption cues — same timing as preview
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

    audio_path = 'voice/dahi_vada_hindi_narration.wav'
    out_final = 'Exports/Dahi_Vada_Recipe_Final_1080x1920.mp4'

    read_cmd = ['ffmpeg', '-i', 'voice/temp_final/base_1080.mp4',
                '-f', 'rawvideo', '-pix_fmt', 'rgba', '-']
    pipe_in = subprocess.Popen(read_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    write_cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo', '-vcodec', 'rawvideo',
        '-s', '1080x1920', '-pix_fmt', 'rgba', '-r', '60',
        '-i', '-',
        '-i', audio_path,
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
        '-c:a', 'aac', '-b:a', '256k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        out_final
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

        # 1. Scene 1 Top Badge (1.0s – 3.3s)
        if 1.0 <= t < 3.3:
            prog = min(1.0, (t - 1.0) / 0.4)
            badge_text = 'दीवाली स्पेशल'
            bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
            bw = bbox[2] - bbox[0] + 72
            bh = bbox[3] - bbox[1] + 32
            bx = (w - bw) // 2
            by = 160
            draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=28,
                                   fill=(20, 16, 12, int(210 * prog)),
                                   outline=(243, 201, 62, int(230 * prog)), width=3)
            draw.text((bx + 36, by + 12), badge_text, font=font_badge,
                      fill=(243, 201, 62, int(245 * prog)))

        # 2. Single soft light leak at intro cut (3.35s – 3.65s)
        if 3.35 <= t <= 3.65:
            leak_prog = 1.0 - abs(t - 3.50) / 0.15
            leak_alpha = int(140 * math.sin(leak_prog * math.pi * 0.5))
            draw.rectangle([0, 0, w, h], fill=(255, 215, 120, leak_alpha))

        # 3. Scene 2 Badge (3.8s – 8.8s)
        if 3.8 <= t < 8.8:
            prog = min(1.0, (t - 3.8) / 0.4)
            vada_text = 'नरम और स्पंजी दही वड़ा'
            bbox = draw.textbbox((0, 0), vada_text, font=font_badge)
            bw = bbox[2] - bbox[0] + 72
            bh = bbox[3] - bbox[1] + 32
            bx = (w - bw) // 2
            by = 160
            draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=28,
                                   fill=(20, 16, 12, int(210 * prog)),
                                   outline=(243, 201, 62, int(230 * prog)), width=3)
            draw.text((bx + 36, by + 12), vada_text, font=font_badge,
                      fill=(243, 201, 62, int(245 * prog)))

        # 4. Scene 3 Cutaway Cards (9.0s – 12.0s)
        if 9.0 <= t < 12.0:
            prog = min(1.0, (t - 9.0) / 0.35)
            # Ingredient card
            cw_card, ch_card = 760, 170
            cx = (w - cw_card) // 2
            cy = int(260 + 40 * (1.0 - math.exp(-prog * 5.0)))
            draw.rounded_rectangle([cx, cy, cx+cw_card, cy+ch_card], radius=32,
                                   fill=(18, 14, 12, 230),
                                   outline=(243, 201, 62, 220), width=3)
            draw.text((cx + 44, cy + 28), 'उड़द दाल (Urad Dal)', font=font_card_title,
                      fill=(243, 201, 62, 255))
            draw.text((cx + 44, cy + 100), 'धुली उड़द दाल का फूला हुआ बैटर', font=font_card_sub,
                      fill=(245, 240, 235, 240))

            # Tip card (appears at 9.5s)
            if t >= 9.5:
                prog_t = min(1.0, (t - 9.5) / 0.35)
                tw, th = 880, 120
                tx = (w - tw) // 2
                ty = int(490 + 30 * (1.0 - math.exp(-prog_t * 5.0)))
                draw.rounded_rectangle([tx, ty, tx+tw, ty+th], radius=28,
                                       fill=(35, 22, 12, 235),
                                       outline=(255, 215, 60, 220), width=3)
                draw.text((tx + 40, ty + 30), 'प्रो टिप: गुनगुने पानी में 10 मिनट भिगोएं',
                          font=font_badge, fill=(255, 235, 140, 255))

        # 5. Scene 4 Curd Card (12.3s – 16.2s)
        if 12.3 <= t < 16.2:
            prog = min(1.0, (t - 12.3) / 0.35)
            cw_card, ch_card = 760, 170
            cx = (w - cw_card) // 2
            cy = int(240 + 40 * (1.0 - math.exp(-prog * 5.0)))
            draw.rounded_rectangle([cx, cy, cx+cw_card, cy+ch_card], radius=32,
                                   fill=(18, 14, 12, 230),
                                   outline=(243, 201, 62, 220), width=3)
            draw.text((cx + 44, cy + 28), 'दही (Sweet Beaten Curd)', font=font_card_title,
                      fill=(243, 201, 62, 255))
            draw.text((cx + 44, cy + 100), 'गाढ़ा और मीठा फेंटा हुआ दही', font=font_card_sub,
                      fill=(245, 240, 235, 240))

        # 6. Toppings Cards
        # 5A: Tamarind (16.5s – 18.7s)
        if 16.5 <= t < 18.7:
            prog = min(1.0, (t - 16.5) / 0.3)
            cw_card, ch_card = 720, 170
            cx = (w - cw_card) // 2
            cy = int(240 + 30 * (1.0 - math.exp(-prog * 5.0)))
            draw.rounded_rectangle([cx, cy, cx+cw_card, cy+ch_card], radius=32,
                                   fill=(22, 14, 10, 230),
                                   outline=(243, 201, 62, 220), width=3)
            draw.text((cx + 44, cy + 28), 'इमली चटनी', font=font_card_title,
                      fill=(243, 201, 62, 255))
            draw.text((cx + 44, cy + 100), 'खट्टी-मीठी गाढ़ी सोंठ चटनी', font=font_card_sub,
                      fill=(245, 240, 235, 240))

        # 5B: Mint (18.8s – 21.0s)
        elif 18.8 <= t < 21.0:
            prog = min(1.0, (t - 18.8) / 0.3)
            cw_card, ch_card = 720, 170
            cx = (w - cw_card) // 2
            cy = int(240 + 30 * (1.0 - math.exp(-prog * 5.0)))
            draw.rounded_rectangle([cx, cy, cx+cw_card, cy+ch_card], radius=32,
                                   fill=(14, 20, 12, 230),
                                   outline=(243, 201, 62, 220), width=3)
            draw.text((cx + 44, cy + 28), 'हरी चटनी', font=font_card_title,
                      fill=(243, 201, 62, 255))
            draw.text((cx + 44, cy + 100), 'ताज़ा धनिया-पुदीना चटनी', font=font_card_sub,
                      fill=(245, 240, 235, 240))

        # 5C: Spices (21.1s – 23.3s)
        elif 21.1 <= t < 23.3:
            prog = min(1.0, (t - 21.1) / 0.3)
            cw_card, ch_card = 780, 170
            cx = (w - cw_card) // 2
            cy = int(240 + 30 * (1.0 - math.exp(-prog * 5.0)))
            draw.rounded_rectangle([cx, cy, cx+cw_card, cy+ch_card], radius=32,
                                   fill=(22, 16, 10, 230),
                                   outline=(243, 201, 62, 220), width=3)
            draw.text((cx + 44, cy + 28), 'भुना जीरा और चाट मसाला', font=font_card_title,
                      fill=(243, 201, 62, 255))
            draw.text((cx + 44, cy + 100), 'शाही स्वाद और खुशबूदार मसाले', font=font_card_sub,
                      fill=(245, 240, 235, 240))

        # 7. Outro Card (25.2s – 28.0s)
        if 25.2 <= t <= 28.0:
            prog = min(1.0, (t - 25.2) / 0.35)
            ow, oh = 860, 240
            ox = (w - ow) // 2
            oy = int(240 + 40 * (1.0 - math.exp(-prog * 5.0)))
            draw.rounded_rectangle([ox, oy, ox+ow, oy+oh], radius=36,
                                   fill=(24, 14, 10, int(230 * prog)),
                                   outline=(255, 215, 60, int(240 * prog)), width=3)

            t1 = 'शुभ दीपावली'
            b1 = draw.textbbox((0, 0), t1, font=font_outro_title)
            t1_w = b1[2] - b1[0]
            draw.text((ox + (ow - t1_w)//2, oy + 32), t1, font=font_outro_title,
                      fill=(255, 220, 80, 255))

            t2 = 'दही वड़ा रेसिपी | सेव करें'
            b2 = draw.textbbox((0, 0), t2, font=font_outro_sub)
            t2_w = b2[2] - b2[0]
            draw.text((ox + (ow - t2_w)//2, oy + 136), t2, font=font_outro_sub,
                      fill=(245, 240, 235, 255))

        # 8. Word-by-word Karaoke Captions at 62% height (y ≈ 1190px on 1920)
        cap_y = 1190
        for cue_start, cue_end, words in caption_cues:
            if cue_start <= t <= cue_end:
                word_strings = [w_item[2] for w_item in words]
                w_widths = [draw.textbbox((0, 0), ws, font=font_cap)[2] - draw.textbbox((0, 0), ws, font=font_cap)[0] for ws in word_strings]
                space_w = draw.textbbox((0, 0), ' ', font=font_cap)[2] - draw.textbbox((0, 0), ' ', font=font_cap)[0]
                total_w = sum(w_widths) + space_w * (len(words) - 1)

                start_x = (w - total_w) // 2
                pad_x, pad_y = 30, 16

                draw.rounded_rectangle(
                    [start_x - pad_x, cap_y - pad_y,
                     start_x + total_w + pad_x, cap_y + 68 + pad_y],
                    radius=24, fill=(16, 12, 10, 225),
                    outline=(243, 201, 62, 140), width=2)

                curr_x = start_x
                for (w_st, w_en, w_str), ww in zip(words, w_widths):
                    is_active = (w_st <= t <= w_en)
                    color = (243, 201, 62, 255) if is_active else (255, 255, 255, 255)
                    # Shadow
                    draw.text((curr_x + 2, cap_y + 2), w_str, font=font_cap, fill=(0, 0, 0, 230))
                    draw.text((curr_x, cap_y), w_str, font=font_cap, fill=color)
                    curr_x += ww + space_w
                break

        final_frame = Image.alpha_composite(base_img, overlay)
        pipe_out.stdin.write(final_frame.tobytes())

        if f % 120 == 0:
            pct = (f / total_frames) * 100
            print(f"  Compositing: {f}/{total_frames} frames ({pct:.0f}%) — {t:.1f}s / 28.0s")

    pipe_in.stdout.close()
    pipe_in.wait()
    pipe_out.stdin.close()
    pipe_out.wait()
    print("\n=== FINAL 1080x1920 RENDER COMPLETE ===")
    print("Output:", out_final)

if __name__ == "__main__":
    render_final()
