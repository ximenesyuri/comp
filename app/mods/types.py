from typed import Str, TypedFuncType
from app.helper.meta import __JinjaStr, __Component

JinjaStr  = __JinjaStr('JinjaStr', (Str,), {})
Component = __Component('Component', (TypedFuncType,), {})

JinjaStr.__display__  = "JinjaStr"
Component.__display__ = "Component"
