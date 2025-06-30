from typed import *
from app.main import *

@definer
def f(depends_on: Str=[]) -> Jinja:
    return "aaa"
