@echo off

color 4f

echo "Installing requirements..."

FOR /F "tokens=1" %%i IN ('type requirements.txt') DO pip install %%i

color 3f
echo "Requirements installed. Successfuly, press any key to continue..."
pause