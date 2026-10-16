# As a plot: pick a garden style and fit the largest size that goes (7x6 down to 3x3)
execute store result score #r ky.var run random value 1..100
data modify storage kyoto:tmp garden.kind set value "kare"
execute if score #r ky.var matches 41..75 run data modify storage kyoto:tmp garden.kind set value "moss"
execute if score #r ky.var matches 76..100 run data modify storage kyoto:tmp garden.kind set value "pond"
data modify storage kyoto:tmp garden.small set value "kare"
execute if score #r ky.var matches 51..100 run data modify storage kyoto:tmp garden.small set value "moss"
execute store result storage kyoto:tmp garden.v int 1 run random value 0..2
function kyoto:util/rot
data modify storage kyoto:tmp garden.rot set from storage kyoto:tmp rot
function kyoto:gen/garden
