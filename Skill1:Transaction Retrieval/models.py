from typing import Any, Optional
from pydantic import BaseModel, Field


class TransactionRetrievalInput(BaseModel):
    cod_interaccion: str
    include_similar: bool = False
    similar_top_n: int = 10


class BaseTransaction(BaseModel):
    fec_corte: Optional[str] = None
    cod_interaccion: str
    cod_cliente: Optional[str] = None
    cod_producto: Optional[str] = None
    cod_moneda: Optional[str] = None
    cod_canal: Optional[str] = None
    cod_pais: Optional[str] = None
    cod_comercio: Optional[str] = None
    monto_interaccion: Optional[float] = None


class InteractionContext(BaseModel):
    cod_tipo_interaccion: Optional[str] = None
    tipo_interaccion: Optional[str] = None
    subtipo_interaccion: Optional[str] = None
    categoria_interaccion: Optional[str] = None
    subcategoria_interaccion: Optional[str] = None


class CurrencyContext(BaseModel):
    cod_moneda: Optional[str] = None
    descripcion_moneda: Optional[str] = None


class ChannelContext(BaseModel):
    cod_canal: Optional[str] = None
    canal: Optional[str] = None
    categoria_canal: Optional[str] = None
    subcategoria_canal: Optional[str] = None


class CountryContext(BaseModel):
    cod_pais: Optional[str] = None
    pais: Optional[str] = None
    region: Optional[str] = None
    continente: Optional[str] = None


class ProductContext(BaseModel):
    fec_apertura: Optional[str] = None
    fec_vencimiento: Optional[str] = None
    monto_inicial: Optional[float] = None
    cuota_mensual: Optional[float] = None
    tasa_inicial: Optional[float] = None
    tipo_tasa: Optional[str] = None
    plazo_dias: Optional[int] = None


class ProductSnapshotContext(BaseModel):
    cod_tipo_producto: Optional[str] = None
    saldo_producto: Optional[float] = None
    monto_transacciones: Optional[float] = None
    cantidad_transacciones: Optional[int] = None
    tasa_interes: Optional[float] = None


class ProductTypeContext(BaseModel):
    nom_producto: Optional[str] = None
    desc_producto: Optional[str] = None
    tipo_producto: Optional[str] = None
    tipo_producto_core: Optional[str] = None
    subtipo_producto: Optional[str] = None
    tipo_necesidad: Optional[str] = None
    producto_core_flag: Optional[int] = None
    verde_flag: Optional[int] = None


class MerchantContext(BaseModel):
    cod_comercio: Optional[str] = None
    nombre_comercio: Optional[str] = None
    descripcion_mcc: Optional[str] = None
    descripcion_mcg: Optional[str] = None
    ecommerce_flag: Optional[int] = None
    grupo_huella_flag: Optional[int] = None
    cod_estado_comercio: Optional[str] = None
    categoria_consumo: Optional[str] = None
    tipo_consumo: Optional[str] = None
    cod_mcc: Optional[int] = None
    cod_mcg: Optional[float] = None


class CustomerGeography(BaseModel):
    pais_cliente: Optional[str] = None
    provincia: Optional[str] = None
    canton: Optional[str] = None
    distrito: Optional[str] = None
    direccion_cliente: Optional[str] = None
    codigo_postal: Optional[str] = None
    latitud: Optional[str] = None
    longitud: Optional[str] = None


class TransactionRetrievalOutput(BaseModel):
    base_transaction: BaseTransaction
    interaction_context: InteractionContext
    currency_context: CurrencyContext
    channel_context: ChannelContext
    country_context: CountryContext
    product_context: ProductContext
    product_snapshot_context: ProductSnapshotContext
    product_type_context: ProductTypeContext
    merchant_context: MerchantContext
    customer_geography: CustomerGeography
    similar_transactions: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
