# Try a 5x4 garden. Macro args: kind, small, v, rot. Returns 1 if placed.
execute store result score #blocked ky.var run function kyoto:gen/gcheck_5x4
execute if score #blocked ky.var matches 1 run return 0
fill ^-2 ^ ^1 ^2 ^5 ^5 air replace #kyoto:garden_clear
fill ^-2 ^-2 ^1 ^2 ^-7 ^4 stone replace #kyoto:fillable
$place template kyoto:garden/5x4_$(kind)_$(v) ^-2 ^-4 ^1 $(rot)
return 1
