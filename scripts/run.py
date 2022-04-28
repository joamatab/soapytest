from soapytest import makeplots, transfertoweb
import soapy
import sys
import os


def runtests(soapybuild_path):
    # make plots
    PLOT_DIR = os.path.join(soapybuild_path, 'plots/')
    os.makedirs(PLOT_DIR)
    #os.environ["PYTHONPATH"] = "{}:{}".format(os.path.join(soapybuild_path, 'soapytest/scripts'), os.environ["PYTHONPATH"])

    print(f"Use Soapy Version: {soapy.__version__}")
    makeplots.makePlots(PLOT_DIR)
    transfertoweb.transfer(PLOT_DIR)

if __name__ == "__main__":
    path = sys.argv[1]
    runtests(path)
