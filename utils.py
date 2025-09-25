import json
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple
import pandas as pd
import inflect
import re

# Initialize inflect engine for singularization
p = inflect.engine()

def load_recipes(file_path: str = "data/recipes.json") -> List[Dict[str, Any]]:
    """Load recipes from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Recipe file not found at {file_path}")

def normalize_ingredient(ingredient: str) -> str:
    """
    Normalize an ingredient string by:
    1. Converting to lowercase
    2. Removing extra whitespace
    3. Converting to singular form
    4. Removing quantities and measurements
    """
    # Convert to lowercase and strip whitespace
    ingredient = ingredient.lower().strip()
    
    # Remove quantities and measurements (e.g., "2 cups of milk" -> "milk")
    ingredient = re.sub(r'\b\d+\s*[\w/.-]*\s*', '', ingredient)
    
    # Remove common measurement words
    measurement_words = [
        'teaspoon', 'tablespoon', 'cup', 'cups', 'pinch', 'dash', 'pound',
        'ounce', 'gram', 'kilogram', 'liter', 'milliliter', 'pint', 'quart',
        'gallon', 'can', 'jar', 'package', 'bunch', 'sprig', 'clove', 'slice',
        'of', 'and', 'or', 'to', 'taste', 'for', 'as', 'needed'
    ]
    
    words = [word for word in ingredient.split() if word not in measurement_words]
    ingredient = ' '.join(words)
    
    # Convert to singular form
    singular = p.singular_noun(ingredient)
    if singular:
        return singular
    return ingredient

def parse_ingredients(ingredients_input: str) -> Set[str]:
    """
    Parse a comma-separated string of ingredients into a set of normalized ingredients.
    """
    if not ingredients_input.strip():
        return set()
    
    # Split by comma and clean each ingredient
    ingredients = [ing.strip() for ing in ingredients_input.split(',')]
    
    # Normalize each ingredient
    return {normalize_ingredient(ing) for ing in ingredients if ing.strip()}

def recipe_matches_diet(recipe: Dict[str, Any], dietary_prefs: List[str]) -> bool:
    """Check if a recipe matches the dietary preferences."""
    if not dietary_prefs:
        return True
    
    recipe_tags = {tag.lower() for tag in recipe.get('tags', [])}
    
    # Map dietary preferences to recipe tags
    pref_mapping = {
        'vegetarian': 'vegetarian',
        'vegan': 'vegan',
        'gluten-free': 'gluten-free'
    }
    
    required_tags = {pref_mapping[pref.lower()] for pref in dietary_prefs 
                    if pref.lower() in pref_mapping}
    
    return required_tags.issubset(recipe_tags)

def score_recipe(recipe: Dict[str, Any], available_ingredients: Set[str]) -> float:
    """
    Score a recipe based on the number of matching ingredients.
    Returns a tuple of (match_percent, missing_ingredients)
    """
    recipe_ingredients = {normalize_ingredient(ing) for ing in recipe['ingredients']}
    
    # Find matching and missing ingredients
    matching = available_ingredients.intersection(recipe_ingredients)
    missing = recipe_ingredients - available_ingredients
    
    # Calculate match percentage
    if not recipe_ingredients:  # Avoid division by zero
        return 0.0, list(missing)
    
    match_percent = (len(matching) / len(recipe_ingredients)) * 100
    return match_percent, list(missing)

def find_matching_recipes(
    recipes: List[Dict[str, Any]],
    available_ingredients: Set[str],
    max_cook_time: int = 60,
    dietary_prefs: List[str] = None,
    servings: int = 2
) -> List[Dict[str, Any]]:
    """
    Find recipes that match the given criteria and ingredients.
    """
    if dietary_prefs is None:
        dietary_prefs = []
    
    results = []
    
    for recipe in recipes:
        # Skip if cook time exceeds maximum
        if recipe.get('cook_time_mins', 0) > max_cook_time:
            continue
            
        # Skip if doesn't match dietary preferences
        if not recipe_matches_diet(recipe, dietary_prefs):
            continue
            
        # Score the recipe
        score, missing = score_recipe(recipe, available_ingredients)
        
        # Skip recipes with 0% match
        if score <= 0:
            continue
            
        # Create result entry
        result = recipe.copy()
        result['match_percent'] = score
        result['missing_ingredients'] = missing
        results.append(result)
    
    # Sort by match percentage (descending) and cook time (ascending)
    results.sort(key=lambda x: (-x['match_percent'], x.get('cook_time_mins', float('inf'))))
    
    return results

def generate_shopping_list(recipes: List[Dict[str, Any]]) -> Set[str]:
    """
    Generate a shopping list of missing ingredients from selected recipes.
    """
    shopping_list = set()
    
    for recipe in recipes:
        if 'missing_ingredients' in recipe:
            shopping_list.update(recipe['missing_ingredients'])
    
    return shopping_list
