########10########10########10########10########10########10########10#######79

import csv


class Component:
    def __init__(self, name: str):
        self.name = name
        self.recipe = {}
        
    def add_recipe(self, component_name: str, qty_reqd_per_craft: float,
                   qty_per_craft: float):
        self.recipe[component_name] = qty_reqd_per_craft / qty_per_craft
            # normalize to qty_reqd / 1 component




def requirements(component: Component, amount_needed: float, comp_dict: dict,
                 totals: dict = None):
    # initialize accumulator dict once
    if totals is None:
        totals = {}   
        
    # accumulate
    if component.name in totals:
        totals[component.name] += amount_needed
    else:
        totals[component.name] = amount_needed
        
        
    # if item does not have recipe i.e. "raw_resource", skip        
    if not component.recipe:
        return totals

        
    # recurse
    for name, qty_reqd in component.recipe.items():
        totals = requirements(comp_dict[name], amount_needed * qty_reqd, comp_dict,
                              totals)
    
    return totals




csv_list_dict = []
# create dict where everything is a string
with open("Factorio_recipes_2.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # any() returns true if there is at least one item in the iterable
        if any(row.values()):    # because "empty" rows are not ignored
            csv_list_dict.append(row)
        
##Debug
#     for row in csv_list_dict:
#         print(row)
#     print()
        
        
        
        
        
        
        
        
# demonstration
if __name__ == "__main__":
    components_dict = {}
    
    # add some components
    for row in csv_list_dict:
        name = row['component']
        components_dict[name] = Component(name)
        
##Debug
#     for name, c_obj in components_dict.items():
#         print(f"{name}: {c_obj}")
#     print()        

    
    # add recipes
    for row in csv_list_dict:
        name = row['component']
        if row['qty_reqd_per_craft'] != '' and row['recipe_id'] == 'default':
           qty_reqd = float(row['qty_reqd_per_craft'])
           qty_per_craft = float(row['qty_per_craft'])
           components_dict[name].add_recipe(row['component_reqd'], qty_reqd,
                                            qty_per_craft)
##Debug           
#     for name, c_obj in components_dict.items():
#         print(f"{name}: {c_obj.recipe}")
#     print()
           

     
    
    
    my_factory = 'my_factory'
    components_dict[my_factory] = Component(my_factory)
#     components_dict[my_factory].add_recipe('red_science', 1, 1)
#     components_dict[my_factory].add_recipe('green_science', 1, 1)
#     components_dict[my_factory].add_recipe('black_science', 1, 1)
#     components_dict[my_factory].add_recipe('blue_science', 1, 1)
#     components_dict[my_factory].add_recipe('purple_science', 1, 1)
    components_dict[my_factory].add_recipe('yellow_science', 5, 1)
#     components_dict[my_factory].add_recipe('white_science', 1, 1)
  
    totals_dict = requirements(components_dict["my_factory"], 1, components_dict)
    
    for name, val in totals_dict.items():
        print(f"{name}: {val}")
    print()
       
     
    print("=)")
     
 