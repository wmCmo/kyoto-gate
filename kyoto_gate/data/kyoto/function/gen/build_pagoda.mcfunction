# Builds the pagoda. Macro arg: rot
fill ^-5 ^ ^ ^5 ^36 ^10 air replace #kyoto:diggable
fill ^-4 ^-2 ^1 ^4 ^-10 ^9 stone_bricks replace #kyoto:fillable
$place template kyoto:pagoda ^-5 ^-1 ^ $(rot)
summon marker ^ ^ ^5 {Tags:["ky.house"]}
summon marker ^ ^ ^5 {Tags:["ky.offering"]}
