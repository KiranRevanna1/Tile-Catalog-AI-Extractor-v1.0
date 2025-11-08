import os, random
from PIL import Image, ImageDraw

# Create folders
base_dir = "datasets/tiles_demo"
for sub in ["images/train", "images/val", "labels/train", "labels/val"]:
    os.makedirs(os.path.join(base_dir, sub), exist_ok=True)

# Generate synthetic tile images
def make_tile(path, label_path):
    img = Image.new("RGB", (640, 640), (random.randint(150,255),)*3)
    draw = ImageDraw.Draw(img)

    # draw 2–5 rectangles as "tiles"
    for _ in range(random.randint(2,5)):
        x1, y1 = random.randint(50,400), random.randint(50,400)
        w, h = random.randint(100,200), random.randint(100,200)
        x2, y2 = x1+w, y1+h
        color = (random.randint(50,200), random.randint(50,200), random.randint(50,200))
        draw.rectangle([x1,y1,x2,y2], fill=color)
        # YOLO label: class 0, normalized bbox center x,y,w,h
        cx, cy = (x1+x2)/2/640, (y1+y2)/2/640
        bw, bh = w/640, h/640
        with open(label_path, "a") as f:
            f.write(f"0 {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n")

    img.save(path)

# generate ~20 train + 10 val images
for split, n in [("train",20), ("val",10)]:
    for i in range(n):
        img_path = f"{base_dir}/images/{split}/img_{i}.jpg"
        lbl_path = f"{base_dir}/labels/{split}/img_{i}.txt"
        make_tile(img_path, lbl_path)

print("✅ Synthetic tile dataset created at:", base_dir)
