import os

if os.getuid() == 0:
    DIRBALAK_DIR = "/var/lib/dirbalak"
else:
    DIRBALAK_DIR = os.path.join(os.environ['HOME'], ".dirbalak")
REPO_MIRRORS_BASEDIR = os.path.join(DIRBALAK_DIR, "repomirrors")
REPO_MIRRORS_LOCKFILE = os.path.join(REPO_MIRRORS_BASEDIR, "lock")

BUILD_CHROOT = os.path.join(DIRBALAK_DIR, "chroot")
BUILD_DIRECTORY = os.path.join(BUILD_CHROOT, "home", "dirbalak")

OFFICIAL_BUILD_ROOTFS = "rootfs-build__rootfs__4f3e35e69f5014eaeda422c21def14d36ca1972d__bootstrap"
NO_DIRBALAK_MANIFEST_BUILD_ROOTFS = \
    "rootfs-build__rootfs__4f3e35e69f5014eaeda422c21def14d36ca1972d__bootstrap"

LOGBEAM_ROOT_DIR = "dirbalak"
CLEANBUILD_LOG_FILENAME = "dirbalak.cleanbuild.log"
