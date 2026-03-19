# Skill: `transaction-retrieval`

## 1. Propósito

`transaction-retrieval` es el skill encargado de recuperar y estructurar el contexto de una transacción de tarjeta de crédito a partir de datos transaccionales y dimensiones de negocio en Fabric.

Su función es servir como capa de recuperación para las siguientes capacidades del agente:

* normalización transaccional
* clasificación de transacciones
* resolución de comercio
* explicación de consumo
* análisis de contexto del producto
* análisis geográfico del cliente

Este skill no toma decisiones finales de clasificación ni detecta anomalías por sí solo. Su responsabilidad es **traer evidencia estructurada y consistente**.

---

## 2. Alcance funcional

### Incluye

* recuperación de transacciones de tarjeta de crédito
* enriquecimiento con dimensiones de interacción, moneda, canal, país, producto, tipo de producto, comercio y geografía del cliente
* recuperación de snapshot del producto desde `FctProductos`
* salida estructurada para consumo por otras skills o por el agente principal

### No incluye

* clasificación final del movimiento
* detección de fraude
* scoring de anomalías
* inferencia libre sobre estados no modelados
* uso de `COD_INFO_INTERACCION` como fuente principal
* uso de `DimEstado` en esta primera versión

---

## 3. Regla de identificación del dominio

Una interacción pertenece al alcance de este skill si cumple:

```sql
f.COD_INTERACCION LIKE '%TC_%'
```

Y para la ventana inicial definida:

```sql
f.FEC_CORTE >= '2025-12-01'
```

---

## 4. Fuente principal

### Tabla principal

* `gold.FctInteraccionesBeta`

### Llave única

* `COD_INTERACCION`

---

## 5. Fuentes y relaciones

## 5.1 Tabla principal: `FctInteraccionesBeta`

Campos utilizados:

* `FEC_CORTE`
* `COD_INTERACCION`
* `COD_TIPO_INTERACCION`
* `COD_CLIENTE`
* `COD_PRODUCTO`
* `COD_MONEDA`
* `COD_CANAL`
* `COD_PAIS`
* `COD_COMERCIO`
* `MONTO_INTERACCION`

## 5.2 Dimensiones y tablas relacionadas

### `DimTipoInteraccion`

Relación:

```sql
f.COD_TIPO_INTERACCION = dti.COD_TIPO_INTERACCION
```

Campos útiles:

* `TIPO_INTERACCION`
* `SUBTIPO_INTERACCION`
* `CATEGORIA_INTERACCION`
* `SUBCATEGORIA_INTERACCION`

### `DimMoneda`

Relación:

```sql
f.COD_MONEDA = dm.COD_MONEDA
```

Campos útiles:

* `DESCRIPCION_MONEDA`

### `DimCanal`

Relación:

```sql
f.COD_CANAL = dc.COD_CANAL
```

Campos útiles:

* `CANAL`
* `CATEGORIA_CANAL`
* `SUBCATEGORIA_CANAL`

### `DimPais`

Relación:

```sql
f.COD_PAIS = dp.COD_PAIS
```

Campos útiles:

* `PAIS`
* `REGION`
* `CONTINENTE`

### `DimProducto`

Relación:

```sql
f.COD_PRODUCTO = dpr.COD_PRODUCTO
```

Campos útiles:

* `FEC_APERTURA`
* `FEC_VENCIMIENTO`
* `MONTO_INICIAL`
* `CUOTA_MENSUAL`
* `TASA_INICIAL`
* `TIPO_TASA`
* `PLAZO_DIAS`

### `FctProductos`

Relación confirmada:

```sql
f.COD_PRODUCTO = fp.COD_PRODUCTO
AND f.COD_CLIENTE = fp.COD_CLIENTE
AND f.FEC_CORTE = fp.FEC_CORTE
```

Campos útiles:

* `COD_TIPO_PRODUCTO`
* `SALDO_PRODUCTO`
* `MONTO_TRANSACCIONES`
* `CANTIDAD_TRANSACCIONES`
* `TASA_INTERES`

### `DimTipoProducto`

Relación:

```sql
fp.COD_TIPO_PRODUCTO = dtp.COD_TIPO_PRODUCTO
```

Campos útiles:

* `NOM_PRODUCTO`
* `DESC_PRODUCTO`
* `TIPO_PRODUCTO`
* `TIPO_PRODUCTO_CORE`
* `SUBTIPO_PRODUCTO`
* `TIPO_NECESIDAD`
* `PRODUCTO_CORE_FLAG`
* `VERDE_FLAG`

### `DimComercio`

Relación:

