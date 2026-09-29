# Lógica de Mapeo y Decodificación del Controlador NES

Este documento detalla la estructura de datos del mando de NES, cómo se recolecta la información a nivel de hardware (FPGA) y cómo se interpreta a nivel de software en la CPU FemtoRV32.

---

## 1. Tabla de orden de salida bit por bit

El hardware del NES transmite el estado de los botones a través de la línea `DATA` en una secuencia temporal estricta de 8 bits. La siguiente tabla define el orden exacto de llegada de cada bit, el estímulo que lo genera (LATCH o CLOCK) y su valor hexadecimal correspondiente para la posterior decodificación en software.

| Señal de Control | Índice en el Vector | Botón correspondiente | Valor Hexadecimal (Máscara) |
| :--- | :--- | :--- | :--- |
| **LATCH** (Captura) | Bit 0 (LSB) | A | `0x01` |
| **CLOCK 1** | Bit 1 | B | `0x02` |
| **CLOCK 2** | Bit 2 | Select | `0x04` |
| **CLOCK 3** | Bit 3 | Start | `0x08` |
| **CLOCK 4** | Bit 4 | Arriba (Up) | `0x10` |
| **CLOCK 5** | Bit 5 | Abajo (Down) | `0x20` |
| **CLOCK 6** | Bit 6 | Izquierda (Left) | `0x40` |
| **CLOCK 7** | Bit 7 (MSB) | Derecha (Right) | `0x80` |

---

## 2. Definición del vector de 8 bits (Registro Receptor en Verilog)

A nivel de hardware, la FPGA necesita un lugar en memoria para ir apilando los bits que llegan uno por uno desde el control. Para esto, se define un registro de desplazamiento (*shift register*) de 8 bits. 

Dado que el control original utiliza resistencias *pull-up* (lógica negativa donde `0` es presionado), el hardware se encarga de invertir el registro final (`~registro_temp`) antes de enviarlo a la CPU. De esta forma, el software de alto nivel recibe los datos en lógica positiva (*Active HIGH*).

```verilog
// Definición del registro temporal para almacenar los bits desplazados en serie
reg [7:0] registro_temp;

// Definición del vector final que se mapea a la memoria (MMIO) para la CPU
// Se aplica una inversión de bits (~) para convertir la lógica Active LOW a Active HIGH
wire [7:0] nes_byte_final;
assign nes_byte_final = ~registro_temp; 
3. Constantes de enmascaramiento en C (Software SoC)
Una vez que el módulo Verilog deposita el byte completo en la dirección de memoria asignada al periférico (MMIO), el software ejecutado por el procesador FemtoRV32 debe aislar cada bit para determinar qué botón específico fue presionado.

Esto se logra definiendo constantes de enmascaramiento (bitmasks) y utilizando el operador lógico AND a nivel de bits (&).

C
// Definición de la dirección de memoria asignada al mando NES (Memory-Mapped I/O)
#define NES_PORT_ADDR 0x450000
#define IO_NES        (*((volatile uint32_t *)NES_PORT_ADDR))

// Constantes de enmascaramiento (Máscaras de bits)
#define NES_MASK_A      0x01  // 0000 0001
#define NES_MASK_B      0x02  // 0000 0010
#define NES_MASK_SELECT 0x04  // 0000 0100
#define NES_MASK_START  0x08  // 0000 1000
#define NES_MASK_UP     0x10  // 0001 0000
#define NES_MASK_DOWN   0x20  // 0010 0000
#define NES_MASK_LEFT   0x40  // 0100 0000
#define NES_MASK_RIGHT  0x80  // 1000 0000

// Ejemplo de lectura y procesamiento de los comandos
void procesar_entradas_nes() {
    // Se lee el byte completo entregado por el hardware de la FPGA
    uint8_t nes_data = IO_NES; 

    // Uso de máscaras para aislar y verificar el estado de botones individuales
    if (nes_data & NES_MASK_START) {
        // Se ejecuta si el Bit 3 es '1'
        iniciar_juego();
    }
    
    if (nes_data & NES_MASK_RIGHT) {
        // Se ejecuta si el Bit 7 es '1'
        mover_personaje_derecha();
    }
}
