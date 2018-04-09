#! /usr/bin/env python3

"""
>>> import os
>>> import tempfile
>>> red = "#FF0000"
>>> blue = "#0000FF"
>>> img = os.path.join(tempfile.gettempdir(), "test.img")
>>> xpm = os.path.join(tempfile.gettempdir(), "test.jpg")
>>> image = Image(10, 8, img)
>>> for x, y in ((0, 0), (0, 7), (1, 0), (1, 1), (1, 6), (1, 7), (2, 1),
...             (2, 2), (2, 5), (2, 6), (2, 7), (3, 2), (3, 3), (3, 4),
...             (3, 5), (3, 6), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4),
...             (5, 5), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (7, 1),
...             (7, 2), (7, 5), (7, 6), (7, 7), (8, 0), (8, 1), (8, 6),
...             (8, 7), (9, 0), (9, 7)):
...    image[x, y] = blue
>>> for x, y in ((3, 1), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2),
...             (6, 1)):
...    image[(x, y)] = red
>>> print(image.width, image.height, len(image.colors), image.background)
10 8 3 #FFFFFF
>>> border_color = "#FF0000" # red
>>> square_color = "#0000FF" # blue
>>> width, height = 240, 60
>>> midx, midy = width // 2, height // 2
>>> image = Image(width, height, img, "#F0F0F0")
>>> for x in range(width):
...     for y in range(height):
...         if x < 5 or x >= width - 5 or y < 5 or y >= height -5:
...             image[x, y] = border_color
...         elif midx - 20 < x < midx + 20 and midy - 20 < y < midy + 20:
...             image[x, y] = square_color
>>> print(image.width, image.height, len(image.colors), image.background)
240 60 3 #F0F0F0
>>> image.save()
>>> newimage = Image(1, 1, img)
>>> newimage.load()
>>> print(newimage.width, newimage.height, len(newimage.colors), newimage.background)
240 60 3 #F0F0F0
>>> image.export(xpm)
>>> image.thing
Traceback (most recent call last):
...
AttributeError: 'Image' object has no attribute 'thing'
>>> for name in (img, xpm):
...     try:
...         os.remove(name)
...     except EnvironmentError:
...         pass

"""
import os
import pickle


class ImageError(Exception):pass
class CoordinateError(ImageError):pass
class LoaderError(ImageError):pass
class SaveError(ImageError):pass
class ExportError(ImageError):pass
class NoFileNameError(ImageError):pass

class Image:

    def __init__(self, width, height, filename="", background="#FFFFFF"):
        self.__width = width
        self.__height = height
        self.filename = filename
        self.__background = background
        self.__data = {}
        self.__colors = {self.__background}

    @property
    def background(self):
        return self.__background

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def colors(self):
        return self.__colors

    def __getitem__(self, coordinate):
        """
        return the coordinate of identyfied
        :param coordinate:coordinate
        :return: color,if not set colors,return backgroud
        """
        assert len(coordinate) == 2, "coordinate should be 2-values"
        if (not (0 < coordinate[0] < self.width) or
            not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        return self.__data.get(tuple(coordinate),self.__background)

    def __setitem__(self, coordinate, color):
        """
        set the color to the specified coordinate
        :param coordinate:
        :param color:
        :return:
        """
        assert len(coordinate) == 2, "coordinate should be 2-values"
        if( not (0 <= coordinate[0] <= self.width) or
            not (0 <= coordinate[1] <= self.height)):
            raise CoordinateError(str(coordinate))
        if color == self.__background:
            self.__data.pop(tuple(coordinate),None)
        else:
            self.__data[tuple(coordinate)] =color
            self.colors.add(color)

    def __delitem__(self, coordinate):
        """
        delete a item
        :param coordinate:
        :return:
        """
        assert len(coordinate) == 2, "coordinate should be 2-values"
        if (not (0 <= coordinate[0] <= self.width) or
                not (0 <= coordinate[1] <= self.height)):
            raise CoordinateError(str(coordinate))
        self.__data.pop(tuple(coordinate),None)

    def save(self,filename=None):
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFileNameError()

        fh = None
        try:
            data = [self.width,self.height,self.__background,self.__data]
            fh = open(self.filename,"wb")
            pickle.dump(data,fh,pickle.HIGHEST_PROTOCOL)
        except(EnvironmentError,pickle.PicklingError) as err:
            raise SaveError(str(err))
        finally:
            if fh is not None:
                fh.close()

    def load(self,filename=None):
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFileNameError

        fh = None
        try:
            fh = open(self.filename,"rb")
            data = pickle.load(fh)
            (self.__width,self.__height,self.__background,self.__data) = data
            self.__colors = (set(self.__data.values()) | {self.__background})
        except(EnvironmentError,pickle.UnpicklingError) as err:
            raise LoaderError(str(err))
        finally:
            if fh is not None:
                fh.close()

    def export(self,filename):
        if filename.lower().endswith(".jpg"):
            self.__export_jpg(filename)
        else:
            raise ExportError("Unsupported export format:"+os.path.splitext(filename)[1])

    def __export_jpg(self, filename):
        """Exports the image as an XPM file if less than 8930 colors are
        used
        """
        name = os.path.splitext(os.path.basename(filename))[0]
        count = len(self.__colors)
        chars = [chr(x) for x in range(32, 127) if chr(x) != '"']
        if count > len(chars):
            chars = []
            for x in range(32, 127):
                if chr(x) == '"':
                    continue
                for y in range(32, 127):
                    if chr(y) == '"':
                        continue
                    chars.append(chr(x) + chr(y))
        chars.reverse()
        if count > len(chars):
            raise ExportError("cannot export XPM: too many colors")
        fh = None
        try:
            fh = open(filename, "w", encoding="ascii")
            fh.write("/* XPM */\n")
            fh.write("static char *{0}[] = {{\n".format(name))
            fh.write("/* columns rows colors chars-per-pixel */\n")
            fh.write('"{0.width} {0.height} {1} {2}",\n'.format(
                     self, count, len(chars[0])))
            char_for_colour = {}
            for color in self.__colors:
                char = chars.pop()
                fh.write('"{char} c {color}",\n'.format(**locals()))
                char_for_colour[color] = char
            fh.write("/* pixels */\n")
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    color = self.__data.get((x, y), self.__background)
                    row.append(char_for_colour[color])
                fh.write('"{0}",\n'.format("".join(row)))
            fh.write("};\n")
        except EnvironmentError as err:
            raise ExportError(str(err))
        finally:
            if fh is not None:
                fh.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()



