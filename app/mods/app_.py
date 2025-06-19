from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader, ChoiceLoader

class App(FastAPI):
    def __init__(self, **kwargs):
        # Initialize the base FastAPI class
        super().__init__(**kwargs)
        self._templates = None # Initialize _templates attribute

    def include_static(self, path: str, dir: str, name: str):
        """ 
        Mounts a StaticFiles instance to the application.

        Args:
            path: The URL path where the static files will be served.
            dir: The directory containing the static files.
            name: The name for the static files mount.
        """
        self.mount(path, StaticFiles(directory=dir), name=name)

    def include_templates(self, dir: list[str]):
        """
        Sets up Jinja2Templates with the specified directories.

        Args:
            dir: A list of directories to load templates from.
        """
        # Create a list of FileSystemLoader instances from the provided directories
        loaders = [FileSystemLoader(d) for d in dir]
        # Set up Jinja2Templates with a ChoiceLoader containing the FileSystemLoaders
        self._templates = Jinja2Templates(directory=dir[0])  # Initialize with the first directory
        self._templates.env.loader = ChoiceLoader(loaders) # Set the ChoiceLoader

    @property
    def templates(self) -> Jinja2Templates:
        """
        Provides access to the configured Jinja2Templates instance.
        Ensures templates are initialized before access.
        """
        if self._templates is None:
            raise RuntimeError("Templates are not initialized. Call include_templates() first.")
        return self._templates

# Example Usage (assuming you have defined your routers and directory paths)

# from fastapi import APIRouter
#
# core_router = APIRouter()
# api_router = APIRouter()
# ui_router = APIRouter()
#
# STATIC_DIR = "./static"
# MOCK_DIR = "./mock"
# BUILDER_STATIC_DIR = "./static-builder"
# TEMPLATES_DIR = "./templates"
# CATALOG_DIR = "./catalog"
# BUILDER_TEMPLATES_DIR = "./builder_templates"
# CATALOG_BUILDER_DIR = "./catalog_builder"
#
# # using app
# vor = APP(redirect_slashes=False) # Pass FastAPI arguments here
# vor.include_router(core_router)
# vor.include_router(api_router, prefix='/api')
# vor.include_router(ui_router)
#
# vor.include_static(path="/static", dir=STATIC_DIR, name="static")
# vor.include_static(path="/mock", dir=MOCK_DIR, name="mock")
# vor.include_static(path="/static-builder", dir=BUILDER_STATIC_DIR, name="builder")
#
# vor.include_templates(dir=[TEMPLATES_DIR, CATALOG_DIR, BUILDER_TEMPLATES_DIR, CATALOG_BUILDER_DIR])
#
# # You can now access the templates via vor.templates
# # For example:
# # @vor.get("/")
# # async def read_root(request: Request):
# #     return vor.templates.TemplateResponse("index.html", {"request": request})
