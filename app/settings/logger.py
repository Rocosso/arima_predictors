import logging

def setup_logger():
    # Configurar el logger
    logger = logging.getLogger("LOGS")
    logger.setLevel(logging.INFO)

    # Configurar el formato de los logs
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

    # Configurar el handler para salida en consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Añadir el handler al logger
    logger.addHandler(console_handler)

    return logger
