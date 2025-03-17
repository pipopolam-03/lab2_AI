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
        temp_state = self.copy()
        actions = ''
        if temp_state.up():
            actions += 'u'
            temp_state.down()
        if temp_state.down():
            actions += 'd'
            temp_state.up()
        if temp_state.right():
            actions += 'r'
            temp_state.left()
        if temp_state.left():
            actions += 'l'
            temp_state.right()
        return actions

    def check_goal(self, target):
        return self.matrix == target.matrix

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
        # positions = []
        f_values = []
        for i in range(3):
            for j in range(3):
                item = self.matrix[i][j]
                position = target.find_item(item)
                # positions.append(position)
                f_values.append(abs(position[0] - i) + abs(position[1] - j))
    
        return sum(f_values)
# вроде как не правильно в качестве g возьму просто глубину узла
#    def g(self, start):
#        item = 0
#        # positions = []
#        f_values = []
#        for i in range(3):
#            for j in range(3):
#                item = self.matrix[i][j]
#                position = start.find_item(item)
#                # positions.append(position)
#                f_values.append(abs(position[0] - i) + abs(position[1] - j))
#
#        return sum(f_values)
    

#    def f1(self, start, target):
#        h1 = self.h1(target)
#        g = self.g(start)
#
#        return g + h1
#
#    def f2(self, start, target):
#        h2 = self.h2(target)
#        g = self.g(start)
#
#        return g + h2


class Node:
    def __init__(self, state, parent=None, depth=0, action=None): # тут поменяла значение глубины на 0
        self.depth = depth
        self.action = action
        self.parent = parent
        self.state = state

# Функция эвристического поиска


def A(start, target):

    start_node = Node(start, None, 0)

    # Если начальное состояние = конечное, то возвращаем его
    if start_node.state.check_goal(target):
        return start_node

    # Объявляем очередь из узлов
    a_queue = [start_node]
    # Пройденные узлы записываем в виде множества
    passed_state_matrixes = set()
    step = 0

    # Считаем аддитивную оценочную стоимость
    f = start_node.depth + start.h1(target)

    print(f)

    node = a_queue[0]
    repeated_nodes = [] # за цикл

    # Пока не дошли до конечного состояния или не прошли все возможные узлы
    for _ in range(50):
        step += 1
        passed_state_matrixes.add(str(node.state.matrix))

        print(f"\n--- Шаг {step} ---")
        print(f"Текущая вершина для раскрытия (глубина {node.depth}):")
        print(node.state)

        new_nodes = []
        f_values = []
        new_state = node.state.copy()
        moves = node.state.sequence()
        f_parent = f #родительское f для проверки на монотонность #какая-то хуйня надо разобраться 

        # print(*moves)
        
        if 'u' in moves and node.action != 'd':
            u_state = new_state.up()
            new_state.down()  # возвращаем в исходное состояние
            u_node = Node(u_state, node, node.depth + 1, 'u')
            new_nodes.append(u_node) # записываем в очередь КАЖДЫЙ возможный ход
            a_queue.append(u_node)
            f = u_state.h1(target) + node.depth + 1 #тут взяла h1 и прибавила глубину = g
            print(node.depth)
            f_values.append(f)
            print(u_state.h1(target))
        else:
            f_values.append(math.inf)

        if 'd' in moves and node.action != 'u':
            d_state = new_state.down()
            new_state.up() # возвращаем в исходное состояние
            d_node = Node(d_state, node, node.depth + 1, 'd')
            new_nodes.append(d_node) # записываем в очередь КАЖДЫЙ возможный ход
            a_queue.append(d_node)
            f = d_state.h1(target) + node.depth + 1
            f_values.append(f)
            print(d_state.h1(target))
        else:
            f_values.append(math.inf)

        if 'r' in moves and node.action != 'l':
            r_state = new_state.right()
            new_state.left() # возвращаем в исходное состояние
            r_node = Node(r_state, node, node.depth + 1, 'r')
            new_nodes.append(r_node) # записываем в очередь КАЖДЫЙ возможный ход
            a_queue.append(r_node)
            f = r_state.h1(target) + node.depth + 1
            f_values.append(f)
            print(r_state.h1(target))
        else:
            f_values.append(math.inf)

        if 'l' in moves and node.action != 'r':
            l_state = new_state.left()
            new_state.right() # возвращаем в исходное состояние
            l_node = Node(l_state, node, node.depth + 1, 'l')
            new_nodes.append(l_node) # записываем в очередь КАЖДЫЙ возможный ход
            a_queue.append(l_node)
            f = l_state.h1(target) + node.depth + 1
            f_values.append(f)
            print(l_state.h1(target))
        else:
            f_values.append(math.inf)

        print(*f_values)

        if node in repeated_nodes:
            print(new_state.matrix)
            node = a_queue[a_queue.index(node) + 1]  # мб будет работать если это починить
            print(node.state.matrix)
        else:
            min_f = max(f_parent, min(f_values))

            if f_values.index(min_f) == 0 and node.action != 'd':
                    new_state.up()
                    move = 'u'
            elif f_values.index(min_f) == 1 and node.action != 'u':
                    new_state.down()
                    move = 'd'
            elif f_values.index(min_f) == 3 and node.action != 'r':
                    new_state.left()
                    move = 'l'
            elif f_values.index(min_f) == 2 and node.action != 'l':
                    new_state.right()
                    move = 'r'

            child_node = Node(new_state, node, node.depth + 1, move)
            # new_nodes.append(child_node)
            # a_queue.append(child_node)
            passed_state_matrixes.add(str(new_state.matrix)) # добавляем в пройденные

            node = child_node

            print(child_node.action)

        if new_state.check_goal(target): # является ли целевым
            print("Целевое состояние достигнуто!")
            print(f"Глубина {node.depth}")
            return node

        repeated_nodes.append(node)
        f_values = []  # мы забывали очищать этот список

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
