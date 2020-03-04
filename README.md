# Swiftly
 additional commands for a faster workflow

## Install
Just "Clone or download" -> "Download ZIP", and inside Blender "Install" from the zipfile

## Features
### GPU info
Get gpu info from nvidia-smi commandline win/linux -> 3Dview N-panel "Swiftly" -> GPU info

click "update"

getting: 
temperature.gpu, fan.speed, memory.used, memory.free

dual GPU supported (could be made better)

### Empty to location ###
Adds an Empty to current selected location, also inside editmode, this makes (my) riggin workflow much faster, as I can snap bones to these empties fast (activate Snap with Vertex)

F3 -> "Swiftly: Add Empty to current selected location" or

SHIFT + A -> (m Mesh -> ) a "Swiftly: add RiggingHelper"

A Collection will be used named "RiggingHelpers" with all the "RiggingHelper" empties inside, so the all can easily be removed afterwards

### Copy scene settings ###
Copy scene settings to other scenes

Properties -> Scene -> "Swiftly: Copy scene settings to other scenes" -> "copy CURRENT scene render/output"

every setting for cycles inside render and output-panel should copy over BUT not, as (in my eyes) scene depended :

frame start and end, frame time remapping, resolution XY and bordersetting
