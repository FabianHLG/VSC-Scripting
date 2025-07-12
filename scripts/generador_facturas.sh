#!/bin/bash

INPUT="datos/compras_$(date +%Y%m%d).csv"
TEMPLATE="plantilla_factura.tex"
OUTPUT_DIR="facturas_pdf"
LOG_DIR="logs/logs_facturas"
LOG_DIARIO="logs/log_diario.log"
PENDIENTES="datos/pendientes_envio.csv"

mkdir -p $OUTPUT_DIR
mkdir -p $LOG_DIR
mkdir -p logs

# Limpiar archivo pendientes_envio.csv y log_diario.log
> $PENDIENTES
> $LOG_DIARIO

tail -n +2 "$INPUT" | while IFS=',' read -r id_transaccion fecha_emision nombre correo telefono direccion ciudad cantidad monto pago estado_pago ip timestamp observaciones
do
    TEXFILE="$OUTPUT_DIR/factura_${id_transaccion}.tex"
    PDF_FILE="$OUTPUT_DIR/factura_${id_transaccion}.pdf"
    LOGFILE="$LOG_DIR/log_${id_transaccion}.log"

    cp "$TEMPLATE" "$TEXFILE"

    # Reemplazo de placeholders campo por campo
    sed -i "s/{id_transaccion}/$id_transaccion/g" "$TEXFILE"
    sed -i "s/{fecha_emision}/$fecha_emision/g" "$TEXFILE"
    sed -i "s/{nombre}/$nombre/g" "$TEXFILE"
    sed -i "s/{correo}/$correo/g" "$TEXFILE"
    sed -i "s/{telefono}/$telefono/g" "$TEXFILE"
    sed -i "s/{direccion}/$direccion/g" "$TEXFILE"
    sed -i "s/{ciudad}/$ciudad/g" "$TEXFILE"
    sed -i "s/{cantidad}/$cantidad/g" "$TEXFILE"
    sed -i "s/{monto}/$monto/g" "$TEXFILE"
    sed -i "s/{pago}/$pago/g" "$TEXFILE"
    sed -i "s/{estado_pago}/$estado_pago/g" "$TEXFILE"
    sed -i "s/{ip}/$ip/g" "$TEXFILE"
    sed -i "s/{timestamp}/$timestamp/g" "$TEXFILE"
    sed -i "s/{observaciones}/$observaciones/g" "$TEXFILE"

    # Compilar PDF con pdflatex, redirigir logs
    pdflatex -output-directory="$OUTPUT_DIR" "$TEXFILE" > "$LOGFILE" 2>&1

    # Verificar errores de compilación
    if grep -q "!" "$LOGFILE"; then
        echo "Error compilando factura $id_transaccion" >> "$LOG_DIARIO"
    else
        echo "${PDF_FILE},${correo}" >> "$PENDIENTES"
        echo "Factura $id_transaccion generada correctamente." >> "$LOG_DIARIO"
    fi

done

echo "Proceso finalizado. Facturas generadas y pendientes para envío listadas en $PENDIENTES"
