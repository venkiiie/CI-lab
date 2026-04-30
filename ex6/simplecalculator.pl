% ============================================================
% Prolog Program: Combination of Simple Arithmetic & Set Theory
% 8 Operations: 4 Arithmetic + 4 Set Theory
% ============================================================

% -----------------------------------------------------------
% ARITHMETIC OPERATIONS (1–4)
% -----------------------------------------------------------

% 1. Addition
add(X, Y, Result) :-
    number(X),
    number(Y),
    Result is X + Y.

% 2. Subtraction
subract(X, Y, Result) :-
    number(X),
    number(Y),
    Result is X - Y.

% 3. Multiplication
multiply(X, Y, Result) :-
    number(X),
    number(Y),
    Result is X * Y.

% 4. Integer Division (with zero-check)
divide(_, 0, _) :-
    write('Error: Division by zero'), nl, fail.
divide(X, Y, Result) :-
    number(X),
    number(Y),
    Y =\= 0,
    Result is X / Y.

% -----------------------------------------------------------
% SET THEORY OPERATIONS (5–8)
% -----------------------------------------------------------

% 5. Union of two sets (A ∪ B)
%    Combines both sets, removing duplicates.
set_union([], B, B).
set_union([H|T], B, Union) :-
    member(H, B), !,
    set_union(T, B, Union).
set_union([H|T], B, [H|Union]) :-
    set_union(T, B, Union).

% 6. Intersection of two sets (A ∩ B)
%    Elements common to both sets.
set_intersection([], _, []).
set_intersection([H|T], B, [H|Intersection]) :-
    member(H, B), !,
    set_intersection(T, B, Intersection).
set_intersection([_|T], B, Intersection) :-
    set_intersection(T, B, Intersection).

% 7. Difference of two sets (A \ B)
%    Elements in A but not in B.
set_difference([], _, []).
set_difference([H|T], B, Difference) :-
    member(H, B), !,
    set_difference(T, B, Difference).
set_difference([H|T], B, [H|Difference]) :-
    set_difference(T, B, Difference).

% 8. Subset check (A ⊆ B)
%    True if every element of A is in B.
set_subset([], _).
set_subset([H|T], B) :-
    member(H, B),
    set_subset(T, B).

% -----------------------------------------------------------
% COMBINED OPERATIONS (Arithmetic on Set Results)
% -----------------------------------------------------------

% Sum all elements of a set
set_sum([], 0).
set_sum([H|T], Sum) :-
    number(H),
    set_sum(T, RestSum),
    Sum is H + RestSum.

% Compute the size (cardinality) of a set
set_size([], 0).
set_size([_|T], Size) :-
    set_size(T, RestSize),
    Size is RestSize + 1.

% -----------------------------------------------------------
% DEMO / TEST PREDICATES
% -----------------------------------------------------------

demo_arithmetic :-
    nl, write('=== ARITHMETIC OPERATIONS ==='), nl,

    add(10, 5, R1),
    format('1. Addition:       10 + 5  = ~w~n', [R1]),

    subtract(10, 5, R2),
    format('2. Subtraction:    10 - 5  = ~w~n', [R2]),

    multiply(10, 5, R3),
    format('3. Multiplication: 10 * 5  = ~w~n', [R3]),

    divide(10, 5, R4),
    format('4. Division:       10 / 5  = ~w~n', [R4]).

demo_set_theory :-
    nl, write('=== SET THEORY OPERATIONS ==='), nl,

    A = [1, 2, 3, 4, 5],
    B = [3, 4, 5, 6, 7],
    format('Set A = ~w~n', [A]),
    format('Set B = ~w~n', [B]), nl,

    set_union(A, B, Union),
    format('5. Union (A ∪ B):        ~w~n', [Union]),

    set_intersection(A, B, Inter),
    format('6. Intersection (A ∩ B): ~w~n', [Inter]),

    set_difference(A, B, Diff),
    format('7. Difference (A \\ B):   ~w~n', [Diff]),

    ( set_subset([3, 4], A)
    -> format('8. Subset: [3,4] ⊆ A?   true~n')
    ;  format('8. Subset: [3,4] ⊆ A?   false~n')
    ).

demo_combined :-
    nl, write('=== COMBINED OPERATIONS ==='), nl,

    A = [1, 2, 3, 4, 5],
    B = [3, 4, 5, 6, 7],

    set_intersection(A, B, Inter),
    set_sum(Inter, SumInter),
    format('Sum of intersection elements:  ~w~n', [SumInter]),

    set_union(A, B, Union),
    set_size(Union, SizeUnion),
    format('Cardinality of union:          ~w~n', [SizeUnion]),

    set_difference(A, B, Diff),
    set_sum(Diff, SumDiff),
    set_size(Diff, SizeDiff),
    divide(SumDiff, SizeDiff, AvgDiff),
    format('Average of difference elements: ~w~n', [AvgDiff]).

% Master demo runner
run :-
    demo_arithmetic,
    demo_set_theory,
    demo_combined,
    nl, write('=== ALL DEMOS COMPLETE ==='), nl.
