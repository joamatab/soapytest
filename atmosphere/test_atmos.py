import numpy

from soapy import atmosphere

from aotools.circle import zernike

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

    print freqs

    plt.figure()
    plt.plot(freqs[:freqs.size/2], power_spec)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    return None


def testNollSpectrum(nZerns, nScrns, scrnSize, subScrnSize, r0):

    Zs = zernike.zernikeArray(nZerns+1, subScrnSize)[1:]

    Zs.shape = nZerns, subScrnSize*subScrnSize

    subsPerScrn = scrnSize/subScrnSize
    zCoeffs = numpy.zeros((nZerns, nScrns*(subsPerScrn**2)))

    i = 0
    for n in range(nScrns):
        # Make one big screen
        scrn = atmosphere.ft_phase_screen(
                r0, scrnSize, 1./subScrnSize, 100., 0.01)

        # Pick out as many sub-scrns as possible to actually test
        for x in range(subsPerScrn):
            for y in range(subsPerScrn):
                subScrn = scrn[
                        x*subScrnSize: (x+1)*subScrnSize,
                        y*subScrnSize: (y+1)*subScrnSize]
                subScrn = subScrn.reshape(subScrnSize*subScrnSize)

                # Dot with zernikes to get powerspec
                zCoeffs[:, i] = (Zs*subScrn).sum(1)
                i+=1

    return zCoeffs

if __name__=="__main__":

    # Number of scrns to average over
    nScrns = 500
    r0 = 1. # R0 value to use in test
    nZerns = 50
    subScrnSize = 256
    scrnSize = 512

    zCoeffs = testNollSpectrum(nZerns, nScrns, scrnSize, subScrnSize, r0)
