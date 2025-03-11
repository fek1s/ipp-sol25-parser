# Desc: Makefile for the parse.py script
VER=python3.11
EXE=parse.py
INPUT=test.sol
OUTPUT=test.sol.out

all: $(EXE)
	$(VER) $(EXE) < $(INPUT)

test:
	pytest tests/ --tb=short

clean:
	rm -f $(OUTPUT)
	



