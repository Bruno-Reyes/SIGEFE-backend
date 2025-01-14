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

def mensaje_asignacion_beca(lec_name: str, tipo_beca: str) -> str:
    mensaje = f"""
    <div>
        <p>Hola <b>{lec_name}</b>,</p>
        <p>Te informamos que se te ha asignado la siguiente beca: <b>{tipo_beca}</b>.</p>
        <p>Recuerda que puedes consultar más detalles en tu cuenta de usuario.</p>
        <br>
        <p>Saludos cordiales,<br>El Equipo de SIGEFE</p>
    </div>
    """
    return mensaje

def mensaje_registro_pago(lec_name: str, monto: float) -> str:
    mensaje = f"""
    <div>
        <p>Hola <b>{lec_name}</b>,</p>
        <p>Se ha registrado un pago a tu nombre por la cantidad de <b>${monto} MXN</b>.</p>
        <p>Recuerda confirmar la recepción del pago en tu cuenta de usuario.</p>
        <br>
        <p>Saludos cordiales,<br>El Equipo de SIGEFE</p>
    </div>
    """
    return mensaje

def mensaje_confirmacion_pago(lec_name: str, monto: float) -> str:
    mensaje = f"""
    <div>
        <p>Hola <b>{lec_name}</b>,</p>
        <p>Has confirmado la recepción del pago por la cantidad de <b>${monto:,.2f} MXN</b>.</p>
        <p>Gracias por tu confirmación.</p>
        <br>
        <p>Saludos cordiales,<br>El Equipo de SIGEFE</p>
    </div>
    """
    return mensaje

def mensaje_rechazo_pago(lec_name: str, monto: float) -> str:
    mensaje = f"""
    <div>
        <p>Hola <b>{lec_name}</b>,</p>
        <p>Has rechazado el pago registrado por la cantidad de <b>${monto:,.2f} MXN</b>.</p>
        <p>Si esto ha sido un error, por favor contacta al equipo de soporte.</p>
        <br>
        <p>Saludos cordiales,<br>El Equipo de SIGEFE</p>
    </div>
    """
    return mensaje

def mensaje_eliminacion_pago(lec_name: str, monto: float) -> str:
    mensaje = f"""
    <div>
        <p>Hola <b>{lec_name}</b>,</p>
        <p>Lamentamos informarte que el registro de pago por la cantidad de <b>${monto:,.2f} MXN</b> ha sido eliminado.</p>
        <p>Si tienes alguna duda o necesitas más información, por favor contacta al equipo de soporte.</p>
        <br>
        <p>Saludos cordiales,<br>El Equipo de SIGEFE</p>
    </div>
    """
    return mensaje