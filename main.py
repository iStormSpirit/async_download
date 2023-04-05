import asyncio
import hashlib
import os
import random
import shutil

import aiohttp


class TmpDir:
    def __init__(self, path: str, remove_tmp_dir: bool = True):
        self.path = path
        self.remove_tmp_dir = remove_tmp_dir

    def __enter__(self):
        if os.path.exists(self.path):
            raise RuntimeError(f"Can't make already existing directory a temporary one: {os.path.abspath(self.path)}")

        os.makedirs(self.path, exist_ok=True)
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.remove_tmp_dir is False:
            pass
        else:
            shutil.rmtree(self.path, ignore_errors=True)


def salt():
    return str(random.random())


async def download_repo(url: str, dir_path: str, postfix: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            repo_name = url.split("/")[-3] + '_' + str(postfix)
            file_type = url.split(".")[-1]
            with open(f'{dir_path}/{repo_name}.{file_type}', "wb") as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            return f'{dir_path}/{repo_name}.{file_type}'


def get_link_branch_download(url: str, branch: str = 'master', file_type: str = 'zip') -> str:
    link = f'{url}/archive/{branch}.{file_type}'
    return link


def calculate_sha256_hash(path_file: str) -> tuple[str, str]:
    with open(path_file, 'rb') as f:
        file = f.read()
        sha256_hash = hashlib.sha256(file).hexdigest()
        return path_file, sha256_hash


async def main():
    dir_path = f'{os.path.abspath(os.curdir)}/temp'
    url = 'https://gitea.radium.group/radium/project-configuration'
    new_url = get_link_branch_download(url)

    with TmpDir(dir_path, remove_tmp_dir=True):
        tasks_download = []
        for task_number in range(3):
            task = asyncio.create_task(download_repo(new_url, dir_path, str(task_number)))
            tasks_download.append(task)
        result_download = await asyncio.gather(*tasks_download)

        result_hash = []
        for path_file in result_download:
            result_hash.append(calculate_sha256_hash(path_file))
        print(result_hash)


if __name__ == '__main__':
    asyncio.run(main())
