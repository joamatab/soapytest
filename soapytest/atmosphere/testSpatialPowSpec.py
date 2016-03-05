import numpy

from soapy import atmosphere

from aotools.circle import zernike
from aotools import circle

import matplotlib.pylab as plt

def test_power_spectra(r0, N, delta, L0, l0):
    N*= 10
    phase_screen = atmosphere.ft_phase_screen(r0, N, delta, L0, l0)
    phase_screen = phase_screen[:N/10, :N/10]
    power_spec_2d = numpy.fft.fft2(phase_screen, s=(N*2, N*2))

    plt.figure()
    plt.imshow(numpy.abs(numpy.fft.fftshift(power_spec_2d)), interpolation='nearest')

    power_spec = circle.aziAvg(numpy.abs(numpy.fft.fftshift(power_spec_2d)))
    power_spec /= power_spec.sum()

    freqs = numpy.fft.fftfreq(power_spec_2d.shape[0], delta)

    # Theoretical Model of Power Spectrum

    print freqs

    plt.figure()
    plt.plot(freqs[:freqs.size/2], power_spec)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    return None

def theoPowerSpec(cn2, freqs, L0=None, l0=None):


    # if no l0 or L0, assume kolmogorov
    if L0==None and l0==None:
        powSpec = 0.033 * cn2 * freqs**(-11./3)

    # Assumume Von Karman
    if L0!=None and l0==None:
        k0 = 2*numpy.pi/L0
        powSpec = 0.033 * cn2 * (freqs**2 + k0**2)**(-11./6)

    # Assume modified Von Karman
    if L0!=None and l0!=None:
        k0 = 2*numpy.pi/L0
        km = 5.92/l0
        powSpec = 0.033 * cn2 * numpy.exp(-(freqs/km)**2) * (freqs**2 + k0**2)**(-11./6)

    else:
        raise ValueError("Aint got a power spectrum for that L0/l0 combo!")

    return powSpec
