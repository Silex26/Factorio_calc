########10########10########10########10########10########10########10#######79

import streamlit as st
import csv



class Component:
    def __init__(self, name: str):
        self.name = name
        self.recipe = {}
        
    def add_recipe(self, component_name: str, qty_reqd_per_craft: float,
                   qty_per_craft: float):
        self.recipe[component_name] = qty_reqd_per_craft / qty_per_craft
            # normalize to qty_reqd / 1 component


def create_csv_list_dict(file: str):
    csv_list_dict = []
    # create dict where everything is a string
    with open(file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # any() returns true if there is at least one item in the iterable
            if any(row.values()):    # because "empty" rows are not ignored
                csv_list_dict.append(row)
    return csv_list_dict

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
        
    # recurse for any components in recipe
    for name, qty_reqd in component.recipe.items():
        totals = requirements(comp_dict[name], amount_needed * qty_reqd, comp_dict,
                              totals)
    
    return totals



# read csv of recipe data
csv_list_dict = create_csv_list_dict("Factorio_recipes_2.csv")
        
##Debug
# for row in csv_list_dict:
#     st.write(f"{row}")

# add some components
components_dict = {}

for row in csv_list_dict:
    name = row['component']
    components_dict[name] = Component(name)
    
##Debug           
# for name, c_obj in components_dict.items():
#     st.write(f"{name}: {c_obj}")


# add recipes
for row in csv_list_dict:
    name = row['component']
    if row['qty_reqd_per_craft'] != '' and row['recipe_id'] == 'default':
       qty_reqd = float(row['qty_reqd_per_craft'])
       qty_per_craft = float(row['qty_per_craft'])
       components_dict[name].add_recipe(row['component_reqd'], qty_reqd,
                                        qty_per_craft)
       
##Debug           
# for name, c_obj in components_dict.items():
#     st.write(f"{name}: {c_obj.recipe}")


st.title("Factorio Calculator =)")


errors = []

#initialize session state once, with one starter row
if 'targets' not in st.session_state:
    st.session_state.targets = [ {'item': '', 'rate': 1.0} ]
    
if st.button("Click to add more items to produce"):
    st.session_state.targets.append( {'item': '','rate': 1.0} )

# generate keys and input boxes for each item and rate
# store them in targets list-dict
for i, target in enumerate(st.session_state.targets):
    st.subheader(f"Target {i+1}")
    
    st.caption("Enter what item you wish to produce (ex. red_science).")
    item_name = st.selectbox("Select item",
                             list(components_dict.keys()),
                             key=f"item_{i}")
    
    if item_name not in components_dict:
        errors.append(f"'{item_name}' is not a valid component.")
    
    rate = st.number_input(
        f"Rate {i+1}",
        min_value=0.0,
        value=float(target["rate"]),
        step=0.1,
        key=f"rate_{i}")
    
    if rate <= 0:
        errors.append("Rate must be greater than 0.")
    
    st.session_state.targets[i]["item"] = item_name
    st.session_state.targets[i]["rate"] = rate


if st.button("Click to remove items"):
    del st.session_state.targets[-1]





    

# st.caption(f"Enter how many different items do you want to produce?")
# num_items = st.number_input(f"number of different items",
#                        min_value = int(1),
#                        value = int(1),
#                        step = int(1))
# 
#     st.caption("Enter what item you wish to produce (ex. red_science).")
#     item_name = st.selectbox("Select item", list(components_dict.keys()) )
#     if item_name not in components_dict:
#         errors.append(f"'{item_name}' is not a valid component.")
# 
# 
#     st.caption(f"Enter how many {item_name} you want to produce per second.")
#     rate = st.number_input(f"Target {item_name} per second",
#                            min_value = 0.0001,
#                            value = 1.0,
#                            step = 0.1)
#     if rate <= 0:
#         errors.append("Rate must be greater than 0.")






if st.button("Calculate"):
    my_factory = Component('my_factory')
    
    if errors:
        for err in errors:
            st.error(err)
    else:
        pass
        for i, target in enumerate(st.session_state.targets):
            item = target['item']
            rate = target['rate']
            
            my_factory.add_recipe(item, rate, 1)
            totals_dict = requirements(my_factory, 1, components_dict)
            st.subheader("This will require:")
            
            for name, val in totals_dict.items():
                st.write(f"{name}: {val}")
            
            st.info("This assumes base recipes with no bonuses.")
            
            
            
#         my_factory = Component('my_factory')
#         my_factory.add_recipe(item_name, rate, 1)
#         totals_dict = requirements(my_factory, 1, components_dict)
#         st.subheader("This will require:")
#         
#         for name, val in totals_dict.items():
#             st.write(f"{name}: {val}")
#             
#         st.info("This assumes base recipes with no bonuses.")
    

    
