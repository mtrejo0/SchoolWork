#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as PILImage

## NO ADDITIONAL IMPORTS ALLOWED!

class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels

    def get_pixel(self, x, y):
        if(x < 0 and y < 0 ):
            return self.pixels[0]

        elif(x >= self.width and y >= self.height ):
            return self.pixels[(self.height-1)*self.width + self.width-1]

        elif(y < 0 and x >= self.width):
            return self.pixels[self.width-1]

        elif(x < 0 and y >= self.height):
            return self.pixels[(self.height-1)*self.width]

        elif(x < 0):
            return self.pixels[y*self.width]

        elif(x >= self.width):
            return self.pixels[y*self.width + self.width-1]

        elif(y < 0):
            return self.pixels[x]

        elif(y >= self.height):
            return self.pixels[(self.height-1)*self.width + x]

        else:
            return self.pixels[y*self.width + x]
       

    def set_pixel(self, x, y, c):
        self.pixels[y*self.width + x] = c

    def apply_per_pixel(self, func):
        result = Image.new(self.width, self.height)
        for x in range(result.width):
            for y in range(result.height):
                color = self.get_pixel(x, y)
                newcolor = func(color)
                result.set_pixel(x, y, newcolor)
        return result

    def correlation(self,k):
        result = Image.new(self.width, self.height)


        for x in range(self.width):
            for y in range(self.height):
                res = 0
                for i in range(len(k)):
                    for j in range(len(k)):
                        res+=self.get_pixel(x-len(k)//2+j, y-len(k)//2+i)*k[i][j]

                #clip
                if(res<0):
                    res = 0
                elif(res>255):
                    res = 255
                result.set_pixel(x, y, round(res))
        return result

    def correlationNotRounded(self,k):
        result = Image.new(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                res = 0
                for i in range(len(k)):
                    for j in range(len(k)):
                        res+=self.get_pixel(x-len(k)//2+j, y-len(k)//2+i)*k[i][j]
                result.set_pixel(x, y, res)
        return result

    def inverted(self):
        return self.apply_per_pixel(self.subtract)
    def subtract(self,x):
        return 255-x


    def blurred(self, n):
        kern = []
        for i in range(n):
            l = []
            for j in range(n):
                l +=[1/(n**2)]
            kern+=[l]
        return self.correlation(kern)


    def sharpened(self,n):
        blur = self.blurred(n)
        
        result = Image.new(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                pix = self.get_pixel(x,y)
                res = pix*2 - blur.get_pixel(x,y)
                
                if(res<0):
                    res = 0
                elif(res>255):
                    res = 255
                result.set_pixel(x, y, round(res))
        return result

    def brute_sharpened(self,n):
        blur = self.blurred(n)
        result = Image.new(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                pix = get_pixel(x,y)
                res = pix*2 - blur.get_pixel(x,y)

                #clip
                if(res<0):
                    res = 0
                elif(res>255):
                    res = 255
                result.set_pixel(x, y, round(res))

        return result

    def edges(self):

        k_1 = [[-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1]]


        k_2 =  [[-1, -2, -1],
                [0, 0, 0],
                [1, 2, 1]]
        
        a = self.correlationNotRounded(k_1)
        b = self.correlationNotRounded(k_2)


        result = Image.new(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                res = ( a.get_pixel(x,y)**2 + b.get_pixel(x,y)**2  )**.5

                if(res<0):
                    res = 0
                elif(res>255):
                    res = 255

                result.set_pixel(x, y, round(res))
        return result



    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    def __repr__(self):
        return "Image(%s, %s, %s)" % (self.width, self.height, self.pixels)

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))

        # when the window is closed, the program should stop
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()
    def reafter():
        tcl.after(500,reafter)
    tcl.after(500,reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    
    
    i = Image.load("ricky.PNG")
    i =i.inverted()
    i.show()
    i =i.edges()
    i.show()
    i.save("profile.png")


    
    



    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
