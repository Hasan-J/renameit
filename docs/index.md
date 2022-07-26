[TOC]

# Installation

You can directly install it within your virtual environment:

    pip install renameit

Additional library support for a specific cloud provider can be installed as extra requirement:

    pip install renameit[aws, azure, google]

---

If you don't want to worry about cluttering an existing production environment, we provide
a [PEX](https://pex.readthedocs.io/en/latest/) file for each release that can be directly downloaded:

    curl https://github.com/Hasan-J/renameit/releases/download/{release-name}/renameit.pex -o renameit

We also publish a docker image to [docker hub](https://hub.docker.com/r/hasanj/renameit) for each release:

    docker pull hasanj/renameit:<tag-name>


> **_NOTE:_** Both pex file and docker image contain all dependencies

# Usage

`renameit` needs some kind of user input to tell it what kind of jobs to run.

Users can basically define a list of jobs that will be run in sequence (job parralalism could be introduced in later versions).

### Configure your jobs

Provide job configuration file (.ini, .toml, .json, .yaml, .yml) in the user directory,
`~/.config/renameit/config.<extension>` for **Linux and macos** or `%USERPROFILE%/.config/renameit/config.<extension>`
for **windows**.

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

### Run jobs:

#### Using virtual environment or pex file

    renameit

or with a custom config file:

    renameit --config-path /custom/path/config.yaml

#### Using docker:

Docker run needs some additional mount points for the config file, 
suppose you have a local dir that contains the config file `/my/configs/config.yaml`

    docker run --rm -v '/my/configs:/configs' hasanj/renameit:<tag-name> \
      renameit --config-path /configs/config.yaml

If you're using the `local` file system, you also need to provide mount point for directories that should contain
source and renamed files:

    docker run --rm \
      -v '/my/configs:/configs' \
      -v '/data:/data' \
      hasanj/renameit:<tag-name> renameit --config-path /configs/config.yaml

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
    * **rename_handler**: specifies what type of file name transformation should be done 
      and how ([available rename handlers](#rename-handlers))

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
| local | Operate on local file system | copy, rename | [FileSystemLocal](https://hasan-j.github.io/renameit/ref/file_systems/#renameit.file_systems.local.FileSystemLocal) |
| azure_datalake_storage | Operate on azure datalake storage | rename | [FileSystemAzureDatalakeStorage](https://hasan-j.github.io/renameit/ref/file_systems/#renameit.file_systems.azure.FileSystemAzureDatalakeStorage) |
| aws_s3 | Operate on aws s3 storage | copy | [FileSystemAwsS3](https://hasan-j.github.io/renameit/ref/file_systems/#renameit.file_systems.aws.FileSystemAwsS3) |
| google_cloud_storage | Operate on google cloud storage | copy, rename | [FileSystemGoogleCloudStorage](https://hasan-j.github.io/renameit/ref/file_systems/#renameit.file_systems.google.FileSystemGoogleCloudStorage) |


# Rename handlers

| type  |          description         |  docs  |
|-------|:-----------------------------|:-------|
| basic | Provides simple file name transformations | [BasicHandler](https://hasan-j.github.io/renameit/ref/handlers/#renameit.handlers.basic.BasicHandler) |
| regex | Use regular expressions to match and replace patterns in file names | [RegexHandler](https://hasan-j.github.io/renameit/ref/handlers/#renameit.handlers.regex.RegexHandler) |
| datetime | Use datetime values and place them in file names | [DateTimeHandler](https://hasan-j.github.io/renameit/ref/handlers/#renameit.handlers.datetime.DateTimeHandler) |
