from avl_tree import AVLTree
from random import randint


def main():
    tree = AVLTree()
    vals = [randint(1, 20) for _ in range(10)]
    tree.insert_range(vals)
    print(f'AVL:\n{tree}')
    print(f'Min = {tree.min()}')
    print(f'Max = {tree.max()}')
    print(f'Sum = {tree.sum()}')


if __name__ == "__main__":
    main()
