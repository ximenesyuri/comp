from typed import optional
from comp import Logo, Link, build_row

@optional
class X:
    logo: Logo
    link: Link
X.__display__ = "X"

print(build_row(X))
