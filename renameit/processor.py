import pathlib
import shutil
from .handlers import FileNameHandler


class Processor(object):
    def __init__(
        self,
        dir_path,
        file_name_handler: FileNameHandler,
        backup_dir=None,
        renamed_dir=None,
        keep_tree_structure=True,
        recursive=False,
    ):
        self.dir_path = dir_path
        self.file_name_handler = file_name_handler
        self.backup_dir = backup_dir
        self.renamed_dir = renamed_dir
        self.keep_tree_structure = keep_tree_structure
        self.recursive = recursive

    def scan_dir(self):
        glob_pattern = "*"
        if self.recursive:
            glob_pattern = "**/*"

        return pathlib.Path(self.dir_path).glob(glob_pattern)

    def process(self):
        for file_path in self.scan_dir():
            if file_path.is_file():
                renamed_file_name = self.file_name_handler.process(file_path.name)
                renamed_file_path = file_path.parent / renamed_file_name

                if file_path != renamed_file_path:
                    self.backup(file_path)
                    self.rename(file_path, renamed_file_path)

    def rename(self, old_file_path, new_file_path):
        if self.renamed_dir is not None:
            self.renamed_dir = pathlib.Path(self.renamed_dir)
            new_file_path = self.gork_target(self.renamed_dir, new_file_path)

        print(f"Renaming {old_file_path} to {new_file_path}")
        old_file_path.rename(new_file_path)

    def backup(self, file_path):
        if self.backup_dir is not None:
            self.backup_dir = pathlib.Path(self.backup_dir)
            backup_file_path = self.gork_target(self.backup_dir, file_path)
            backup_file_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(file_path), str(backup_file_path))

    def gork_target(self, target_dir, file_path):
        if self.keep_tree_structure:
            return target_dir / file_path.relative_to(self.dir_path)
        else:
            return target_dir / file_path.name
