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
        self.ast_root = ast_root # Korenovy uzel AST stromu
        self.defined_classes = set()  # Taulka s definovanymi tridami (bez built-in trid)
        self.builtin_classes = {"Object", "String", "Integer", "Nil", "True", "False", "Block", "Nil"}
        #TODO self.builtin_methods = {

    def check(self):
        '''Spusteni semantickych kontrol'''
        self._collect_classes() # Naplni self.defined_classes
        self._check_main_class() # (31) Kontrola existence Main tridy
        self._check_all_classes() # (33) Kontrola vsech trid

    def _collect_classes(self):
        '''Naplneni seznamu definovanych trid'''
        for c in self.ast_root.classes:
            # Registrace tridy do seznamu
            self.defined_classes.add(c.name)

    def _check_main_class(self):
        '''Kontrola existence Main tridy a metody run'''
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
    
    def _check_all_classes(self):
        '''Kontrola vsech trid'''
        for c in self.ast_root.classes:
            # (32) Kontrola existence rodicovske tridy
            if c.parent not in (self.defined_classes | self.builtin_classes):
                print(f"Parent class {c.parent} not defined", file=sys.stderr)
                sys.exit(32)
            for m in c.methods:
                # (33) Kontrola poctu parametru metody
                expected_params =  m.selector.count(":")
                block_params_count = len(m.block.params)
                if expected_params != block_params_count:
                    print(f"Method {m.selector} expected {expected_params} params, got {block_params_count}", file=sys.stderr)
                    sys.exit(33) # Arita metody

                builtins_vars = {"self", "nil", "true", "false"}

                initial_defined = set(m.block.params) | builtins_vars

                if len(m.block.params) != len(set(m.block.params)):
                    sys.exit(34) # Duplicitni parametry

                self._check_block(m.block, initial_defined)

    def _check_block(self, block, defined_vars):
        # Kopie lokalnich promennych
        local_vars = set(defined_vars)

        for st in block.statements: # Pro kazdy statement
            if isinstance(st, AssignNode):
                self._check_expr(st.expr, local_vars)
                # Kolize jmen promennych
                if st.var in local_vars:
                    print(f"Variable {st.var} already defined", file=sys.stderr)
                    sys.exit(34)
                # Pak kontrola vyrazu, zda neni pouzita nedefinovana promenna
                self._check_expr(st.expr, local_vars)

                # Pridani promenne do lokalnich promennych
                local_vars.add(st.var)
            else:
                print("Unknown statement type", file=sys.stderr)
                sys.exit(99)

    def _check_expr(self, expr, local_vars):
        if isinstance(expr, VarNode):
            if expr.var not in local_vars:
                print(f"Variable {expr.var} not defined", file=sys.stderr)
                sys.exit(32)
        elif isinstance(expr, LiteralNode):
            if expr.type == "class" :
                if expr.value not in (self.defined_classes | self.builtin_classes):
                    print(f"Class {expr.value} not defined", file=sys.stderr)
                    sys.exit(32)
                else:
                    # Je to "int", "string", "nil", "true", "false" => nic nedelame
                    pass
        
        elif isinstance(expr, SendNode):
            # rekurze => receiver, arguments
            self._check_expr(expr.receiver, local_vars)
            for arg in expr.arguments:
                self._check_expr(arg, local_vars)
        
        elif isinstance(expr, BlockNode):
            buildins = {"self", "nil", "true", "false"}
            new_scope = set(expr.params) | buildins
            # Kolize parametru => [ :x :x ] => error 34
            if len(expr.params) != len(set(expr.params)):
                print("Duplicate block params", file=sys.stderr)
                sys.exit(34)
            self._check_block(expr, new_scope)
        else:
            pass
            

     
                    
                    


    