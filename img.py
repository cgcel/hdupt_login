# -*- coding: utf-8 -*-

from PIL import Image
import pytesseract


class MyImg(object):

    def __init__(self, img_name):

        img = self.img_convert(img_name)
        self.final_img = self.noise_remove_pil(img, 1.5)
        # self.final_img.show()

    # 图片灰度二值化
    def img_convert(self, img_name):

        # 打开原始图片
        im = Image.open(img_name)

        # 将原始图片灰度化
        grey_im = im.convert('L')

        # 打开灰度化图片并进行二值处理
        binary_im = grey_im.point(self.get_table(120), "1")

        return binary_im

    # 二值处理
    # 设定阈值threshold，像素值小于阈值，取值0，像素值大于阈值，取值1
    # 阈值具体多少需要多次尝试，不同阈值效果不一样
    def get_table(self, threshold=115):
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        return table

    # 8邻域降噪处理, k为判断阈值, 0<k<8
    def noise_remove_pil(self, image_name, k):

        def calculate_noise_count(img_obj, w, h):
            """
            计算邻域非白色的个数
            Args:
                img_obj: img obj
                w: width
                h: height
            Returns:
                count (int)
            """
            count = 0
            width, height = img_obj.size
            for _w_ in [w - 1, w, w + 1]:
                for _h_ in [h - 1, h, h + 1]:
                    if _w_ > width - 1:
                        continue
                    if _h_ > height - 1:
                        continue
                    if _w_ == w and _h_ == h:
                        continue
                    if img_obj.getpixel((_w_, _h_)) < 230:  # 这里因为是灰度图像，设置小于230为非白色
                        count += 1
            return count

        img = image_name
        # 灰度
        gray_img = img.convert('L')

        w, h = gray_img.size
        for _w in range(w):
            for _h in range(h):
                if _w == 0 or _h == 0:
                    gray_img.putpixel((_w, _h), 255)
                    continue
                # 计算邻域非白色的个数
                pixel = gray_img.getpixel((_w, _h))
                if pixel == 255:
                    continue

                if calculate_noise_count(gray_img, _w, _h) < k:
                    gray_img.putpixel((_w, _h), 255)
        # gray_img.show()
        return gray_img

    def get_str(self):
        # return input("str: ")
        return pytesseract.image_to_string(self.final_img).strip().replace(' ', '').replace('\n', '').replace('|', '')


if __name__ == '__main__':
    text = MyImg("image.png").get_str()
    print(text)
