# Desc: Makefile for the parse.py script
VER=python3.11
EXE=parse.py
INPUT=test.sol
OUTPUT=test.sol.out

all: $(EXE)
	$(VER) $(EXE) < $(INPUT) > $(OUTPUT)

test:
	pytest

clean:
	rm -f $(OUTPUT)
	



