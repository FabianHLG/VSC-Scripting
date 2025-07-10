# scripts/generador_compras.py
import csv
import random
from datetime import datetime
from faker import Faker

fake = Faker()

def generar_compras(cantidad=10):
    nombre_archivo = f"datos/compras_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        campos = ['id_transaccion', 'fecha_emision', 'nombre', 'correo', 'telefono', 'direccion', 'ciudad',
                  'cantidad', 'monto', 'pago', 'estado_pago', 'ip', 'timestamp', 'observaciones']
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for i in range(1, cantidad + 1):
            fila = {
                'id_transaccion': f"T{i:04d}",
                'fecha_emision': datetime.now().strftime('%Y-%m-%d'),
                'nombre': fake.name(),
                'correo': fake.email(),
                'telefono': fake.phone_number(),
                'direccion': fake.street_address(),
                'ciudad': fake.city(),
                'cantidad': random.randint(1, 5),
                'monto': round(random.uniform(10000, 100000), 2),
                'pago': random.choice(['completo', 'fraccionado']),
                'estado_pago': random.choices(['exitoso', 'fallido'], weights=[90, 10])[0],
                'ip': fake.ipv4(),
                'timestamp': datetime.now().isoformat(),
                'observaciones': random.choice(['cliente frecuente', 'promoción aplicada', ''])
            }
            escritor.writerow(fila)
    print(f"Archivo generado: {nombre_archivo}")

if __name__ == "__main__":
    generar_compras(10)
