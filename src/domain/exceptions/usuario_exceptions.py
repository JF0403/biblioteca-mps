class UsuarioException(Exception):
    pass


class UsuarioDuplicadoException(UsuarioException):
    pass


class DadosUsuarioInvalidosException(UsuarioException):
    pass


class LoginInvalidoException(UsuarioException):
    pass


class SenhaFracaException(UsuarioException):
    pass


class PersistenciaException(UsuarioException):
    pass