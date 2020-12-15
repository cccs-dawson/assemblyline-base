import os
import tempfile

import pytest

from assemblyline.filestore import FileStore
from assemblyline.filestore.transport.base import TransportException


def test_azure():
    """
    Azure filestore by downloading a file from our public storage blob
    """
    fs = FileStore("azure://alpytest.blob.core.windows.net/pytest/", connection_attempts=2)
    assert fs.exists('test') != []
    assert fs.get('test') is not None
    assert fs.read('test').read() is not None
    with pytest.raises(TransportException):
        fs.put('bob', 'bob')


def test_http():
    """
    Test HTTP FileStore by fetching the assemblyline page on
    CSE's cyber center page.
    """
    fs = FileStore('http://cyber.gc.ca/en/')
    assert fs.exists('assemblyline') != []
    assert fs.get('assemblyline') is not None
    tempf = tempfile.NamedTemporaryFile()
    fs.download('assembyline', tempf.name)
    assert open(tempf.name, 'r').read() is not None
    httpObject = fs.read('assemblyline')
    assert httpObject.read(chunk_size=32) is not None

def test_https():
    """
    Test HTTPS FileStore by fetching the assemblyline page on
    CSE's cyber center page.
    """
    fs = FileStore('https://cyber.gc.ca/en/')
    assert fs.exists('assemblyline') != []
    assert fs.get('assemblyline') is not None
    tempf = tempfile.NamedTemporaryFile()
    fs.download('assembyline', tempf.name)
    assert open(tempf.name, 'r').read() is not None
    assert fs.read('assemblyline').read(chunk_size=24) is not None


# def test_sftp():
#     """
#     Test SFTP FileStore by fetching the readme.txt file from
#     Rebex test server.
#     """
#     fs = FileStore('sftp://demo:password@test.rebex.net')
#     assert fs.exists('readme.txt') != []
#     assert fs.get('readme.txt') is not None


def test_ftp():
    """
    Test FTP FileStore by fetching the readme.txt file from
    Rebex test server.
    """
    fs = FileStore('ftp://al_test_user:password@localhost')

    # fs = FileStore('ftp://demo:password@test.rebex.net')
    assert fs.exists('readme.txt') != []
    assert fs.get('readme.txt') is not None
    ftpfile = fs.read('readme.txt')
    assert ftpfile.read() is not None


# def test_ftps():
#     """
#     Test FTP over TLS FileStore by fetching the readme.txt file from
#     Rebex test server.
#     """
#     fs = FileStore('ftps://demo:password@test.rebex.net')
#     assert fs.exists('readme.txt') != []
#     assert fs.get('readme.txt') is not None


def test_file():
    """
    Test Local FileStore by fetching the README.md file from
    the assemblyline core repo directory.

    Note: This test will fail if pytest is not ran from the root
          of the assemblyline core repo.
    """
    fs = FileStore('file://%s' % os.path.dirname(__file__))
    assert fs.exists(os.path.basename(__file__)) != []
    assert fs.get(os.path.basename(__file__)) is not None
    assert fs.read(os.path.basename(__file__)) is not None


def test_s3():
    """
    Test Amazon S3 FileStore by fetching a test file from
    the assemblyline-support bucket on Amazon S3.
    """
    fs = FileStore('s3://AKIAIIESFCKMSXUP6KWQ:Uud08qLQ48Cbo9RB7b+H+M97aA2wdR8OXaHXIKwL@'
                   's3.amazonaws.com/?s3_bucket=assemblyline-support&aws_region=us-east-1')
    tempf = tempfile.NamedTemporaryFile()
    assert fs.exists('al4_s3_pytest.txt') != []
    assert fs.get('al4_s3_pytest.txt') is not None
    assert fs.read('al4_s3_pytest.txt') is not None
    fs.download('al4_s3_pytest.txt', tempf.name)
    assert open(tempf.name, 'r').read() is not None
