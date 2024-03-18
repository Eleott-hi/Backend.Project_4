from opyoid import Module, Injector

from services.Interfaces.IClientService import IClientService
from services.Implementations.ClientService import ClientService

from services.Interfaces.IProductService import IProductService
from services.Implementations.ProductService import ProductService

from services.Interfaces.ISupplierService import ISupplierService
from services.Implementations.SupplierService import SupplierService

from services.Interfaces.IImageService import IImageService
from services.Implementations.ImageService import ImageService


# class ServiceInjector(Module):
#     def configure(self):
#         self.bind(IClientService, to=ClientService)
#         self.bind(IProductService, to=ProductService)
#         self.bind(ISupplierService, to=SupplierService)
#         self.bind(IImageService, to=ImageService)
