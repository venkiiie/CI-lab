% Prevent warnings if facts are scattered
:- discontiguous male/1.
:- discontiguous female/1.
:- discontiguous parent/2.

% --- GENDER FACTS ---
male(karamchand_gandhi).
male(laxmidas_gandhi).
male(karsandas_gandhi).
male(mahatma_gandhi).
male(harilal_gandhi).
male(manilal_gandhi).
male(ramdas_gandhi).
male(devdas_gandhi).

female(putlibai).
female(raliatbehn).
female(kasturba_gandhi).

% --- PARENT FACTS ---
% Karamchand & Putlibai children
parent(karamchand_gandhi, laxmidas_gandhi).
parent(putlibai, laxmidas_gandhi).

parent(karamchand_gandhi, karsandas_gandhi).
parent(putlibai, karsandas_gandhi).

parent(karamchand_gandhi, mahatma_gandhi).
parent(putlibai, mahatma_gandhi).

parent(karamchand_gandhi, raliatbehn).
parent(putlibai, raliatbehn).

% Mahatma & Kasturba children
parent(mahatma_gandhi, harilal_gandhi).
parent(kasturba_gandhi, harilal_gandhi).

parent(mahatma_gandhi, manilal_gandhi).
parent(kasturba_gandhi, manilal_gandhi).

parent(mahatma_gandhi, ramdas_gandhi).
parent(kasturba_gandhi, ramdas_gandhi).

parent(mahatma_gandhi, devdas_gandhi).
parent(kasturba_gandhi, devdas_gandhi).

% --- RULES ---
father(F, C) :- male(F), parent(F, C).
mother(M, C) :- female(M), parent(M, C).

% Full siblings share both the same father and the same mother
sibling(A, B) :-
    father(F, A), father(F, B),
    mother(M, A), mother(M, B),
    A \= B.

brother(Bro, Sib) :- male(Bro), sibling(Bro, Sib).
sister(Sis, Sib)  :- female(Sis), sibling(Sis, Sib).

grandparent(GP, GC) :- parent(GP, P), parent(P, GC).
grandfather(GF, GC) :- male(GF), grandparent(GF, GC).
grandmother(GM, GC) :- female(GM), grandparent(GM, GC).

% Recursive ancestor rule
ancestor(Anc, Desc) :- parent(Anc, Desc).
ancestor(Anc, Desc) :- parent(Anc, X), ancestor(X, Desc).
