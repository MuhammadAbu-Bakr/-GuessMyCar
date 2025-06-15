from pyswip import Prolog
import os

def init_prolog():
    """Initialize Prolog and load the knowledge base."""
    prolog = Prolog()
    
    # Set dynamic predicates using assertz
    prolog.assertz("dynamic(yes/1)")
    prolog.assertz("dynamic(no/1)")
    
    # Define the rules directly
    rules = [
        "car(tesla_model_s) :- electric, sedan",
        "car(toyota_prius) :- hybrid, sedan",
        "car(ford_f150) :- truck, gasoline",
        "car(bmw_x5) :- suv, gasoline",
        "car(nissan_leaf) :- electric, hatchback",
        "electric :- ask(electric)",
        "hybrid :- ask(hybrid)",
        "gasoline :- ask(gasoline)",
        "sedan :- ask(sedan)",
        "truck :- ask(truck)",
        "suv :- ask(suv)",
        "hatchback :- ask(hatchback)",
        "ask(X) :- (yes(X) -> true ; no(X) -> fail ; ask_user(X))",
        "ask_user(X) :- fail"  # Placeholder: disables user input in Prolog
    ]
    
    # Assert each rule
    for rule in rules:
        prolog.assertz(rule)
    
    return prolog

def query_cars(prolog):
    """Query all possible cars from the knowledge base."""
    return list(prolog.query("car(X)"))

