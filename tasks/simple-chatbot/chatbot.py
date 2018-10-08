#!/usr/bin/env python3

import os, sys, rl3

# init RL3 engine
engine = rl3.RL3Engine()

# load 'intents' model
engine.load('./intent.rl3c')

# init factsheet for background knowledge and user input
facts = engine.create_factsheet()

# default answer
def answer_default(weight, subfacts):
    return 'How can I help you?'

# answer to 'hello' intent
def answer_hello(weight, subfacts):
    return 'Hi! Nice to meet you.'

#answer to 'goodbye' intent
def answer_goodbye(weight, subfacts):
    return 'Bye-bye!'

# init answers db
answers = {
    '': answer_default,
    'hello': answer_hello,
    'goodbye': answer_goodbye
}

# find best intent
def get_intent(fs):
    name = ''
    weight = 0.0
    subfacts = None

    if fs.has_fact('intent'):
        for i in fs.get_facts('intent'):
            if i.get_weight() > weight:
                name = i.get_value()
                weight = i.get_weight()
                if i.has_factsheet():
                    subfacts = i.get_factsheet()

    return (name, weight, subfacts)

# produce bot answer
def think(user_input):
    # init factsheet for conclusions
    conclusions = engine.create_factsheet()

    # delete old input fact
    facts.retract_facts('text')

    # assert new input fact
    facts.assert_simple_fact('text', user_input)

    # detect all intents
    engine.run(facts, conclusions)

    # find best intent
    name, weight, subfacts = get_intent(conclusions)

    stop = (name == 'goodbye')
    if name in answers:
        answer = answers[name](weight, subfacts)
    else:
        answer = answers[''](weight, subfacts)

    return (answer, stop)

def main():
    user_input = ''

    # main loop
    while True:
        # process user input
        answer, stop = think(user_input)

        # print answer
        print('Bot: ' + answer)
        print()

        if stop:
            break

        # get new user input
        user_input = input('You: ')

main()
