import streamlit as st
from typing import List, Dict, Any, Optional
import json
from pathlib import Path
import pandas as pd
from utils import (
    load_recipes,
    parse_ingredients,
    find_matching_recipes,
    generate_shopping_list,
    normalize_ingredient
)

def main():
    st.set_page_config(
        page_title="Recipe Finder by Fridge",
        page_icon="🍳",
        layout="wide"
    )

    st.title("🍳 Recipe Finder by Fridge")
    st.markdown("### Find recipes based on ingredients you have!")

    # Load recipes
    recipes = load_recipes()
    
    # Sidebar for filters
    with st.sidebar:
        st.header("🔧 Filters")
        max_cook_time = st.slider("Max Cook Time (minutes)", 15, 240, 60, 15)
        dietary_prefs = st.multiselect(
            "Dietary Preferences",
            ["Vegetarian", "Vegan", "Gluten-Free"]
        )
        servings = st.number_input("Number of Servings", 1, 10, 2)
        
        # API Key input
        api_key = st.text_input("Spoonacular API Key (optional)", type="password")
        if api_key:
            st.success("Using API mode")

    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Ingredient input
        ingredients_input = st.text_area(
            "Enter ingredients you have (comma-separated):",
            placeholder="e.g., eggs, milk, spinach, tomatoes"
        )
        
        # Find recipes button
        if st.button("Find Recipes"):
            if not ingredients_input.strip():
                st.warning("Please enter some ingredients!")
            else:
                with st.spinner("Finding matching recipes..."):
                    # Parse ingredients
                    ingredients = parse_ingredients(ingredients_input)
                    
                    # Find matching recipes
                    matched_recipes = find_matching_recipes(
                        recipes,
                        ingredients,
                        max_cook_time=max_cook_time,
                        dietary_prefs=dietary_prefs,
                        servings=servings
                    )
                    
                    # Store in session state
                    st.session_state.matched_recipes = matched_recipes
                    st.session_state.ingredients = ingredients

    # Display results if available
    if 'matched_recipes' in st.session_state and st.session_state.matched_recipes:
        st.subheader("🍽️ Matching Recipes")
        
        for recipe in st.session_state.matched_recipes[:5]:  # Show top 5
            with st.expander(f"{recipe['title']} - {recipe['match_percent']:.0f}% match"):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if recipe.get('image_url'):
                        st.image(recipe['image_url'], use_column_width=True)
                
                with col2:
                    st.markdown(f"**Cook Time:** {recipe['cook_time_mins']} minutes")
                    st.markdown(f"**Servings:** {recipe['servings']}")
                    
                    # Show missing ingredients
                    if recipe['missing_ingredients']:
                        missing = ", ".join(recipe['missing_ingredients'])
                        st.warning(f"Missing: {missing}")
                    
                    # Show full recipe
                    if st.checkbox("Show full recipe", key=f"show_recipe_{recipe['id']}"):
                        st.subheader("Ingredients")
                        for ing in recipe['ingredients']:
                            st.markdown(f"- {ing}")
                        
                        st.subheader("Instructions")
                        for i, step in enumerate(recipe['instructions'], 1):
                            st.markdown(f"{i}. {step}")
                    
                    # Shopping list button
                    if recipe['missing_ingredients']:
                        if st.button("Add to Shopping List", key=f"shop_{recipe['id']}"):
                            if 'shopping_list' not in st.session_state:
                                st.session_state.shopping_list = set()
                            st.session_state.shopping_list.update(recipe['missing_ingredients'])
                            st.success("Added to shopping list!")
    
    # Shopping list section
    if 'shopping_list' in st.session_state and st.session_state.shopping_list:
        with col2:
            st.subheader("🛒 Shopping List")
            for item in st.session_state.shopping_list:
                st.markdown(f"- {item}")
            
            # Download shopping list
            shopping_text = "\n".join(st.session_state.shopping_list)
            st.download_button(
                label="Download Shopping List",
                data=shopping_text,
                file_name="shopping_list.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
