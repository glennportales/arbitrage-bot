# arbitrage-bot
 Python Arbitrage Bot testing

A continuación se presenta la documentación del código en español (puertorriqueño). Las secciones comentadas en el código en inglés permanecerán igual, pero las explicaciones y descripciones se presentarán en español entendido por puertorriqueños.

---

### Descripción General

Este script es un bot de arbitraje que busca diferencias de precio (arbitraje) en el par de trading **SOL/USDT** entre múltiples casas de cambio (exchanges). Si el bot encuentra una oportunidad de arbitraje, lo reporta y, dependiendo del modo en que se esté ejecutando (de prueba o "paper trading" vs. modo real), simulará la operación o intentará ejecutarla en la(s) casa(s) de cambio seleccionada(s).

**Paper Trading (Modo de Prueba):**  
Cuando `paper_trade` está en `True`, el bot NO colocará órdenes reales. Simplemente imprimirá en la consola qué orden se hubiera ejecutado. Esto es ideal para probar la lógica sin arriesgar fondos reales.

**Modo Real (Live Trading):**  
Si en algún momento cambias `paper_trade` a `False` y configuras las llaves API y “secret” para las casas de cambio, el bot intentará colocar órdenes reales. ¡Hazlo con precaución y en un entorno controlado!

---

### Parámetros Importantes

- `paper_trade = True`:  
  Controla si el bot opera de forma simulada. Si está en `True`, no ejecutará órdenes reales, solo las simulará.
  
- `exchanges` (diccionario):  
  Aquí se definen las casas de cambio con las que se trabajará a través de la librería **ccxt**. Se pueden agregar más intercambios según se necesite.
  
- `symbol = "SOL/USDT"`:  
  El par de trading que se va a monitorear. Puedes cambiarlo a otro par, siempre y cuando las casas de cambio seleccionadas ofrezcan ese par.
  
- `fee_tolerance = 0.005`:  
  Porcentaje que representa la tolerancia a las comisiones. En este caso, 0.5%. Esto quiere decir que el bot busca oportunidades con ganancias mayores a 0.5% del precio de compra para que la operación valga la pena después de considerar comisiones.
  
- `sleep_interval = 10`:  
  Intervalo en segundos entre cada verificación de precios y oportunidades de arbitraje. Puedes ajustarlo a tu gusto.

---

### Funciones

1. **get_prices()**  
   Esta función obtiene los precios actuales de compra (`bid`) y venta (`ask`) para el símbolo seleccionado desde cada casa de cambio configurada en el diccionario `exchanges`.  
   - Intenta llamar a `fetch_ticker(symbol)` en cada casa de cambio.  
   - Si obtiene el `bid` y el `ask`, guarda estos valores en un diccionario `prices`.
   - Si ocurre un error (por ejemplo, si la casa de cambio no soporta el símbolo o hay un problema con la conexión), imprime el error en pantalla y pasa a la siguiente casa de cambio.

2. **find_arbitrage_opportunity(prices)**  
   Esta función toma el diccionario de precios obtenido por `get_prices()` y busca diferencias de precio que puedan dar una ganancia de arbitraje.  
   - Compara todos los pares de casas de cambio (por ejemplo, comprar en A y vender en B).
   - Calcula la ganancia potencial: `profit = precio_venta(B) - precio_compra(A)`.
   - Si la ganancia supera el `fee_tolerance` (ej. 0.5% del precio de compra), se considera una oportunidad válida.
   - Si encuentra una oportunidad, la retorna como una tupla con la información relevante. Si no, retorna `None`.

3. **execute_trade(buy_exchange_name, sell_exchange_name, buy_price, sell_price, amount)**  
   Esta función ejecuta el trade real si `paper_trade` está en `False`.  
   - Intentará crear una orden de compra en la casa de cambio `buy_exchange_name` y luego una orden de venta en `sell_exchange_name`.
   - Muestra mensajes en pantalla con la información de las órdenes.
   - En caso de error, muestra el error en pantalla.  
   
   **Nota:** En el modo `paper_trade = True`, esta función no se llama, ya que las operaciones se simulan y no se colocan órdenes reales.

---

### Flujo del Programa (main)

La función `main()` ejecuta un ciclo infinito (`while True`) en el cual:

1. Llama a `get_prices()` para obtener los precios actuales.
2. Verifica si hay al menos 2 casas de cambio con datos válidos (ya que se necesitan mínimo dos para arbitraje).
3. Llama a `find_arbitrage_opportunity()` para ver si hay oportunidades.
   - Si hay una oportunidad, imprime detalles:
     - En `paper_trade = True`, solo simula la operación (imprime la información de la operación sin ejecutar órdenes).
     - En `paper_trade = False`, llama a `execute_trade()` para colocar órdenes reales (requiere claves API y configuración adecuada).
4. Si no hay oportunidades, imprime que no se encontraron.
5. Espera `sleep_interval` segundos y vuelve a comenzar.

---

### Recomendaciones

- **Antes de Hacer Trading Real:**  
  Asegúrate de probar con `paper_trade = True` el tiempo que sea necesario. Verifica que las casas de cambio y el par de trading estén disponibles, y que el bot se comporte de acuerdo a lo esperado.
  
- **API Keys y Testnets:**  
  Cuando desees operar de verdad, necesitas agregar las llaves (`apiKey` y `secret`) de la casa de cambio seleccionada (siempre y cuando lo permita en tu país). También puedes usar testnets si la casa de cambio dispone de entornos de prueba.

- **Riesgo y Responsabilidad:**  
  El arbitraje puede ser riesgoso. Los precios pueden cambiar mientras la orden se ejecuta (slippage), la liquidez puede no ser suficiente, y los retiros entre casas de cambio toman tiempo. Siempre ten un plan de gestión de riesgo.

---
