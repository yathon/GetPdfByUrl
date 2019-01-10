import os
import re
import time

import PIL.ExifTags
import PIL.Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Image


def img_search(mypath, filenames):
    for lists in os.listdir(mypath):
        path = os.path.join(mypath, lists)
        if os.path.isfile(path):
            expression = r'[\w]+\.(jpg|png|jpeg)$'
            if re.search(expression, path, re.IGNORECASE):
                filenames.append(path)
        elif os.path.isdir(path):
            img_search(path, filenames)


def img_search1(mypath, filenames):
    for lists in os.listdir(mypath):
        path = os.path.join(mypath, lists)
        if os.path.isfile(path):
            a = path.split('.')
            if a[-1] in ['jpg', 'png', 'JPEG']:
                filenames.append(path)
        elif os.path.isdir(path):
            img_search1(path, filenames)


def rotate_img_to_proper(image):
    try:
        orientation = 0
        # image = Image.open(filename)
        if hasattr(image, '_getexif'):  # only present in JPEGs
            for orientation in PIL.ExifTags.TAGS.keys():
                if PIL.ExifTags.TAGS[orientation] == 'Orientation':
                    break
            e = image._getexif()  # returns None if no EXIF data
            if e is not None:
                # log.info('EXIF data found: %r', e)
                exif = dict(e.items())
                orientation = exif[orientation]
                # print('found, ',orientation)

                if orientation == 3:
                    image = image.transpose(Image.ROTATE_180)
                elif orientation == 6:
                    image = image.transpose(Image.ROTATE_270)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
    except:
        pass
    return image


def main():
    output_file_name = 'out.pdf'
    # doc = SimpleDocTemplate(save_file_name, pagesize=A1,
    #                     rightMargin=72, leftMargin=72,
    #                     topMargin=72, bottomMargin=18)
    img_doc = canvas.Canvas(output_file_name)  # pagesize=letter
    img_doc.setPageSize(A4)
    document_width, document_height = A4
    mypath = input('Input the image folder please:')
    filenames = []
    start = time.clock()
    img_search(mypath, filenames)
    end = time.clock()
    print('run time: ', end - start, 'find: ', len(filenames))
    # for f in filenames:
    #     print(f)
    for image in filenames:
        try:
            image_file = PIL.Image.open(image)
            image_file = rotate_img_to_proper(image_file)

            image_width, image_height = image_file.size
            print(image_file.size)
            if not (image_width > 0 and image_height > 0):
                raise Exception
            image_aspect = image_height / float(image_width)
            # Determins the demensions of the image in the overview
            print_width = document_width
            print_height = document_width * image_aspect
            img_doc.drawImage(ImageReader(image_file), document_width - print_width,
                              document_height - print_height, width=print_width,
                              height=print_height, preserveAspectRatio=True)
            # inform the reportlab we want a new page
            img_doc.showPage()
            img_doc.save()
        except Exception as e:
            print('error:', e, image)
    print('Done')


# story=[]
# #story.append('1.jpg')
# story.append(Image('1.jpg'),preserveAspectRatio=True)
# doc.build(story)
if __name__ == '__main__':
    main()
