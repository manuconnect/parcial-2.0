# Mapa de Bits y Decodificación del Controlador NES

## 1. Descripción de la Trama
El controlador de NES no envía comandos complejos ni requiere inicialización. Responde a un pulso de `LATCH` capturando el estado de sus 8 botones y los transmite secuencialmente a través del pin `DATA` mediante 7 pulsos de `CLOCK`. 

El resultado es una trama plana de **8 bits (1 byte)**. El hardware original opera con lógica negativa (*Active LOW*), pero en nuestro módulo de lectura en Verilog, los datos se invierten (`~registro_temp`) para que un `1` lógico represente un botón presionado (*Active HIGH*).

## 2. Mapa del Controlador (Bit Mapping)
El procesador lee los bits en formato binario estándar (de derecha a izquierda, donde el Bit 0 es el Menos Significativo o LSB). El orden estricto en el que el chip CD4021B entrega los datos define el siguiente mapa:

| Posición de llegada | Índice del Bit | Botón Físico | Valor Presionado (Invertido) |
| :--- | :--- | :--- | :--- |
| 1er bit (En el Latch) | **Bit 0** | A | `1` |
| 2do bit (Clock 1) | **Bit 1** | B | `1` |
| 3er bit (Clock 2) | **Bit 2** | Select | `1` |
| 4to bit (Clock 3) | **Bit 3** | Start | `1` |
| 5to bit (Clock 4) | **Bit 4** | Arriba (Up) | `1` |
| 6to bit (Clock 5) | **Bit 5** | Abajo (Down) | `1` |
| 7mo bit (Clock 6) | **Bit 6** | Izquierda (Left) | `1` |
| 8vo bit (Clock 7) | **Bit 7** | Derecha (Right) | `1` |

## 3. Ejemplo de Lectura
Si se presiona el botón **Start**, el bit correspondiente es el Bit 3. En formato binario (leyendo del Bit 7 al Bit 0), el byte completo se visualizará en la memoria como:
`00001000`

Si se presiona el botón **Abajo (Down)**, el bit correspondiente es el Bit 5. El byte completo se visualizará como:
`00100000`

## 4. Implementación en Hardware (Verilog)
Para traducir esta trama cruda de 8 bits en señales individuales útiles para el sistema SoC (FemtoRV32), se utiliza el siguiente decodificador combinacional. Este módulo extrae cada bit de la trama y lo asigna a un cable individual.

```verilog
module decodificador_nes (
    input  wire [7:0] trama_botones, // El byte final recibido e invertido
    output wire btn_A,
    output wire btn_B,
    output wire btn_Select,
    output wire btn_Start,
    output wire btn_Up,
    output wire btn_Down,
    output wire btn_Left,
    output wire btn_Right
);

    // Mapeo directo de bits a botones
    assign btn_A      = trama_botones[0];
    assign btn_B      = trama_botones[1];
    assign btn_Select = trama_botones[2];
    assign btn_Start  = trama_botones[3];
    assign btn_Up     = trama_botones[4];
    assign btn_Down   = trama_botones[5];
    assign btn_Left   = trama_botones[6];
    assign btn_Right  = trama_botones[7];

endmodule
