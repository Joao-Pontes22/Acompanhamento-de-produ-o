# app/models/__init__.py

# importa a Base central
from app.models.Models import base

# importa todos os models
from app.models.Assembly_production import AssemblyProduction
from app.models.Clients import Clients
from app.models.ComponentsAndParts import ComponentsAndParts
from app.models.Employers import Employers
from app.models.Machines import Machines
from app.models.Machining_production import MachiningProduction
from app.models.Movimentations import movimentations
from app.models.Relation import Relation
from app.models.Scraps import Scraps
from app.models.Sectors import Sectors
from app.models.Stock import Stock
from app.models.Suppliers import Suppliers

# agora todos os modelos estão carregados e registrados no Base.metadata
