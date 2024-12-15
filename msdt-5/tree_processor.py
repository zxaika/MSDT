class TreeProcessor:
    def process_input(self, input_data, separator=","):
        if not input_data.strip():
            return "Дерево пустое"
        try:
            elements = input_data.split(separator)

            # Если первый элемент - "null", то возвращаем "Дерево пустое"
            if elements[0] == "null":
                return "Дерево пустое"

            # Проверка на некорректные данные
            for element in elements:
                if element != "null":
                    try:
                        int(element)  # Пробуем преобразовать в число
                    except ValueError:
                        return "Неверный ввод"  # Возвращаем ошибку, если элемент не число и не "null"

            tree = self.build_tree(elements)
            if tree is None:
                return "Неверный ввод"  # Возвращаем ошибку, если дерево не удалось построить
            return self.count_leaves(tree)
        except ValueError:
            return "Неверный ввод"

    def build_tree(self, elements):
        from collections import deque

        if not elements or elements[0] == "":
            return None

        root_value = elements.pop(0)
        if root_value == "null":
            return None

        root = {"value": int(root_value), "left": None, "right": None}
        queue = deque([root])

        while elements:
            current = queue.popleft()

            # Левый потомок
            if elements:
                left_value = elements.pop(0)
                if left_value != "null":
                    left_node = {"value": int(left_value), "left": None, "right": None}
                    current["left"] = left_node
                    queue.append(left_node)

            # Правый потомок
            if elements:
                right_value = elements.pop(0)
                if right_value != "null":
                    right_node = {"value": int(right_value), "left": None, "right": None}
                    current["right"] = right_node
                    queue.append(right_node)

        return root

    def count_leaves(self, tree):
        if not tree:
            return 0
        # Узел считается листом, если у него нет потомков
        if tree["left"] is None and tree["right"] is None:
            return 1
        return self.count_leaves(tree["left"]) + self.count_leaves(tree["right"])