```sql
f.COD_COMERCIO = dco.COD_COMERCIO
```

Campos útiles:

* `NOMBRE_COMERCIO`
* `DESCRIPCION_MCC`
* `DESCRIPCION_MCG`
* `ECOMMERCE_FLAG`
* `GRUPO_HUELLA_FLAG`
* `COD_ESTADO`
* `CATEGORIA_CONSUMO`
* `TIPO_CONSUMO`
* `COD_MCC`
* `COD_MCG`

### `DimGeografico`

Relación:

```sql
f.COD_CLIENTE = dg.COD_CLIENTE
```

Campos útiles:

* `PAIS`
* `PROVINCIA`
* `CANTON`
* `DISTRITO`
* `DIRECCION_CLIENTE`
* `CODIGO_POSTAL`
* `LATITUD`
* `LONGITUD`

---

## 6. Campos ignorados en esta versión

### `COD_INFO_INTERACCION`

Se omite porque fue definido como información adicional que no calza en una categoría estructural relevante para esta primera versión.

### `DimEstado`

Se omite por ahora.

---

## 7. Query base del skill

```sql
SELECT
    f.FEC_CORTE,
    f.COD_INTERACCION,
    f.COD_TIPO_INTERACCION,
    f.COD_CLIENTE,
    f.COD_PRODUCTO,
    f.COD_MONEDA,
    f.COD_CANAL,
    f.COD_PAIS,
    f.COD_COMERCIO,
    f.MONTO_INTERACCION,

    dti.TIPO_INTERACCION,
    dti.SUBTIPO_INTERACCION,
    dti.CATEGORIA_INTERACCION,
    dti.SUBCATEGORIA_INTERACCION,

    dm.DESCRIPCION_MONEDA,

    dc.CANAL,
    dc.CATEGORIA_CANAL,
    dc.SUBCATEGORIA_CANAL,

    dp.PAIS,
    dp.REGION,
    dp.CONTINENTE,

    dpr.FEC_APERTURA,
    dpr.FEC_VENCIMIENTO,
    dpr.MONTO_INICIAL,
    dpr.CUOTA_MENSUAL,
    dpr.TASA_INICIAL,
    dpr.TIPO_TASA,
    dpr.PLAZO_DIAS,

    fp.COD_TIPO_PRODUCTO,
    fp.SALDO_PRODUCTO,
    fp.MONTO_TRANSACCIONES,
    fp.CANTIDAD_TRANSACCIONES,
    fp.TASA_INTERES,

    dtp.NOM_PRODUCTO,
    dtp.DESC_PRODUCTO,
    dtp.TIPO_PRODUCTO,
    dtp.TIPO_PRODUCTO_CORE,
    dtp.SUBTIPO_PRODUCTO,
    dtp.TIPO_NECESIDAD,
    dtp.PRODUCTO_CORE_FLAG,
    dtp.VERDE_FLAG,

    dco.NOMBRE_COMERCIO,
    dco.DESCRIPCION_MCC,
    dco.DESCRIPCION_MCG,
    dco.ECOMMERCE_FLAG,
    dco.GRUPO_HUELLA_FLAG,
    dco.COD_ESTADO AS COD_ESTADO_COMERCIO,
    dco.CATEGORIA_CONSUMO,
    dco.TIPO_CONSUMO,
    dco.COD_MCC,
    dco.COD_MCG,

    dg.PAIS AS PAIS_CLIENTE,
    dg.PROVINCIA,
    dg.CANTON,
    dg.DISTRITO,
    dg.DIRECCION_CLIENTE,
    dg.CODIGO_POSTAL,
    dg.LATITUD,
    dg.LONGITUD

FROM gold.FctInteraccionesBeta f
LEFT JOIN gold.DimTipoInteraccion dti
    ON f.COD_TIPO_INTERACCION = dti.COD_TIPO_INTERACCION
LEFT JOIN gold.DimMoneda dm
    ON f.COD_MONEDA = dm.COD_MONEDA
LEFT JOIN gold.DimCanal dc
    ON f.COD_CANAL = dc.COD_CANAL
LEFT JOIN gold.DimPais dp
    ON f.COD_PAIS = dp.COD_PAIS
LEFT JOIN gold.DimProducto dpr
    ON f.COD_PRODUCTO = dpr.COD_PRODUCTO
LEFT JOIN gold.FctProductos fp
    ON f.COD_PRODUCTO = fp.COD_PRODUCTO
   AND f.COD_CLIENTE = fp.COD_CLIENTE
   AND f.FEC_CORTE = fp.FEC_CORTE
LEFT JOIN gold.DimTipoProducto dtp
    ON fp.COD_TIPO_PRODUCTO = dtp.COD_TIPO_PRODUCTO
LEFT JOIN gold.DimComercio dco
    ON f.COD_COMERCIO = dco.COD_COMERCIO
LEFT JOIN gold.DimGeografico dg
    ON f.COD_CLIENTE = dg.COD_CLIENTE
WHERE f.COD_INTERACCION LIKE '%TC_%'
  AND f.FEC_CORTE >= '2025-12-01'
```

