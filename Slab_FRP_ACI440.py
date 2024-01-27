import math
import re
import streamlit as st
import subprocess
import os

st.image('IITB_Logo.png', caption=None, width=50, use_column_width=50, clamp=False, channels="RGB", output_format="auto")
st.header('Design of FRP Strengthening for RC Slabs', divider='rainbow')

# Function to replace variables in the template
def replace_variables(template, variables):
    for variable, value in variables.items():
        template = re.sub(f"var_{variable}", str(value), template)
    return template
#
variables = {}

with open("FRP_SlabCalc.tex", "r") as f:
    template_content=f.read()

col1, col2, col3 = st.columns(3)


# Define your variables
variables["fck"] = col1.number_input("Concrete Cube Strength (MPa)",value = 30)
variables["fy"] = col2.number_input("Rebar Yield Strength (MPa)",value = 500)
variables["D"] = col3.number_input("Thickness of slab (mm)",value = 200)
variables["ddash"] = col1.number_input("Cover to slab (mm)",value = 30)
variables["w_all"] = col2.number_input("Allowable crack-width (mm)",value = 0.2)
variables["bar_dia"] = col3.number_input("Dia of rebar (mm)",value = 10)
variables["bar_spa"] = col1.number_input("Spacing of rebar (mm)",value = 100)
variables["CEval"] = col2.number_input("Environmental Factor",value = 0.95)
variables["f_fu_star"] = col3.number_input("Ultimate Strength of FRP (MPa)",value = 2500)
variables["eps_fu_star"] = col1.number_input("Ultimate Strain of FRP ",value = 0.018)
variables["M_new"]= col2.number_input("New Design Moment (kN-m)",value = 118)
variables["M_DL"] = col3.number_input("Moment due to dead load (kN-m)",value = 200)
variables["Noply"] = col1.number_input("No of FRP layers ",value = 1)
variables["tf"] = col2.number_input("Thickness of FRP (mm)",value = 3)
variables["wf"] = col3.number_input("Width of FRP strip (mm)",value = 200)
variables["Ef"] = col1.number_input("Modulus of elasticity of FRP (MPa)",value = 200000)
variables["Es"] = col2.number_input("Modulus of elasticity of steel (MPa)",value = 185000)

FName = st.text_input("New File Name", value="Calculations")
if os.path.isfile(FName+".pdf"):
    os.remove(FName+".pdf")

# INPUT DATA
# fck = 50
# fy = 500
# D = 200
# ddash = 25
# w_all = 0.3
#
# bar_dia = 10
# bar_spa = 100
# CEval = 0.95
# f_fu_star = 2900
# eps_fu_star = 0.018
# M_new = 115.08
# M_DL = 12.97
# Noply = 1
# tf = 3
# wf = 243
# Ef = 1.65e5
# Es = 2e5

# Calculations

variables["Ast_pr"] = round(((1000/variables["bar_spa"])*0.25*math.pi*variables["bar_dia"]**2), 4)
variables["f_fu"] = variables["CEval"]*variables["f_fu_star"]
variables["eps_fu"] = round(variables["CEval"]*variables["eps_fu_star"], 4)
variables["fc"] = 0.8*variables["fck"]
variables["Ec"] = round(4700*math.sqrt(variables["fc"]), 4)
variables["Af"] = variables["Noply"]*variables["tf"]*variables["wf"]
variables["df"] = variables["D"]
variables["deff"] = variables["D"] - variables["ddash"] - variables["bar_dia"]/2
variables["modrat"] = round(variables["Es"]/variables["Ec"], 4)
variables["pt_pr"] = round(100*variables["Ast_pr"]/(1000*variables["deff"]), 4)
variables["rho"] = round(variables["pt_pr"]/100, 4)
variables["kval"] = round(math.sqrt((variables["rho"]*variables["modrat"])**2 + (2*variables["rho"]*variables["modrat"])) - (variables["rho"]*variables["modrat"]), 4)
variables["kdval"] = round(variables["kval"]*variables["deff"], 4)
variables["Icr"] = round((1000*variables["kdval"]**3)/3 + ((variables["modrat"]*variables["Ast_pr"])*(variables["deff"] - variables["kdval"])**2), 4)
variables["eps_bi"] = round(variables["M_DL"]*10**6*(variables["df"] - variables["kdval"])/(variables["Icr"]*variables["Ec"]), 6)
variables["eps_fd"] = round(min(0.41*math.sqrt(variables["fc"]/(variables["Noply"]*variables["Ef"]*variables["tf"])),0.9*variables["eps_fu"]), 6)

