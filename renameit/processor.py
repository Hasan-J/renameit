import logging
import pathlib


class Processor(object):
    def __init__(
        self,
        source_container,
        file_name_handler,
        file_manager,
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
    ):

        self.file_name_handler = file_name_handler()
        self.file_manager = file_manager()

        self.source_container = source_container
        self.target_container = target_container or source_container
        self.error_container = error_container or source_container
        self.idle_container = idle_container
        self.source_prefix = source_prefix
        self.target_prefix = target_prefix
        self.errors_prefix = errors_prefix
        self.idle_prefix = idle_prefix
        self.keep_original = keep_original
        self.keep_tree_structure = keep_tree_structure
        self.report_idle = report_idle

    def process(self):
        for source_file_path in self.file_manager.list_files(
            self.source_container, prefix=self.source_prefix
        ):
            source_file_path = pathlib.Path(source_file_path)
            source_file_name = source_file_path.name
            try:
                target_file_name = self.file_name_handler.process(source_file_path.name)
            except Exception as identifier:
                # TODO move to errors container and log
                continue

            if source_file_name != target_file_name:
                if self.keep_tree_structure:
                    target_file_path = source_file_path.parent / target_file_name
                else:
                    target_file_path = target_file_name

                if self.target_prefix:
                    target_file_path = (
                        pathlib.Path(self.target_prefix) / target_file_path
                    )

                try:
                    if self.keep_original:
                        print(
                            f"Copying: {self.source_container}/{source_file_path} to "
                            + f"{self.target_container}/{target_file_path}"
                        )
                        self.file_manager.copy_file(
                            source_container=self.source_container,
                            source_file_name=str(source_file_path),
                            target_container=self.target_container,
                            target_file_name=str(target_file_path),
                        )
                    else:
                        raise NotImplementedError("Moving file not yet implemented")

                except Exception as identifier:
                    # TODO move to errors container and log
                    raise identifier
            else:
                if self.idle_container:
                    if self.idle_prefix:
                        self.file_manager.copy_file(
                            source_container=self.source_container,
                            source_file_name=str(source_file_path),
                            target_container=self.idle_container,
                            target_file_name=str(
                                pathlib.Path(self.idle_prefix) / source_file_path.name
                            ),
                        )
