import textwrap

TESTED_FUNCTION = textwrap.dedent("""\
    def iterate_over_the_string(s: str) -> None:
        for i in s:
            print(i)
    """)

FUNCTION_CALL = textwrap.dedent("""\
    iterate_over_the_string('Sasha')
    """)
