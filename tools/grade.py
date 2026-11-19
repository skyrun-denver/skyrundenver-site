# Shared photo grade for skyrundenver.com: neutral whites, one brightness target, loud colors pulled back slightly.
# Applied to every home photo so different sources read as one set. Used by tools/make_photos.py.
import sys, numpy as np
from PIL import Image
try: import pillow_avif
except: pass
def srgb2lin(x): return np.where(x<=0.04045,x/12.92,((x+0.055)/1.055)**2.4)
def lin2srgb(x): return np.where(x<=0.0031308,x*12.92,1.055*np.clip(x,0,None)**(1/2.4)-0.055)
def grade(im, target_L=0.60, target_sat=0.20, wb=0.6, warmth=0.01):
    a=np.asarray(im.convert('RGB')).astype(np.float32)/255
    lin=srgb2lin(a)
    # white balance from bright neutral-ish pixels (walls, ceilings)
    lum=lin.mean(2); mask=(lum>np.percentile(lum,60))&(lum<np.percentile(lum,98))
    m=lin[mask].mean(0); g=m.mean()/m; g=1+(g-1)*wb
    g=g*np.array([1+warmth,1,1-warmth]); lin=lin*g
    s=lin2srgb(np.clip(lin,0,1))
    # exposure to target mean luminance (gamma), gentle s-curve
    L=(0.2126*s[...,0]+0.7152*s[...,1]+0.0722*s[...,2])
    gam=np.clip(np.log(target_L)/np.log(max(L.mean(),1e-3)),0.75,1.35)
    s=np.clip(s,0,1)**gam
    s=s+0.06*np.sin(2*np.pi*s)/ (2*np.pi)*-1  # slight contrast
    s=np.clip(s,0,1)
    # saturation normalize
    mx=s.max(2);mn=s.min(2);sat=((mx-mn)/(mx+1e-6)).mean()
    k=np.clip(target_sat/max(sat,1e-3),0.82,1.08)
    gray=(0.2126*s[...,0]+0.7152*s[...,1]+0.0722*s[...,2])[...,None]
    s=np.clip(gray+(s-gray)*k,0,1)
    return Image.fromarray((s*255+0.5).astype(np.uint8))
if __name__=='__main__':
    grade(Image.open(sys.argv[1])).save(sys.argv[2],quality=90)
