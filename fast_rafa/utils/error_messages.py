# error_messages.py

# Mensagens gerais
NOT_FOUND_DETAIL = '{} não encontrado(a)! Por favor, insira um valor válido.'
CONFLICT_DETAIL = '{} já existe! Por favor, insira um valor único.'
CREATION_ERROR_DETAIL = 'Erro ao criar {}. Por favor, tente novamente.'
UPDATE_ERROR_DETAIL = 'Erro ao atualizar {}. Por favor, tente novamente.'
DELETION_ERROR_DETAIL = 'Erro ao excluir {}. Por favor, tente novamente.'
UNEXPECTED_ERROR_DETAIL = (
    'Erro inesperado ao {}: {} . Por favor, tente novamente.'
)
SUCCESS_DETAIL = '{} com sucesso!'


def get_not_found_message(entity_name):
    return NOT_FOUND_DETAIL.format(entity_name)


def get_conflict_message(entity_name: str) -> str:
    return CONFLICT_DETAIL.format(entity_name)


def get_creation_error_message(entity_name):
    return CREATION_ERROR_DETAIL.format(entity_name)


def get_update_error_message(entity_name):
    return UPDATE_ERROR_DETAIL.format(entity_name)


def get_deletion_error_message(entity_name):
    return DELETION_ERROR_DETAIL.format(entity_name)


def get_unexpected_error_message(action, error):
    return UNEXPECTED_ERROR_DETAIL.format(action, error)


def get_success_message(entity_name):
    return SUCCESS_DETAIL.format(entity_name)
