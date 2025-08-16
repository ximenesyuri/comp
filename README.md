```ruby   
  /0000000  /000000  /000000/0000   /000000 
 /00_____/ /00__  00| 00_  00_  00 /00__  00
| 00      | 00  \ 00| 00 \ 00 \ 00| 00  \ 00
| 00      | 00  | 00| 00 | 00 | 00| 00  | 00
|  0000000|  000000/| 00 | 00 | 00| 0000000/
 \_______/ \______/ |__/ |__/ |__/| 00____/ 
                                  | 00      
                                  | 00      
                                  |__/   
```
# About

`comp` is a functional style component system for Python, presenting strong type safety through an extensive use of [ximenesyuri/typed](https://github.com/ximenesyuri/typed).
    
# Overview

With `comp` you can construct _components_, which are _typed functions_ (in the sense of [ximenesyuri/typed](https://github.com/ximenesyuri/typed)) returning _jinja strings_ (i.e, strings presenting a valid [jinja](https://jinja.palletsprojects.com/en/stable/) syntax), constituting a type `COMPONENT`.

Components (i.e, instances of `COMPONENT`) have the structure determined by _models_ (in the sense of [ximenesyuri/typed](https://github.com/ximenesyuri/typed)). Furthermore, they can be composed through four _component operations_ (`join`, `concat`, `eval` and `copy`), which corresponds, respectively, to certain magic methods in `COMPONENT`. This allow us to create _derived components_ from _primitive components_ by making use of _component equations_.

After constructed, components can be _rendered_ into raw HTML strings by making use of the `render` service function. To render a component we need to pass a _context_, which is the minimum information needed to provide a sense to the component. This could include, for example, `markdown` content (which is rendered through [python-markdown](https://github.com/Python-Markdown/markdown)), `rst` content (rendered via [docutils](https://docutils.sourceforge.io/)), other components, and so on. This flexibility allows the use of `comp` in  both dynamic and static environments.

Components can also be _previewed_ by putting them into a _preview stack_.

# Install

With `pip`:
```bash
pip install git+https://github.com/ximenesyuri/comp 
```

With [py](https://github.com/ximenesyuri/py):
```bash
py i ximenesyuri/comp
```

# Documentation

See [ximenesyuri/libs/comp](https://ximenesyuri/libs/app).
