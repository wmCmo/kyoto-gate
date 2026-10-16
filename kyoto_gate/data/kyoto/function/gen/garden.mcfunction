# Fit the largest garden that will go here (args in storage kyoto:tmp garden). Returns 1 if placed.
execute store result score #ok ky.var run function kyoto:gen/gtry_7x6 with storage kyoto:tmp garden
execute if score #ok ky.var matches 1 positioned ^ ^ ^4 run function kyoto:deco/garden_tree
execute if score #ok ky.var matches 1 run return 1
execute store result score #ok ky.var run function kyoto:gen/gtry_5x5 with storage kyoto:tmp garden
execute if score #ok ky.var matches 1 positioned ^ ^ ^3 run function kyoto:deco/garden_tree
execute if score #ok ky.var matches 1 run return 1
execute store result score #ok ky.var run function kyoto:gen/gtry_5x4 with storage kyoto:tmp garden
execute if score #ok ky.var matches 1 positioned ^ ^ ^3 run function kyoto:deco/garden_tree
execute if score #ok ky.var matches 1 run return 1
execute store result score #ok ky.var run function kyoto:gen/gtry_3x3 with storage kyoto:tmp garden
execute if score #ok ky.var matches 1 run return 1
return 0
