# Install Maya 2015
# Inspired by: https://gist.github.com/MRTELIMS/c7452f8106874f30117e

import subprocess
import tempfile
import urllib2
import os

class Step(object):
    """Perform a step of the installation"""
    def __enter__(s):
        s.cleanup = None # Cleanup function
        return s

    def __exit__(s, err, type, pos):
        if err:
            if s.cleanup:
                s.cleanup()

def Title(message):
    print "#" * 40
    print message
    print "#" * 40

def GetDependencies():
    Title("Grabbing Required Dependencies")
    deps = ["sudo", "apt-get", "install", "-y",
        "alien",
        "csh",
        "tcsh",
        "libaudiofile-dev",
        "libglw1-mesa",
        "elfutils",
        "gamin",
        "libglw1-mesa-dev",
        "mesa-utils",
        "xfstt",
        "ttf-liberation",
        "xfonts-100dpi",
        "xfonts-75dpi",
        "ttf-mscorefonts-installer",
        "tar"
        ]
    subprocess.call(deps)

def DownloadPackage(working, version):
    if version == "2015":
        url = "http://download.autodesk.com/us/support/files/maya_2015_service_pack_6/Autodesk_Maya_2015_SP6_EN_Linux.tgz"
        download = os.path.join(working, "Maya2015.tgz")

    if not os.path.isdir(working):
        os.mkdir(working)

    if not os.path.isfile(download):
        Title("Downloading Maya")
        tempf = tempfile.NamedTemporaryFile()
        #print tempf.name
        u = urllib2.urlopen(url)
        meta = u.info()
        size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s" % size
        dl_size = 0
        block_size = 8192
        while True:
            buffering = u.read(block_size)
            if not buffering:
                break
            dl_size += len(buffering)
            tempf.write(buffering)
            status = r"%10d [%3.2f%%]" % (dl_size, dl_size * 100 / size)
            status = status + chr(8) * (len(status)+1)
            print "Downloading Maya", status
        os.rename(tempf.name, download)

HOME = os.path.expanduser("~")
WORKING = os.path.join(HOME, "maya_temp_install")
VERSION = "2015"

# Title("Step 1")
# GetDependencies()

Title("Step 2")
DownloadPackage(WORKING, VERSION)