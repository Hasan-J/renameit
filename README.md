# renameit
> Pure python CLI tool for renaming files and folders locally or on the cloud.

# Description

Reshape your data lakes by transforming files and folders structure with a single command and without the complications of writing manual scripts.
Data engineers and data analysts constantly have to worry about keeping the structure of their data organized in order to efficiently read
and access them. This tool allows them to change the file or folder structure of their data lakes on a cloud storage system or even on local storage
(e.g. locally mounted cloud storage).

---

[![Open in Remote - Containers](https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Hasan-J/renameit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Main](https://github.com/Hasan-J/renameit/actions/workflows/main.yml/badge.svg)](https://github.com/Hasan-J/renameit/actions/workflows/main.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/renameit)
![PyPI](https://img.shields.io/pypi/v/renameit)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)


# Table of Contents
1. [Installation](#Installation)
2. [Usage](#Usage)
    - [Configure your jobs](#configure-your-jobs)
    - [Run jobs](#run-jobs)
3. [Job Configuration schema](#job-configuration-schema)
4. [File systems](#file-systems)
5. [Rename handlers](#rename-handlers)


# Installation

You can directly install it within your virtual environment:

`> pip install renameit`

Additional library support for a specific cloud provider can be installed as extra requirement:

`> pip install renameit[aws, azure, google]`

---

If you don't want to worry about cluttering an existing production environment, we provide
a [PEX](https://pex.readthedocs.io/en/latest/) file for each release that can be directly downloaded:

`> curl https://github.com/Hasan-J/renameit/releases/download/{release-name}/renameit.pex -o renameit`

We also publish a docker image to [docker hub](https://hub.docker.com/r/hasanj/renameit) for each release:

`> docker pull hasanj/renameit:<tag-name>`


> **_NOTE:_** Both pex file and docker image contain all dependencies

# Usage

`renameit` needs some kind of user input to tell it what kind of jobs to run.

Users can basically define a list of jobs that will be run in sequence (job parralalism could be introduced in later versions).

### Configure your jobs

Provide job configuration file (.ini, .toml, .json, .yaml, .yml) in the user directory:

*config.yaml example*

``` yaml
version: 0.1
jobs:
  - name: local_job_1
    operation: copy
    file_system:
      type: local
      args:
        source_dir: /data/source_files
        target_dir: /data/target_files
        recursive: True
    rename_handler:
      type: basic
      args:
        method: add_prefix
        value: TEST_PREFIX_
```

**Linux and macos**

`~/.config/renameit/config.<extension>`

**windows**

`%USERPROFILE%/.config/renameit/config.<extension>`

### Run jobs:

#### Using virtual environment or pex file

    > renameit

*OR*

Provide custom config file path:

    > renameit --config-path /custom/path/config.yaml

#### Using docker:

Docker run needs some additional mount points for the config file:

```bash
# Suppose you have a local dir that contains the config file `/my/configs/config.yaml`
> docker run --rm -v '/my/configs:/configs' hasanj/renameit:<tag-name> renameit --config-path /configs/config.yaml
```

You can define environment variables for the run:

`--env LOGLEVEL=INFO`

If you're using the `local` file system, you also need to provide mount point for directories that should contain
source and renamed files:

```bash
> docker run --rm \
  -v '/my/configs:/configs' \
  -v '/data:/data' \
  hasanj/renameit:<tag-name> renameit --config-path /configs/config.yaml
```

*Optionally change log level*

Define environment variable `LOGLEVEL` before running the command, default is `DEBUG`.

### Job Configuration schema

Lets walk through the above example to understand the different components needed:

- First `version` key defines the config schema version (fixed/latest is `0.1`)
- `jobs` key contains the list of jobs the user needs to run
- Each job dict needs to have the following key value pairs:

    * **name**: user-defined string value
    * **operation**: can be either `copy` or `rename` (depends on `file_system`)
    * **file_system**: the file storage system where files are located ([available file systems](#file-systems))
    * **rename_handler**: specifies what type of file name transformation should be done and how ([available rename handlers](#rename-handlers))

*run the above job definition*

Assuming we are running on linux with local dir `/data/source_files` containing 2 files:

    /data/source_files/file1.txt
    /data/source_files/subfolder/file2.txt

output:

```bash
/home/foo:~$ export LOGLEVEL=INFO; renameit --config-path config.yaml
2022-01-01 04:00:00 PM [INFO] Parsing 'yaml' config file from '/home/foo/config.yaml'
2022-01-01 04:00:00 PM [INFO] Running job local_job_1
2022-01-01 04:00:00 PM [INFO] Copying: /data/source_files/file1.txt to /data/target_files/TEST_PREFIX_file1.txt
2022-01-01 04:00:00 PM [INFO] Copying: /data/source_files/subfolder/file2.txt to /data/target_files/subfolder/TEST_PREFIX_file2.txt
```

# File systems

| type  |          description         |  operations  |  docs |
|-------|:-----------------------------|--------------|-------|
| local | Operate on local file system | copy, rename | [FileSystemLocal](https://hasan-j.github.io/renameit/file_systems/local.html#renameit.file_systems.local.FileSystemLocal) |
| azure_datalake_storage | Operate on azure datalake storage | rename | [FileSystemAzureDatalakeStorage](https://hasan-j.github.io/renameit/file_systems/azure.html#renameit.file_systems.azure.FileSystemAzureDatalakeStorage) |
| aws_s3 | Operate on aws s3 storage | copy | [FileSystemAwsS3](https://hasan-j.github.io/renameit/file_systems/aws.html#renameit.file_systems.aws.FileSystemAwsS3) |
| google_cloud_storage | Operate on google cloud storage | copy, rename | [FileSystemGoogleCloudStorage](https://hasan-j.github.io/renameit/file_systems/google.html#renameit.file_systems.google.FileSystemGoogleCloudStorage) |


# Rename handlers

| type  |          description         |  docs  |
|-------|:-----------------------------|:-------|
| basic | Provides simple file name transformations | [BasicHandler](https://hasan-j.github.io/renameit/handlers/basic.html#renameit.handlers.basic.BasicHandler) |
| regex | Use regular expressions to match and replace patterns in file names | [RegexHandler](https://hasan-j.github.io/renameit/handlers/regex.html#renameit.handlers.regex.RegexHandler) |
| datetime | Use datetime values and place them in file names | [DateTimeHandler](https://hasan-j.github.io/renameit/handlers/datetime.html#renameit.handlers.datetime.DateTimeHandler) |
