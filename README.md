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
the solver will iterate, and `-p` specifies which relations will
be included when showing models.

For instance, if you write a logic program for graph coloring in a file named
`graphs.tl`, and you only want to see the 'edge' and 'color' relation, and want
to list 200 models, you can call the program with

`python pipeline.py graphs.tl -n 200 -p edge color`

Output includes negations of predicates, equality and inequality,
and so on, so full models include lots of unnecesary information.

## Language

The language is similar to ASP languages. You can write horn rules
that are implicitly universally quantified, but you can also use
atomic negation freely without worrying about whether the program
will behave the way you'd expect.

Disjunction is also available, but not together with implication.

A program looks something like this:

```
a, b, c, d : A.
var x, y : A.

p (x, x).
p (a, b).
p (x, y), p (y, x), y != x -> False.
r (x, y) -> not p (y, x).
```

You can populate a sort with a given number of constants by using

```
fill prefix n : Sort.
```

That simply means `Sort` will have `prefix1`, `prefix2`, `prefix3`, ..., `prefixn`
as members.

You can create an ordered sort using

```
order ord n : Sort.
```

That means the same as before, but also that `ord1.next` refers to `ord2`, `ord2.next` to
`ord3`, and `ord[k]` to `ord[k+1]`, when `k` is less than `n`.

If you want to make sure a given relation is a function without explicitly
writing all the rules, you can use

```
let f : A -> B.
```

This is nicer and a bit faster (embedding-wise) than writing something
like `f (a, b), f (a, c), b != c -> False`, and ensures functions are
total, which is more roundabout to write otherwise.

## Examples

The `models` directory contains some examples.
