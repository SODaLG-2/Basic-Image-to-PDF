from PIL import Image, ExifTags
import os

input_dir = './Input'
output_dir = './Output'

def converter(path):
    images = []
    for f in path:
        file_name, file_ext = os.path.splitext(f)
        img = Image.open(f)

        # Preserve orientation
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(img._getexif().items())
        
                # Ensure all images are RGB (PDF requires RGB mode)
        if file_ext.lower() in ['.jpg', '.jpeg','.png']:
            img = img.convert('RGB')

        if exif[orientation] == 3:
            img=img.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6:
            img=img.transpose(Image.ROTATE_270)
        elif exif[orientation] == 8:
            img=img.transpose(Image.ROTATE_90)

        images.append(img)

    pdf_path = os.path.join(output_dir, 'PDF conversion.pdf')

    # Save the images to a PDF
    images[0].save(
        pdf_path, "PDF", save_all=True, append_images=images[1:]
    )

if __name__ == "__main__":
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(input_dir, exist_ok=True)
    os.chdir(os.getcwd())
    pathway = [os.path.join(input_dir, i) for i in os.listdir(input_dir)]
    Pathway_sorted = sorted(filter(os.path.isfile, pathway), key=os.path.getatime)
    converter(Pathway_sorted)
