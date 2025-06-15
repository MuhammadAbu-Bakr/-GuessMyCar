% Facts and rules about cars
car(tesla_model_s) :- electric, sedan.
car(toyota_prius) :- hybrid, sedan.
car(ford_f150) :- truck, gasoline.
car(bmw_x5) :- suv, gasoline.
car(nissan_leaf) :- electric, hatchback.

% Features
electric :- ask(electric).
hybrid :- ask(hybrid).
gasoline :- ask(gasoline).
sedan :- ask(sedan).
truck :- ask(truck).
suv :- ask(suv).
hatchback :- ask(hatchback).

% Dynamic predicate to store answers
:- dynamic yes/1, no/1.

ask(X) :-
    (yes(X) -> true ;
     no(X) -> fail ;
     ask_user(X)).

ask_user(X) :-
    format('Is the car ~w? (yes/no) ', [X]),
    read(Answer),
    ( (Answer == yes ; Answer == y)
      -> assertz(yes(X)) ;
         assertz(no(X)), fail). 