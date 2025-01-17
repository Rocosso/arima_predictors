# ARIMA Predictors Project

Este proyecto implementa un servicio de predicción de series temporales utilizando modelos ARIMA a través de una API REST.

## Requisitos Previos

### 1. Instalar Docker Desktop en Windows

1. Descargar Docker Desktop desde [Docker Hub](https://www.docker.com/products/docker-desktop/)
2. Ejecutar el instalador descargado
3. Seguir las instrucciones del asistente de instalación
4. Reiniciar el equipo cuando se solicite
5. Verificar que Docker Desktop se está ejecutando en la barra de tareas

### 2. Instalar Git en Windows

1. Descargar Git desde [Git SCM](https://git-scm.com/download/win)
2. Ejecutar el instalador
3. Mantener las opciones por defecto durante la instalación
4. Finalizar la instalación

## Configuración del Proyecto

### 1. Clonar el Repositorio

1. Abrir PowerShell o Command Prompt
2. Navegar a la carpeta donde deseas clonar el proyecto
3. Ejecutar el comando:

```bash
git clone https://github.com/Rocosso/arima_predictors.git
```

### 2. Iniciar el Proyecto con Docker

1. Navegar a la carpeta del proyecto:

```bash
cd arima_predictors
```

2. Construir e iniciar los contenedores con Docker Compose:

```bash
docker-compose up --build
```

3. Esperar a que todos los servicios estén en funcionamiento
   - Verás los logs de inicialización en la consola
   - El servicio estará listo cuando veas mensajes indicando que la aplicación está ejecutándose

## Uso de la API

### Acceder a la Documentación Swagger

1. Abrir tu navegador web
2. Ir a la URL: `http://localhost:8000/docs#/`
3. Verás la interfaz de Swagger UI con todos los endpoints disponibles

### Usar los Endpoints con Swagger UI

1. **Expandir un Endpoint**

   - Hacer clic en el endpoint que deseas probar
   - Verás la descripción detallada y los parámetros requeridos
2. **Usar "Try it Out"**

   - Hacer clic en el botón "Try it out" en la esquina superior derecha del endpoint
   - Los campos de entrada se volverán editables
3. **Ejemplo de Uso del Endpoint /arima/top-product**

   - Expandir el endpoint POST `/arima/top-product`
   - Hacer clic en "Try it out"
   - Insertar el siguiente JSON en el campo Request body:

   ```json
   {
     "start_date": "2023-01-01",
     "end_date": "2023-12-31",
     "store_id": "14bce06b5959"
   }
   ```

   - Hacer clic en "Execute"
   - Ver la respuesta en la sección "Response body"
4. **Ejemplo de Uso del Endpoint /arima/predict**

   - Expandir el endpoint POST `/arima/predict`
   - Hacer clic en "Try it out"
   - Insertar el siguiente JSON:

   ```json
   {
     "product_id": "16a562fb5931",
     "store_id": "14bce06b5959",
     "steps": 7,
     "future_prices": [10.99, 10.99, 10.99, 11.99, 11.99, 11.99, 11.99]
   }
   ```

   - Hacer clic en "Execute"
5. **Ejemplo de Uso del Endpoint /arima/train**

   - Expandir el endpoint POST `/arima/train`
   - Hacer clic en "Try it out"
   - Insertar el siguiente JSON:

   ```json
   {
     "product_id": "16a562fb5931",
     "store_id": "14bce06b5959",
     "parameters": {
       "order": [1, 1, 1],
       "seasonal_order": [1, 1, 1, 7],
       "trend": "n",
       "enforce_stationarity": false,
       "enforce_invertibility": false
     }
   }
   ```

   - Hacer clic en "Execute"

## Solución de Problemas Comunes

### Docker Desktop no inicia

- Verificar que la virtualización está habilitada en la BIOS
- Reiniciar Docker Desktop
- Reiniciar el equipo

### El servicio no responde

1. Verificar que Docker Desktop está ejecutándose
2. Verificar los logs con:

```bash
docker-compose logs
```

3. Reiniciar los contenedores:

```bash
docker-compose down
docker-compose up --build
```

### Errores de puerto ocupado

Si el puerto 8000 está en uso:

1. Verificar qué proceso está usando el puerto:

```bash
netstat -ano | findstr :8000
```

2. Cerrar el proceso o modificar el puerto en el archivo `docker-compose.yml`

## Detener el Proyecto

Para detener los contenedores:

1. Si estás ejecutando en primer plano (con logs visibles): Presionar `Ctrl+C`
2. O ejecutar en la terminal:

```bash
docker-compose down
```

## Notas Adicionales

- Los datos de prueba se cargan automáticamente al iniciar el servicio
- Todos los endpoints requieren datos en formato JSON
- Las fechas deben estar en formato "YYYY-MM-DD"
- Los IDs de productos y tiendas son strings alfanuméricos
