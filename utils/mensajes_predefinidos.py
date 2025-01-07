def mensaje_registro_exitoso(nombre: str) -> str:
    mensaje = f'<div> <p>Hola <b>{nombre}</b></p> <p>Gracias por registrarte en nuestro sistema. Estamos emocionados de tenerte con nosotros, en los próximos días te haremos saber por este medio si tus datos fueron aprobados y los siguientes pasos. </p> <br> <p>Si no solicitaste este registro, por favor ignora este correo.</p> <p>Saludos cordiales,<br>El Equipo de SIGEFE</p></div>'
    return mensaje    

def asignación_centro_exitoso(lec_email: str, lec_name: str, centro: dict, token: str):
    mensaje = f"""
    Hola {lec_name},
    <br>
    <br>
    Te informamos que has sido asignado al siguiente centro de trabajo:
    <br>
    Centro: {centro['nombre_turno']}<br>
    CCT: {centro['clave_centro_trabajo']}<br>
    Estado: {centro['estado']}<br>
    Municipio: {centro['municipio']}<br>
    Turno: {centro['nombre_turno']}<br>
    Nivel Educativo: {centro['nivel_educativo']}<br>
    Código Postal: {centro['codigo_postal']}<br>
    Domicilio: {centro['domicilio']}<br>
    <br>
    Saludos cordiales,
    Equipo de SIGEFE
    """
    return mensaje

def mensaje_aceptacion(nombre: str, lugar_convocatoria:str) -> str:
    mensaje = f'<div> <p>Hola <b>{nombre}</b></p> <p>¡Felicidades! Has sido aceptado como LEC en la convocatoria de {lugar_convocatoria}. Próximamente se te hará llegar otro correo donde te informaremos en qué centro has sido asignado. </p> <br> <p>Si no solicitaste este registro, por favor ignora este correo.</p> <p>Saludos cordiales,<br>El Equipo de SIGEFE</p></div>'
    return mensaje
    
def mensaje_rechazo(nombre: str, lugar_convocatoria:str) -> str:
    mensaje = f'<div> <p>Hola <b>{nombre}</b></p> <p>Lamentamos informarte que no has sido aceptado como LEC en la convocatoria de {lugar_convocatoria}. Agradecemos tu interés y te invitamos a participar en nuestras futuras convocatorias. </p> <br> <p>Si no solicitaste este registro, por favor ignora este correo.</p> <p>Saludos cordiales,<br>El Equipo de SIGEFE</p></div>'
    return mensaje