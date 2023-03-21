### EMBEDDINGS

- When you declare a function f with let, but then add some other
  rule (like p x y -> f x y), f ceases to behave like a function.
  It might be an issue with Either.clausify, a problem with the
  embedding, a more general problem with how negation is being
  handled, or something else entirely, so we'll have to be patient.

- Total orders with 'next' leave lots of 'hanging' facts about the
  out-of-bounds constant next of the last element.

### GRID

- I got stuck with the visualization / verification part.

- The approach taken with objects.py (first write procedural
  tests checking if a certain Python object has a property,
  then write a function that turns a relational specification
  into that Python object, and check it using a testing framework,
  which allows very fast, repeatable and hassle-free iteration)
  worked, so we should try that again (maybe using some of the
  same functions for trees).

- This might have been superseded by 'functions plus levels'.
  Obviousy checking specifications with procedural tests is
  still a useful approach. p(x) <=> f(g(x)) = True, etc-

### FUNCTIONS

- I got stuck with the debugging part (is the logic program
  wrong, is there a bug in the program, or is there a bug
  in some assumption there? - some issue with negation, or
  an incomplete translation)

- So far these are working in lots of contexts

- Equality and 'actual functions' can be implemented using
  these. You can have a function assign : A' -> A, and since
  each a' is assigned exactly one a, that can be used as some
  form of equality (together with p(a'), assign(a', a) <-> p (a))

  The arity of predicates and rules can be reduced using that
  kind of workaround, which reduces the size of embeddings, since
  assign (a.f, b) lets you assert stuff about b without explicit
  references to anything other than a (unfolding iterates only
  over a's sort, as in 'p(a), q(a.f), r(a.g), s(a.f, a.g) -> t(a, a.g)',
  which will be especially useful when using DRTs and working
  with local properties of nodes that involve lots of arguments.

### SYMMETRY BREAKING

- using totally ordered sorts works as long as there are no
  'loose' predicates that can be true or false for the same
  model, when you only consider 'structurally relevant' predicates.
  In the example of trees, many models did not differ in who
  was left of whom, but did differ in some of the 'auxiliary' predicates,
  so their trees were isomorphic, but showed up more than once while
  enumerating models.


### INTERFACE / COUPLING / MODULARITY

The current interface does not let you use pysat's 'solve with'
(you cannot say 'hey, give me a model using the current state, but
temporarily add the literals in L to it. Give me just one model, then
forget'). Also, I don't think pysat lets you iterate over more than
one model that way.

### SOLVING

- Solve an instance with respect to a background theory (you unfold
  all general facts once, and add instance facts with `solve_with`)

### MODELING

- The relational specification for tiling / 2D string parsing is
  still very sketchy. Using a leveled DAG looks promising, as well
  as 'storing semantic data' (same as DRT, but a bit simpler), but
  I'm not sure how to properly represent spatial information.
  
  A possible workaround is to 'hardcode' spatial hierarchy data
  ('A large area is a rectangle with NM tiles. Large areas may
  contain small and mid areas, and all areas within a large
  area must be mutually accessible', and so on). Since only valid
  tilings should be produced, and no valid large area should have
  just one small child, this could be made to work, although it is
  very ad-hoc.
  
  Using corners seems like a more general alternative ('all children
  of an area must be within the bounds of its corners'), and probably
  could be generalized to convex shapes very easily. Corner data could
  be 'stored' in a vertex's DRS, and reasoning about total orders is
  easy with what we already have (and we want to model arithmetic anyway,
  so that should be ready at some point).

### NEGATIVE FEEDBACK

- I tried modeling some problems with stable marriages.
  
  The end goal was to be able to come up with preference configurations
  that never end in a stable configuration.

  With preferences yielding periodic changes, and never having anyone
  stay with the same person during even one turn, this seems possible:
  you make sure b.next is like a cyclic linked list, and state
  `with (g, b), with (g.next, b.next) -> False`.

  But more complex situations seem hard to model.

  One option is to be able to tell when any couple has changed (parts
  can remain stable, but some couple has to split).

  This can be done used one of the 'cheap, awkward tricks' we used
  with artale (the 'any' macro, or something a bit more general, like
  using a list, A+, A-, etc).

  But it has the same 'blind spot' quantifier nesting issue program
  synthesis has (You cannot synthezise a program aiming for the 
  instance to be satisfiable and at the same time say 'the instance
  is unsatisfiable is there is one input that...', because you either
  get a satisfying assignment or you don't, and with no satisfying
  assignment, there is no program).

  Ultimately, this is not relevant, but shows many of the limitations
  of the approach.

  ```
  prefer (g, b),
  with (g, b'),
  b != b',
  available (b', g),
  with (g.next, b.next) -> False.
  ```

### ARITHMETIC

- Addition is straightforward to model with carries and 'bitwise logic',
  but other operations are not that straightforward, so it is best to
  take the 'truth table -> conjunctive normal form -> minimized function'
  approach. Even if the resulting function requires nesting, it can be
  hardcoded with predicates directly (no need for any generality there),
  like with context free grammar parsing when the grammar is fixed.

- Other alternatives seem far worse.

  With multiplication and addition for natural numbers and rationals 
  and their operations defined on pairs of naturals, maybe we could
  handle small numbers

  ```
  * a / b + c / d = (a' + b') / [bd], where
        [bd] = lcm(b, d),
        a' = a * [bd] / b,
        b' = b * [bd] / d

  * (a / b) * (c / d) = ((a * [bd] / b) * (c * [bd] / d)) / [bd]
  ```

  But factorization is not straightforward, so the best thing
  is to implement division and substraction as separate operations.

### OPTIMIZATION

- Define a feasible region
- Define criteria for sufficiency
- Define criteria for order

- Test cases (proof of concept / sanity check)
	- string length and some string property
	- lexicographic order and some string property
	  (shortest string that is part of a regular
           language, and so on)
        - Shortest arithmetic expression evaluating to n,
          using just one as 'leaf value'
          (this one is fun)

- Test cases (toy):
	Referring expressions
	Propositional proofs

- Test cases (serious):
	Synthesis of mapreduce programs

### SEMANTICS FOR FUNCTIONS

(A more detailed note on a comment above, under *MODELING*)

`B.f : A`
    * Create a sort `A'` with `|A|` fresh constants
    * Declare a function assign from `A'` to `A`
    * State P(a'), assign (a', a) <-> P(a)
    * State that
        ```
        R(a', b), assign (a', a) -> R (a, b)
        R(a, b), assign (a', a) -> R (a', b) 
        R(a, b'), assign (b', b) -> R (a, b) 
        R(a, b), assign (b', b) -> R (a, b')
        ```
        (for n-ary relations this is the same. 
        Since you do it for a variable at a time,
        it should be linear)
        
    That way you can have functions without needing
    to specify both variables, and that may reduce
    the size of embeddings a lot.
    
    Is this enough? Check it when you have the time

### PARSING AND EVALUATION

- Ta dah! The parser evaluates and parses -((5 + 4) + 1)
  and (-(5 + 4)) + 1

- However, we're missing some comfort features, and at
  least two absolutely essential ones:

#### ESSENTIAL

  * Rule precedence

  * Error messages

#### COMFORT

  * EBNF goodies, like A -> B* or A -> <B, but n times>

  * Defining semantics directly in the grammar, instead of
    using rule names and providing a separate action map.
    Something like a [+] b := lambda x, y : x + y
    (named arguments and 'where' clauses seems like a lot).

  * Token sets and disjunction.

    Currently you have to write `A -> a1, A -> a2, ..., A -> an`,
    instead of the infinitely more reasonable `A -> a1 | a2 | a3 | ... | an`.

    It would be nice to have some predefined productions, like
    for ascii, digits, alpha, and so on.
    `A -> {a b c d e f g h}` could be used instead of `|`,
    but deciding on sound syntax and semantics is a delicate task.
    
    For instance, unrestricted composition licenses
    stuff like `A -> {B C D E} A {G D A} | A A`.
    Do we want that?

    In this case 'unfolding' to vanilla rules is simple, 
    ```
    A -> A A
    A -> B C G
    A -> B C D
    A -> B C A
    A -> C A G
        ...
    A -> S_i A T_j
    ```
    (and so on, as per our very well known and universally
    loved cartesian product...), but nesting can make things blow up.

  * Whitespace handling

  * Allowing the use of preprocessors / tokenizers

- We should include a check for sources of undefined behavior,
  so as to directly disallow them, and good error messages.

  Cycles in the graph of unary productions can be easily
  detected, and are the one kind of productions that make
  it possible to write semantics with nonterminating evaluation,
  but I'm not sure what's a sound criterion for allowing and
  disallowing cycles when binary productions are involved.
   
  They might not be necessary, since every application of
  a binary rule 'consumes' at least one node.

  ```
  A -> B
  B -> A
  ```
- If you feel like wasting your entire life on this, maybe
  prove some relation between LL(k) grammars and the worst
  case complexity of parsing.
 
  The worst worst you get is cubic (the parser is CYK, but
  instead of blindly cycling through i, j, k, it adds new
  nodes to a queue, and checks their neighbors for feasible
  rule applications. So amortized complexity is lower or
  equal than that of plain CYK, but we don't know how much).

###  PRECEDENCE

  * When is precedence necessary?

  `a + bc` is either `(a + b)c` or `a + (bc)`, the intended reading.

  So it is necessary to override a reading when it overlaps with
  a reading of higher priority -
  
  ```
  a + b c
  _____ 
      ___
  ```

  so we may get rid of all spans for the same.
  Is that criterion enough? I never know ´_`

  In any case, when you finish a parse, you can prune it,
  and remove all branches having such overlap, and all
  nodes depending on them.

  That should be easy to do, provided spans[i, j] is annotated
  with its priority level

  That is...

  ```python
  for index, token in tokens:
      for label in labels:
          conflicts = sorted(overlap(spans, index, label), key=getPrecedence)
          # cut and leave the prefix up to the second highest precedence value
          stay, leave = ?(conflicts)
          remove |= leave
  
  for key in spans.pairs():
      if remove & set(spans[key]):
          remove.add(spans[key])

  spans = spans - remove # so to speak
  ```

  ```python
  def overlap(i, j, k, l):
      end = max(j, l)
      if end == j:
          return i <= l
      if end == l:
          return k <= j
  ```   

  since every span data item should have a priority, it could
  now be the first component.

### PARAMETRIC CONTEXT-FREE GRAMMARS

* `A (n - 1) -> A (n) B (n)`

- Parsing is easy (you check if the parameters in a pair
  of neighboring spans are such that they match some rule,
  and set head parameters using some f)

- This allows you to handle indentation and similar
  properties without having to change things much.

- Presentation will be a bit non-declarative, but oh well,
  'users are not morons'

### MODELING IDIOMS

Abstract predicates (similar to alloy's abstract sigs)

- Suppose you want to say in the next state p(a), but p
  must be one of p1, p2 and p3, not just p.
  This is `p <-> p1 v p2 v p3` and umhh, `-p1, -p2, -p3 -> -p`,
  but what is `p <-> p1 v p2 v p3` in horn clauses?
  
  ```
  p, -p1, -p2 -> p3
  p, -p2, -p3 -> p1
  p, -p1, -p3 -> p2
  ```

  This could be made into something you can unfold

  Humhh, soo
  what is `p1 v p2 v p3 <-> q1 v q2 v q3`?

  ```
  -p1, -p2, -p3 -> -q1, -q2, -q3
  -q1, -q2, -q3 -> -p1, -p2, -p3
  
  -p1, -p2, qi -> p3 (e t c . . . )

    /\         /\
   /  \       /  \   -pi /\ qj -> pk
  j: 1..|q|  i != k
  ```

  Is there something missing?

## TODOS

* Check equality of `a.f` with assign
* DAGS
* Arithmetic (parse the arithmetic file with the new parser)
* Natural deduction
* PDL planning
* PDL planning with resources
* Symmetry breaking with leftOf defined like before (i.e. as a relation using induction on i.next)
* Compositional types
* 'Bare' composition with arbitrary predicates as restrictions on arguments
  (instead of types), without composition
* Log number of clauses and literals added to solver
  instance, without necessarily storing them
* Write down 'old' model of semantic composition
  (DRT with inheritance), check against AMR (Copestake)
* Survey cases where it fails (like 'the fake fake
  muffler and the actual fake muffler'), and see if that
  can be modeled with functions  (with identity being the
  most common case)

## Done

* Parsing and evaluation without precedence.
* Parsing and evaluation with precedence.
* Try ordering vertices with level : vertex -> index (it seems to work).
* Test quadratic tree embedding (in test_trees.py)
* Check parsing and evaluation with precedence
* Obtain strings from a fixed grammar
* Log using flags instead of verbosity
* Use ArgumentList instead of sequence
