class TreeNode:
    def __init__(self, value = None):
        self.children: list["TreeNode"] = []
        self.parent: "TreeNode" = None
        self.value: object = value

    def goto_root(self, store: list = None):
        store.append(self.value)
        if self.parent is not None:
            self.parent.goto_root(store)

    def append_children(self, nodes: list["TreeNode"]) -> None:
        for node in nodes:
            self.children.append(node)
            node.parent = self

    def append_child(self, node: "TreeNode") -> None:
        self.children.append(node)
        node.parent = self

def print_tree(root: TreeNode, lvl = 0):
    print(f"{'-'*lvl}> Node:{lvl} Value: \n{root.value}")
    if root.children != []:
        for node in root.children:
            print_tree(node, lvl+1)


def test_goto_root() -> None:
    CHILDNO = 2
    globalList = []
    z_child = None
    
    a = TreeNode()
    a.value = "Hijo de nadie"
    a_children = [TreeNode() for i in range(CHILDNO)]
    a.append_children(a_children)

    for x in a.children:
        x_children = [TreeNode() for i in range(CHILDNO)]
        x.value = "Hijo de A"
        x.append_children(x_children)

        for y in x.children:
            y.value = "Hijo de X"
            y_children = [TreeNode() for i in range(CHILDNO)]
            y.append_children(y_children)

            for z in y.children:
                x.value = "Hijo de Y"
                z_children = [TreeNode() for i in range(CHILDNO)]
                z.append_children(z_children)

                for w in z.children:
                    w.value = "Hijo de Z"
                    z_child = w     # Solo el ultimo va a quedar guardado

    z_child.goto_root(globalList)
    print(globalList)


if __name__ == "__main__":
    MAXITER = 10

    root = TreeNode()
    curr_nodes = [root]

    for i in range(MAXITER):
        print(f"Nivel: {i}")
        next_nodes = []

        for j in range(len(curr_nodes)):
            children_nodes = []
            curr_node = curr_nodes[j]

            for k in range(2):
                child_node = TreeNode()
                children_nodes.append(child_node)
                next_nodes.append(child_node)

            curr_node.append_children(children_nodes)

        curr_nodes = next_nodes

    print("Arbol listo!")

    print_tree(root)

    
