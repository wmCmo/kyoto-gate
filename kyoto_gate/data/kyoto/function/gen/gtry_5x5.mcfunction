# Try a 5x5 garden. Macro args: kind, small, v, rot. Returns 1 if placed.
execute store result score #blocked ky.var run function kyoto:gen/gcheck_5x5
execute if score #blocked ky.var matches 1 run return 0
fill ^-2 ^ ^1 ^2 ^5 ^6 air replace #kyoto:garden_clear
fill ^-2 ^-2 ^1 ^2 ^-7 ^5 stone replace #kyoto:fillable
$place template kyoto:garden/5x5_$(kind)_$(v) ^-2 ^-4 ^1 $(rot)
return 1
