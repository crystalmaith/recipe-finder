import pytest
from pathlib import Path
import sys
import os

# Add the parent directory to the path so we can import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    normalize_ingredient,
    parse_ingredients,
    score_recipe,
    recipe_matches_diet
)

def test_normalize_ingredient():
    # Test basic normalization
    assert normalize_ingredient("  Eggs  ") == "egg"
    assert normalize_ingredient("2 cups of Milk") == "milk"
    assert normalize_ingredient("FRESH basil leaves") == "fresh basil leaf"
    assert normalize_ingredient("1/2 teaspoon salt") == "salt"
    assert normalize_ingredient("garlic cloves") == "garlic clove"

def test_parse_ingredients():
    # Test parsing of ingredient strings
    ingredients = parse_ingredients("eggs, milk, 2 cups flour, fresh basil")
    assert "egg" in ingredients
    assert "milk" in ingredients
    assert "flour" in ingredients
    assert "fresh basil" in ingredients
    assert len(ingredients) == 4
    
    # Test empty input
    assert parse_ingredients("") == set()
    assert parse_ingredients("   ") == set()

def test_score_recipe():
    # Create a test recipe
    recipe = {
        'ingredients': ['eggs', 'milk', 'flour', 'sugar'],
        'cook_time_mins': 20
    }
    
    # Test with all ingredients available
    score, missing = score_recipe(recipe, {'egg', 'milk', 'flour', 'sugar'})
    assert score == 100.0
    assert missing == []
    
    # Test with some ingredients missing
    score, missing = score_recipe(recipe, {'egg', 'milk'})
    assert score == 50.0
    assert set(missing) == {'flour', 'sugar'}
    
    # Test with no matching ingredients
    score, missing = score_recipe(recipe, {'chicken', 'rice'})
    assert score == 0.0
    assert set(missing) == {'egg', 'milk', 'flour', 'sugar'}

def test_recipe_matches_diet():
    # Create test recipes
    vegetarian_recipe = {'tags': ['vegetarian', 'italian']}
    vegan_recipe = {'tags': ['vegan', 'gluten-free']}
    regular_recipe = {'tags': ['meat', 'dinner']}
    
    # Test vegetarian filter
    assert recipe_matches_diet(vegetarian_recipe, ['Vegetarian']) is True
    assert recipe_matches_diet(vegan_recipe, ['Vegetarian']) is False
    assert recipe_matches_diet(regular_recipe, ['Vegetarian']) is False
    
    # Test vegan filter
    assert recipe_matches_diet(vegetarian_recipe, ['Vegan']) is False
    assert recipe_matches_diet(vegan_recipe, ['Vegan']) is True
    
    # Test multiple filters
    assert recipe_matches_diet(vegan_recipe, ['Vegan', 'Gluten-Free']) is True
    assert recipe_matches_diet(vegetarian_recipe, ['Vegan', 'Gluten-Free']) is False
    
    # Test no filters
    assert recipe_matches_diet(vegetarian_recipe, []) is True

def test_load_recipes():
    from utils import load_recipes
    
    # Test loading recipes from the data file
    recipes = load_recipes('data/recipes.json')
    
    # Should load all 10 test recipes
    assert len(recipes) == 10
    
    # Check structure of first recipe
    first_recipe = recipes[0]
    assert 'title' in first_recipe
    assert 'ingredients' in first_recipe
    assert 'instructions' in first_recipe
    assert 'cook_time_mins' in first_recipe
    
    # Test with non-existent file
    with pytest.raises(FileNotFoundError):
        load_recipes('non_existent_file.json')
