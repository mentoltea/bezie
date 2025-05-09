# Idea
This algorithm draws image from scratch with various Bezie curves (3rd order). 

## Collecting
It takes random start points, random middle points in range `2*MAX_ENDPIXEL_DEVIATION` of previous one and endpoint in range `MAX_ENDPIXEL_DEVIATION` of the starting one. After creating curve, the avarage color along this curve is computed.
This stage can be distributed among number of threads (although it does not improve perfomance).

## Drawing
Curves are sequentially drawn on a white board. The curves has transparency and during the drawing final color is determined based on computed color along the curve of original image, color along the curve on image being modified (making one curve 'lay' on the other) and little random deviation.

# Usage
## Settings
Settings are defined in `settings.py`:
- `CURVE_COUNT_PER_10x10`   -   number of curves per block 10x10
- `MAX_ENDPIXEL_DEVIATION`  -   deviation of bezie curve points relative to each other
- `MAX_WIDTH_DEVIATION`     -   deviation in width of curve in [Drawing](README.md/#drawing) 
- `BASE_WIDTH`              -   base stable width of curve
- `THREADS_COUNT`           -   number of threads in [Collecting](README.md/#collecting) stage

Suggestion: If you change `MAX_ENDPIXEL_DEVIATION` with some multiple `k` (for example, from `0.04` to `0.02` with multiple `1/2`), change the `CURVE_COUNT_PER_10x10` by about `1/k` (in stated example, from `7` to `14`), because otherwhise some artifacts may appear.

## CLI tool
`usage: start.py [-h] [-o OUTPUT] input` 

# Artifacts
When the `CURVE_COUNT_PER_10x10` is relatively small and/or `MAX_ENDPIXEL_DEVIATION` is small as well (resulting in less average length of curve), some parts of the image may stay blank causing effect like in these images:
- [this image](examples/карим_out_1.jpg)
- [this image](examples/джарик_out_2.jpg)

Based on your goals, you may like to include those artifacts to achive the effect of real paint drawing like in:
- [this image](examples/не%20рыпаемся_out_3.jpg)
- [this image](examples/пейзаж_out_1.jpg)