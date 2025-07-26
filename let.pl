% --- Dynamic predicates for properties ---
:- dynamic property/5.
% property(ID, Location, Type, Rent, Available)

% --- Sample properties ---
property(1, 'Lahore', 'Apartment', 25000, yes).
property(2, 'Karachi', 'House', 40000, yes).
property(3, 'Islamabad', 'Flat', 30000, yes).

% --- Menu ---
menu :-
    nl, write('--- Property Rental System ---'), nl,
    write('1. View All Properties'), nl,
    write('2. Search by Location'), nl,
    write('3. Search by Rent Range'), nl,
    write('4. Add New Property'), nl,
    write('5. Book a Property'), nl,
    write('6. Exit'), nl,
    write('Enter your choice: '), read(Choice),
    handle_choice(Choice).

% --- Handle Menu Options ---
handle_choice(1) :- view_properties, menu.
handle_choice(2) :- search_location, menu.
handle_choice(3) :- search_rent, menu.
handle_choice(4) :- add_property, menu.
handle_choice(5) :- book_property, menu.
handle_choice(6) :- write('Exiting...'), nl.
handle_choice(_) :- write('Invalid choice!'), nl, menu.

% --- View All Properties ---
view_properties :-
    nl, write('--- Available Properties ---'), nl,
    property(ID, Location, Type, Rent, yes),
    format('ID: ~w, Location: ~w, Type: ~w, Rent: ~w~n', [ID, Location, Type, Rent]),
    fail.
view_properties.

% --- Search by Location ---
search_location :-
    write('Enter location to search: '), read(Loc),
    property(ID, Loc, Type, Rent, yes),
    format('ID: ~w, Location: ~w, Type: ~w, Rent: ~w~n', [ID, Loc, Type, Rent]),
    fail.
search_location.

% --- Search by Rent Range ---
search_rent :-
    write('Enter minimum rent: '), read(Min),
    write('Enter maximum rent: '), read(Max),
    property(ID, Loc, Type, Rent, yes),
    Rent >= Min, Rent =< Max,
    format('ID: ~w, Location: ~w, Type: ~w, Rent: ~w~n', [ID, Loc, Type, Rent]),
    fail.
search_rent.

% --- Add New Property ---
add_property :-
    write('Enter ID: '), read(ID),
    write('Enter Location: '), read(Location),
    write('Enter Type: '), read(Type),
    write('Enter Rent: '), read(Rent),
    assertz(property(ID, Location, Type, Rent, yes)),
    write('Property added successfully!'), nl.

% --- Book Property ---
book_property :-
    write('Enter property ID to book: '), read(ID),
    retract(property(ID, Location, Type, Rent, yes)),
    assertz(property(ID, Location, Type, Rent, no)),
    write('Property booked successfully!'), nl, !.
book_property :-
    write('Property not found or already booked.'), nl.

% --- Start the program ---
start :- menu.