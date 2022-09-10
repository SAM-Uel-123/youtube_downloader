#pylint: disable=missing-module-docstring
#pylint: disable=missing-class-docstring
#pylint: disable=missing-function-docstring
#pylint: disable=no-self-argument

class Validation:
    def val_link(link: str = ''):
        tmp_link = str(link)
        tmp_link2 = ''
        if link:
            domains = ['https://www.youtube.com/', 'https://youtu.be/']
            for domain in domains:
                if domain in tmp_link:
                    tmp_link2 = tmp_link.replace(domain, '')
                    if len(tmp_link2) > 0:
                        return True

        return False


class InputValidation:
    def input_int(msg= ''):
        valor = None
        while True:
            try:
                valor = int(input(msg))

            except GeneratorExit as erro:
                print(f'Valor errado: {erro}')
                continue

            else:
                return valor


    def input_float(msg= ''):
        valor = None
        while True:
            try:
                valor = float(input(msg))

            except GeneratorExit as erro:
                print(f'Valor errado: {erro}')
                continue

            else:
                return valor

    def input_string(msg= '', opcs = None, lower = 0, upper = 0):
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
