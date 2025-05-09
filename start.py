import PIL
from PIL import Image
import algorithm
import webbrowser
import argparse
import os
from os import path

def get_outname(filename: str) -> str:
    if not path.exists(filename): return filename
    dot_idx = len(filename)-filename[::-1].find(".")
    fmt = filename[dot_idx:len(filename)]
    name = filename[0:dot_idx-1]
    
    i=1
    outname = name + f"_{i}" + "." + fmt
    while (path.exists(outname)):
        outname = name + f"_{i}" + "." + fmt
        i += 1
        
    return outname

def main(inname: str, outname: str = None):
    if outname==None:
        dot_idx = len(inname)-inname[::-1].find(".")
        fmt = inname[dot_idx:len(inname)]
        name = inname[0:dot_idx-1]
        outname = name + "_out" + "." + fmt
        
    outname = get_outname(outname)
    print(f"inname: {input}\noutname: {outname}")
    image = Image.open(inname).convert("RGBA")
    
    img = algorithm.alg(image)
    
    img = img.convert("RGB")
    
    img.show(outname)
    img.save(outname)
    # webbrowser.open(outname)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Args")
    
    parser.add_argument('input', type=str, help='Input image')
    parser.add_argument('-o', '--output', type=str, help='Output name')
    
    Args = parser.parse_args()
    
    input = Args.input
    output = Args.output
    
    main(input, output)