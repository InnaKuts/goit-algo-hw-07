class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

    def __str__(self, direction=0, level="", prefix="─── "):
        ret = ""
        if self.left:
            ret += self.left.__str__(-1, level + ("│   " if direction == 1 else "    "), "┌── ")
        ret += level + prefix + str(self.key) + "\n"
        if self.right:
            ret += self.right.__str__(1, level + ("│   " if direction == -1 else "    "), "└── ")
        return ret


class AVLTree:
    _node: AVLNode = None

    @property
    def height(self):
        return get_height(self._node)

    @property
    def balance(self):
        return get_balance(self._node)

    def insert(self, key):
        self._node = insert(self._node, key)

    def insert_range(self, rng: list):
        for k in rng:
            self.insert(k)

    def delete(self, key):
        self._node = delete_node(self._node, key)

    def __str__(self):
        return str(self._node)

    # task_01
    def min(self):
        if self._node is None:
            return None
        node = self._node
        while node.left is not None:
            node = node.left
        return node.key

    # task_02
    def max(self):
        if self._node is None:
            return None
        node = self._node
        while node.right is not None:
            node = node.right
        return node.key

    # task_03
    def traverse(self, fun: callable):
        traverse(self._node, fun)

    def reduce(self, fun: callable, init=0):
        result = init

        def reducer(x):
            nonlocal result
            result = fun(result, x)
        self.traverse(reducer)
        return result

    def sum(self):
        return self.reduce(int.__add__)


def get_height(node):
    if not node:
        return 0
    return node.height


def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)


def left_rotate(z):
    y = z.right
    t2 = y.left

    y.left = z
    z.right = t2

    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))

    return y


def right_rotate(y):
    x = y.left
    t3 = x.right

    x.right = y
    y.left = t3

    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))

    return x


def min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current


def insert(root, key):
    if not root:
        return AVLNode(key)

    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))

    balance = get_balance(root)

    if balance > 1:
        if key < root.left.key:
            return right_rotate(root)
        else:
            root.left = left_rotate(root.left)
            return right_rotate(root)

    if balance < -1:
        if key > root.right.key:
            return left_rotate(root)
        else:
            root.right = right_rotate(root.right)
            return left_rotate(root)

    return root


def delete_node(root, key):
    if not root:
        return root

    if key < root.key:
        root.left = delete_node(root.left, key)
    elif key > root.key:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            temp = root.right
            root = None
            return temp
        elif root.right is None:
            temp = root.left
            root = None
            return temp

        temp = min_value_node(root.right)
        root.key = temp.key
        root.right = delete_node(root.right, temp.key)

    if root is None:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))

    balance = get_balance(root)

    if balance > 1:
        if get_balance(root.left) >= 0:
            return right_rotate(root)
        else:
            root.left = left_rotate(root.left)
            return right_rotate(root)

    if balance < -1:
        if get_balance(root.right) <= 0:
            return left_rotate(root)
        else:
            root.right = right_rotate(root.right)
            return left_rotate(root)

    return root


def traverse(root: AVLNode, fun: callable):
    if root is None:
        return
    visited = set()
    stack = [root]
    while len(stack) > 0:
        node = stack.pop()
        if node in visited:
            continue
        fun(node.key)
        if node.left and node.left not in visited:
            stack.append(node.left)
        if node.right and node.right not in visited:
            stack.append(node.right)
