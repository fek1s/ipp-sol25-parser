# Desc: Makefile for the parse.py script
VER=python3.11
EXE=parse.py
INPUT=test.sol
OUTPUT=out.xml

all: $(EXE)
	$(VER) $(EXE) < $(INPUT) > $(OUTPUT)

test:
	pytest tests/ --tb=short

pack:
	rm -rf testdir
	./pack.sh 
	./is_it_ok.sh xfukal01.zip testdir

clean:
	rm -f $(OUTPUT)
	rm -rf testdir
	rm -f is_it_ok.log
	



