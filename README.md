[![Actions Status](https://github.com/mjh-sakh/python-project-lvl2/workflows/hexlet-check/badge.svg)](https://github.com/mjh-sakh/python-project-lvl2/actions)
[![linter](https://github.com/mjh-sakh/python-project-lvl2/actions/workflows/lint.yml/badge.svg)](https://github.com/mjh-sakh/python-project-lvl2/actions/workflows/lint.yml)
[![tests](https://github.com/mjh-sakh/python-project-lvl2/actions/workflows/tests.yml/badge.svg)](https://github.com/mjh-sakh/python-project-lvl2/actions/workflows/tests.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/1b93335c104c8793f2a4/maintainability)](https://codeclimate.com/github/mjh-sakh/python-project-lvl2/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/1b93335c104c8793f2a4/test_coverage)](https://codeclimate.com/github/mjh-sakh/python-project-lvl2/test_coverage)

# Overview

Вычислитель отличий – программа определяющая разницу между двумя структурами данных. Это популярная задача, для решения которой существует множество онлайн-сервисов http://www.jsondiff.com/. Подобный механизм, например, используется при выводе тестов или при автоматическом отслеживании изменении в конфигурационных файлах.

Возможности утилиты:

Поддержка разных входных форматов: yaml, json
Генерация отчета в виде plain text, stylish и json
Пример использования:

```python
$ gendiff --format plain filepath1.json filepath2.yml

Setting "common.setting4" was added with value: False
Setting "group1.baz" was updated. From 'bas' to 'bars'
Section "group2" was removed
```

# gendiff: print json format for json and yaml

[![gendiff step 5](https://img.youtube.com/vi/6zkkTDvJUrI/0.jpg)](https://www.youtube.com/watch?v=6zkkTDvJUrI "gendiff step 5")


# Processing for nested json/yaml

[![gendiff step 6](https://img.youtube.com/vi/rlIN1mhjbiM/0.jpg)](https://www.youtube.com/watch?v=rlIN1mhjbiM "gendiff step 6")


# Plain format

[![gendiff step 7](https://img.youtube.com/vi/WfA9NkfR8xw/0.jpg)](https://www.youtube.com/watch?v=WfA9NkfR8xw "gendiff step 7")


# json as output 

[![gendiff step 8](https://img.youtube.com/vi/62N7bR6KEnM/0.jpg)](https://www.youtube.com/watch?v=62N7bR6KEnM "gendiff step 8")