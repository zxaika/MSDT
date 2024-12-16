import pytest
import tempfile


from tree_processor import TreeProcessor  # Импортируем класс TreeProcessor

@pytest.fixture
def processor():
    return TreeProcessor()

def test_empty_tree(processor):
    # Пустой ввод значит дерево пустое
    assert processor.process_input("   ") == "Дерево пустое"

def test_invalid_input(processor):
    # Некорректный ввод должен вывести сообщение неверный ввод
    assert processor.process_input("1,2,3,abc,5") == "Неверный ввод"
    assert processor.process_input("1,,2,3") == "Неверный ввод"
    assert processor.process_input("1,2,abc") == "Неверный ввод"

def test_valid_tree_with_leaves(processor):
    # Пример: "1,2,3,null,null,4,5"
    # результат: 3 (листья: 2, 4, 5)
    input_data = "1,2,3,null,null,4,5"
    assert processor.process_input(input_data) == 3

def test_tree_with_single_leaf(processor):
    # Пример: "1,null, null"
    # результат: 1 (листьев в дереве 1)
    input_data = "1,null,null"
    assert processor.process_input(input_data) == 1

def test_tree_with_single_node(processor):
    # Пример: "1"
    # результат: 1 (так как только один узел, который является листом)
    input_data = "1"
    assert processor.process_input(input_data) == 1

def test_tree_with_multiple_nulls(processor):
    # Пример: "1,2,3,null,null,null,4"
    # результат: 2 (листья: 2 и 4)
    input_data = "1,2,3,null,null,null,4"
    assert processor.process_input(input_data) == 2

def test_tree_with_empty_input(processor):
    # Пустой ввод (без данных) результат "Дерево пустое"
    assert processor.process_input("") == "Дерево пустое"

def test_tree_with_null_as_root(processor):
    # Пример с null
    # результат: "Дерево пустое"
    input_data = "null"
    assert processor.process_input(input_data) == "Дерево пустое"

def test_tree_input_from_file(processor):
    # временный файл с данными дерева
    input_data = "1,2,3,null,null,4,5"

    with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmpfile:
        tmpfile.write(input_data)
        tmpfile_path = tmpfile.name

    with open(tmpfile_path, 'r') as file:
        data = file.read().strip()

    # проверка на правильность обработки программы
    assert processor.process_input(data) == 3

    # удаление
    import os
    os.remove(tmpfile_path)

def test_tree_with_large_valid_input(processor):
    # большое дерево с большим количеством данных
    input_data = "1," + ",".join(str(i) for i in range(2, 100001)) + ",null"
    # проверка корректности работы программы
    assert processor.process_input(input_data) == 50000
