from __future__ import annotations

from typing import Any, Optional

from .models import (
    BaseTransaction,
    ChannelContext,
    CountryContext,
    CurrencyContext,
    CustomerGeography,
    InteractionContext,
    MerchantContext,
    ProductContext,
    ProductSnapshotContext,
    ProductTypeContext,
    TransactionRetrievalOutput,
)
from .queries import (
    GET_SIMILAR_TRANSACTIONS_QUERY,
    GET_TRANSACTION_BY_ID_QUERY,
    GET_TRANSACTIONS_BY_CUSTOMER_QUERY,
)


def execute_query(query: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Placeholder de acceso a base de datos.
    Reemplazar por la implementación real con pyodbc, sqlalchemy o el cliente que usen en Fabric.
    """
    raise NotImplementedError("Implementar conexión real a la base de datos.")


def validate_transaction_scope(row: dict[str, Any]) -> tuple[bool, list[str]]:
    warnings: list[str] = []

    cod_interaccion = (row.get("COD_INTERACCION") or "").strip()
    fec_corte = row.get("FEC_CORTE")

    if "TC_" not in cod_interaccion:
        warnings.append("La transacción no pertenece al alcance de tarjeta de crédito.")

    if fec_corte is None:
        warnings.append("La transacción no tiene FEC_CORTE.")
    else:
        fec_corte_str = str(fec_corte)
        if fec_corte_str < "2025-12-01":
            warnings.append("La transacción está fuera de la ventana temporal definida.")

    return len(warnings) == 0, warnings


def build_warnings(row: dict[str, Any]) -> list[str]:
    warnings: list[str] = []

    if not row.get("NOMBRE_COMERCIO"):
        warnings.append("No se encontró contexto de comercio.")

    if not row.get("COD_TIPO_PRODUCTO"):
        warnings.append("No se encontró snapshot de producto.")

    if not row.get("TIPO_PRODUCTO"):
        warnings.append("No se encontró contexto de tipo de producto.")

    if not row.get("PAIS_CLIENTE"):
        warnings.append("No se encontró geografía del cliente.")

    if not row.get("COD_CANAL"):
        warnings.append("No se encontró canal de la transacción.")

    if not row.get("COD_PAIS"):
        warnings.append("No se encontró país de la transacción.")

    return warnings


def build_output_payload(
    row: dict[str, Any],
    similar_transactions: Optional[list[dict[str, Any]]] = None,
) -> TransactionRetrievalOutput:
    return TransactionRetrievalOutput(
        base_transaction=BaseTransaction(
            fec_corte=str(row.get("FEC_CORTE")) if row.get("FEC_CORTE") is not None else None,
            cod_interaccion=row.get("COD_INTERACCION"),
            cod_cliente=row.get("COD_CLIENTE"),
            cod_producto=row.get("COD_PRODUCTO"),
            cod_moneda=row.get("COD_MONEDA"),
            cod_canal=row.get("COD_CANAL"),
            cod_pais=row.get("COD_PAIS"),
            cod_comercio=row.get("COD_COMERCIO"),
            monto_interaccion=row.get("MONTO_INTERACCION"),
        ),
        interaction_context=InteractionContext(
            cod_tipo_interaccion=row.get("COD_TIPO_INTERACCION"),
            tipo_interaccion=row.get("TIPO_INTERACCION"),
            subtipo_interaccion=row.get("SUBTIPO_INTERACCION"),
            categoria_interaccion=row.get("CATEGORIA_INTERACCION"),
            subcategoria_interaccion=row.get("SUBCATEGORIA_INTERACCION"),
        ),
        currency_context=CurrencyContext(
            cod_moneda=row.get("COD_MONEDA"),
            descripcion_moneda=row.get("DESCRIPCION_MONEDA"),
        ),
        channel_context=ChannelContext(
            cod_canal=row.get("COD_CANAL"),
            canal=row.get("CANAL"),
            categoria_canal=row.get("CATEGORIA_CANAL"),
            subcategoria_canal=row.get("SUBCATEGORIA_CANAL"),
        ),
        country_context=CountryContext(
            cod_pais=row.get("COD_PAIS"),
            pais=row.get("PAIS"),
            region=row.get("REGION"),
            continente=row.get("CONTINENTE"),
        ),
        product_context=ProductContext(
            fec_apertura=str(row.get("FEC_APERTURA")) if row.get("FEC_APERTURA") is not None else None,
            fec_vencimiento=str(row.get("FEC_VENCIMIENTO")) if row.get("FEC_VENCIMIENTO") is not None else None,
            monto_inicial=row.get("MONTO_INICIAL"),
            cuota_mensual=row.get("CUOTA_MENSUAL"),
            tasa_inicial=row.get("TASA_INICIAL"),
            tipo_tasa=row.get("TIPO_TASA"),
            plazo_dias=row.get("PLAZO_DIAS"),
        ),
        product_snapshot_context=ProductSnapshotContext(
            cod_tipo_producto=row.get("COD_TIPO_PRODUCTO"),
            saldo_producto=row.get("SALDO_PRODUCTO"),
            monto_transacciones=row.get("MONTO_TRANSACCIONES"),
            cantidad_transacciones=row.get("CANTIDAD_TRANSACCIONES"),
            tasa_interes=row.get("TASA_INTERES"),
        ),
        product_type_context=ProductTypeContext(
            nom_producto=row.get("NOM_PRODUCTO"),
            desc_producto=row.get("DESC_PRODUCTO"),
            tipo_producto=row.get("TIPO_PRODUCTO"),
            tipo_producto_core=row.get("TIPO_PRODUCTO_CORE"),
            subtipo_producto=row.get("SUBTIPO_PRODUCTO"),
            tipo_necesidad=row.get("TIPO_NECESIDAD"),
            producto_core_flag=row.get("PRODUCTO_CORE_FLAG"),
            verde_flag=row.get("VERDE_FLAG"),
        ),
        merchant_context=MerchantContext(
            cod_comercio=row.get("COD_COMERCIO"),
            nombre_comercio=row.get("NOMBRE_COMERCIO"),
            descripcion_mcc=row.get("DESCRIPCION_MCC"),
            descripcion_mcg=row.get("DESCRIPCION_MCG"),
            ecommerce_flag=row.get("ECOMMERCE_FLAG"),
            grupo_huella_flag=row.get("GRUPO_HUELLA_FLAG"),
            cod_estado_comercio=row.get("COD_ESTADO_COMERCIO"),
            categoria_consumo=row.get("CATEGORIA_CONSUMO"),
            tipo_consumo=row.get("TIPO_CONSUMO"),
            cod_mcc=row.get("COD_MCC"),
            cod_mcg=row.get("COD_MCG"),
        ),
        customer_geography=CustomerGeography(
            pais_cliente=row.get("PAIS_CLIENTE"),
            provincia=row.get("PROVINCIA"),
            canton=row.get("CANTON"),
            distrito=row.get("DISTRITO"),
            direccion_cliente=row.get("DIRECCION_CLIENTE"),
            codigo_postal=row.get("CODIGO_POSTAL"),
            latitud=row.get("LATITUD"),
            longitud=row.get("LONGITUD"),
        ),
        similar_transactions=similar_transactions or [],
        warnings=[],
    )


def get_transaction_by_id(cod_interaccion: str) -> dict[str, Any]:
    rows = execute_query(
        GET_TRANSACTION_BY_ID_QUERY,
        {"cod_interaccion": cod_interaccion},
    )

    if not rows:
        return {"warnings": ["No se encontró la transacción."]}

    if len(rows) > 1:
        return {"warnings": ["Se encontró más de un registro para la misma transacción."]}

    row = rows[0]
    _, scope_warnings = validate_transaction_scope(row)
    context_warnings = build_warnings(row)

    payload = build_output_payload(row)
    payload.warnings.extend(scope_warnings)
    payload.warnings.extend(context_warnings)

    return payload.model_dump()


def get_transactions_by_customer(
    cod_cliente: str,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    top_n: int = 50,
) -> list[dict[str, Any]]:
    rows = execute_query(
        GET_TRANSACTIONS_BY_CUSTOMER_QUERY,
        {
            "cod_cliente": cod_cliente,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        },
    )

    return rows[:top_n]


def get_similar_transactions(
    cod_cliente: str,
    cod_tipo_interaccion: Optional[str] = None,
    fec_corte: Optional[str] = None,
    monto_interaccion: Optional[float] = None,
    top_n: int = 10,
) -> list[dict[str, Any]]:
    fecha_inicio = None
    fecha_fin = fec_corte

    rows = execute_query(
        GET_SIMILAR_TRANSACTIONS_QUERY,
        {
            "cod_cliente": cod_cliente,
            "cod_tipo_interaccion": cod_tipo_interaccion,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "monto_interaccion": monto_interaccion,
        },
    )

    return rows[:top_n]
