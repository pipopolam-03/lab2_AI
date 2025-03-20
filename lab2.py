import math

class State:
    def __init__(self, matrix, empty_one_x, empty_one_y):
        # начальное состояние
        self.matrix = matrix
        # x - столбец (элемент внутри списка)
        # y - строка (список внутри списка)
        self.empty_one_x = empty_one_x
        self.empty_one_y = empty_one_y

    # переопределяем print для красивого вывода
    def __str__(self):
        result = ['\n']

        for i in range(3):
            row = ' '.join(str(self.matrix[i][j]) for j in range(3))
            result.append(row)

        result.append('\n')

        return '\n'.join(result)

    # проверяем, совпадают ли два состояния
    def check_goal(self, target):
        return self.matrix == target.matrix

    # копируем состояние, чтобы случайно не изменить то, что менять нельзя
    def copy(self):
        new_matrix = [row.copy() for row in self.matrix]
        return State(new_matrix, self.empty_one_x, self.empty_one_y)

    #  перемещаем пустоту слева направо
    def left(self):
        left_state = self.copy()
        if left_state.empty_one_y > 0:
            left_state.matrix[left_state.empty_one_x][left_state.empty_one_y], left_state.matrix[left_state.empty_one_x][left_state.empty_one_y - 1] \
                = left_state.matrix[left_state.empty_one_x][left_state.empty_one_y - 1], left_state.matrix[left_state.empty_one_x][left_state.empty_one_y]
            left_state.empty_one_y -= 1
            return left_state

    #  перемещаем пустоту справа налево
    def right(self):
        right_state = self.copy()
        if right_state.empty_one_y < 2:
            right_state.matrix[right_state.empty_one_x][right_state.empty_one_y], right_state.matrix[right_state.empty_one_x][right_state.empty_one_y + 1] \
                = right_state.matrix[right_state.empty_one_x][right_state.empty_one_y + 1], right_state.matrix[right_state.empty_one_x][right_state.empty_one_y]
            right_state.empty_one_y += 1
            return right_state

    #  перемещselfаем пустоту сверху вниз
    def down(self):
        down_state = self.copy()
        if down_state.empty_one_x < 2:
            down_state.matrix[down_state.empty_one_x][down_state.empty_one_y], down_state.matrix[down_state.empty_one_x + 1][down_state.empty_one_y] \
                = down_state.matrix[down_state.empty_one_x + 1][down_state.empty_one_y], down_state.matrix[down_state.empty_one_x][down_state.empty_one_y]
            down_state.empty_one_x += 1
            return down_state

    #  перемещаем пустоту снизу вверх
    def up(self):
        up_state = self.copy()
        if up_state.empty_one_x > 0:
            up_state.matrix[up_state.empty_one_x][up_state.empty_one_y], up_state.matrix[up_state.empty_one_x - 1][up_state.empty_one_y] \
                = up_state.matrix[up_state.empty_one_x - 1][up_state.empty_one_y], up_state.matrix[up_state.empty_one_x][up_state.empty_one_y]
            up_state.empty_one_x -= 1
            return up_state

    # проверяем, куда можем пойти на текущем шаге
    # тут я сделала копию и возвращается тоже копия, чтобы не менялось состояние self, а то опасненько
    def sequence(self):
        temp_state = self.copy()
        actions = ''
        if temp_state.up():
            actions += 'u'
        if temp_state.down():
            actions += 'd'
        if temp_state.right():
            actions += 'r'
        if temp_state.left():
            actions += 'l'
        return actions

    # ищем в матрице нужный элемент, возвращаем координаты
    def find_item(self, item):
        for i in range(3):
            for j in range(3):
                if item == self.matrix[i][j]:
                    return (i, j)
        return False

    # функция h1 из методички (количество элементов не на своем месте)
    def h1(self, target):
        count = 0
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != target.matrix[i][j]:
                    count += 1
        return count

    # функция h1 из методички (сумма расстояний от каждого элемента в self до его положения в целевой матрице)
    def h2(self, target):
        f_values = []
        for i in range(3):
            for j in range(3):
                item = self.matrix[i][j]
                position = target.find_item(item)
                if position:  
                    f_values.append(abs(position[0] - i) + abs(position[1] - j))

        return sum(f_values)


class Node:
    def __init__(self, state, parent=None, depth=0, action=None): # тут поменяла значение глубины на 0
        self.depth = depth
        self.action = action
        self.parent = parent
        self.state = state

    # просто красивый вывод инфы об узле
    def about_node(self):
        if self.parent:
            print(f"Матрица моего родителя: {self.parent.state.matrix}")
            print(f"Как в меня пришли: {self.action}")
        print(f"Моя матрица: {self.state.matrix}")
        print(f"Моя глубина: {self.depth}")

    # проверка, совпадают ли два узла (проверяем по матрице, если просто через равно - пиздеж получался)
    def are_we_same(self, sibling):
        if self.state.matrix == sibling.state.matrix:
            return True
        return False

    # создание копии узла - на всякий, я тут копирую всё и везде, чтобы не дай бог что-то не поменять лишний раз
    def copy(self):
        node_state = self.state.copy()
        return Node(node_state, self.parent, self.depth, self.action)

    # проверка, есть ли узел self в пройденных - опять же, если циклом с равно проверять ...
    # ... он пиздел и заработало с такой проверкой. nodes - словарь, у которого ключи - это узлы, а ...
    # ... значения - f узла (чтобы не ебаться с двумя списками), и вот он ключи(узлы) через  are_we_same
    # ... сравнивает с self

    def is_there_siblings(self, nodes):
        for node in nodes:
            if self.are_we_same(node):
                return True
        return False


