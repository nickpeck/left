xcopy /s /Y src sampleapp
cd sampleapp
flet build web --module-name main_web.py
python -m http.server --directory build/web