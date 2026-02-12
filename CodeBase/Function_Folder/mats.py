### Material Library for Cask materials and TRISO Pebble materials

import openmc

##########
### MPC Canister Stainless Steal S_316
##########
S_316 = openmc.Material(name='Stainless Steel 316')

# C Carbon - 0.08% maximum
# Mn Manganese - 2.00% maximum
# Si Silicon - 0.75% maximum
# Cr Chromium - 16.00 - 18.00%
# Ni Nickel - 10.00 - 14.00%
# Mo Molybdenum - 2.00 - 3.00%
# P Phosphorous - 0.045% max
# S Sulfur - 0.030% maximum
# N Nitrogen - 0.10% max
# Fe Iron - Balance

S_316.set_density('g/cm3',8.027)
S_316.add_element('C', 0.08 / 100 , percent_type='wo')
S_316.add_element('Mn', 2 / 100, percent_type='wo')
S_316.add_element('Si', 0.75 / 100, percent_type='wo')
S_316.add_element('Cr', 17 / 100, percent_type='wo')
S_316.add_element('Ni', 12 / 100, percent_type='wo')
S_316.add_element('Mo', 2.5 / 100, percent_type='wo')
S_316.add_element('P', 0.045 / 100, percent_type='wo')
S_316.add_element('S', 0.030 / 100, percent_type='wo')
S_316.add_element('N', 0.1 / 100, percent_type='wo')
S_316.add_element('Fe', 1 - (0.08 + 2 + 0.75 + 17 + 12 + 2.5 + 0.045 + 0.030 + 0.1) / 100 , percent_type='wo')

############
### Overpack
############

# Type II Portland Cement
Concrete = openmc.Material(name='Concrete')

# Atomic number | Fraction by weight
# 1 0.010000 
# 6 0.001000 
# 8 0.529107 
# 11 0.016000 
# 12 0.002000 
# 13 0.033872 
# 14 0.337021 
# 19 0.013000 
# 20 0.044000 
# 26 0.014000

Concrete.set_density('g/cm3',2.3)
Concrete.add_element('H', 0.010000, percent_type='wo')
Concrete.add_element('C', 0.001000, percent_type='wo')
Concrete.add_element('O', 0.529107, percent_type='wo')
Concrete.add_element('Na', 0.016000, percent_type='wo')
Concrete.add_element('Mg', 0.002000, percent_type='wo')
Concrete.add_element('Al', 0.033872, percent_type='wo')
Concrete.add_element('Si', 0.337021, percent_type='wo') 
Concrete.add_element('K', 0.013000, percent_type='wo')   
Concrete.add_element('Ca', 0.044000, percent_type='wo')  
Concrete.add_element('Fe', 1 - (0.010000 + 0.001000 + 0.529107 + 0.016000 + 0.002000 + 0.033872 + 0.337021 + 0.013000 + 0.044000), percent_type='wo')

#ASTM A516 Grade 70 / ASME SA516 Grade 70

A516_70 = openmc.Material(name='A516_70')
A516_70.set_density('g/cm3' , 7.85)

### https://www.azom.com/article.aspx?ArticleID=4787

A516_70.add_element('C',  0.1 /100, percent_type='wo')
A516_70.add_element('Si', 0.6 /100, percent_type='wo')
A516_70.add_element('Mn', 1 /100,   percent_type='wo')
A516_70.add_element('P',  0.03 /100,percent_type='wo')
A516_70.add_element('S',  0.03 /100,percent_type='wo')
A516_70.add_element('Al', 0.02 /100,percent_type='wo')
A516_70.add_element('Cr', 0.3 /100, percent_type='wo')
A516_70.add_element('Cu', 0.3 /100, percent_type='wo')
A516_70.add_element('Ni', 0.03 /100,percent_type='wo')
A516_70.add_element('Mo', 0.08 /100,percent_type='wo')
A516_70.add_element('Nb', 0.01 /100,percent_type='wo')
A516_70.add_element('Ti', 0.03 /100,percent_type='wo')
A516_70.add_element('V',  0.02 /100,percent_type='wo')
A516_70.add_element('Fe',1-(0.1 + 0.6 + 1 + 0.03 + 0.03 + 0.02 + 0.3 + 0.3 + 0.03 + 0.08 + 0.01 + 0.03 + 0.02)/100, percent_type='wo')

#############
# Fuel Basket
#############

#Dosed Stainless Steel

S_316_borated = openmc.Material(name='Fuel Basket')

# C Carbon - 0.08% maximum
# Mn Manganese - 2.00% maximum
# Si Silicon - 0.75% maximum
# Cr Chromium - 16.00 - 18.00%
# Ni Nickel - 10.00 - 14.00%
# Mo Molybdenum - 2.00 - 3.00%
# P Phosphorous - 0.045% max
# S Sulfur - 0.030% maximum
# N Nitrogen - 0.10% max
# Fe Iron - Balance

# B - whatever i want, but in practice around 1.5 w%o

B_wo = 1.5 / 100

S_316_borated.set_density('g/cm3',8.027)
S_316_borated.add_element('C', 0.08 / 100 , percent_type='wo')
S_316_borated.add_element('Mn', 2 / 100, percent_type='wo')
S_316_borated.add_element('Si', 0.75 / 100, percent_type='wo')
S_316_borated.add_element('Cr', 17 / 100, percent_type='wo')
S_316_borated.add_element('Ni', 12 / 100, percent_type='wo')
S_316_borated.add_element('Mo', 2.5 / 100, percent_type='wo')
S_316_borated.add_element('P', 0.045 / 100, percent_type='wo')
S_316_borated.add_element('S', 0.030 / 100, percent_type='wo')
S_316_borated.add_element('N', 0.1 / 100, percent_type='wo')


S_316_borated.add_element('B', B_wo, percent_type='wo')
S_316_borated.add_element('Fe', 1 - (0.08 + 2 + 0.75 + 17 + 12 + 2.5 + 0.045 + 0.030 + 0.1 + B_wo) / 100 , percent_type='wo')



#Ambient air
AIR = openmc.Material(name='Air')
AIR.set_density('g/cm3', 0.00120)
AIR.add_element('N', 78.1 / 100, percent_type='wo')
AIR.add_element('O', 20.95 / 100, percent_type='wo')
AIR.add_element('Ar', 0.95 / 100, percent_type='wo')


#helium for inside cask at normal conditions
He2 = openmc.Material(name='Helium')
He2.set_density('g/cm3', 0.000178)
He2.add_element('He', 1.0, percent_type='ao')


#accident case scenario where cask is submerged in water
water = openmc.Material(name='Water')


#### TODO : Make graphite for triso pebble 
#### TODO : Make depleted particle compotision for each particle
#### TODO : Or make smear triso pebble for entire pebble? 

graphite = openmc.Material()
graphite.set_density('g/cm3', 1.1995)
graphite.add_element('C', 1.0)
graphite.add_s_alpha_beta('c_Graphite')


material_colors = {S_316.id : "#b71732",
                   Concrete.id : '#aba596' , 
                   He2.id : '#ebab63',
                   water.id : '#1F3A5F',
                   AIR.id : '#B7D9F2',
                   A516_70.id : '#22223b',
                   S_316_borated.id : "#5c0110",
                   graphite.id : "#2B2828"}