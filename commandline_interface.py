#pylint: disable=missing-module-docstring
#pylint: disable=missing-class-docstring
#pylint: disable=missing-function-docstring

# ============================== #
#       - Importações -          #
# ============================== #

from os import system
from youtube_downloader import YouTubeDownloader
from function_validation import InputValidation

class Cli:
    def __init__(self):
        return None

    def linhas(self, msg= '', linha= '='):
        print(linha * 60)
        print(f'{msg:^60}')
        print(linha * 60)


    def clear(self = None):
        system('clear')


if __name__ == '__main__':
    # =============================== #
    # - Variaveis e objetos globais - #
    # =============================== #
    CLEAR = Cli.clear
    LINK = None
    DIRECTORY = './'
    LIMPAR = 1
    InputValidation = InputValidation()
    if LIMPAR:
        CLEAR()

    if not LINK:
        try:
            LINK = input(' link: ')

        except GeneratorExit as erro:
            print(erro)


    downloader = YouTubeDownloader(LINK, DIRECTORY)


    # ================== #
    # - Loop principal - #
    # ================== #
    while True:
        if LIMPAR:
            CLEAR()

        Cli.linhas('Downloader for YouTube Videos')

        # ==================================================== #
        # - Mostra o(s) titulo(s) do LINK(s) que você passou - #
        # ==================================================== #
        if downloader.titulo:
            print('\n', '-=' * 30)
            if type(downloader.titulo).__name__ == 'str':
                print(f' 01 -> [ {downloader.titulo} ]')

            elif type(downloader.titulo).__name__ == 'list':
                for index, t in enumerate(downloader.titulo):
                    index += 1
                    print(f' {index if len(str(index)) > 1 else f"0{index}"} -> [ {t} ] ')
            print('-=' * 30, '\n')

        #===================================== #
        # - Opções para baixar o video/audio - #
        # ==================================== #
        print('''
1 - Baixar Video(s)
2 - Baixar Audios(s)    
3 - Escolher diretorio de saida
4 - Ler arquivo com LINKs
5 - Trocar o LINK de download

0 - Sair

    ''')
        opc = InputValidation.input_int(' Opção: ')

        if opc == 0:
            break

        elif opc == 1:
            downloader.download()

        elif opc == 2:
            downloader.download(only_audio = 1)

        elif opc == 3:
            downloader.change_directory()

        elif opc == 4:
            downloader.read_file()

        elif opc == 5:
            downloader.change_link(atualizar_caches= 1)

        else:
            print(' Opção invalida.')

        input(' Press "ENTER" for continue.')
