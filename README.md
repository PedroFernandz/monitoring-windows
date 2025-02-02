# Windows Monitoring Scripts 🚀🖥️

Este repositorio contiene una colección de scripts en **Python** diseñados para analizar datos de rendimiento de CPU y GPU en sistemas Windows, extrayendo información desde archivos CSV generados por **Open Hardware Monitor**.

## 📖 Descripción

**Open Hardware Monitor** es una herramienta de código abierto que permite monitorear sensores de hardware en tiempo real, como temperatura, voltaje, carga y frecuencias de CPU y GPU. Los datos generados pueden exportarse a archivos CSV, los cuales son procesados por estos scripts para análisis y optimización.

Puedes descargar **Open Hardware Monitor** desde su sitio oficial: [Open Hardware Monitor](https://openhardwaremonitor.org/).

Estos scripts están diseñados para automatizar la recopilación y análisis de datos, facilitando la detección de anomalías, la optimización del rendimiento del sistema y la integración con herramientas de monitoreo como **Zabbix**.

---

## 📂 Contenido del Repositorio

| Script                       | Descripción                                                                                |
| ---------------------------- | ------------------------------------------------------------------------------------------ |
| `cpu_power_monitor.py`       | Analiza el consumo de energía de la CPU a partir de un archivo CSV.                        |
| `cpu_temperature_monitor.py` | Extrae la temperatura de la CPU desde un registro en CSV y permite su análisis.           |
| `gpu_frecuency_monitor.py`   | Obtiene la frecuencia de la GPU desde un archivo CSV para evaluar su rendimiento.         |
| `gpu_memory_frecuency.py`    | Registra la frecuencia de la memoria de la GPU basada en datos almacenados en CSV.       |
| `csv_file_pruner.py`         | Limpia archivos CSV eliminando datos antiguos o innecesarios.                            |

---

## ⚙️ Requisitos

- **Python 3.x**: Asegúrate de tener instalada la versión 3.x de Python.
- **Open Hardware Monitor**: Debe estar instalado y configurado para generar los archivos CSV.
- **Zabbix Agent (Opcional)**: Se puede configurar para monitorear automáticamente los valores extraídos de los scripts.
- **Dependencias específicas**:
  - `pandas`: Para la manipulación y análisis de archivos CSV.

Puedes instalarlo con:
```bash
pip install pandas
```

---

## 🚀 Instalación

1. **Descargar e instalar Open Hardware Monitor**
   - Descarga Open Hardware Monitor desde [su sitio oficial](https://openhardwaremonitor.org/).
   - Configura la opción de **exportación automática** de datos en CSV.

2. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/PedroFernandz/monitoring-windows.git
   cd monitoring-windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuración en Zabbix Agent (Opcional)**
   Para integrar estos scripts con **Zabbix**, agrega las siguientes líneas al archivo de configuración de Zabbix Agent (`zabbix_agentd.conf`):
   ```ini
   UserParameter=cpu.temperature, "C:\Users\pedro\AppData\Local\Programs\Python\Python313\python.exe" "C:\Program Files\Zabbix Agent\scripts\temperature_cpu.py"
   UserParameter=cpu.power, "C:\Users\pedro\AppData\Local\Programs\Python\Python313\python.exe" "C:\Program Files\Zabbix Agent\scripts\power_cpu.py"
   UserParameter=gpu.frecuency, "C:\Users\pedro\AppData\Local\Programs\Python\Python313\python.exe" "C:\Program Files\Zabbix Agent\scripts\gpu_frequency.py"
   UserParameter=gpu.frecuency.memory, "C:\Users\pedro\AppData\Local\Programs\Python\Python313\python.exe" "C:\Program Files\Zabbix Agent\scripts\gpu_memory_frequency.py"
   ```
   Luego, reinicia el agente de Zabbix para aplicar los cambios.

---

## 📌 Consideraciones Finales

- Asegúrate de que **Open Hardware Monitor** esté en ejecución y configurado para exportar los datos en formato CSV antes de ejecutar los scripts.
- Para integración con **Zabbix**, verifica que los scripts se encuentren en la ubicación adecuada y que los permisos sean correctos.
- Se recomienda programar estos scripts en tareas automatizadas para garantizar una monitorización continua.

> **Nota:** Asegúrate de revisar y entender cada script antes de ejecutarlo en tu sistema. Algunos scripts pueden requerir configuraciones específicas para su correcto funcionamiento.
