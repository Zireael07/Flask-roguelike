# extends noise.py to add more complex stuff on top, e.g. octaves
from . import noise

# based on http://flafla2.github.io/2014/08/09/perlinnoise.html
def octave_perlin(x,y, octaves=2, persistence=2, x_freq = 1, y_freq = 1, amplitude=1):
    total = 0
    #maxValue = 0 # used to normalize to 0-1 range
    # freq = 1
    # amplitude = 1
    for i in range(0, octaves):
        total += noise.noise_2d(x*x_freq,y*y_freq) * amplitude
        # black magic here!
        amplitude *= persistence
        x_freq *= 2
        y_freq *= 2
    
    return total