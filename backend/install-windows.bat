@echo off
echo ======================================
echo Installing XLIFF Editor Backend
echo Windows-compatible installation
echo ======================================
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install packages one by one
echo Installing FastAPI...
pip install fastapi
echo.

echo Installing Uvicorn...
pip install uvicorn
echo.

echo Installing python-multipart...
pip install python-multipart
echo.

echo Installing lxml...
pip install lxml
echo.

echo Installing Pydantic...
pip install pydantic
echo.

echo Installing python-dotenv...
pip install python-dotenv
echo.

echo ======================================
echo Installation complete!
echo ======================================
echo.
echo You can now run: python main.py
echo.
pause