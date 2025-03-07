import keyboard
import tracemalloc
import time
import sys
import math

class State:
    def __init__(self, matrix, empty_one_x, empty_one_y):
        # начальное состояние
        self.matrix = matrix
        # x - столбец (элемент внутри списка)
        # y - строка (список внутри списка)
        self.empty_one_x = empty_one_x
        self.empty_one_y = empty_one_y

    #  перемещаем пустоту слева направо
    def left(self):
        if self.empty_one_y > 0:
            self.matrix[self.empty_one_x][self.empty_one_y], self.matrix[self.empty_one_x][self.empty_one_y - 1] \
                = self.matrix[self.empty_one_x][self.empty_one_y - 1], self.matrix[self.empty_one_x][self.empty_one_y]
            self.empty_one_y -= 1
            return self

    #  перемещаем пустоту справа налево
    def right(self):
        if self.empty_one_y < 2:
            self.matrix[self.empty_one_x][self.empty_one_y], self.matrix[self.empty_one_x][self.empty_one_y + 1] \
                = self.matrix[self.empty_one_x][self.empty_one_y + 1], self.matrix[self.empty_one_x][self.empty_one_y]
            self.empty_one_y += 1
            return self

    #  перемещselfаем пустоту сверху вниз
    def down(self):
        if self.empty_one_x < 2:
            self.matrix[self.empty_one_x][self.empty_one_y], self.matrix[self.empty_one_x + 1][self.empty_one_y] \
                = self.matrix[self.empty_one_x + 1][self.empty_one_y], self.matrix[self.empty_one_x][self.empty_one_y]
            self.empty_one_x += 1
            return self

    #  перемещаем пустоту снизу вверх
    def up(self):
        if self.empty_one_x > 0:
            self.matrix[self.empty_one_x][self.empty_one_y], self.matrix[self.empty_one_x - 1][self.empty_one_y] \
                = self.matrix[self.empty_one_x - 1][self.empty_one_y], self.matrix[self.empty_one_x][self.empty_one_y]
            self.empty_one_x -= 1
            return self

    # вот эта шняга теперь просто возвращает строку, а не печатает, чтобы можно было в файл записать
    def __str__(self):
        result = ['\n']
        
        for i in range(3):
            row = ' '.join(str(self.matrix[i][j]) for j in range(3))
            result.append(row)

        result.append('\n')

        return '\n'.join(result)

    def sequence(self):
        actions = ''
        if self.up():
            actions += 'u'
            self.down()
        if self.down():
            actions += 'd'
            self.up()
        if self.right():
            actions += 'r'
            self.left()
        if self.left():
            actions += 'l'
            self.right()
        return actions

    def check_goal(self, target_matrix):
        return self.matrix == target_matrix

    def copy(self):
        new_matrix = [row.copy() for row in self.matrix]
        return State(new_matrix, self.empty_one_x, self.empty_one_y)

    def h1(self, target):
        count = 0
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != target.matrix[i][j]:
                    count += 1
        return count

    def find_item(self, item):
        for i in range(3):
            for j in range(3):
                if item == self.matrix[i][j]:
                    return (i, j)
        return False

    def h2(self, target):
        item = 0
        #positions = []
        lengths = []
        for i in range(3):
            for j in range(3):
                item = self.matrix[i][j]
                position = target.find_item(item)
                #positions.append(position)
                lengths.append(abs(position[0] - i) + abs(position[1] - j))
    
        return sum(lengths)


class Node:
    def __init__(self, state, parent=None, depth=0, action=None): #тут поменяла значение глубины на 0
        self.depth = depth
        self.action = action
        self.parent = parent
        self.state = state

# Функция эвристического поиска

def A(start, target_matrix):

    start_node = Node(start, None, 0)

    # Если начальное состояние = конечное, то возвращаем его
    if start_node.state.check_goal(target_matrix):
        return start_node

    # Объявляем очередь из узлов
    a_queue = [start_node]
    # Пройденные узлы записываем в виде множества
    passed_state_matrixes = set()
    step = 0

    # Считаем аддитивную оценочную стоимость
    f = start_node.depth + start.h1(target_matrix)

    print(f)

    node = a_queue[0]

    # Пока не дошли до конечного состояния или не прошли все возможные узлы
    while len(a_queue) < 10:
        step += 1
        passed_state_matrixes.add(str(node.state.matrix))

        print(f"\n--- Шаг {step} ---")
        print(f"Текущая вершина для раскрытия (глубина {node.depth}):")
        print(node.state)

        new_nodes = []
        repeated_nodes = []
        lengths = []

        for move in node.state.sequence():

            new_state = node.state.copy()

            if move == 'u':
                u_state = new_state.up()
                u_node = Node(u_state, node, node.depth + 1, move)
                f = u_node.depth + u_state.h1(target_matrix)
                lengths.append(f)
            else:
                lengths.append(math.inf)

            if move == 'd':
                d_state = new_state.down()
                d_node = Node(d_state, node, node.depth + 1, move)
                f = d_node.depth + d_state.h1(target_matrix)
                lengths.append(f)
            else:
                lengths.append(math.inf)

            if move == 'r':
                r_state = new_state.right()
                r_node = Node(r_state, node, node.depth + 1, move)
                f = r_node.depth + r_state.h1(target_matrix)
                lengths.append(f)
            else:
                lengths.append(math.inf)

            if move == 'l':
                l_state = new_state.left()
                l_node = Node(l_state, node, node.depth + 1, move)
                f = l_node.depth + l_state.h1(target_matrix)
                lengths.append(f)
            else:
                lengths.append(math.inf)

            if str(new_state.matrix) in passed_state_matrixes:
                repeated_nodes.append(new_state)
                new_state = node.state.copy()
                shortest = lengths.index(min(lengths))

                if shortest == 0:
                    new_state.up()
                elif shortest == 1:
                    new_state.down()
                elif shortest == 2:
                    new_state.left()
                elif shortest == 3:
                    new_state.right()

                child_node = Node(new_state, node, node.depth + 1, move)
                new_nodes.append(child_node)
                a_queue.append(child_node)
                passed_state_matrixes.add(str(new_state.matrix)) #добавляем в пройденные

            else:
                # новый узел для нового состояния
                child_node = Node(new_state, node, node.depth + 1, move)
                new_nodes.append(child_node)
                a_queue.append(child_node)
                passed_state_matrixes.add(str(new_state.matrix)) #добавляем в пройденные

            node = child_node

            if new_state.check_goal(target_matrix): # является ли целевым
                print("Целевое состояние достигнуто!")
                print(f"Глубина {node.depth}")
                return node
    return None


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
        
    result = A(start, target)

    if result:
        print("\nпоследовательность:", end=' ')
        actions = [] #список для последовательности перемещений
        while result:
            if result.action:
                actions.append(result.action) # заносим перемещение в список
            result = result.parent # переход к родительскому узлу
        actions.reverse() # переворачиваем список
        print(" ".join(actions)) # вывод последовательности в консоль


info()
