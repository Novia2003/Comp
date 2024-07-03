from abc import abstractmethod, ABC
from typing import Tuple, Callable, Optional


class TreeNode(ABC):
    def __init__(self, row: Optional, col: Optional):
        super().__init__()
        self.row = row
        self.col = col

    @property
    def children(self) -> Tuple['TreeNode', ...]:
        return ()

    @property
    def tree(self) -> [str, ...]:
        res = [str(self)]
        children_temp = self.children
        for i, child in enumerate(children_temp):
            ch0, ch = '├', '│'
            if i == len(children_temp) - 1:
                ch0, ch = '└', ' '
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return res

    @abstractmethod
    def __str__(self):
        pass

    def visit(self, func: Callable[['TreeNode'], None]) -> None:
        func(self)
        map(func, self.children)

    def __getitem__(self, index):
        return self.children[index] if index < len(self.children) else None


class EvalNode(TreeNode):
    pass


class ValueNode(EvalNode):
    pass


class ExprNode(EvalNode):
    pass


class LiteralNode(ValueNode):
    def __init__(self, row, col, value):
        super().__init__(row, col)
        self.value = value

    def __str__(self) -> str:
        return str(self.value) if not isinstance(self.value, str) else '"{}"'.format(self.value)


class IdentNode(ValueNode):
    def __init__(self, row, col, name):
        super().__init__(row, col)
        self.name = name

    def __str__(self) -> str:
        return str(self.name)


class BinExprNode(ExprNode):
    def __init__(self, row, col, op, left, right):
        super().__init__(row, col)
        self.left = left
        self.right = right
        self.op = op

    @property
    def children(self) -> Tuple[EvalNode, EvalNode]:
        return self.left, self.right

    def __str__(self) -> str:
        return str(self.op.value)


class UnaryExprNode(ExprNode):
    def __init__(self, row, col, op, argument):
        super().__init__(row, col)
        self.op = op
        self.argument = argument

    @property
    def children(self) -> Tuple[EvalNode]:
        return (self.argument,) if self.argument else tuple()

    def __str__(self) -> str:
        return str(self.op.value)


class DeclaratorNode(TreeNode):
    def __init__(self, row, col, ident: IdentNode, init: EvalNode = None):
        super().__init__(row, col)
        self.ident = ident
        self.init = init

    @property
    def children(self) -> Tuple[EvalNode]:
        return (self.init,) if self.init else tuple()

    def __str__(self) -> str:
        return str(self.ident)


class VarDeclarationNode(TreeNode):
    def __init__(self, row, col, *declarations: DeclaratorNode):
        super().__init__(row, col)
        self.declarations = declarations

    @property
    def children(self) -> Tuple[DeclaratorNode]:
        return self.declarations

    def __str__(self) -> str:
        return 'var'


class BlockStatementNode(TreeNode):
    def __init__(self, row, col, *nodes: TreeNode):
        super().__init__(row, col)
        self.nodes = nodes

    @property
    def children(self) -> Tuple[TreeNode]:
        return self.nodes

    def __str__(self) -> str:
        return 'block'


class ArgsNode(TreeNode):
    def __init__(self, row, col, *params: Tuple[IdentNode]):
        super().__init__(row, col)
        self.params = params

    def __str__(self) -> str:
        return 'args: ' + ', '.join(str(p) for p in self.params)


class FuncDeclarationNode(TreeNode):
    def __init__(self, row, col, ident: IdentNode, params: Optional[ArgsNode], block: BlockStatementNode):
        super().__init__(row, col)
        self.ident = ident
        self.params = params
        self.block = block

    @property
    def children(self) -> Tuple[ArgsNode, BlockStatementNode]:
        return self.params, self.block

    def __str__(self) -> str:
        return 'function ' + str(self.ident)


class IfNode(TreeNode):
    def __init__(self, row, col, test: EvalNode, consequent: BlockStatementNode, alternate: BlockStatementNode = None):
        super().__init__(row, col)
        self.test = test
        self.consequent = consequent
        self.alternate = alternate

    @property
    def children(self) -> Tuple[EvalNode, ...]:
        return (self.test, self.consequent) + ((self.alternate,) if self.alternate else tuple())

    def __str__(self) -> str:
        return 'if'


class ForNode(TreeNode):
    def __init__(self, row, col, init: VarDeclarationNode, test: EvalNode, update: EvalNode, block: BlockStatementNode):
        super().__init__(row, col)
        self.init = init
        self.test = test
        self.update = update
        self.block = block

    @property
    def children(self) -> Tuple[VarDeclarationNode, EvalNode, EvalNode, BlockStatementNode]:
        return self.init, self.test, self.update, self.block

    def __str__(self) -> str:
        return 'for'


class WhileNode(TreeNode):
    def __init__(self, row, col, test: EvalNode, block: BlockStatementNode):
        super().__init__(row, col)
        self.test = test
        self.block = block

    @property
    def children(self) -> Tuple[EvalNode, BlockStatementNode]:
        return self.test, self.block

    def __str__(self) -> str:
        return 'while'


class DoWhileNode(TreeNode):
    def __init__(self, row, col, block: BlockStatementNode, test: EvalNode):
        super().__init__(row, col)
        self.block = block
        self.test = test

    @property
    def children(self) -> Tuple[BlockStatementNode, EvalNode]:
        return self.block, self.test

    def __str__(self) -> str:
        return 'do while'


class CallNode(TreeNode):
    def __init__(self, row, col, ident: IdentNode, *args: EvalNode):
        super().__init__(row, col)
        self.ident = ident
        self.args = args
        self.name = ident.name

    @property
    def children(self) -> Tuple[IdentNode, EvalNode]:
        return (self.ident,) + self.args

    def __str__(self) -> str:
        return 'call'


class ReturnNode(TreeNode):
    def __init__(self, row, col, argument: EvalNode):
        super().__init__(row, col)
        self.argument = argument

    @property
    def children(self) -> Tuple[EvalNode, ...]:
        return self.argument,

    def __str__(self) -> str:
        return 'return'