# Car data for MCQ-based guessing game
CARS = [
    {"name": "Suzuki Mehran", "brand": "Suzuki", "body": "Hatchback", "engine": "800cc", "fuel": "Gasoline", "seating": 4, "price": "Budget"},
    {"name": "Suzuki Alto", "brand": "Suzuki", "body": "Hatchback", "engine": "660cc", "fuel": "Gasoline", "seating": 4, "price": "Budget"},
    {"name": "Suzuki Cultus", "brand": "Suzuki", "body": "Hatchback", "engine": "1.0L", "fuel": "Gasoline", "seating": 4, "price": "Budget"},
    {"name": "Suzuki Wagon R", "brand": "Suzuki", "body": "Hatchback", "engine": "1.0L", "fuel": "Gasoline", "seating": 4, "price": "Budget"},
    {"name": "Suzuki Bolan", "brand": "Suzuki", "body": "Minivan", "engine": "800cc", "fuel": "Gasoline", "seating": 7, "price": "Budget"},
    {"name": "Suzuki Swift", "brand": "Suzuki", "body": "Hatchback", "engine": "1.2L", "fuel": "Gasoline", "seating": 4, "price": "Medium"},
    {"name": "Toyota Corolla", "brand": "Toyota", "body": "Sedan", "engine": "1.3L", "fuel": "Gasoline", "seating": 5, "price": "Medium"},
    {"name": "Toyota Yaris", "brand": "Toyota", "body": "Sedan", "engine": "1.3L", "fuel": "Gasoline", "seating": 5, "price": "Medium"},
    {"name": "Toyota Fortuner", "brand": "Toyota", "body": "SUV", "engine": "2.7L", "fuel": "Gasoline", "seating": 7, "price": "Premium"},
    {"name": "Toyota Hilux", "brand": "Toyota", "body": "Pickup", "engine": "2.8L", "fuel": "Diesel", "seating": 5, "price": "Premium"},
    {"name": "Honda Civic", "brand": "Honda", "body": "Sedan", "engine": "1.5L", "fuel": "Gasoline", "seating": 5, "price": "Premium"},
    {"name": "Honda City", "brand": "Honda", "body": "Sedan", "engine": "1.2L", "fuel": "Gasoline", "seating": 5, "price": "Medium"},
    {"name": "Honda BR-V", "brand": "Honda", "body": "MPV", "engine": "1.5L", "fuel": "Gasoline", "seating": 7, "price": "Medium"},
    {"name": "Hyundai Tucson", "brand": "Hyundai", "body": "SUV", "engine": "2.0L", "fuel": "Gasoline", "seating": 5, "price": "Premium"},
    {"name": "Hyundai Elantra", "brand": "Hyundai", "body": "Sedan", "engine": "1.6L", "fuel": "Gasoline", "seating": 5, "price": "Premium"},
    {"name": "Hyundai Sonata", "brand": "Hyundai", "body": "Sedan", "engine": "2.0L", "fuel": "Gasoline", "seating": 5, "price": "Premium"},
    {"name": "KIA Sportage", "brand": "KIA", "body": "SUV", "engine": "2.0L", "fuel": "Gasoline", "seating": 5, "price": "Premium"},
    {"name": "KIA Picanto", "brand": "KIA", "body": "Hatchback", "engine": "1.0L", "fuel": "Gasoline", "seating": 4, "price": "Budget"},
    {"name": "KIA Stonic", "brand": "KIA", "body": "Crossover", "engine": "1.4L", "fuel": "Hybrid", "seating": 5, "price": "Medium"},
    {"name": "Changan Alsvin", "brand": "Changan", "body": "Sedan", "engine": "1.5L", "fuel": "Gasoline", "seating": 5, "price": "Budget"},
    {"name": "Changan Oshan X7", "brand": "Changan", "body": "SUV", "engine": "1.5L", "fuel": "Turbo", "seating": 7, "price": "Premium"},
    {"name": "Changan Karvaan", "brand": "Changan", "body": "MPV", "engine": "1.0L", "fuel": "Gasoline", "seating": 7, "price": "Budget"},
    {"name": "MG HS", "brand": "MG", "body": "Crossover", "engine": "1.5L", "fuel": "Turbo", "seating": 5, "price": "Premium"},
    {"name": "MG ZS EV", "brand": "MG", "body": "Crossover", "engine": "Electric", "fuel": "Electric", "seating": 5, "price": "Premium"},
    {"name": "Haval H6", "brand": "Haval", "body": "SUV", "engine": "1.5L", "fuel": "Turbo", "seating": 5, "price": "Premium"},
    {"name": "Haval Jolion", "brand": "Haval", "body": "SUV", "engine": "1.5L", "fuel": "Turbo", "seating": 5, "price": "Premium"},
    {"name": "BAIC BJ40 Plus", "brand": "BAIC", "body": "SUV", "engine": "2.0L", "fuel": "Turbo", "seating": 5, "price": "Premium"},
    {"name": "Proton Saga", "brand": "Proton", "body": "Sedan", "engine": "1.3L", "fuel": "Gasoline", "seating": 5, "price": "Budget"},
    {"name": "Proton X70", "brand": "Proton", "body": "SUV", "engine": "1.5L", "fuel": "Turbo", "seating": 5, "price": "Premium"},
    {"name": "NUR E 75", "brand": "NUR", "body": "Sedan", "engine": "Electric", "fuel": "Electric", "seating": 5, "price": "Medium"},
    {"name": "Adam Revo", "brand": "Adam", "body": "Hatchback", "engine": "800cc", "fuel": "Gasoline", "seating": 4, "price": "Budget"},
    {"name": "DFSK Glory 580", "brand": "DFSK", "body": "SUV", "engine": "1.5L", "fuel": "Gasoline", "seating": 7, "price": "Medium"},
    {"name": "Isuzu D-Max", "brand": "Isuzu", "body": "Pickup", "engine": "3.0L", "fuel": "Diesel", "seating": 5, "price": "Premium"},
    {"name": "Peugeot 2008", "brand": "Peugeot", "body": "Crossover", "engine": "1.2L", "fuel": "Turbo", "seating": 5, "price": "Premium"},
    {"name": "Chery Tiggo 4 Pro", "brand": "Chery", "body": "SUV", "engine": "1.5L", "fuel": "Turbo", "seating": 5, "price": "Medium"},
    {"name": "Chery Tiggo 8 Pro", "brand": "Chery", "body": "SUV", "engine": "1.6L", "fuel": "Turbo", "seating": 7, "price": "Premium"},
]

# Features and their possible options for MCQ
FEATURES = [
    ("brand", ["Suzuki", "Toyota", "Honda", "Hyundai", "KIA", "Changan", "MG", "Haval", "BAIC", "Proton", "NUR", "Adam", "DFSK", "Isuzu", "Peugeot", "Chery"]),
    ("body", ["Hatchback", "Sedan", "SUV", "MPV", "Minivan", "Pickup", "Crossover"]),
    ("engine", ["660cc", "800cc", "1.0L", "1.2L", "1.3L", "1.4L", "1.5L", "1.6L", "2.0L", "2.5L", "2.7L", "2.8L", "3.0L", "Electric"]),
    ("fuel", ["Gasoline", "Diesel", "Hybrid", "Electric", "Turbo"]),
    ("seating", [4, 5, 7]),
    ("price", ["Budget", "Medium", "Premium"]),
]

def filter_cars(cars, feature, value):
    """Return a filtered list of cars matching the feature/value."""
    return [car for car in cars if car[feature] == value]
