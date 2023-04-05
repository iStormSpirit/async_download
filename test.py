import os
import shutil
import time

import pytest

from main import TmpDir, calculate_sha256_hash, download_repo, get_link_branch_download


@pytest.fixture
def example_url():
    return ['www', 'main', 'tar']


@pytest.fixture
def example_dir():
    return os.path.abspath(os.curdir)


def test_get_link_branch_download(example_url):
    assert get_link_branch_download(url=example_url[0], branch=example_url[1],
                                    file_type=example_url[2]) == 'www/archive/main.tar'
    assert get_link_branch_download(url=example_url[0], file_type=example_url[2]) == 'www/archive/master.tar'
    assert get_link_branch_download(url=example_url[0]) == 'www/archive/master.zip'
    assert get_link_branch_download(url=example_url[0], file_type='tg') != 'www/archive/master.zip'


def test_calculate_sha256_hash():
    filename = f"test.txt"
    with open(filename, 'w+') as f:
        f.write("test data")
    result = calculate_sha256_hash(filename)
    assert result[1] == '916f0027a575074ce72a331777c3478d6513f786a591bd892da1a577bf2335f9'
    assert result[0] != '78d6513f786a591bd892da1a577bf2335f978d6513f786a591a1a577bf2335f9'
    os.remove(filename)


def test_tmpdir(example_dir):
    with TmpDir(example_dir + '/temp', remove_tmp_dir=True):
        assert f'{example_dir}/temp' == '/home/geo/Projects/radium_test/temp'
        os.rmdir(example_dir + '/temp')


def test_tmpdir2(example_dir):
    with TmpDir(example_dir + '/temp', remove_tmp_dir=False):
        pass
    assert f'{example_dir}/temp' == '/home/geo/Projects/radium_test/temp'
    os.rmdir(example_dir + '/temp')


@pytest.mark.asyncio
async def test_download_file():
    cur_dir = os.path.abspath(os.curdir)
    dir_path = f'{cur_dir}/temp'
    os.mkdir(dir_path)
    url = 'https://gitea.radium.group/radium/project-configuration/archive/master.zip'
    result = await download_repo(url, dir_path, postfix='test')
    assert result == f'{cur_dir}/temp/project-configuration_test.zip'
    shutil.rmtree(dir_path)
