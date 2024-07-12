import pyperclip
from html2rtf import html2rtf

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Correo</title>
</head>
<body>
    <p>De: Julia &lt;juliamendez22@yahoo.es&gt;</p>
    <p>Enviado: lunes, 1 de julio de 2024 15:22</p>
    <p>Para: roydavid79@hotmail.com &lt;roydavid79@hotmail.com&gt;</p>
    <p>Asunto: Enlace corregido para herramienta propuesta Cáncer Capt VIII</p>
    <br>
    <p>Estimado Dr. Roy Montoya,</p>
    <p>Espero se encuentre bien. Le escribo para agradecerle la reunión del 23 de mayo, donde revisamos las Tablas N° 1 y 2 del Capítulo VIII sobre Cáncer. Esta revisión ha mejorado significativamente las tablas.</p>
    <p>Adjunto los 7 casos solicitados para su calificación. He corregido el enlace para acceder a los expedientes:</p>
    <p><a href="https://1drv.ms/f/s!AqF1d4t3mC6Xjtsuh61pwWc5B_lwVg">Enlace corregido</a></p>
    <p>Contraseña: hi-5471me</p>
    <br>
    <p>Atentamente,</p>
    <p>Dra. Julia Méndez C.</p>
</body>
</html>
"""

# Convert HTML to RTF
rtf_content = html2rtf.html2rtf(html_content)

# Copy to clipboard
pyperclip.copy(rtf_content)
print("El contenido del correo ha sido copiado al portapapeles en formato RTF.")
