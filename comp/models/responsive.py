from typed import model

@model
class Desktop:
    pass

Desktop.__display__ = "Desktop"

@model
class Tablet:
    pass

Tablet.__display__ = "Tablet"

@model
class Phone:
    pass

Phone.__display__ = "Phone"
