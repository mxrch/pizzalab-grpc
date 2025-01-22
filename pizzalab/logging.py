import logging
from rich.logging import RichHandler


LOG = logging.getLogger("pizzalab")

# LOG.handlers = [h for h in LOG.handlers if not isinstance(h, logging.StreamHandler)] # Remove default console handler

handler = RichHandler(highlighter=False, markup=True)
handler.setFormatter(logging.Formatter('%(message)s'))
LOG.addHandler(handler)

LOG.level = logging.DEBUG