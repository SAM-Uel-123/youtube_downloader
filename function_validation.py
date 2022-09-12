#pylint: disable=missing-module-docstring

class InputValidation:
    """
    Classe: Responsavel por tratar entradas do usuario,
tais como Numeros inteiros, como 1, 2, 3...
tais como Floats: 1.1, 2.2, 3.3, 0.00001...
tais como Strings: 's', 'n', 'o', 'p'...
    """
    def __init__(self) -> None:
        self.domains = ['https://www.youtube.com/', 'https://youtu.be/']


    def input_int(self, msg: str= '') -> int:
        """
    Função: Resṕonsavel por tratar de entradas de numeros inteiros.

    Ex.:
    > InputValidation.input_int('Digite um numero: ')
    > Digite um numero: 1
    > 1
    > Digite um numero: s
    > Valor errado.

        """
        valor = None
        while True:
            try:
                valor = int(input(msg))

            except GeneratorExit as erro:
                print(f'Valor errado: {erro}')
                continue

            else:
                return valor


    def input_float(self, msg: str= '') -> float:
        """
    Função: Resṕonsavel por tratar de entradas de numeros flutuantes.

    Ex.:
    > InputValidation.input_int('Digite um float: ')
    > Digite um numero: 1.1
    > 1.1
    > Digite um numero: s
    > Valor errado.

        """

        valor = None
        while True:
            try:
                valor = float(input(msg))

            except GeneratorExit as erro:
                print(f'Valor errado: {erro}')
                continue

            else:
                return valor


    def input_string(self, msg : str = '', opcs = None, lower : int = 0, upper : int = 0) -> str:
        """
    Função: Responsavel por tratar de entradas de Strings.

    Ex.:
    > InputValidation.input_int('Digite uma string: ', opcs = ['s', 'n'])
    > Digite [S/N]: s
    > s
    > Digite [S/N]: l
    > Valor errado.

        """

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
                print(f'Valor errado: {erro}')
                continue


            else:
                return valor


    def val_link(self, link : str = '') -> bool:
        """
    Função: Responsavel por tratar a veracidade das URLs passadas como argumentos,

    Ex.:
    > InputValidation.val_link('https://youtu.be/...')
    > True
        """

        tmp_link = str(link)
        tmp_link2 = ''
        if link:
            for domain in self.domains:
                if domain in tmp_link:
                    tmp_link2 = tmp_link.replace(domain, '')
                    if len(tmp_link2) > 0:
                        return True

        return False
