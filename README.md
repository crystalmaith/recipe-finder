# Recipe Finder by Fridge

A Streamlit web application that helps you find recipes based on the ingredients you have in your fridge. The app suggests recipes based on available ingredients, shows matching percentages, and can generate shopping lists for missing items.

## Features

- 🍳 Find recipes based on available ingredients
- 📊 See match percentages for each recipe
- 🕒 Filter by cook time and dietary preferences
- 🛒 Generate shopping lists for missing ingredients
- 📱 Responsive design that works on all devices
- 🌐 Optional Spoonacular API integration for more recipes
- 💾 Works offline with the included recipe database

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/recipe-finder.git
   cd recipe-finder
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Enter the ingredients you have (comma-separated) and click "Find Recipes"

4. Use the filters in the sidebar to refine your search:
   - Maximum cook time
   - Dietary preferences (Vegetarian, Vegan, Gluten-Free)
   - Number of servings

5. For each recipe, you can:
   - View the full recipe with ingredients and instructions
   - See what ingredients you're missing
   - Add missing ingredients to your shopping list

### Spoonacular API (Optional)

For access to more recipes, you can use the Spoonacular API:

1. Get a free API key from [Spoonacular](https://spoonacular.com/food-api)
2. Enter your API key in the sidebar when the app is running
3. The app will fetch additional recipes from the API

## Project Structure

```
recipe-finder/
├── app.py                # Main Streamlit application
├── utils.py              # Utility functions for recipe processing
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore file
├── data/
│   └── recipes.json     # Sample recipe database
└── tests/
    └── test_utils.py    # Unit tests for utility functions
```

## Running Tests

To run the test suite:

```bash
pytest tests/
```

## Example Usage

1. Enter these ingredients: `eggs, milk, spinach, tomatoes, onion`
2. Click "Find Recipes"
3. You should see recipes like "Spinach Omelette" with a high match percentage
4. Click on a recipe to see details and add missing ingredients to your shopping list

## Screenshots

(Add screenshots of your application here)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Recipe data from various open sources
- Icons from [Font Awesome](https://fontawesome.com/)
- Built with [Streamlit](https://streamlit.io/)
