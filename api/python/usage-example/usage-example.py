#!/usr/bin/env python3

import rl3

# create engine
engine = rl3.RL3Engine()

# parse and compile (link) simple annotation pattern
definition = engine.make_simple_annotation_def("text", r"(?i:{dawg continent})", "continent")
engine.parse(definition)
engine.link()

# create factsheet
fs = engine.create_factsheet()

# assert input text
fs.assert_simple_fact("text", "Antarctica is Earth's southernmost continent... Europe is the sixth largest continent in size.")

# run engine - it should now annotate a continent names mentioned in our text
engine.update(fs);

# iterate and print all "continent" annotations
for i in fs.get_facts("continent"):
    print (i.get_value())
