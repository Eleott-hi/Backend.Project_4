from opyoid import Module, Injector

from repositories.Interfaces.IClientRepository import IClientRepository
from repositories.Implementations.ClientRepository import ClientRepository

from repositories.Interfaces.IProductRepository import IProductRepository
from repositories.Implementations.ProductRepository import ProductRepository

from repositories.Interfaces.ISupplierRepository import ISupplierRepository
from repositories.Implementations.SupplierRepository import SupplierRepository

from repositories.Interfaces.IImageRepository import IImageRepository
from repositories.Implementations.ImageRepository import ImageRepository


# class RepositoryInjector(Module):
#     def configure(self):
#         self.bind(IClientRepository, to=ClientRepository)
#         self.bind(IProductRepository, to=ProductRepository)
#         self.bind(ISupplierRepository, to=SupplierRepository)
#         self.bind(IImageRepository, to=ImageRepository)
