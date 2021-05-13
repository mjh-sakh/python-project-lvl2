class Comparisons(list):
    """
    Container to store per-value comparisons based on list.
    Provides two methods on top of list type:
      add_item: adds tuple to the list (flag, key, value)
      convert_value_to_string: converts all values to strings
    """

    def __init__(self):
        super().__init__()

    def add_item(self, flag, key, value):
        """
        Add comparison item into list.

        :param flag from FLAGS indicating comparison result, str.
        :param key: str.
        :param value: original value, that will be converted to str.
        """
        self.append((flag, key, value))

    # def __getitem__(self, item):
    #     return dict(zip(["flag", "key", "value"], super().__getitem__(item)))


FLAGS = {
    "new": "n+",
    "removed": "r-",
    "changed_new": "c+",
    "changed_old": "c-",
    "unchanged": "u ",
}
