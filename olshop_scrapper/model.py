from dataclasses import dataclass, fields, asdict

@dataclass
class ProductModel:
    def to_dict(self):
        return asdict(self)

@dataclass
class TokopediaProductModel(ProductModel):
    url: str = None
    image_url: str = None
    name: str = None
    place: str = None
    seller: str = None
    current_price: float = None
    previous_price: float = None
    rating: float = None
    sold: int = None
    trait: str = None


if __name__ == "__main__":
    product = TokopediaProductModel()
    product.to_csv()