rmdir /s /q "R:/Minecraft/QCraft-1.19/run/saves/%~1/datapacks/QModeStructs-1.19"
xcopy /s /y /d /I "%appdata%/.minecraft/datapacks/QModeStructs-1.19" "R:/Minecraft/QCraft-1.19/run/saves/%~1/datapacks/QModeStructs-1.19"

rmdir /s /q "R:/Minecraft/QCraft-1.19/run/saves/%~1 2/datapacks/QModeStructs-1.19"
xcopy /s /y /d /I "%appdata%/.minecraft/datapacks/QModeStructs-1.19" "R:/Minecraft/QCraft-1.19/run/saves/%~1 2/datapacks/QModeStructs-1.19"