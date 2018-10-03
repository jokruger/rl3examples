all:
	rl3c -p ./ai/intent/project.cfg -o intent.rl3c
	rl3c -p ./ai/ner/project.cfg -o ner.rl3c

run:
	rl3run -m intent.rl3c -t text -n text -i text.txt
	rl3run -m ner.rl3c -t text -n text -i text.txt
