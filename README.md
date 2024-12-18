# arbitrage-bot
 Python Arbitrage Bot testing

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
   Obtiene los precios actuales de compra (`bid`) y venta (`ask`) para el símbolo seleccionado desde cada casa de cambio configurada. Si hay errores (ej. símbolo no soportado), se informan y se continúa con las demás casas de cambio.

2. **find_arbitrage_opportunity(prices)**  
   Analiza las diferencias de precio entre las casas de cambio. Si la ganancia potencial supera la tolerancia a las comisiones, considera la oportunidad como válida.

3. **execute_trade(buy_exchange_name, sell_exchange_name, buy_price, sell_price, amount)**  
   Ejecuta la operación real si `paper_trade = False`. En modo prueba (`True`), solo simula y no coloca órdenes reales.

---

### Flujo del Programa (main)

1. El programa llama a `get_prices()` para obtener los precios actuales.
2. Comprueba si hay al menos dos casas de cambio con datos.
3. Llama a `find_arbitrage_opportunity()` para detectar oportunidades.
   - En `paper_trade = True`, imprime lo que haría sin ejecutar.
   - En `paper_trade = False`, llama a `execute_trade()` para colocar órdenes reales.
4. Si no hay oportunidades, lo indica en la consola.
5. Espera `sleep_interval` segundos antes de repetir el ciclo.

---

### Recomendaciones

- **API Keys y Testnets:**  
  Antes de operar en vivo, configura tus llaves de API en la casa de cambio y, si es posible, practica en un testnet. Esto te permite probar sin riesgo real.

- **Riesgo y Responsabilidad:**  
  El arbitraje conlleva riesgos. Los precios pueden variar rápidamente (slippage), la liquidez puede ser limitada y mover fondos entre casas de cambio toma tiempo. Ten un plan de gestión de riesgo.

- **Visualización de Precios en Múltiples Casas de Cambio:**  
  Si integras la funcionalidad de trazar gráficas de velas (candlestick charts) para diferentes intercambios en simultáneo, es normal que notes diferencias en precios y velas entre ellos. Esto no se debe a un error en el código, sino a las características propias de cada mercado:

  - **Mercados Independientes:** Cada casa de cambio tiene su propia liquidez, spread y dinámica de precios. Por eso, el mismo activo puede verse con precios ligeramente diferentes.
  - **Distinta Precisión en el Precio (Tick Size):** Un exchange puede reportar precios con tres decimales y otro con cuatro, lo cual impacta el aspecto de las velas.
  - **Variaciones en el Tiempo y Latencia:** Los datos se obtienen a intervalos regulares, y cada mercado puede cambiar entre lecturas de distinta forma.
  - **Sin Manipulación de Datos:** El código muestra la data tal cual la recibe de cada exchange. Las diferencias en las velas reflejan condiciones reales del mercado, no fallos del programa.

Estas discrepancias en las velas y precios entre intercambios son parte del escenario real de arbitraje, y conocerlas te ayuda a interpretar mejor el panorama al momento de decidir tus estrategias.

---