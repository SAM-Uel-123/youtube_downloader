#pylint: disable=missing-module-docstring
#pylint: disable=missing-class-docstring
#pylint: disable=missing-function-docstring


class InputValidation:
    def __init__(self = None):
        self.domains = ['https://www.youtube.com/', 'https://youtu.be/']


    def val_link(self, link: str = ''):
        tmp_link = str(link)
        tmp_link2 = ''
        if link:

            for domain in self.domains:
                if domain in tmp_link:
                    tmp_link2 = tmp_link.replace(domain, '')
                    if len(tmp_link2) > 0:
                        return True

        return False


    def input_int(self, msg= ''):
        valor = None
        while True:
            try:
                valor = int(input(msg))

            except GeneratorExit as erro:
                print(f'Valor errado: {erro}')
                continue

            else:
                return valor


    def input_float(self, msg= ''):
        valor = None
        while True:
            try:
                valor = float(input(msg))

            except GeneratorExit as erro:
                print(f'Valor errado: {erro}')
                continue

            else:
                return valor


    def input_string(self, msg= '', opcs = None, lower = 0, upper = 0):
        if not opcs:
            opcs = []

        valor = None

        while True:
            try:
                valor = str(input(msg))
                if valor in opcs:
                    if lower:
                        valor = valor.lower()

                    if upper:
                        valor = valor.upper()

                    return valor


            except GeneratorExit as erro:
                print(f'Entrada invalida: {erro}')
                continue


            else:
                return valor
