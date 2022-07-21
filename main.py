import random
from graphviz import Digraph
from collections import deque


class BinaryTree:
    root = None

    class Node:
        def __init__(self, elem):
            self.elem = elem
            self.left = None
            self.right = None
            self.parent = None

    def __init__(self):
        self.root = None
        self.amount = 0
        self.width = 0

    def _push(self, elem, root):
        if root.elem > elem:
            if root.left is None:
                root.left = self.Node(elem)
            else:
                self._push(elem, root.left)
        else:
            if root.right is None:
                root.right = self.Node(elem)
            else:
                self._push(elem, root.right)

    def push(self, elem):
        if self.root is None:
            self.root = self.Node(elem)
            self.amount += 1
        else:
            self._push(elem, self.root)
            self.amount += 1

    def push_iter(self, elem):
        new_elem = self.root
        while new_elem:
            if elem >= new_elem.elem:
                if new_elem.right:
                    new_elem = new_elem.right
                    continue
                else:
                    new_elem.right = self.Node(elem)
                    return
            else:
                if new_elem.left:
                    new_elem = new_elem.left
                    continue
                else:
                    new_elem.left = self.Node(elem)
                    return

    def _dfs(self, root):
        if root is None:
            return
        self._dfs(root.left)
        print(root.elem, end=' ')
        self._dfs(root.right)

    def dfs(self):
        self._dfs(self.root)

    def _get_height(self, root):
        if root is None:
            return 0
        else:
            return 1 + max(self._get_height(root.left), self._get_height(root.right))

    def get_height(self):
        return self._get_height(self.root)

    def _get_height_iter(self, root):
        if root is None:
            return
        queue = deque()
        queue.append(root)
        height = 0
        while queue:
            size = len(queue)
            while size > 0:
                front = queue.popleft()
                if front.left:
                    queue.append(front.left)
                if front.right:
                    queue.append(front.right)
                size = size - 1
            height = height + 1
        return height

    def get_height_iter(self):
        return self._get_height_iter(self.root)

    def _find_max(self, root):
        if root.right is not None:
            self._find_max(root.right)
        else:
            print(root.elem)

    def find_max(self):
        if self.root is None:
            self.root = self.Node(self.root)
        else:
            self._find_max(self.root)

    def _find_min(self, root):
        if root is None:
            return
        if root.left is not None:
            self._find_min(root.left)
        else:
            print(root.elem)

    def find_min(self):
        self._find_min(self.root)

    def _current_level(self, root, level):
        if root is None:
            return
        if level == 1:
            print(root.elem, end=' ')
        elif level > 1:
            self._current_level(root.left, level - 1)
            self._current_level(root.right, level - 1)

    def _level_order(self, root):
        h = self.get_height()
        for i in range(1, h + 1):
            self._current_level(root, i)
            print('\n')

    def print_level_order(self):
        self._level_order(self.root)

    def get_width(self, root, level):
        if root is None:
            return 0
        if level == 1:
            return 1
        elif level > 1:
            return self.get_width(root.left, level - 1) + self.get_width(root.right, level - 1)
        self.get_width(root.right, level - 1)

    def get_max_width(self, root):
        max_width = 0
        i = 1
        width = 0
        h = self.get_height()
        while i < h:
            width = self.get_width(root, i)
            if width > max_width:
                max_width = width
            i += 1
        return max_width

    def visualize(self, node=None):
        tree = self.root

        def add_nodes_edges(tree, dot=None):
            col = "black"
            if dot is None:
                dot = Digraph()
                dot.node(name=str(tree), label=str(tree.elem),
                         color=col, shape="circle", fixedsize="True", width="0.4")
            if tree.left:
                if node is not None and tree.left.elem == node.elem:
                    col = "green"
                dot.node(name=str(tree.left), label=str(tree.left.elem),
                         color=col, shape="circle", fixedsize="True", width="0.4")
                dot.edge(str(tree), str(tree.left))
                dot = add_nodes_edges(tree.left, dot=dot)
            if tree.right:
                if node is not None and tree.right.elem == node.elem:
                    col = "red"
                dot.node(name=str(tree.right), label=str(tree.right.elem),
                         color=col, shape="circle", fixedsize="True", width="0.4")
                dot.edge(str(tree), str(tree.right))
                dot = add_nodes_edges(tree.right, dot=dot)
            return dot

        return add_nodes_edges(tree)

    def __str__(self):
        if self.root is None:
            return ''

        def recurse(root):
            if root is None:
                return [], 0, 0
            label = str(root.elem)
            left_lines, left_pos, left_width = recurse(root.left)
            right_lines, right_pos, right_width = recurse(root.right)
            middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos
            while len(left_lines) < len(right_lines):
                left_lines.append(' ' * left_width)
            while len(right_lines) < len(left_lines):
                right_lines.append(' ' * right_width)
            if (middle - len(label)) % 2 == 1 and root.right is not None and \
                    root is root.right.left and len(label) < middle:
                label += '.'
            label = label.center(middle, '.')
            if label[0] == '.':
                label = ' ' + label[1:]
            if label[-1] == '.':
                label = label[:-1] + ' '
            lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                     ' ' * left_pos + '/' + ' ' * (middle - 2) +
                     '\\' + ' ' * (right_width - right_pos)] + \
                    [left_line + ' ' * (width - left_width - right_width) +
                     right_line
                     for left_line, right_line in zip(left_lines, right_lines)]
            return lines, pos, width

        return '\n'.join(recurse(self.root)[0])


if __name__ == '__main__':
    btr = BinaryTree()

    list_nums = [random.randint(0, 60) for _ in range(30)]
    print("Random list = ", list_nums)

    list_txt = open('list-binary-tree.txt', 'wt')
    for i in list_nums:
        list_txt.write(str(i) + ' ')
    list_txt.close()

    list_txt = open('list-binary-tree.txt', 'r')
    str_nums = list_txt.readline().split()
    new_s = [int(item) for item in str_nums]
    for i in new_s:
        btr.push(i)
    list_txt.close()

    print("Height:", btr.get_height())
    print("Height iter:", btr.get_height_iter())
    print("Width:", btr.get_max_width(btr.root), end=" ")
    print("\nMax:", end=" ")
    btr.find_max()
    print("Min:", end=" ")
    btr.find_min()

    print("Depth-first search:", end=" ")
    btr.dfs()
    print('\nBreadth-first search:')
    btr.print_level_order()

    print(btr)
    bin_tree_txt = open('binary-tree.txt', 'w')
    bin_tree_txt.write(str(btr))
    bin_tree_txt.close()

    btr.visualize().render('binary-tree', view=True)
    print("Successfully!!!")
