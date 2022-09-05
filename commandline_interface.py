class cli:
    def linhas(msg= '', linha= '='):
        print(linha * 60)
        print(f'{msg:^60}')
        print(linha * 60)



if __name__ == '__main__':
    # ============================== #
    #       - Importações -          #
    # ============================== #
    from os import system
    from YouTubeDownloader import *
    from function_validation import *

    # =============================== #
    # - Variaveis e objetos globais - #
    # =============================== #
    clear = lambda: system('clear')
    link = None
    directory = './'
    limpar = 1

    if limpar:
        clear()

    if not link:
        link = input(' Link: ')

    downloader = YouTubeDownloader(link, directory)


    # ================== #
    # - Loop principal - #
    # ================== #
    while True:
        if limpar:
            clear()

        cli.linhas('Downloader for YouTube Videos')

        # ==================================================== #
        # - Mostra o(s) titulo(s) do link(s) que você passou - #
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
    4 - Ler arquivo com links
    5 - Trocar o link de download

    0 - Sair

    ''')
        opc = input_validation.inputValInt(' Opção: ')
            
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