import tarfile
import zipfile

def get_archive_paths(filename):
    """Tries to open an archive and return all the paths contained inside it."""

    if tarfile.is_tarfile(filename):
        archive = tarfile.open(filename)
        return archive.getnames()

    elif zipfile.is_zipfile(filename):
        archive = zipfile.ZipFile(filename)
        return archive.namelist()
