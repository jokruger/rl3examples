all:
	rl3c -m model.rl3 -o model.rl3c

run:
	rl3run --model model.rl3c --type text --input test.txt

grep:
	rl3grep -o "{EMAIL}" test.txt | sort | uniq
