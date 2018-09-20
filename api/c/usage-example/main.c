#include <stdio.h>
#include <stdlib.h>

#include <rl3.h>

/* check for engine execution errors */
void check_for_errors(struct RL3_Engine* engine)
{
    if (rl3_engine_has_error(engine) != 0)
    {
        printf("Failed with error: %s\n", rl3_engine_get_error_str(engine));
        exit(-1);
    }
}

int main(void)
{
    /* create engine and init it as "rl3" engine */
    struct RL3_Engine* engine = rl3_engine_create(); check_for_errors(engine);
    rl3_engine_init(engine, "rl3"); check_for_errors(engine);

    /* parse and compile (link) simple annotation pattern */
    const char* definition = rl3_make_simple_annotation_def(engine, "text", "(?i:{dawg continent})", "continent"); check_for_errors(engine);
    rl3_engine_parse_inline(engine, definition, ".", 1); check_for_errors(engine);
    rl3_engine_link(engine, 1); check_for_errors(engine);

    /* create factsheet */
    struct RL3_Factsheet* fs = rl3_factsheet_create(engine); check_for_errors(engine);

    /* assert input text */
    rl3_factsheet_assert_simple_fact(engine, fs, "text", "Antarctica is Earth's southernmost continent... Europe is the sixth largest continent in size.", 1.0);
    check_for_errors(engine);

    /* run engine - it should now annotate a continent names mentioned in our text */
    rl3_engine_update(engine, fs); check_for_errors(engine);

    /* iterate and print all "continent" annotations */
    struct RL3_FactIterator* i = rl3_factsheet_get_fact_iterator(engine, fs, "continent"); check_for_errors(engine);
    while (!rl3_factiterator_is_end(engine, i))
    {
        printf("%s\n", rl3_factiterator_get_value(engine, i)); check_for_errors(engine);
        rl3_factiterator_next(engine, i); check_for_errors(engine);
    }
    /* release iterator */
    rl3_factiterator_destroy(engine, i); check_for_errors(engine);

    /* release engine */
    rl3_engine_destroy(engine);

    return 0;
}
