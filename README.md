# LEFT, a Minimalist Flet Framework

I have enjoyed creating a number of apps using the flet library, so I decided to organize my common boilerplate 
code into this small framework.

I have deliberately kept things extremely simple, leaving it free for the end user to leverage whatever kind of data/service
layer they see fit. The example uses tinydb, although it is set up to be fairly agnostic and could be quickly re-worked 
to another database engine. There is some React-influenced state management in the example view implementation, 
but once again it's up to the end user to freely organise the presentation layer as required.

See sampleapp/ for a simple CRUD-app example

dev usage:
~~~
pip install -r requirements.txt
python setup.py develop
python -m sampleapp
~~~