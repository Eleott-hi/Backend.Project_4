
from opyoid import Injector, Module
from routers.ClientRouter import ClientRouter
from services.Interfaces.IClientService import IClientService
from services.Implementations.ClientService import ClientService
from repositories.Interfaces.IClientRepository import IClientRepository
from repositories.Implementations.ClientRepository import ClientRepository

from routers.ProductRouter import ProductRouter
from services.Interfaces.IProductService import IProductService
from services.Implementations.ProductService import ProductService
from repositories.Interfaces.IProductRepository import IProductRepository
from repositories.Implementations.ProductRepository import ProductRepository

from routers.SupplierRouter import SupplierRouter
from services.Interfaces.ISupplierService import ISupplierService
from services.Implementations.SupplierService import SupplierService
from repositories.Interfaces.ISupplierRepository import ISupplierRepository
from repositories.Implementations.SupplierRepository import SupplierRepository

from routers.ImageRouter import ImageRouter
from services.Interfaces.IImageService import IImageService
from services.Implementations.ImageService import ImageService
from repositories.Interfaces.IImageRepository import IImageRepository
from repositories.Implementations.ImageRepository import ImageRepository


class InjectionModule(Module):
    def configure(self):
        self.bind(IClientRepository, to_class=ClientRepository)
        self.bind(IProductRepository, to_class=ProductRepository)
        self.bind(ISupplierRepository, to_class=SupplierRepository)
        self.bind(IImageRepository, to_class=ImageRepository)
  
        self.bind(IClientService, to_class=ClientService)
        self.bind(IProductService, to_class=ProductService)
        self.bind(ISupplierService, to_class=SupplierService)
        self.bind(IImageService, to_class=ImageService)

        self.bind(ClientRouter)
        self.bind(ProductRouter)
        self.bind(SupplierRouter)
        self.bind(ImageRouter)

injector = Injector([InjectionModule()])