# Эвристический поиск

def A(start, target, h): #h = True - h1, иначе h2

    start_node = Node(start, None, 0)

    # это костыль чтобы не ломалось условие на строке 195, убирать нельзя
    start_node.parent = start_node

    # На всякий выводим инфу о корне
    start_node.about_node()

    queue = {} # из куеуе
    passed = {}

    # Если начальное состояние = конечное, то возвращаем его
    if start_node.state.check_goal(target):
        return start_node

    step = 0

    # сразу обзываем узел на текущем шаге current
    current_node = start_node.copy()

    while True:
        step += 1

        # если текущее состояние = целевое - возвращаем его
        if current_node.state.check_goal(target):
            return current_node

        # если попали в узел, где уже были, берем следующий по приоритету (с минимальным f) из куеуе
        if current_node.is_there_siblings(queue):
            print('Я дубликат')
            current_node = min(queue, key=queue.get).copy()
            print("Замена мне: ")
            current_node.about_node()

        print(f"\n--- Шаг {step} ---")
        print(f"Текущая вершина для раскрытия (глубина {current_node.depth}):")
        print(current_node.state)

        # словарь для значений f. Вид - {узел Node : значение f его состояния}
        f_values = {}

        # записали в moves доступные ходы
        moves = current_node.state.sequence()

        if 'u' in moves:
            up_state = current_node.state.up()
            up_node = Node(up_state, current_node, current_node.depth + 1, 'u')

            # условие - проверяем матрицу родителя, чтобы не ходить кругами и проверяем, не попадем 
            # ли в пройденное состояние, если пойдет по этому пути
            if str(up_state.matrix) not in passed and up_node.state.matrix != current_node.parent.state.matrix:
                if h == True:
                    f_values[up_node] = up_node.depth + up_state.h1(target)
                if h == False:
                    f_values[up_node] = up_node.depth + up_state.h2(target)

        if 'd' in moves:
            down_state = current_node.state.down()
            down_node = Node(down_state, current_node, current_node.depth + 1, 'd')

            # условие - проверяем матрицу родителя, чтобы не ходить кругами и проверяем, не попадем 
            # ли в пройденное состояние, если пойдет по этому пути
            if str(down_state.matrix) not in passed  and down_node.state.matrix != current_node.parent.state.matrix:
                if h == True:
                    f_values[down_node] = down_node.depth + down_state.h1(target)
                if h == False:
                    f_values[down_node] = down_node.depth + down_state.h2(target)

        if 'r' in moves:
            right_state = current_node.state.right()
            right_node = Node(right_state, current_node, current_node.depth + 1, 'r')

            # условие - проверяем матрицу родителя, чтобы не ходить кругами и проверяем, не попадем 
            # ли в пройденное состояние, если пойдет по этому пути
            if str(right_state.matrix) not in passed and right_node.state.matrix != current_node.parent.state.matrix:
                if h == True:
                    f_values[right_node] = right_node.depth + right_state.h1(target)
                elif h == False:
                    f_values[right_node] = right_node.depth + right_state.h2(target)


        if 'l' in moves:
            left_state = current_node.state.left()
            left_node = Node(left_state, current_node, current_node.depth + 1, 'l')

            # условие - проверяем матрицу родителя, чтобы не ходить кругами и проверяем, не попадем 
            # ли в пройденное состояние, если пойдет по этому пути
            if str(left_state.matrix) not in passed and left_node.state.matrix != current_node.parent.state.matrix:
                if h == True:
                    f_values[left_node] = left_node.depth + left_state.h1(target)
                if h == False:
                    f_values[left_node] = left_node.depth + left_state.h2(target)

        # в passed по ключу current_node записываем его значение f
        if h == True:
            passed[current_node] = current_node.depth + current_node.state.h1(target)
        if h == False:
            passed[current_node] = current_node.depth + current_node.state.h2(target)

        # new_node по приколу копия, в нее записываем приоритетный узел с минимальным f
        new_node = min(f_values, key=f_values.get)

        # удаляем new_node чтобы потом по нему еще раз не сходить
        f_values.pop(new_node)

        # добавляем в куеуе f_values, чтобы потом можно было по ним сходить
        queue.update(f_values)

        # очищаем f_values, чтобы на новом шаге цикла снова рассматривать текущие 4 варианта куда пойти
        f_values = {}

        # ура, current_node становится new_node
        current_node = new_node.copy()


def info():

    start_matrix = [[5, 8, 3], [4, '*', 2], [7, 6, 1]]
    target_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, '*']]

    empty_x = 1
    empty_y = 1

    start = State(start_matrix, empty_x, empty_y)
    print('Матрица с начальным состоянием: ')
    print(start)

    # создали матрицу с целевым состоянием
    target = State(target_matrix, 2, 2)
    print('Матрица с конечным состоянием:')
    print(target)
    choice = 0
    while choice != 3:
        print('Вы хотите обход:\n   1. h1\n   2. h2\n   3. Выход\n')
        choice = int(input())
        if choice == 1:
            A(start, target, True)
        elif choice == 2:
            A(start, target, False)
        elif choice == 3:
            print('Выход')
        else:
            print('Некорректный ввод')


info()