import re


class FileNameHandler(object):
    def process(self):
        pass


class RegexFileNameHandler(FileNameHandler):
    def __init__(self, regex_config, case_sensitive=True):
        self.regex_config = regex_config
        self.case_sensitive = case_sensitive
        if self.case_sensitive:
            self.regex_pattern = re.compile(self.regex_config["regex_pattern"])
        else:
            self.regex_pattern = re.compile(
                self.regex_config["regex_pattern"], re.IGNORECASE
            )
        self.groups = self.regex_config["groups"]
        if not self.case_sensitive:
            for group_key, group_map in self.groups.items():
                self.groups[group_key] = {
                    key.lower(): value for key, value in group_map.items()
                }

    def process(self, file_name):
        match = self.regex_pattern.match(string=file_name)
        if match is not None:
            string_formatter_dict = dict()
            for group_name, group_value in match.groupdict().items():

                if group_name in self.regex_config["groups"].keys():
                    string_formatter_dict[group_name] = self.regex_config["groups"][
                        group_name
                    ].get(self.gork_str_case(group_value), group_value)
                else:
                    string_formatter_dict[group_name] = group_value

        return self.regex_config["replace_pattern"].format(**string_formatter_dict)

    def gork_str_case(self, arg: str):
        if self.case_sensitive:
            return arg
        return arg.lower()
