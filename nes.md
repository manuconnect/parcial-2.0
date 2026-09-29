# Control NES

Recibe el protocolo serial del control NES (latch, clock, data) y expone el estado de los 8 botones al procesador como un registro de lectura, mapeado en `0x450000 - 0x45FFFF`.

## Contrato de puertos

| Señal | Dirección | Descripción |
|---|---|---|
| `d_in` | entrada | Datos que escribe el CPU (sin uso: este periférico es solo lectura) |
| `cs` | entrada | Chip select — activo cuando `mem_addr` cae en el rango del NES |
| `addr` | entrada | Offset dentro del rango del periférico |
| `rd` | entrada | Solicitud de lectura del CPU |
| `wr` | entrada | Solicitud de escritura del CPU (sin uso) |
| `d_out` | salida | Estado actual de los 8 botones |

## Mapa de registros

| Offset | Registro | Acceso | Descripción |
|---|---|---|---|
| `0x00` | `NES_BUTTONS` | Lectura | Byte con el estado de los 8 botones (1 = presionado) |

### Distribución de bits

| Bit | Botón |
|---|---|
| 0 | A |
| 1 | B |
| 2 | Select |
| 3 | Start |
| 4 | Arriba |
| 5 | Abajo |
| 6 | Izquierda |
| 7 | Derecha |

*El orden de los bits es una decisión de implementación — aquí se sigue el mismo orden en que salen del control, que es el más simple.*

## Protocolo del control (latch / clock / data)

El control NES no manda los botones por separado: tiene un registro de desplazamiento interno que hay que "vaciar" bit a bit.

1. **Latch**: el FPGA sube `LATCH` y lo baja — le dice al control "congela el estado actual de tus 8 botones".
2. **Primer bit**: justo después del latch, `DATA` ya trae el estado del botón A, en lógica activa en bajo (0 = presionado).
3. **Clock**: cada pulso de `CLOCK` avanza el registro un bit, en este orden fijo: A, B, Select, Start, Arriba, Abajo, Izquierda, Derecha.
4. El módulo captura esos 8 bits, los invierte (para que 1 = presionado sea más intuitivo) y los deja listos en `NES_BUTTONS`.

Este ciclo se repite periódicamente (por ejemplo, una vez por cuadro) para mantener el estado actualizado.
