# Lógica de Mapeo y Decodificación del Controlador NES

Este documento detalla cómo se extrae la información de los botones del mando, cómo se agrupa en un vector de 8 bits y cómo el procesador filtra esa información para saber qué botón se presionó. Todo el proceso ocurre en tres etapas lógicas.

---

## 1. Tabla de orden de salida bit por bit

El mando de NES no envía todos los botones al mismo tiempo. Al recibir la orden de `LATCH`, toma una "foto" de qué botones están presionados y luego los envía en fila india (uno por uno) por el cable `DATA` cada vez que recibe un pulso de `CLOCK`. 

El orden estricto de llegada define nuestro mapa:

| Señal que lo envía | Índice en el Vector | Botón correspondiente | Valor de su "Máscara" |
| :--- | :--- | :--- | :--- |
| **LATCH** | Bit 0 (Extremo derecho / LSB) | A | Hex: `0x01` |
| **CLOCK 1** | Bit 1 | B | Hex: `0x02` |
| **CLOCK 2** | Bit 2 | Select | Hex: `0x04` |
| **CLOCK 3** | Bit 3 | Start | Hex: `0x08` |
| **CLOCK 4** | Bit 4 | Arriba (Up) | Hex: `0x10` |
| **CLOCK 5** | Bit 5 | Abajo (Down) | Hex: `0x20` |
| **CLOCK 6** | Bit 6 | Izquierda (Left) | Hex: `0x40` |
| **CLOCK 7** | Bit 7 (Extremo izquierdo / MSB)| Derecha (Right) | Hex: `0x80` |

---

## 2. Diagrama de Flujo de los Datos

El siguiente diagrama ilustra el viaje de los datos desde que salen del mando como pulsos individuales, hasta que se convierten en un comando de acción en el procesador de la consola.

```mermaid
flowchart TD
    Mando([MANDO NES]) -- "Envía 1 bit a la vez\n(Cable DATA)" --> Reg

    subgraph FASE1 [FASE 1: HARDWARE - Placa FPGA]
        direction TB
        Reg[Registro Receptor\nAcomoda los bits: 7 6 5 4 3 2 1 0]
        Inv[Inversor de Lógica\nConvierte '0' físico a '1' lógico]
        
        Reg --> Inv
    end

    Inv -- "Entrega el paquete completo\nde 8 bits (1 Byte)" --> Rx

    subgraph FASE2 [FASE 2: SOFTWARE - CPU / SoC]
        direction TB
        Rx[Recepción del Byte\nEj: 00001000]
        Mask{Enmascaramiento\nAplica filtro Hexadecimal\nEj: Máscara 0x08}
        Accion([Decisión / Acción\nEj: Iniciar el juego])
        
        Rx --> Mask
        Mask -- "Si el bit aislado es '1'" --> Accion
    end
