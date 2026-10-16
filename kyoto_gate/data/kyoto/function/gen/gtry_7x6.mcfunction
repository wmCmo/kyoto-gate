# Try a 7x6 garden. Macro args: kind, small, v, rot. Returns 1 if placed.
execute store result score #blocked ky.var run function kyoto:gen/gcheck_7x6
execute if score #blocked ky.var matches 1 run return 0
fill ^-3 ^ ^1 ^3 ^5 ^7 air replace #kyoto:garden_clear
fill ^-3 ^-2 ^1 ^3 ^-7 ^6 stone replace #kyoto:fillable
$place template kyoto:garden/7x6_$(kind)_$(v) ^-3 ^-4 ^1 $(rot)
return 1
