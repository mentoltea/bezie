import pygame
from curve import *
import functools
import itertools

pygame.init()

RUN = True
WIN_X = 1280
WIN_Y = 720

YX_RATIO = WIN_Y/WIN_X
XY_RATIO = WIN_X/WIN_Y

MAX = 3
SAMPLES = 200
SHIFT=Point2(1/2,1/2)

window = pygame.display.set_mode((WIN_X, WIN_Y))
clock = clock = pygame.time.Clock()
FPS = 60

def coord2uv(p: Point2) -> Point2:
    return Point2(p.x*YX_RATIO, -p.y)/MAX + SHIFT

def uv2coord(p: Point2) -> Point2:
    return Point2( (p.x - SHIFT.x)*MAX*XY_RATIO, -(p.y - SHIFT.y)*MAX )
    
def uv2xy(p: Point2) -> tuple[float, float]:
    return (
        p.x*WIN_X,
        p.y*WIN_Y
    )

def coord2xy(p: Point2) -> tuple[float, float]:
    return uv2xy(coord2uv(p))

def xy2coord(t: tuple[int,int]) -> Point2:
    (x,y) = t
    return Point2( (x/WIN_X - SHIFT.x)*MAX*XY_RATIO, -(y/WIN_Y - SHIFT.y)*MAX )

def xy2uv(t: tuple[int,int]) -> Point2:
    (x,y) = t
    return Point2(
        x/WIN_X,
        y/WIN_Y
    )

def draw_text(text, xy, size, surf = window, font = 'timesnewroman'):
    (x,y) = xy
    window.blit(pygame.font.Font(pygame.font.match_font('timesnewroman'), size).render(text,True,(0,0,0)), (x,y))

points = [ Point2(-1,1), Point2(2,0), Point2(1,-1), Point2(-3, -2)]
curves: list[BezieCurve2] = []
for perm in itertools.permutations(points):
    curves.append(BezieCurve2(list(perm)))


def draw_bcurve(surf: pygame.Surface, crv: BezieCurve2, pointclr=(0,0,255), lineclr=(255,0,0), width=2):
    for p in crv.points:
        pygame.draw.circle(surf, pointclr, uv2xy(coord2uv(p)), 4)
    
    for i in range(SAMPLES+1):
        t = i/SAMPLES
        p = crv(t)
        if (i>0):
            # pygame.draw.circle(window, (255,0,0), uv2xy(p+SHIFT), 2)
            pygame.draw.line(surf, lineclr, uv2xy(coord2uv(p)), uv2xy(coord2uv(pp)), width) # type: ignore
        pp: Point2 = p

def draw_basis(surf: pygame.Surface, crv: BezieCurve2, t: float, pointclr=(10,10,190), tangentclr=(10,10,190), normalclr=(190,140,10), width=3):
    p = crv(t)
    v = crv.tangent(t)
    n = crv.normal(t)
    
    pygame.draw.circle(surf, pointclr, coord2xy(p), 2)
    pygame.draw.line(surf, tangentclr, coord2xy(p), coord2xy(p+v), width)
    pygame.draw.line(surf, normalclr, coord2xy(p), coord2xy(p+n), width)

choosen = 1
t = 0
cooldown_choosen = 0
trans = False
while RUN:
    clock.tick(FPS)
    
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            RUN = False
            
        if event.type == pygame.MOUSEWHEEL:
            if (event.y > 0):
                MAX = max(0.2, MAX-0.3)
            elif (event.y < 0):
                MAX += 0.3
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not trans:
                trans = True
                old_mouse_pos = pygame.mouse.get_pos()
                old_shift = SHIFT
        if event.type == pygame.MOUSEBUTTONUP:
            trans = False
            diff = xy2uv(mouse_pos) - xy2uv(old_mouse_pos) 
            SHIFT = old_shift + diff

            
    
    if trans:
        diff = xy2uv(mouse_pos) - xy2uv(old_mouse_pos) 
        SHIFT = old_shift + diff
            
    if keys[pygame.K_UP]:
        MAX = max(0.2, MAX-0.1)
    elif keys[pygame.K_DOWN]:
        MAX += 0.1
    
    if cooldown_choosen==0:
        if keys[pygame.K_RIGHT]:
            choosen = (choosen + 1) % len(curves)
            t=0
            cooldown_choosen = 10
        elif keys[pygame.K_LEFT]:
            choosen = (choosen - 1) % len(curves)
            t=0
            cooldown_choosen = 10
    else:
        cooldown_choosen -= 1
            
    window.fill((255,255,255))
    # pygame.draw.line(window, (0,0,0), uv2xy(Point2(0, -1/2)+SHIFT), uv2xy(Point2(0, 1/2)+SHIFT))
    pygame.draw.line(window, (0,0,0), (SHIFT.x*WIN_X, 0), (SHIFT.x*WIN_X, WIN_Y))
    # pygame.draw.line(window, (0,0,0), uv2xy(Point2(-1/2, 0)+SHIFT), uv2xy(Point2(1/2, 0)+SHIFT))
    pygame.draw.line(window, (0,0,0), (0, SHIFT.y*WIN_Y), (WIN_X, SHIFT.y*WIN_Y))

    
    
    for c in curves:
        draw_bcurve(window, c, pointclr=(50,50,180), lineclr=(100,150,100))
    
    draw_bcurve(window, curves[choosen])
    draw_basis(window, curves[choosen], t)
    
    mp = xy2coord(mouse_pos)
    
    draw_text(f"{round(mp.x,1)} {round(mp.y,1)}", uv2xy(Point2(0.02, 0.96)), 20)
    draw_text(f"{round(MAX, 1)}", uv2xy(Point2(0.96, 0.96)), 20)
    
    t += 1/SAMPLES
    if (t>1):
        choosen = (choosen + 1) % len(curves)
        t=0
    
    pygame.display.update()