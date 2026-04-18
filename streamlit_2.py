########10########10########10########10########10########10########10#######79

import streamlit as st
import csv
import os


# a graph-like structure for holding connections between components thru recipes
class Component:
    def __init__(self, name: str):
        self.name = name
        self.recipe = {}
        
    def add_recipe(self, component_name: str, qty_reqd_per_craft: float,
                   qty_per_craft: float):
        self.recipe[component_name] = qty_reqd_per_craft / qty_per_craft
            # normalize to qty_reqd / 1 component

# read a csv, using csv
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

#recursive function to accumulate required components
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

# helper function to find file path
BASE_DIR = os.path.dirname(__file__)
csv_path = os.path.join(BASE_DIR, "Factorio_recipes_2.csv")

# read csv of recipe data
csv_list_dict = create_csv_list_dict(csv_path)
        
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


st.title("Factorio Calculator =D")


errors = []

#initialize session state once, with one starter row
if 'targets' not in st.session_state:
    st.session_state.targets = [ {'item': '', 'rate': 1.0} ]
    
if 'calc_result' not in st.session_state:
    st.session_state.calc_result = None
    
if 'calc_errors' not in st.session_state:
    st.session_state.calc_errors = []
    

# forces a screen refresh
def clear_results():
    st.session_state.calc_result = None
    st.session_state.calc_errors = []
    
def add_target():
    st.session_state.targets.append( {'item': '', 'rate': 1.0} )
    clear_results()
    
def delete_target():
    st.session_state.targets.pop()
    clear_results()
    
    
# add item button
st.button("Click to add more items to produce", on_click=add_target)

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
    

# delete item button
st.button("Click to remove items", on_click=delete_target)

# call requirements with inputs
if st.button("Calculate"):
    my_factory = Component('my_factory')
    
    if errors:
        st.session_state.calc_error = errors
        st.session_state.calc_result = None
        for err in errors:
            st.error(err)
            
    else:
        for i, target in enumerate(st.session_state.targets):
            item = target['item']
            rate = target['rate']
            
            my_factory.add_recipe(item, rate, 1)
            st.session_state.calc_result = requirements(my_factory, 1,
                                                        components_dict)
            
    if st.session_state.calc_result is not None:
        st.subheader("This will require:")            
        for name, val in st.session_state.calc_result.items():
            st.write(f"{name}: {val}")
            
        st.info("This assumes base recipes with no bonuses.")
            
            
            

    

    