# NA_ass = 46
# variables["variables["eps_cdash"]"] = round(1.7*variables["variables["fc"]"]/variables["Ec"], 6)
# variables["beta1"] = round((4*variables["variables["eps_cdash"]"] - 0.003)/(6*variables["variables["eps_cdash"]"] - 2*0.003), 7)
# variables["alpha1"] = round((3*variables["variables["eps_cdash"]"]*0.003 - 0.003**2)/(3*variables["beta1"]*variables["variables["eps_cdash"]"]**2), 7)

# variables["eps_fe"] = round(min(0.003*(variables["df"] - NA_ass)/NA_ass,variables["eps_fd"]), 6)
# f_fe = variables["eps_fe"]*variables["Ef"]

# c = (variables["Ast_pr"]*variables["fy"] + variables["Af"]*f_fe)/(variables["alpha1"]*variables["variables["fc"]"]*variables["beta1"]*1000)

# variables["eps_c"] = (variables["eps_fe"] + variables["eps_bi"])*(variables["df"] - NA_ass)/NA_ass
# eps_s = (variables["eps_fe"] + variables["eps_bi"])*NA_ass/(variables["df"] - NA_ass)

# fs_ext = min(variables["Es"]*eps_s,variables["fy"])
eps_c = 0.003
variables["eps_cdash"] = round(1.7*variables["fc"]/variables["Ec"], 6)

NA_ass = 46

variables["beta1"] = round((4 * variables["eps_cdash"] - 0.003) / (6 * variables["eps_cdash"] - 2 * 0.003), 4)
variables["alpha1"] = round((3*variables["eps_cdash"]*eps_c - 0.003**2)/(3*variables["beta1"]*variables["eps_cdash"]**2), 4)
kd = NA_ass
tol = 0.2
error = 1

print(variables["df"], kd, variables["eps_bi"] ,variables["eps_fd"], variables["Ef"], variables["Ast_pr"],  variables["fy"], variables["Af"], variables["alpha1"], variables["fc"], variables["beta1"])

while error > tol:
    variables["eps_fe"] = min(0.003*(variables["df"] - kd)/kd - variables["eps_bi"],variables["eps_fd"])
    variables["f_fe"] = round(variables["eps_fe"] * variables["Ef"], 4)
    c = (variables["Ast_pr"] * variables["fy"] + variables["Af"] * variables["f_fe"]) / (variables["alpha1"] * variables["fc"] * variables["beta1"] * 1000)


    error = abs(c - kd) / kd
    # print(f"Loop {kd} {c}")
    if error < tol:
        # print(f"Break {kd} {c}")
        break
    else:
        kd = (kd+c)/2

variables["c_final"]=round(kd, 4)
variables["eps_c"] = (variables["eps_fe"] + variables["eps_bi"]) * (variables["df"] - kd) / kd
variables["eps_s"] = (variables["eps_fe"] + variables["eps_bi"]) * kd / (variables["df"] - kd)
variables["fs_ext"] = min(variables["Es"]*variables["eps_s"],variables["fy"])


# Calaculation of flexural strength

variables["Mns"] = variables["Ast_pr"]*variables["fs_ext"]*(variables["deff"] - (variables["beta1"]*c)/2)
variables["Mnf"] = variables["Af"]*variables["f_fe"]*(variables["deff"] - (variables["beta1"]*c)/2)
variables["Mn"] = variables["Mns"] + variables["Mnf"]

variables["phival"] = 0.9
variables["phiMn"] = variables["phival"]*variables["Mn"]/10**6

if variables["phiMn"] > variables["M_new"]:
    st.success("SAFE")
else:
    st.error("UNSAFE")

if st.button("Run"):
    # Replace variables in the template
    modified_content = replace_variables(template_content, variables)

    # Write the modified content to a new file
    with open(f'{FName}.tex', 'w') as f:
        f.write(modified_content)
    subprocess.run(["pdflatex", f"{FName}.tex"])