---

## 8. Funciones necesarias del skill

## 8.1 `get_transaction_by_id`

### Objetivo

Recuperar una única transacción por `COD_INTERACCION` con todo su contexto dimensional.

### Entrada

* `cod_interaccion: str`

### Salida

* un objeto estructurado con toda la información recuperada

### Responsabilidad

* consultar la vista o query base
* garantizar que la llave sea única
* devolver warning si no existe registro
* devolver warning si existe más de un registro, aunque no debería ocurrir

---

## 8.2 `get_transactions_by_customer`

### Objetivo

Recuperar transacciones de TC de un cliente dentro de una ventana temporal.

### Entrada

* `cod_cliente: str`
* `fecha_inicio: date | None`
* `fecha_fin: date | None`
* `top_n: int`

### Salida

* lista de transacciones enriquecidas

### Responsabilidad

* limitar por cliente
* limitar por fechas si se envían
* ordenar de más reciente a más antigua

---

## 8.3 `get_similar_transactions`

### Objetivo

Recuperar transacciones parecidas para contexto comparativo.

### Estrategia mínima sugerida

Parecido por:

* mismo cliente
* mismo tipo de interacción o categoría
* ventana temporal cercana
* monto similar opcional

### Entrada

* `cod_cliente: str`
* `cod_tipo_interaccion: str | None`
* `fec_corte: date | None`
* `monto_interaccion: float | None`
* `top_n: int`

### Salida

* lista de transacciones similares

---

## 8.4 `build_output_payload`

### Objetivo

Transformar el resultado plano de SQL en una estructura limpia por secciones.

### Responsabilidad

Agrupar en:

* `base_transaction`
* `interaction_context`
* `currency_context`
* `channel_context`
* `country_context`
* `product_context`
* `product_snapshot_context`
* `product_type_context`
* `merchant_context`
* `customer_geography`
* `warnings`

---

## 8.5 `validate_transaction_scope`

### Objetivo

Validar que la transacción recuperada pertenece al alcance del skill.

### Reglas mínimas

* `COD_INTERACCION` debe contener `TC_`
* `FEC_CORTE` debe ser mayor o igual a `2025-12-01`

### Salida

* `True/False`
* warnings aplicables

---

## 8.6 `build_warnings`

### Objetivo

Registrar faltantes o inconsistencias de contexto.

### Casos típicos

* no existe comercio
* no existe tipo de producto
* no existe geografía del cliente
* `COD_CANAL` vacío
* `COD_PAIS` vacío
* transacción fuera de alcance

---

## 9. Contrato de entrada y salida

## 9.1 Input mínimo

```json
{
  "cod_interaccion": "TC_3569461381_74389215273273512660476"
}
```

## 9.2 Input ampliado

```json
{
  "cod_interaccion": "TC_3569461381_74389215273273512660476",
  "include_similar": true,
  "similar_top_n": 10
}
```

## 9.3 Output esperado

```json
{
  "base_transaction": {
    "fec_corte": "",
    "cod_interaccion": "",
    "cod_cliente": "",
    "cod_producto": "",
    "cod_moneda": "",
    "cod_canal": "",
    "cod_pais": "",
    "cod_comercio": "",
    "monto_interaccion": 0
  },
  "interaction_context": {
    "cod_tipo_interaccion": "",
    "tipo_interaccion": "",
    "subtipo_interaccion": "",
    "categoria_interaccion": "",
    "subcategoria_interaccion": ""
  },
  "currency_context": {
    "cod_moneda": "",
    "descripcion_moneda": ""
  },
  "channel_context": {
    "cod_canal": "",
    "canal": "",
    "categoria_canal": "",
    "subcategoria_canal": ""
  },
  "country_context": {
    "cod_pais": "",
    "pais": "",
    "region": "",
    "continente": ""
  },
  "product_context": {
    "fec_apertura": "",
    "fec_vencimiento": "",
    "monto_inicial": 0,
    "cuota_mensual": 0,
    "tasa_inicial": 0,
    "tipo_tasa": "",
    "plazo_dias": 0
  },
  "product_snapshot_context": {
    "cod_tipo_producto": "",
    "saldo_producto": 0,
    "monto_transacciones": 0,
    "cantidad_transacciones": 0,
    "tasa_interes": 0
  },
  "product_type_context": {
    "nom_producto": "",
    "desc_producto": "",
    "tipo_producto": "",
    "tipo_producto_core": "",
    "subtipo_producto": "",
    "tipo_necesidad": "",
    "producto_core_flag": 0,
    "verde_flag": 0
  },
  "merchant_context": {
    "cod_comercio": "",
    "nombre_comercio": "",
    "descripcion_mcc": "",
    "descripcion_mcg": "",
    "ecommerce_flag": 0,
    "grupo_huella_flag": 0,
    "cod_estado_comercio": "",
    "categoria_consumo": "",
    "tipo_consumo": "",
    "cod_mcc": 0,
    "cod_mcg": 0
  },
  "customer_geography": {
    "pais_cliente": "",
    "provincia": "",
    "canton": "",
    "distrito": "",
    "direccion_cliente": "",
    "codigo_postal": "",
    "latitud": "",
    "longitud": ""
  },
  "similar_transactions": [],
  "warnings": []
}
```

