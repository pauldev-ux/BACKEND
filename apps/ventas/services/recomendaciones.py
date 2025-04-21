from apps.ventas.models import VentaDetalle, Venta
from django.db.models import Count
from collections import defaultdict

def obtener_productos_mas_vendidos(limit=5):
    """
    Obtiene los IDs de los productos más vendidos.
    """
    productos_vendidos = VentaDetalle.objects.values('producto_id').annotate(total_vendido=Count('producto_id')).order_by('-total_vendido')[:limit]
    return [item['producto_id'] for item in productos_vendidos]

def obtener_productos_relacionados(producto_id, limit=5):
    """
    Sugiere productos que a menudo se compran junto con un producto dado.
    """
    ventas_con_producto = VentaDetalle.objects.filter(producto_id=producto_id).values_list('venta_id', flat=True)
    otros_productos = VentaDetalle.objects.filter(venta_id__in=ventas_con_producto).exclude(producto_id=producto_id).values('producto_id').annotate(conteo=Count('producto_id')).order_by('-conteo')[:limit]
    return [item['producto_id'] for item in otros_productos]

def obtener_recomendaciones_basadas_en_carrito(carrito_actual, limit=5):
    """
    Genera recomendaciones basadas en los productos actualmente en el carrito.

    Args:
        carrito_actual (list of int): Lista de IDs de productos en el carrito.
        limit (int): Número máximo de recomendaciones a devolver.

    Returns:
        list of int: Lista de IDs de productos recomendados.
    """
    # Implementación básica: busca productos que a menudo se compran con CUALQUIERA de los productos en el carrito
    recomendaciones = defaultdict(int)
    ventas_ids = set()

    for producto_id in carrito_actual:
        ventas = VentaDetalle.objects.filter(producto_id=producto_id).values_list('venta_id', flat=True)
        ventas_ids.update(ventas)

    detalles_en_ventas = VentaDetalle.objects.filter(venta_id__in=list(ventas_ids)).exclude(producto_id__in=carrito_actual)

    for detalle in detalles_en_ventas:
        recomendaciones[detalle.producto_id] += 1

    sorted_recomendaciones = sorted(recomendaciones.items(), key=lambda item: item[1], reverse=True)[:limit]
    return [item[0] for item in sorted_recomendaciones]

def obtener_recomendaciones_personalizadas_usuario(usuario_id, limit=5):
    """
    Genera recomendaciones basadas en el historial de compras de un usuario.

    Args:
        usuario_id (int): ID del usuario.
        limit (int): Número máximo de recomendaciones a devolver.

    Returns:
        list of int: Lista de IDs de productos recomendados.
    """
    try:
        ventas_usuario = Venta.objects.filter(usuario_id=usuario_id).values_list('id', flat=True)
        productos_comprados = VentaDetalle.objects.filter(venta_id__in=ventas_usuario).values_list('producto_id', flat=True).distinct()
        # Aquí podrías implementar una lógica más sofisticada, como buscar productos similares
        # a los que el usuario ya ha comprado, o los más vendidos en general (excluyendo los ya comprados).
        productos_mas_vendidos = obtener_productos_mas_vendidos(limit=limit * 2) # Obtener más para luego filtrar
        recomendaciones = [pid for pid in productos_mas_vendidos if pid not in productos_comprados][:limit]
        return recomendaciones
    except Venta.DoesNotExist:
        return []

# Lógica para aplicar técnicas de Recomendaciones Inteligentes (Reglas de Asociación - Apriori):
# Esto requeriría una implementación más compleja y posiblemente el uso de librerías específicas.
# Podrías tener una función que analice periódicamente las transacciones históricas
# para identificar reglas como "Si se compra producto A y producto B, también se suele comprar producto C".
# Luego, podrías usar estas reglas en la función obtener_recomendaciones_basadas_en_carrito.

# Ejemplo de cómo se podría estructurar la función para aplicar reglas de asociación:
# def analizar_patrones_compra():
#     """
#     Analiza las transacciones históricas para identificar patrones de compra (reglas de asociación).
#     """
#     # ... lógica para obtener todas las transacciones y aplicar el algoritmo Apriori ...
#     # Guardar las reglas en algún lugar (ej. caché o base de datos) para su uso posterior
#     pass

# def obtener_recomendaciones_con_reglas_asociacion(carrito_actual, reglas, limit=5):
#     """
#     Genera recomendaciones basadas en el carrito actual y las reglas de asociación.
#     """
#     recomendaciones = set()
#     for regla in reglas:
#         if all(producto in carrito_actual for producto in regla['antecedentes']):
#             for consecuente in regla['consecuentes']:
#                 if consecuente not in carrito_actual:
#                     recomendaciones.add(consecuente)
#                     if len(recomendaciones) >= limit:
#                         break
#         if len(recomendaciones) >= limit:
#             break
#     return list(recomendaciones)