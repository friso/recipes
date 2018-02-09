import pandas as pd
import json
import re

def common_ingredients():
    common_ingredients = ['knoflook','traditionele olijfolie','ui','olijfolie','zonnebloemolie',
        'middelgroot ei','boter','uien','olie','kraanwater','zout','water','arachideolie',
        'halfvolle melk','bosui','tomaten','eieren','tarwebloem','tomaat','bloem',
        'margarine','ei','melk','azijn']
    return common_ingredients

def build_dataset():
    print('Building dataset...')
    recipe_id_pattern = re.compile(r'^.*?\/(R-R[0-9]+)\/.*$')

    with open('./../../notebook/recipes.json', 'r') as json_lines_file:
        json_recipes = [json.loads(line.strip()) for line in json_lines_file.readlines()]

    recipes_and_ingredients_df = pd.DataFrame([
        {
            'recipe_id': recipe_id_pattern.match(rcp['location']).group(1),
            'recipe_name': rcp['name'],
            'calories': int(rcp['calories'].replace('.','')[0:-5]) if rcp['calories'] else None,
            'course': rcp['course'],
            'ingredient': ingredient,
            'uncommon_ingredients': list(set(rcp['ingredient_search_terms']) - set(common_ingredients())),
            'uncommon_ingredients_count': len(difference)
        }
        for rcp in json_recipes
        for ingredient in rcp['ingredient_search_terms']
        # TODO: Get rid of this ugliness
        for difference in set(rcp['ingredient_search_terms']) - set(common_ingredients())
    ])
    return recipes_and_ingredients_df

build_dataset().to_pickle('./pickles/dataset.pkl')
