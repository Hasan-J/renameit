"""Main module to expose internal functions as command lines."""

import fire

from .config import ProjectConfig
from .job_runners import JobRunnerStandard


def renameit(config_path: str = None, config_dir: str = None):
    """This is the main API that is used to trigger renaming jobs.

    Args:
        config (str, optional): File path to configs overriding the default path. Defaults to None.
        config_dir (str, optional): Dir path to other config files if needed. Defaults to None.
    """
    config = ProjectConfig.create_new(config_path=config_path, config_dir=config_dir)

    job_runner = JobRunnerStandard(jobs=config.get_jobs())

    job_runner.execute()


def main():
    """Wrapper function for console_script entry_points"""
    fire.Fire(renameit)


# For debugging purposes
if __name__ == "__main__":
    main()
