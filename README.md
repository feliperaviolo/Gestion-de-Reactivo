Gestión de Reactivos para Laboratorios
Descripción

Sistema de escritorio desarrollado en Python + Tkinter + SQLite para la gestión integral de reactivos de laboratorio. Permite controlar el stock, lotes, vencimientos, proveedores, consumos y generar alertas automáticas, mejorando la trazabilidad y reduciendo errores operativos.

Características
Gestión de reactivos.
Gestión de categorías.
Gestión de proveedores.
Gestión de presentaciones por proveedor.
Registro de ingresos de nuevos lotes.
Registro de consumos.
Control de stock en tiempo real.
Control de vencimiento por fecha del fabricante.
Control de vencimiento luego de la apertura.
Alertas de bajo stock.
Alertas de reactivos vencidos.
Alertas de reactivos próximos a vencer.
Indicadores generales del laboratorio.
Gestión de usuarios y roles.
Base de datos SQLite.
Interfaz gráfica desarrollada con Tkinter.
Módulos
Reactivos

Permite administrar toda la información de cada reactivo:

Código interno
Nombre
CAS
GTIN
Categoría
Unidad de medida
Stock mínimo
Condiciones de almacenamiento
Estado activo/inactivo
Proveedores

Registro de proveedores con información como:

Código SAP
Nombre
Tipo de proveedor
Email
Teléfono

Además permite asociar un mismo reactivo a distintos proveedores.

Presentaciones

Cada proveedor puede ofrecer distintas presentaciones de un reactivo.

Se administra:

Cantidad por envase
Unidad
Precio
Días de vencimiento luego de abrir
Estado
Ingresos

Registro de nuevos lotes indicando:

Número de lote
Fecha de ingreso
Fecha de vencimiento
Cantidad ingresada
Ubicación
Observaciones

El sistema calcula automáticamente el stock disponible.

Consumos

Permite registrar el consumo diario de reactivos.

Funciones:

Selección por lote
Cantidad utilizada
Usuario
Observaciones
Apertura automática del frasco
Cálculo automático del vencimiento luego de abrir.
Alertas

El sistema detecta automáticamente:

Reactivos con bajo stock.
Reactivos vencidos.
Reactivos próximos a vencer.
Necesidad de reposición.
Indicadores

Panel principal con indicadores como:

Reactivos activos
Reactivos con stock correcto
Reactivos bajo stock
Reactivos vencidos
Reactivos próximos a vencer
Tecnologías utilizadas
Python
Tkinter
SQLite
ttk
Pandas
OpenPyXL
Win32COM (Outlook)
Estructura del proyecto
GestionReactivos/
│
├── app.py
├── database.py
├── modelos/
├── vistas/
├── controladores/
├── utilidades/
├── recursos/
│
├── database.db
│
└── README.md
Base de datos

El sistema utiliza SQLite, por lo que no requiere instalar un servidor de base de datos.

Entre las principales tablas se encuentran:

usuarios
categorias
proveedores
reactivos
reactivo_proveedor
lotes
ingresos
usos
Beneficios
Centraliza toda la información del laboratorio.
Reduce errores manuales.
Evita quiebres de stock.
Mejora la trazabilidad de los reactivos.
Facilita auditorías.
Automatiza el seguimiento de vencimientos.
Simplifica la reposición de materiales.
Próximas mejoras
Lectura de códigos de barras.
Impresión de etiquetas.
Reportes en PDF y Excel.
Dashboard con gráficos.
Notificaciones automáticas por correo.
Integración con Power BI.
Base de datos SQL Server para múltiples usuarios.
Capturas

Aquí pueden agregarse imágenes del sistema.

<img width="1912" height="983" alt="image" src="https://github.com/user-attachments/assets/64a8e774-1215-43f3-a4e0-42541730914d" />

<img width="1918" height="987" alt="image" src="https://github.com/user-attachments/assets/1bf08670-9cdb-42ca-ad7e-405721e6cb5c" />

<img width="1917" height="986" alt="image" src="https://github.com/user-attachments/assets/37a5583f-1163-4eee-96dd-64039553902e" />


/screenshots/ingresos.png
Autor

Felipe Raviolo

Desarrollador de soluciones de automatización y sistemas para optimizar procesos de laboratorio, calidad e industria mediante herramientas desarrolladas en Python.
