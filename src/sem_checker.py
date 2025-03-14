"""
    @file: sem_checker.py
    @brief: Soubor pro semantickou kontrolu AST stromu
    @author: Jakub Fukala (xfukal01)
    @details:
      - 31: Chybí Main / run
      - 32: Různé nedefinované (třída, proměnná, parent třídy, ...), nedef. třídní metoda
      - 33: Arita
      - 34: Kolize param vs lokální var, param je read-only
      - 35: Duplicitní param vs param, redefinice třídy, cyklická dědičnost
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
        self.builtin_class_methods = {
            "Object": {"new", "from:"},
            "Nil": {"new", "from:"},
            "True": {"new", "from:"},
            "False": {"new", "from:"},
            "Integer": {"new", "from:"},  
            "String": {"new", "from:", "read"},
            "Block": {"new", "from:"}
        }

        self.class_parents = {} # Rodicovske tridy


    def check(self):
        '''Spusteni semantickych kontrol'''
        # Sbírání definovaných tříd 
        self._collect_classes() 
        # Kontrola existence Main tridy a metody run => (31)
        self._check_main_class() 
        # Kontrola definic => rodičovská třída, počet parametrů => (32), (33)
        self._check_all_classes()
        # Kontrola cyklické dědičnosti => (35)
        self.check_no_cycles()



    def _collect_classes(self):
        '''Naplneni seznamu definovanych trid'''
        seen = set()
        for c in self.ast_root.classes:
            # Redeinice tridy?
            if c.name in seen:
                print(f"Class {c.name} redefined", file=sys.stderr)
                sys.exit(35)
            seen.add(c.name)

            self.defined_classes.add(c.name)
            self.class_parents[c.name] = c.parent # pro check_no_cycles

    def get_all_methods(self, class_name):
        ''' Získání všech metod pro danou třídu včetně zděděných '''
        methods = set()
        checked_classes = set()

        while class_name and class_name not in checked_classes:
            checked_classes.add(class_name)

            # Přidání metod aktuální třídy
            class_obj = next((c for c in self.ast_root.classes if c.name == class_name), None)
            if class_obj:
                for method in class_obj.methods:
                    methods.add(method.selector)

            # Posun na rodičovskou třídu
            class_name = self.class_parents.get(class_name)

            # Pokud je to built-in třída, zkusíme její metody
            if class_name in self.builtin_class_methods:
                methods.update(self.builtin_class_methods[class_name])

        return methods


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

                # Kontrola duplicitnich parametru bloku
                if len(m.block.params) != len(set(m.block.params)):
                    print("Duplicate block params", file=sys.stderr)
                    sys.exit(35) # Duplicitni parametry

                self._check_block(m.block, builtins_vars)

    def _check_block(self, block, parent_builtins):
        
        local_vars = set(parent_builtins) 
        param_vars = set(block.params) # Parametry bloku

        local_vars |= param_vars
        
        for st in block.statements: # Pro kazdy statement
            if isinstance(st, AssignNode):
                # Kontrola expr
                self._check_expr(st.expr, local_vars)
                # Kolize jmen promennych
                if st.var in param_vars:
                    print(f"Variable {st.var} already defined", file=sys.stderr)
                    sys.exit(34)
                # Pak kontrola vyrazu, zda neni pouzita nedefinovana promenna

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
            self._check_expr(expr.receiver, local_vars)
            for arg in expr.arguments:
                self._check_expr(arg, local_vars)

            if isinstance(expr.receiver, LiteralNode) and expr.receiver.type == "class":
                # Kontrola, zda trida ma metodu
                class_name = expr.receiver.value    # Napr. "Integer"
                sel = expr.selector                 # Napr. "new"        

                # Zjisteni vsech metod
                available_methods = self.get_all_methods(class_name)

                if sel not in available_methods:
                    print(f"Class {class_name} has no method {sel}", file=sys.stderr)
                    sys.exit(32)
        
        elif isinstance(expr, BlockNode):
            #buildins = {"self", "nil", "true", "false"}
            new_scope = set(expr.params) | local_vars
            # Kontrola duplicitnich parametru bloku
            if len(expr.params) != len(set(expr.params)):
                print("Duplicate block params", file=sys.stderr)
                sys.exit(35)
            self._check_block(expr, new_scope)
        else:
            pass
    
    def check_no_cycles(self):
        """Kontrola cyklické dědičnosti"""
        visited = set()
        stack = set()

        def dfs(cls_name):
            if cls_name in stack:
                print("Cycle in class hierarchy", file=sys.stderr)
                sys.exit(35)
            if cls_name in visited:
                return
            visited.add(cls_name)
            stack.add(cls_name)

            parent = self.class_parents.get(cls_name)
            if parent in self.defined_classes:
                dfs(parent)
            
            stack.remove(cls_name)

        for c in self.defined_classes:
            if c not in visited:
                dfs(c)
                
                

# Konec souboru sem_checker.py (EOF)   
                    
                    


    