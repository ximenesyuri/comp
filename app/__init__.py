from typed import Str
from app.main import *

@component
def my_component(aa: Str) -> JinjaStr:
    return """jinja
        <div> {{aa}} </div>
    """

jinja_str = """jinja
        <div> {{aa}} </div>
    """
