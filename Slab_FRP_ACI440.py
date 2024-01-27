import math
import re
import streamlit as st
import subprocess
import os




# st.image('IITB_Logo.png', caption='IIT Bombay')
st.image('IITB_Logo.png', caption=None, width=50, use_column_width=50, clamp=False, channels="RGB", output_format="auto")
st.header('Design of FRP Strengthening for RC Slabs', divider='rainbow')
# st.header('_Streamlit_ is :blue[cool] :sunglasses:')
#
# Function to replace variables in the template
def replace_variables(template, variables):
    for variable, value in variables.items():
        template = re.sub(f"var-{variable}", str(value), template)
    return template
#
variables = {}

with open("FRP_SlabCalc.tex", "r") as f:
    template_content=f.read()

col1, col2, col3=st.columns(3)


# Define your variables
variables["fck"] = col1.number_input("Concrete Cube Strength (MPa)",value = 30)
variables["fy"] = col1.number_input("Rebar Yield Strength (MPa)",value = 500)
variables["D"] = st.number_input("Thickness of slab (mm)",value = 200)
variables["ddash"] = st.number_input("Cover to slab (mm)",value = 30)
variables["w_all"] = st.number_input("Allowable crack-width (mm)",value = 0.2)
variables["bar_dia"] = st.number_input("Dia of rebar (mm)",value = 10)
variables["bar_spa"] = st.number_input("Spacing of rebar (mm)",value = 100)
variables["CEval"] = st.number_input("Environmental Factor",value = 0.95)
variables["f_fu_star"] = st.number_input("Ultimate Strength of FRP (MPa)",value = 2500)
variables["eps_fu_star"] = st.number_input("Ultimate Strain of FRP ",value = 0.018)
variables["M_new"]= st.number_input("New Design Moment (kN-m)",value = 118)
variables["M_DL"] = st.number_input("Moment due to dead load (kN-m)",value = 200)
variables["Noply"] = st.number_input("No of FRP layers ",value = 1)
variables["tf"] = st.number_input("Thickness of FRP (mm)",value = 3)
variables["wf"] = st.number_input("Width of FRP strip (mm)",value = 200)
variables["Ef"] = st.number_input("Modulus of elasticity of FRP (MPa)",value = 200000)
variables["Es"] = st.number_input("Modulus of elasticity of steel (MPa)",value = 185000)

FName = st.text_input("New File Name")
if os.path.isfile(FName+".pdf"):
    os.remove(FName+".pdf")


# print("fck:", fck)




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

variables["Ast_pr"] = ((1000/variables["bar_spa"])*0.25*math.pi*variables["bar_dia"]**2)
variables["f_fu"] = variables["CEval"]*variables["f_fu_star"]

# eps_fu = CEval*eps_fu_star
# fc = 0.8*fck
# Ec = 4700*math.sqrt(fc)
# Af = Noply*tf*wf
# df = D
# deff = D - ddash - bar_dia/2
# modrat = Es/Ec
# pt_pr = 100*Ast_pr/(1000*deff)
# rho = pt_pr/100
# kval = math.sqrt((rho*modrat)**2 + (2*rho*modrat)) - (rho*modrat)
# kdval = kval*deff
# Icr = (1000*kdval**3)/3 + ((modrat*Ast_pr)*(deff - kdval)**2)
# eps_bi = M_DL*10**6*(df - kdval)/(Icr*Ec)
# eps_fd = min(0.41*math.sqrt(fc/(Noply*Ef*tf)),0.9*eps_fu)
#
# NA_ass = 46
# eps_cdash = 1.7*fc/Ec
# beta1 = (4*eps_cdash - 0.003)/(6*eps_cdash - 2*0.003)
# alpha1 = (3*eps_cdash*0.003 - 0.003**2)/(3*beta1*eps_cdash**2)
#
# eps_fe = min(0.003*(df - NA_ass)/NA_ass,eps_fd)
# f_fe = eps_fe*Ef
#
# c = (Ast_pr*fy + Af*f_fe)/(alpha1*fc*beta1*1000)
#
# eps_c = (eps_fe + eps_bi)*(df - NA_ass)/NA_ass
# eps_s = (eps_fe + eps_bi)*NA_ass/(df - NA_ass)
#
# fs_ext = min(Es*eps_s,fy)
#
# # Calaculation of flexural strength
#
# Mns = Ast_pr*fs_ext*(deff - (beta1*c)/2)
# Mnf = Af*f_fe*(deff - (beta1*c)/2)
# Mn = Mns + Mnf
#
# phival = 0.9
# phiMn = phival*Mn/10**6


if phiMn > M_new:
    st.success("SAFE")
else:
    st.error("UNSAFE")

'''

# file = open("FRP_SlabCalc.tex", "r")
# text = file.read()
# new_text = re.sub("varC_E", str(CEval), text)
# new_file = open("FRP_SlabCalc_new.tex", "w")
# new_file.write(new_text)


print("Ast_pr:", round(Ast_pr,2))
print("fs_ext:", fs_ext)
print("phiMn:", round(phiMn))
'''


if st.button("Run"):
    # variables = {}
    # variables["fck"]=fck
    # variables["fy"]=fy
    # variables["fck"] = fck
    # variables["fy"] = fy
    # variables["fck"] = fck
    # variables["fy"] = fy
    # variables["fck"] = fck
    # variables["fy"] = fy

    # Replace variables in the template
    modified_content = replace_variables(template_content, variables)

    # Write the modified content to a new file
    with open(f'{FName}.tex', 'w') as f:
        f.write(modified_content)
    subprocess.run(["pdflatex", f"{FName}.tex"])


