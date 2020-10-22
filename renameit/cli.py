from typing import Text
from fire import Fire

from .handlers import RegexFileNameHandler
from .managers import S3FileManager, LocalFileManager

from .processor import Processor


class ResourceInitializer:
    def __init__(self, resource, **kwargs) -> None:
        self.resource = resource
        self.kwargs = kwargs

    def __call__(self):
        return self.resource(**self.kwargs)


def renameit_cli(
    source_container,
    file_name_handler: Text,
    file_manager: Text,
    target_container=None,
    error_container=None,
    idle_container=None,
    source_prefix=None,
    target_prefix="renameit_target",
    errors_prefix="renameit_errors",
    idle_prefix=None,
    keep_original=True,
    keep_tree_structure=True,
    report_idle=False,
    **kwargs
):

    file_name_handler = {
        "regex": ResourceInitializer(RegexFileNameHandler, **kwargs)
    }.get(file_name_handler)

    file_manager = {
        "s3": ResourceInitializer(S3FileManager, **kwargs),
        "local": ResourceInitializer(LocalFileManager, **kwargs),
    }.get(file_manager)

    Processor(
        source_container=source_container,
        file_name_handler=file_name_handler,
        file_manager=file_manager,
        target_container=target_container,
        error_container=error_container,
        idle_container=idle_container,
        source_prefix=source_prefix,
        target_prefix=target_prefix,
        errors_prefix=errors_prefix,
        idle_prefix=idle_prefix,
        keep_original=keep_original,
        keep_tree_structure=keep_tree_structure,
        report_idle=report_idle,
    ).process()


def fire_cli():
    Fire(renameit_cli)
