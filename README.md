# PROFITUS ERP V2

Proyecto ERP para gestión empresarial desarrollado en Python con interfaz gráfica moderna usando CustomTkinter. Esta es la versión 2 del proyecto, con mejoras en diseño y funcionalidades de login seguras.

---

## Estado actual del proyecto

- Implementación de sistema de login moderno y funcional, con:
  - Interfaz gráfica amigable y profesional basada en CustomTkinter
  - Validación de usuarios contra base de datos SQLite
  - Hashing de contraseñas con SHA-256 para seguridad
  - Integración del logo oficial en la ventana de login
  - Flujo de login que abre ventana de Dashboard principal (o configuración por ahora)

- Arquitectura modular:
  - `src/` para código fuente separado en módulos manejables
  - `assets/` para imágenes, logos y recursos estáticos
  - Gestión de usuarios con creación, actualización, eliminación en base SQLite

---

## Próximos pasos a desarrollar

- Creación del Dashboard/ Home:
  - Pantalla principal una vez se entra en el sistema, con resumen y accesos directos
  - Navegación clara y organizada hacia configuración, ventas, inventarios, etc.

- Mejoras UI/UX:
  - Añadir funcionalidad “Recordarme” en login
  - Mejorar experiencia visual y flujo entre ventanas

---

## Requisitos para ejecutar el proyecto

- Python 3.10 o superior  
- Librerías:
  - customtkinter
  - pillow
  - sqlite3 (integrada con Python)
- Base de datos SQLite configurada con estructura inicial para usuarios y roles

---

## Cómo instalar y correr

1. Clona este repositorio en tu computadora:  
git clone https://github.com/soyjhoda/PROFITUSV2.git


2. Entra en la carpeta del proyecto:  
cd PROFITUSV2


3. Crea y activa un entorno virtual (opcional pero recomendado):  

python -m venv venv

-En Windows:  

venv\Scripts\activate

-En Linux/macOS:  

source venv/bin/activate



4. Instala las dependencias del proyecto:  

pip install -r requirements.txt



5. Ejecuta la aplicación:  

python -m src.app



---

## Cómo contribuir

- Puedes abrir issues para reportar bugs o sugerir mejoras  
- Envía pull requests si quieres aportar código o documentación  
- Mantén la documentación actualizada y sigue buenas prácticas de codificación

---

## Licencia

Este proyecto es de uso personal y privado. Para otros usos por favor contactar al autor.

---

## Contacto

- Autor: José Daniel Marín  
- GitHub: [soyjhoda](https://github.com/soyjhoda)  
- Email: contactosjhoda@gmail.com / jhoda611@gmail.com

---

Este README se actualizará conforme se avancen en funcionalidades y módulos nuevos. ¡Gracias por interesarte en PROFITUS ERP V2!
