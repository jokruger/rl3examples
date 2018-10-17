#!/usr/bin/env python3

import random, re, rl3

class Answer():
    def __init__(self, message=None, stop=False):
        self.message = message
        self.stop = stop

def substitute(text, factsheet):
    t = text
    if factsheet is not None and len(factsheet) > 0:
        for i in factsheet.get_facts():
            t = t.replace('{%s}' % i.get_label(), i.get_value())
    return t

def make_answer(templates, subfacts, context):
    random.shuffle(templates)
    for i in templates:
        try:
            t = substitute(i, subfacts)
            t = substitute(i, context)
            if re.search(r"{[a-zA-Z0-9_\-]+}", t) is None:
                return Answer(message=t)
        except:
            pass

    return None

class Actions():
    def __init__(self):
        pass

    def bot_name(self, w, subfacts, conclusions, context):
        return Answer(message="Yes?")

    def goodbye(self, w, subfacts, conclusions, context):
        return Answer(message=random.choice(["Goodbye.", "Bye-bye."]), stop=True)

    def hello(self, w, subfacts, conclusions, context):
        return(make_answer(["Hello!", "Hi there!", "Hi."], subfacts, context))

    def what_is_your_name(self, w, subfacts, conclusions, context):
        return make_answer(["My name is {bot_name}.", "Call me {bot_name}."], subfacts, context)

    def what_is_x(self, w, subfacts, conclusions, context):
        return make_answer(["I know nothing about {X}."], subfacts, context)

class Chatbot():
    def __init__(self, name):
        self.name = name
        self.actions = Actions()
        self.engine = rl3.RL3Engine()
        self.engine.load('./intent.rl3c')

    def get_intents(self, fs):
        groups = dict()
        for i in fs.get_facts('intent'):
            k = int(i.get_weight() * 1000)
            if k not in groups:
                groups[k] = []
            groups[k].append((i.get_value(), i.get_weight(), i.get_factsheet() if i.has_factsheet() else None))
        intents = []
        for i in sorted(groups.keys(), reverse=True):
            t = groups[i]
            random.shuffle(t)
            intents += t
        return intents

    def process(self, user_input, context):
        try:
            facts = self.engine.create_factsheet_from_json(context) if context else self.engine.create_factsheet()

            # reset 'bot name' fact
            facts.retract_facts('bot_name')
            facts.assert_simple_fact('bot_name', self.name)

            # reset 'user input' fact
            facts.retract_facts('text')
            facts.assert_simple_fact('text', user_input)

            conclusions = self.engine.create_factsheet()
            self.engine.run(facts, conclusions)
            for name, weight, subfacts in self.get_intents(conclusions):
                action = getattr(self.actions, name, None)
                if action is not None:
                    answer = action(weight, subfacts, conclusions, facts)
                    if answer:
                        facts.retract_facts('prior_intent')
                        facts.assert_simple_fact('prior_intent', name)
                        return (answer, facts.to_json())
        except:
            raise

        return (Answer(message='ouch...'), context)

chatbot = Chatbot('Bot')

print('Bot: Hello!\n')
user_input = ''
context = ''
while True:
    user_input = input('You: ')
    answer, context = chatbot.process(user_input, context)
    print('Bot: %s\n' % answer.message)
    if answer.stop:
        exit(0)
