
class: center, middle

# Being lazy when testing many classes.

---

# Agenda

1. Widgetastic
2. The work hard solution
3. The lazy solution
4. Typing

---

# What is widgetastic.

```python
from widgetastic_patternfly import View, Button, Kebab, Text

def test_some_page(browser):
    class TestView(View):
        any_button = Button()  # will pick up first button...
        button1 = Button('Default Normal')
        button2 = Button(title='Destructive title')
        kebab_menu = Kebab(id="dropdownKebab")
        kebab_output = Text(locator='//*[@id="kebab_display"]')

    view = TestView(browser)

    view.any_button.click()
    # check for display
    assert view.kebab_menu.is_displayed

    # check dropdown open/close methods
    assert not view.kebab_menu.is_opened
    view.kebab_menu.open()
```

---
# There was a nasty problem with DEBUG enabled.
The stringification of one of the widgets during logging.
```
--- Logging error ---
Traceback (most recent call last):
  File "/usr/lib64/python3.7/logging/__init__.py", line 1025, in emit
    msg = self.format(record)
  File "/usr/lib64/python3.7/logging/__init__.py", line 869, in format
    return fmt.format(record)
  File "/usr/lib64/python3.7/logging/__init__.py", line 608, in format
    record.message = record.getMessage()
  File "/usr/lib64/python3.7/logging/__init__.py", line 369, in getMessage
    msg = msg % self.args
  File "/home/jhenner/work/miq/http_503_everywhere/.cfme_venv3/lib64/python3.7/site-packages/widgetastic/widget/base.py", line 67, in wrapped
    return method(self, *new_args, **new_kwargs)
  File "/home/jhenner/work/widgetastic.patternfly/src/widgetastic_patternfly/__init__.py", line 348, in __repr__
    return '{}({!r})'.format(type(self).__name__, self.locator)
AttributeError: 'SettingsNavDropdown' object has no attribute 'locator'
Call stack:
  File "/home/jhenner/work/miq/http_503_everywhere/.cfme_venv3/bin/py.test", line 8, in <module>
    sys.exit(main())
  File "/home/jhenner/work/miq/http_503_everywhere/.cfme_venv3/lib64/python3.7/site-packages/_pytest/config/__init__.py", line 125, in main
    config=config
...
  File "/home/jhenner/work/miq/http_503_everywhere/.cfme_venv3/lib64/python3.7/site-packages/widgetastic/browser.py", line 438, in is_displayed
    return self.move_to_element(locator, *args, **kwargs).is_displayed()
  File "/home/jhenner/work/miq/http_503_everywhere/.cfme_venv3/lib64/python3.7/site-packages/widgetastic/utils.py", line 679, in wrap
    return method(*args, **kwargs)
  File "/home/jhenner/work/miq/http_503_everywhere/.cfme_venv3/lib64/python3.7/site-packages/widgetastic/browser.py", line 456, in move_to_element
    self.logger.debug('move_to_element: %r', locator)
Unable to print the message and arguments - possible formatting error.
Use the traceback above to help find the error.
```
Ok.. fire up the Python shell...
--
```python
class MyView(View):
     the_widget = widgetastic_patternfly.NavDropdown()

str(MyView().the_widget)     
```

---
# What if I need to test the stringification of the Widgets?

```python
class MyWidget:
    def __str__(self):
        return f"This is widget with locator {self.locator}"
    ...
```
--
... when there is 40 of them and they cannot be just instantiated?


---

# The "work hard" solution

```python
from widgetastic_patternfly import View, Button, Kebab, Text, ...

def test_str(browser):
    class TestView(View):
        any_button = Button()  # will pick up first button...
        button1 = Button('Default Normal')
        button2 = Button(title='Destructive title')
        button3 = Button(title='noText', classes=[Button.PRIMARY])
        kebab = Kebab(...)
        kebab2 = Kebab(id="")
        ...

    view = TestView(browser)


    for widget in view.any_button, view.button1, view.button2, view.button3, ...:
        assert type(str(widget)) is str
```
---

# There must be better way...
   
```python
from widgetastic_patternfly import View
class X(View):
    a = 1
```
has the same effect as
```pyhon
X = type('X', (View), dict(a=1))
```
https://docs.python.org/3/library/functions.html#type

---
```python
import widgetastic_patternfly as wp
from widgetastic.widget import View, Widget
from widgetastic.utils import attributize_string
import inspect

DUMMY_NAME = "name_of_the_dummy"
DUMMY_ID = "id_of_the_dummy"
DUMMY_LOCATOR = "/dummy"

collected_widgets = {
    name: t for name, t in inspect.getmembers(wp)
    if (inspect.isclass(t) and issubclass(t, Widget))
}

init_values = {
    wp.AggregateStatusCard: dict(name=DUMMY_NAME),
    wp.AggregateStatusMiniCard: dict(name=DUMMY_NAME, locator=DUMMY_LOCATOR),
    ...
}

# Instantiate objects to be set in the view with required params for __init__.
attributes = {f'{attributize_string(name)}': cls(**init_values.get(cls, {}))
              for name, cls in collected_widgets.items()}

view_class = type('TheTestView', (View,), attributes)
```
---
# Types annotations

 * Python now supports annotation the types of identifiers.
 * Dynamic typing leads to problems:

```python
def foo(a, b):
    a += b
    return a

>>> foo([], "sdaf")
['s', 'd', 'a', 'f']
```
   
  * Compare with

```python
from typing import List

def foo(a: List[str], b: List[str]) -> List[str]:
    a += b
    return a

foo([], "")
```
    
    ```
    MyPy: error: Argument 2 to "foo" has incompatible type "str"; expected "List[str]"
    ```
    
---
# Pycharm and types inference

---
# 

---
# pyi files

---
