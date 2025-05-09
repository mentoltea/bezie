import PIL
from PIL import Image, ImageDraw, ImageDraw2
from basic import *
from curve import *
from settings import *
import random
from threading import Thread

def get_pixel_at(img: Image.Image, x:int, y:int) -> Pixel:
    color = img.getpixel((x,y))
    clr = Color3(color)
    return Pixel(clr, Point2(x,y))

def get_pixel_from_pixels(pixels, x:int, y:int) -> Pixel:
    color = pixels[x,y]
    clr = Color3(color)
    return Pixel(clr, Point2(x,y))

def get_color_at_uv(img: Image.Image, p: Point2) -> Color4:
    (x,y) = uv2xy(img, p)
    clr = img.getpixel((x,y))
    if len(clr)==3:
        clr = unit(clr, tuple(255))
    return Color4(clr)

def get_color_at_uv_pixels(pixels, sizex, sizey, p: Point2) -> Color4:
    x = constrain(int(p.x*sizex), 0, sizex-1)
    y = constrain(int(p.y*sizey), 0, sizey-1)
    clr = pixels[x, y]
    if len(clr)==3:
        clr = unit(clr, tuple(255))
    return Color4(clr)

def color4t3(clr: Color4) -> Color3:
    return Color3((clr.r, clr.b, clr.b))*clr.a/255

def uv2xy(img: Image.Image, p: Point2) -> tuple[int, int]:
    (sizex, sizey) = img.size
    x = constrain(int(p.x*sizex), 0, sizex-1)
    y = constrain(int(p.y*sizey), 0, sizey-1)
    return (x, y)

def xy2uv(img: Image.Image, t: tuple[int,int]) -> Point2:
    (sizex, sizey) = img.size
    return Point2(t[0]/sizex, t[1]/sizey)

def unit(t1: tuple, t2: tuple) -> tuple:
    return tuple(list(t1) + list(t2))

def random_clr4_nrm() -> Color4:
    return Color4((random.random(), random.random(), random.random(), random.random()))

def random_point2_nrm() -> Point2:
    return Point2(random.random(), random.random())

# from -1/2 to 1/2
def random_vec2_nrm() -> Vector2:
    return random_point2_nrm() - Vector2(1/2,1/2)

def get_color_from_crv(img: Image.Image, crv: Curve2, SAMPLES:int=100) -> Color4:
    sumcolor = Color4((0,0,0,255))
    for i in range(SAMPLES+1):
        t = i/SAMPLES
        p = crv(t)
        color = get_color_at_uv(img, p)
        sumcolor += color
    sumcolor = sumcolor/SAMPLES
    return sumcolor

def get_color_from_crv_pixels(pixels, sizex, sizey, crv: Curve2, SAMPLES:int=100) -> Color4:
    sumcolor = Color4((0,0,0,255))
    for i in range(SAMPLES+1):
        t = i/SAMPLES
        p = crv(t)
        color = get_color_at_uv_pixels(pixels, sizex, sizey, p)
        sumcolor += color
    sumcolor = sumcolor/SAMPLES
    return sumcolor

def draw_curve(img: Image.Image, draw: ImageDraw.ImageDraw, crv: Curve2, clr: Color4, width: int, SAMPLES:int=100):
    pp: Point2 = crv(0)
    # draw = ImageDraw.Draw(img)
    for i in range(SAMPLES+1):
        t = i/SAMPLES
        p = crv(t)
        if (i>0):
            # draw line
            color = (get_color_at_uv(img, p) + clr)/2 + random_clr4_nrm()*10
            draw.line( unit(uv2xy(img, pp), uv2xy(img, p)), tuple(color.normalize255()), width, joint="curve") 
        pp: Point2 = p

def collect_curves_func(original_pixels, sizex, sizey, curves: list[tuple[Curve2, Color4]], count:int, allcount: int, num:int):
    for n in range(count):
        if (n%1000==0):
            print(f"COLLECTING {num}: {n}/{count}")
        p0 = random_point2_nrm()
        p1 = p0 + random_vec2_nrm()*MAX_ENDPIXEL_DEVIATION*2
        p2 = p1 + random_vec2_nrm()*MAX_ENDPIXEL_DEVIATION*2
        p3 = p0 + random_vec2_nrm()*MAX_ENDPIXEL_DEVIATION
        curve = BezieCurve2([p0, p1, p2, p3])
        color = get_color_from_crv_pixels(original_pixels, sizex, sizey, curve)
        curves.append( (curve, color) )

def alg(original: Image.Image) -> Image.Image:
    modified = Image.new("RGBA", original.size)
    (xsize, ysize) = modified.size
    modified.paste((255,255,255), (0,0,xsize,ysize))
    draw = ImageDraw.Draw(modified)
    
    original_pixels = original.load()
    
    CURVE_COUNT = (xsize*ysize)//(10*10) *CURVE_COUNT_PER_10x10
    curves: list[tuple[Curve2, Color4]] = []
    
    CURVES_PER_THREAD = CURVE_COUNT//THREADS_COUNT
    collecting_threads: list[Thread] = []
    for i in range(THREADS_COUNT):
        collecting_threads.append (
            Thread (
                target= collect_curves_func,
                args= (original_pixels, xsize, ysize, curves, CURVES_PER_THREAD, CURVE_COUNT, i),
                daemon= True
            )
        )
    
    for t in collecting_threads:
        t.start()
    
    for t in collecting_threads:
        t.join()
    
    n=0
    for (crv, clr) in curves:
        if (n%1000==0):
            print(f"DRAWING: {n}/{CURVE_COUNT}")
        draw_curve(modified, draw, crv, clr, 1+int(round(random.random()*MAX_WIDTH_DEVIATION)))
        n+=1
    
    return modified        
            
        