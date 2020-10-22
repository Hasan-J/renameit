from typing import Iterable, Text
import boto3
import pathlib
import shutil


class FileManager(object):
    def list_files(self):
        pass

    def copy_file(self, source, target):
        pass

    def move_file(self, source, target):
        pass


class S3FileManager(object):
    """
    docstring
    """

    def __init__(self, *args, **kwargs,) -> None:
        self.s3 = boto3.resource("s3")

    def list_files(self, container, prefix=None) -> Iterable[Text]:
        return (
            obj.key for obj in self.s3.Bucket(container).objects.filter(Prefix=prefix)
        )

    def copy_file(
        self, source_container, source_file_name, target_container, target_file_name
    ):
        return self.s3.Bucket(target_container).copy(
            {"Bucket": source_container, "Key": source_file_name}, target_file_name,
        )

    def move_file(self, source, target):
        pass


class LocalFileManager(object):
    """
    docstring
    """

    def __init__(self, recursive=False, *args, **kwargs,) -> None:
        self.recursive = recursive

    def list_files(self, container, prefix=None) -> Iterable[Text]:
        container = pathlib.Path(container)

        container_parts_len = len(container.parts)

        if prefix:
            container = container / prefix

        if self.recursive:
            glob_pattern = "**/*"
        else:
            glob_pattern = "*"

        return (
            self._create_path_from_parts(f.parts[container_parts_len:])
            for f in container.glob(glob_pattern)
        )

    def copy_file(
        self, source_container, source_file_name, target_container, target_file_name
    ):
        source_path = pathlib.Path(source_container) / source_file_name
        target_path = pathlib.Path(target_container) / target_file_name

        target_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copyfile(str(source_path), str(target_path))

    def move_file(self, source, target):
        pass

    def _create_path_from_parts(self, parts):
        if len(parts) == 0:
            raise ValueError("Parts is empty.")
        p = pathlib.Path()
        for part in parts:
            p = p / part
        return p
