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

% Car facts: car(Name, Brand, Body, Engine, Fuel, Seating, Price)
car('Suzuki Mehran', suzuki, hatchback, '800cc', gasoline, 4, budget).
car('Suzuki Alto', suzuki, hatchback, '660cc', gasoline, 4, budget).
car('Suzuki Cultus', suzuki, hatchback, '1.0L', gasoline, 4, budget).
car('Suzuki Wagon R', suzuki, hatchback, '1.0L', gasoline, 4, budget).
car('Suzuki Bolan', suzuki, minivan, '800cc', gasoline, 7, budget).
car('Suzuki Swift', suzuki, hatchback, '1.2L', gasoline, 4, medium).
car('Toyota Corolla', toyota, sedan, '1.3L', gasoline, 5, medium).
car('Toyota Yaris', toyota, sedan, '1.3L', gasoline, 5, medium).
car('Toyota Fortuner', toyota, suv, '2.7L', gasoline, 7, premium).
car('Toyota Hilux', toyota, pickup, '2.8L', diesel, 5, premium).
car('Honda Civic', honda, sedan, '1.5L', gasoline, 5, premium).
car('Honda City', honda, sedan, '1.2L', gasoline, 5, medium).
car('Honda BR-V', honda, mpv, '1.5L', gasoline, 7, medium).
car('Hyundai Tucson', hyundai, suv, '2.0L', gasoline, 5, premium).
car('Hyundai Elantra', hyundai, sedan, '1.6L', gasoline, 5, premium).
car('Hyundai Sonata', hyundai, sedan, '2.0L', gasoline, 5, premium).
car('KIA Sportage', kia, suv, '2.0L', gasoline, 5, premium).
car('KIA Picanto', kia, hatchback, '1.0L', gasoline, 4, budget).
car('KIA Stonic', kia, crossover, '1.4L', hybrid, 5, medium).
car('Changan Alsvin', changan, sedan, '1.5L', gasoline, 5, budget).
car('Changan Oshan X7', changan, suv, '1.5L', turbo, 7, premium).
car('Changan Karvaan', changan, mpv, '1.0L', gasoline, 7, budget).
car('MG HS', mg, crossover, '1.5L', turbo, 5, premium).
car('MG ZS EV', mg, crossover, electric, electric, 5, premium).
car('Haval H6', haval, suv, '1.5L', turbo, 5, premium).
car('Haval Jolion', haval, suv, '1.5L', turbo, 5, premium).
car('BAIC BJ40 Plus', baic, suv, '2.0L', turbo, 5, premium).
car('Proton Saga', proton, sedan, '1.3L', gasoline, 5, budget).
car('Proton X70', proton, suv, '1.5L', turbo, 5, premium).
car('NUR E 75', nur, sedan, electric, electric, 5, medium).
car('Adam Revo', adam, hatchback, '800cc', gasoline, 4, budget).
car('DFSK Glory 580', dfsk, suv, '1.5L', gasoline, 7, medium).
car('Isuzu D-Max', isuzu, pickup, '3.0L', diesel, 5, premium).
car('Peugeot 2008', peugeot, crossover, '1.2L', turbo, 5, premium).
car('Chery Tiggo 4 Pro', chery, suv, '1.5L', turbo, 5, medium).
car('Chery Tiggo 8 Pro', chery, suv, '1.6L', turbo, 7, premium).

% Dynamic predicate for user selections
:- dynamic selected/2.

% A car matches if all selected features match (or are not selected)
matches(Name) :-
    car(Name, Brand, Body, Engine, Fuel, Seating, Price),
    (selected(brand, Brand); \+ selected(brand, _)),
    (selected(body, Body); \+ selected(body, _)),
    (selected(engine, Engine); \+ selected(engine, _)),
    (selected(fuel, Fuel); \+ selected(fuel, _)),
    (selected(seating, Seating); \+ selected(seating, _)),
    (selected(price, Price); \+ selected(price, _)). 