import numpy
from matplotlib import pyplot
from tqdm import tqdm

import aotools
from aotools.turbulence import infinitephasescreen_fried


def test_zerns():
    n_zerns = 100
    nx_size = 128
    pxl_scale = 8./nx_size
    r0 = 0.2
    L0 = 20.

    n_scrns = 50000

    # Create arrary of zernikes
    print("Make Zernikes...")
    Zs = aotools.zernikeArray(n_zerns+1, nx_size)[1:]

    print("Init phase screen")
    phase_screen = infinitephasescreen_fried.PhaseScreen(nx_size, pxl_scale, r0, L0, stencil_length_factor=4)

    print("Run tests")
    z_coeffs = numpy.zeros((n_scrns, n_zerns))
    for i in tqdm(range(n_scrns)):
        phase_screen.addRow()
        z_coeffs[i] = (phase_screen.scrn * Zs).sum((-1, -2))/(nx_size**2)

    z_vars = z_coeffs.var(0)

    pyplot.figure()
    pyplot.semilogy(z_vars)

    pyplot.savefig(f"infps_N-{nx_size}_nz-{n_zerns}.png")
    pyplot.show()

def test_temporal_ps():

    nx_size = 128
    pxl_scale = 8./nx_size
    r0 = 0.2
    L0 = 20.

    n_scrns = 5000

    print("Init phase screen")
    phase_screen = infinitephasescreen_fried.PhaseScreen(nx_size, pxl_scale, r0, L0, stencil_length_factor=4)

    print("alloc screen buffer")
    screen_buffer = numpy.zeros((n_scrns, nx_size**2))

    for i in tqdm(range(n_scrns)):
        phase_screen.addRow()
        screen_buffer[i] = phase_screen.scrn.flatten()

    print("Do FFT...")

    power_spectra = abs(numpy.fft.fft(screen_buffer, axis=0))**2
    power_spectrum = power_spectra.mean(1)

    # Each row is
    x_vals = numpy.fft.fftfreq()

    pyplot.figure()
    pyplot.loglog(power_spectrum)
    pyplot.savefig(f"tps_N-{nx_size}.png")
    pyplot.show()



if __name__ == "__main__":

    test_temporal_ps()