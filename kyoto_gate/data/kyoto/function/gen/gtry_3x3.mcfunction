# Try a 3x3 garden. Macro args: kind, small, v, rot. Returns 1 if placed.
execute store result score #blocked ky.var run function kyoto:gen/gcheck_3x3
execute if score #blocked ky.var matches 1 run return 0
fill ^-1 ^ ^1 ^1 ^5 ^4 air replace #kyoto:garden_clear
fill ^-1 ^-2 ^1 ^1 ^-7 ^3 stone replace #kyoto:fillable
$place template kyoto:garden/3x3_$(small)_$(v) ^-1 ^-4 ^1 $(rot)
return 1
