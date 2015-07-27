# Install Maya 2015
# Inspired by: https://gist.github.com/MRTELIMS/c7452f8106874f30117e

import subprocess
import tempfile
import urllib2
import time
import re
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
        "tar",
        "libssl-dev"
        ]
    subprocess.call(deps)

def DownloadPackage(working, version):
    extract = os.path.join(working, "extracted") # Save extracted files here
    if version == "2015":
        url = "http://download.autodesk.com/us/support/files/maya_2015_service_pack_6/Autodesk_Maya_2015_SP6_EN_Linux.tgz"
        download = os.path.join(working, "Maya2015.tgz")

    if not os.path.isdir(working):
        os.mkdir(working)

    if not os.path.isdir(extract):
        os.mkdir(extract)

    if not os.path.isfile(download):
        Title("Downloading Maya")
        tempf = tempfile.NamedTemporaryFile()
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
        subprocess.call(["tar", "-xf", download], cwd=extract)

    return extract

def ExtractRPM(working):
    reg = re.compile("^.+?\.rpm$")
    rpms = [os.path.join(working, f) for f in os.listdir(working) if reg.match(f)]
    if rpms:
        Title("Converting RPMS. THIS CAN TAKE A WHILE!!")
        time.sleep(5)
        print "Here we go..."
        time.sleep(2)
        print "..."
        time.sleep(2)
    tempf = os.path.join(working, "converted")
    if not os.path.isdir(tempf):
        os.mkdir(tempf)
    # subprocess.call(["export", "RPM_INSTALL_PREFIX=/usr"])
    # subprocess.call(["export", "LD_LIBRARY_PATH=/opt/Autodesk/Adlm/R5/lib64/"])
    for rpm in rpms:
        subprocess.call(["sudo", "alien", "-c", "--veryverbose", rpm], cwd=tempf)
        os.remove(rpm)
    debs = os.listdir(tempf)
    if debs:
        for deb in debs:
            os.rename(os.path.join(tempf, deb), os.path.join(working, deb))
    os.removedirs(tempf)

    return working

def SymLinking(version):
    def link(pathfrom, pathto):
        if not os.path.isfile(pathto):
            os.symlink(pathfrom, pathto)
    def latest(filename):
        files = sorted([f for f in base_files if filename in f])
        return os.path.join(base, files[0]) if files else None
    if version == "2015":
        base = "/usr/lib/x86_64-linux-gnu"
        base_files = os.listdir(base)
        subprocess.call(["sudo", "ln", "-s", latest("libcrypto.so"), os.path.join(base, "libcrypto.so.10")])
        subprocess.call(["sudo", "ln", "-s", latest("libssl.so"), os.path.join(base, "libssl.so.10")])

    subprocess.call(["sudo", "mkdir", "/usr/tmp"])
    subprocess.call(["sudo", "chmod", "777", "/usr/tmp"])

HOME = os.path.expanduser("~")
WORKING = os.path.join(HOME, "maya_temp_install")
VERSION = "2015"

# Title("Step 1")
# GetDependencies()
#
# Title("Step 2")
# extracted = DownloadPackage(WORKING, VERSION)
#
# Title("Step 3")
# extracted = ExtractRPM(extracted)

Title("Step 4")
SymLinking(VERSION)
