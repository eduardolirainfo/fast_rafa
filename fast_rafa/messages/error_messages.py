# error_messages.py

# Mensagens gerais
NOT_FOUND_DETAIL = '{} não encontrado!'
CONFLICT_DETAIL = 'Já existe um campo {} com esses dados.'
CREATION_ERROR_DETAIL = 'Erro ao criar {}.'
UPDATE_ERROR_DETAIL = 'Erro ao atualizar {}.'
DELETION_ERROR_DETAIL = 'Erro ao excluir {}.'
UNEXPECTED_ERROR_DETAIL = 'Erro inesperado ao {}: {}'
SUCCESS_DETAIL = '{} com sucesso!'


# Funções para gerar mensagens contextuais
def get_not_found_message(entity_name):
    return NOT_FOUND_DETAIL.format(entity_name)


def get_conflict_message(entity_name):
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
