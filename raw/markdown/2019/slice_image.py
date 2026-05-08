from PIL import Image

img_path = '/Users/fang/projects/biobloom/raw/markdown/2019/images/question09_dnp_choices.png'
img = Image.open(img_path)
width, height = img.size
slice_height = height // 5

for i, label in enumerate(['A', 'B', 'C', 'D', 'E']):
    box = (0, i * slice_height, width, (i + 1) * slice_height)
    if i == 4:
        box = (0, i * slice_height, width, height)
    img.crop(box).save(f'/Users/fang/projects/biobloom/raw/markdown/2019/images/question09_choice{label}.png')

print("Done")
