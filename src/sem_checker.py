"""
    @file: sem_checker.py
    @brief: Soubor pro semantickou kontrolu AST stromu
    @author: Jakub Fukala (xfukal01)
"""

import sys
from src.ast_nodes import (
    ProgramNode,
    ClassNode,
    MethodNode,
    BlockNode,
    AssignNode,
    SendNode,
    LiteralNode,
    VarNode,
)

class SemChecker:
    def __init__(self, ast_root):
        self.ast_root = ast_root
        self.defined_classes = set()
        self.builtin_classes = {"Object", "String", "Integer", "Nil", "True", "False", "Block", "Nil"}
        #TODO self.builtin_methods = {

    def check(self):
        self._collect_classes() # Naplni self.defined_classes
        self._check_main_class() # Kontrola existence Main tridy
        #self._check_all_classes() # Kontrola vsech trid

    def _collect_classes(self):
        for c in self.ast_root.classes:
            # Registrace tridy do seznamu
            self.defined_classes.add(c.name)

    def _check_main_class(self):
        # Kontrola existence Main tridy
        main_class = None
        for c in self.ast_root.classes:
            if c.name == "Main":
                main_class = c
                break
        
        if main_class is None:
            # Main trida neexistuje
            print("Main class not found", file=sys.stderr)
            sys.exit(31)

        found_run = False
        for m in main_class.methods:
            colon_count = m.selector.count(":")
            if m.selector == "run" and colon_count == 0:
                found_run = True
                break
        
        if not found_run:
            # Metoda run neexistuje
            print("Method run not found in Main class", file=sys.stderr)
            sys.exit(31)


    