---

## 10. Reglas operativas del skill

* No inferir campos no recuperados desde SQL.
* No usar `COD_INFO_INTERACCION` para clasificación en esta versión.
* No usar `DimEstado` hasta que entre al modelo del skill.
* Si falta una dimensión, devolver `null` o vacío y registrar warning.
* Si una transacción no cumple el filtro de TC, devolver warning de alcance.
* Priorizar recuperación estructurada desde SQL antes de usar búsqueda semántica.

---

## 11. Funciones Python necesarias

```python
from typing import Any, Optional


def get_transaction_by_id(cod_interaccion: str) -> dict[str, Any]:
    """Recupera una transacción enriquecida por su identificador único."""


def get_transactions_by_customer(
    cod_cliente: str,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    top_n: int = 50,
) -> list[dict[str, Any]]:
    """Recupera transacciones de tarjeta de crédito de un cliente."""


def get_similar_transactions(
    cod_cliente: str,
    cod_tipo_interaccion: Optional[str] = None,
    fec_corte: Optional[str] = None,
    monto_interaccion: Optional[float] = None,
    top_n: int = 10,
) -> list[dict[str, Any]]:
    """Recupera transacciones similares para contexto comparativo."""


def validate_transaction_scope(row: dict[str, Any]) -> tuple[bool, list[str]]:
    """Valida si la transacción pertenece al alcance del skill."""


def build_warnings(row: dict[str, Any]) -> list[str]:
    """Construye warnings por faltantes o inconsistencias de contexto."""


def build_output_payload(
    row: dict[str, Any],
    similar_transactions: Optional[list[dict[str, Any]]] = None,
) -> dict[str, Any]:
    """Transforma un registro plano en el contrato estructurado del skill."""
```

---

## 12. Modelo Pydantic sugerido

```python
from typing import Optional, Any
from pydantic import BaseModel, Field


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
```

---

## 13. Versión YAML resumida del skill

```yaml
---
name: transaction-retrieval
description: |
  Recupera y estructura contexto de transacciones de tarjeta de crédito desde Fabric,
  enriqueciendo la interacción con dimensiones de negocio para su uso por otras skills.
domain: credit-card-transactions
primary_source: gold.FctInteraccionesBeta
entity_key: COD_INTERACCION
scope_rule: "COD_INTERACCION LIKE '%TC_%'"
time_filter: "FEC_CORTE >= '2025-12-01'"
inputs:
  - cod_interaccion
  - include_similar_optional
  - similar_top_n_optional
outputs:
  - base_transaction
  - interaction_context
  - currency_context
  - channel_context
  - country_context
  - product_context
  - product_snapshot_context
  - product_type_context
  - merchant_context
  - customer_geography
  - similar_transactions
  - warnings
ignored_fields:
  - COD_INFO_INTERACCION
ignored_dimensions:
  - DimEstado
---
```

---

## 14. Entregable técnico mínimo de implementación

Para considerar este skill implementado, debería existir:

1. Una vista SQL o query base equivalente.
2. Una función de recuperación por `COD_INTERACCION`.
3. Una función opcional de similares.
4. Un builder de payload estructurado.
5. Un contrato Pydantic de salida.
6. Reglas de warning básicas.

---

## 15. Siguiente extensión natural

La siguiente skill que usaría este output es:

* `transaction-normalization`

Porque esta recuperación ya entrega:

* contexto comercial
* contexto del producto
* contexto del tipo de interacción
* contexto geográfico

Y con eso ya se puede normalizar y preparar clasificación.

