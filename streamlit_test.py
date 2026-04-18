########10########10########10########10########10########10########10#######79

import streamlit as st

st.title("Factorio Calculator")

st.caption("Enter how many red science packs you want to produce per second.")

rate = st.number_input("Target red science per second", value = 1.0)

r_sci_craft_time = 5.0
a1_speed = 0.5

if st.button("Calculate"):
    copper = rate * 1
    iron = rate * 2
    
    st.subheader("Breakdown")
    
    st.write("Red Science:")
    st.write(f"- Copper plates: {rate}")
    st.write(f"- Iron gear: {rate}")
    
    st.write("Iron Gear:")
    st.write(f"- Iron Plates: {rate * 2}")
    
    st.info("This assumes base recipes with no bonuses.")
    
    rate_per_assembler = a1_speed / r_sci_craft_time
    assemblers = rate / rate_per_assembler
    
    st.subheader("Assembers Needed")
    st.write(f"{assemblers:.2f} assembler 1 machines")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Inputs")
        st.write(f"Target rate: {rate}")
    
    with col2:
        st.subheader("Machines")
        st.write(f"Assemblers: {assemblers:.2f}")
