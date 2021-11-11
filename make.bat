CALL venv\Scripts\activate
pyinstaller --add-binary "chromedriver.exe;chromedriver.exe" --add-binary "./venv/Lib/site-packages/selenium/webdriver/remote/*;./selenium/webdriver/remote/" "autofiller.py"
pause