"""
RGBCIE converter
"""

def rgbcie(r1 ,g1 ,b1):
    # http://www.developers.meethue.com/documentation/color-conversions-rgb-xy
    # 1.) normalize RGB
    r = r1/255.
    g = g1/255.
    b = b1/255.
    # 2.) apply gamma correction
    if (r > 0.04045):
        r = ((r + 0.055) / (1.0 + 0.055))** 2.4
    else:
        r = r / 12.92
    if (g > 0.04045):
        g = ((g + 0.055) / (1.0 + 0.055))** 2.4
    else:
        g = g / 12.92
    if (b > 0.04045):
        b= ((b + 0.055) / (1.0 + 0.055))** 2.4
    else:
        b =b / 12.92
    # 3.) Convert RGB to XYZ
    X = r * 0.664511 + g * 0.154324 + b * 0.162028
    Y = r * 0.283881 + g * 0.668433 + b * 0.047685
    Z = r * 0.000088 + g * 0.072310 + b * 0.986039
    # 4.) Calculate xy from XYZ
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)
    # 7.) Return xyY where Y is brightness
    return (x,y,Y)
