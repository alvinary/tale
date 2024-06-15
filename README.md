This program looks for first-order models of logic programs, similar to
an answer-set programming language.

The module depends on python-sat (for solving SAT instances) and
tatsu (for parsing), so these should be installed before running
`pipeline.py`. 

## Basic Use

```
python pipeline.py some_program_file -n 5 -p my_predicate
```

Here `some_program_file` should be a text file containing a program,
the `-n` parameter specifies the maximum number of models through which
the solver will iterate, and `-p` restricts the predicates that will
be shown (suppose you make a program for graph coloring, and you only
want to see the 'edge' and 'color' relation and not all the rest. Then
you'd run the program with `-p edge color`).

## Examples

The `models` directory contains some examples.

## Syntax

Programs consist of declarations and rules.

```
order a 300 : A.
var x, y : A.

p(x, y), q (x, y) -> r(y, x).
r (x, y), s (y, x) -> False.

```
