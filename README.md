# hosptial-management-system ( HMS module ) 
## Odoo module for hosptial management system
# HMS module features:
1. create models with all relations
 1. patient model
 2. doctor model
 3. department model
 4. log history model for track patient status
2. customize odoo from view
3. using fields attributes for define Characteristics on fields
4. using onchange decorator to update UI or change value based on conditions
5. odoo orm 
 1. override create method to fit in our needs
 2. override delete method to Prevents users from delete objects in some case
6. using API Constraints to define constraints on model fields
7. using SQL Constraints to deifne simple constraints
8. customize CRM module (model and view) and linked with patient
9. Odoo Security 
 1. ordinary user can see only patients menuitem, can't see doctors or departments menuitem
 2. manager can see all menuitems 
10. patients reports using Qweb 
# snippets from HMS module

 
