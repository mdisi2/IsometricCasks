### Holds messy materials like alloyx

import openmc


Alloy_X = openmc.Material(name='Stainless Steel 316')

# Ca Carbon - 0.08% maximum
# Mn Manganese - 2.00% maximum
# Si Silicon - 0.75% maximum
# Cr Chromium - 16.00 - 18.00%
# Ni Nickel - 10.00 - 14.00%
# Mo Molybdenum - 2.00 - 3.00%
# P Phosphorous - 0.045% max
# S Sulfur - 0.030% maximum
# N Nitrogen - 0.10% max
# Fe Iron - Balance

Alloy_X.set_density('g/cm3',8.027)
Alloy_X.add_element('Ca', 0.08 / 100)
Alloy_X.add_element('Mn', 2 / 100)
Alloy_X.add_element('Si', 0.75 / 100)
Alloy_X.add_element('Cr', 17 / 100)
Alloy_X.add_element('Ni', 12 / 100)
Alloy_X.add_element('Mo', 2.5 / 100)
Alloy_X.add_element('P', 0.045 / 100)
Alloy_X.add_element('S', 0.030 / 100)
Alloy_X.add_element('N', 0.1 / 100)
Alloy_X.add_element('Fe', 65.485 )

Concrete = openmc.Material('Concrete')

# 