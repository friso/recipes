import pandas as pd
from tabulate import tabulate
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()

def load_dataset():
    recipes_and_ingredients_df = pd.read_pickle('./pickles/dataset.pkl')
    return recipes_and_ingredients_df

def prompt_ingredients():
    user_input = input('Enter your ingredients (comma-seperated): ')
    return [ps.stem(ing.strip()) for ing in user_input.split(',')]

def prompt_calories():
    user_input = input('Enter max calories:')
    return user_input.strip()

def calories_less_than(comparand, calories):
    try:
        calories = int(calories)
        comparand = int(comparand[0])
    except ValueError:
       return True
    calories = int(calories)
    if ((calories == None) | (calories == 0) | (comparand == None)):
        return True
    return comparand <= calories


def recipes_than_include_ingredients(recipes_and_ingredients_df, input_ingredients, input_calories):
    return recipes_and_ingredients_df[
        (recipes_and_ingredients_df['course'] == 'hoofdgerecht')
        &
        (recipes_and_ingredients_df['ingredient'].isin(input_ingredients))
        &
        (calories_less_than(recipes_and_ingredients_df['calories'], input_calories))
    ].drop_duplicates(
        subset='recipe_id', keep='first', inplace=False
    ).sort_values(
        'uncommon_ingredients_count', ascending=True
    )

def main():
    recipes_and_ingredients_df = load_dataset()
    input_ingredients = prompt_ingredients()
    input_calories = prompt_calories()
    main_course_ingredients_without_common_ones = recipes_than_include_ingredients(recipes_and_ingredients_df, input_ingredients, input_calories)
    final_df = main_course_ingredients_without_common_ones[['recipe_name', 'uncommon_ingredients', 'calories']].head(10)
    print(tabulate(final_df, headers='keys'))
main()
