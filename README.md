# LEFT, a Minimalist Flet Framework

*Note to self; this is an async branch - with the intention of enabling the building apps as a front-end/Pyodide web distribution. See build-web.bat*

A very simple framework using the flet library - the bare boilerplate code I use to get some apps up and running.

I have deliberately kept things extremely simple - it doesn't attempt to hide the flet internals,
 very little enforced convention/configuration, and only a tiny reliance on some 'magic' in 
 the React-influenced state management in the view layer (even this is not mandatory).

Its up to the end user to organise their implementation in a consistent and logical manner that works for them.

See sampleapp/ for a simple CRUD-app example.

dev usage:
~~~
pip install -r requirements.txt
python setup.py develop
python -m sampleapp
~~~