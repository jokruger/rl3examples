#include <iostream>

#include <rl3.hpp>

int main(void)
{
    // create engine
    rl3::RL3Engine engine;

    // parse and compile (link) simple annotation pattern
    auto definition = engine.make_simple_annotation_def("text", "(?i:{dawg continent})", "continent");
    engine.parse(definition);
    engine.link();

    // create factsheet
    auto fs = engine.create_factsheet();

    // assert input text
    fs->assert_fact("text", "Antarctica is Earth's southernmost continent... Europe is the sixth largest continent in size.");

    // run engine - it should now annotate a continent names mentioned in our text
    engine.run(fs);

    // iterate and print all "continent" annotations
    auto i = fs->get_fact_iterator("continent");
    while (!i->is_end())
    {
        std::cout << i->get_value_str() << std::endl;
        i->next();
    }

    return 0;
}
