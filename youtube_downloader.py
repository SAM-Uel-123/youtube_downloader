#pylint: disable=missing-module-docstring
#pylint: disable=import-error

import csv
from os.path import isdir
from os import system
from pytube import YouTube, Playlist
from pytube.cli import on_progress
from pytube.helpers import safe_filename
from function_validation import InputValidation


class YouTubeDownloader:
    """
    Classe: Essa classe trata de receber um endereço e baixar o arquivo.

    Ex.:
 > Obj = YouTubeDownloader(URL, Endereco_salvar_o_arquivo)
 > obj.download()

    e começa a baixar o video, passando somente como parametros, URL e endereço para
salvar os arquivos

    """
    def __init__(self, link : str, directory : str) -> int:
        self.clear = lambda: system('clear')
        self.titulo= ''
        self.directory = directory
        self.link = link
        self.input_validation = InputValidation()
        if link:
            self.__atualizar_caches()


    def __atualizar_caches(self) -> int:
        """
    Função: Ela é responsavel por tratar as informações do video/audio que você for
 baixar do youtube, ela que é responsavel por salvar os titulos por exemplo.

        """
        obj_youtube= None
        titulo= ''
        link = self.link
        if type( link ).__name__ == 'str':
            if 'playlist' in link:
                self.titulo= []
                obj_youtube = Playlist(link).videos
                for video in obj_youtube:
                    titulo= video.title
                    titulo = safe_filename(titulo)
                    self.titulo.append(titulo)

            else:
                obj_youtube = YouTube(link)
                titulo = obj_youtube.title
                titulo= safe_filename(titulo)

                self.titulo= titulo

        elif type( link ).__name__ == 'list':
            self.titulo = []
            for vid in link:
                obj_youtube = YouTube(vid)
                titulo = obj_youtube.title
                titulo = safe_filename(titulo)
                self.titulo.append(titulo)


    def download(self, only_audio : int = 0) -> int:
        """
    Função: Principal, essa função é responsavel por analizar o link passado por argumento
 e identificar o modo de baixa-lo, se é uma Playlist, se é 1 video, ou 1 audio.

        """
        log= 0
        if type(self.link).__name__ == 'list' or self.input_validation.val_link(self.link):
            print('==' * 30, flush= True)
            if 'playlist' in self.link:
                log= self.__playlist_download(self.link, self.directory, only_audio)

            elif type(self.link).__name__ == 'list':
                tmp_link= self.link
                for vid in tmp_link:
                    self.link = vid
                    log= self.download(only_audio)
                    if log:
                        break

            else:
                if only_audio:
                    log= self.__audio_download(self.link, self.directory)

                else:
                    log= self.__video_download(self.link, self.directory)

            print('==' * 30)

        else:
            print('link invalido.')
            log= 1

        return log


    def __video_download(self, link : str, directory : str = './') -> int:
        """
    Função: Responsavel por baixar somente videos, qualquer URL passada para ela, será
 tratada como se fosse um video.
        """
        log= 0
        erro = None
        if self.input_validation.val_link(link):
            try:
                obj_youtube = YouTube(link, on_progress_callback= on_progress)
                titulo= obj_youtube.title
                titulo = safe_filename(titulo)
                print('--' * 30)
                print(f'Baixando o video: {titulo}')
                youtube_streams = obj_youtube.streams.get_highest_resolution()
                youtube_streams.download(filename=titulo, output_path = directory, \
                    skip_existing = True)

                print()
                print('Download Comcluido com sucesso.')
                print('--' * 30)

            except GeneratorExit as erro:
                print(erro)


        else:
            print('ERROR, Link invalido.')
            log= 1

        return log


    def __audio_download(self, link : str, directory : str = './') -> int:
        """
    Função: Responsavel por baixar somente audios, qualquer URL passada para ela, será tratada
 como se fosse somente um audio.
        """
        log= 0
        if self.input_validation.val_link(link):
            try:
                obj_youtube = YouTube(link, on_progress_callback = on_progress)
                titulo = safe_filename(obj_youtube.title)
                titulo += '.mp3'
                print('--' * 30)
                print(f'Baixando o audio: {titulo}')
                youtube_streams = obj_youtube.streams.get_audio_only()
                youtube_streams.download(filename= titulo, output_path= directory, \
                    skip_existing= True)

                print()
                print('Download Concluido com sucesso.')
                print('--' * 30)

            except GeneratorExit() as erro:
                print(erro)
                log= 1

        else:
            print('ERROR, link invalido')
            log= 1

        return log


    def __playlist_download(self, link : str, directory : str = './', only_audio : int = 0 ) -> int:
        """
    Função: Responsavel por baixar somente Playlists, qualquer URL passada para ela será tratada
 como se fosse somente uma Playlist.
        """
        log= 0
        if self.input_validation.val_link(link):
            obj_playlist = Playlist( link )
            print(f'Baixando a playlist: {obj_playlist.title}')
            if only_audio == 0:
                for index, video in enumerate(obj_playlist.video_urls):
                    index += 1
                    print(f' {index if len(str(index)) > 1 else f"0{index}"} -> ', end='')
                    log= self.__video_download( link= video, directory= directory )
                    if log:
                        break

            else:
                for index, video in enumerate( obj_playlist.video_urls ):
                    index += 1
                    print(f' {index if len(str(index)) > 1 else f"0{index}"} -> ', end='')
                    log= self.__audio_download( link= video, directory= directory )
                    if log:
                        break


        else:
            print('ERROR, Link invalido.')
            log= 1

        return log


    def change_directory(self, tmp_directory : str = '', limpar : int = 1) -> None:
        """
    Função: Responsavel por definir o diretorio de saida, onde sua midia será baixada.
        """
        if tmp_directory:
            self.directory = tmp_directory
            return

        while True:
            if limpar:
                self.clear()

            if self.directory:
                print(f' O diretorio atual é: {self.directory}')

            tmp_directory = input('Novo diretorio: ')

            if tmp_directory:
                if isdir(tmp_directory):
                    confirmar = self.input_validation.input_string(\
                        'Deseja confirmar o novo diretorio? [S/N]',
                        ['s', 'n'],
                        1
                        )

                    if confirmar == 's':
                        self.directory = tmp_directory
                        break

                    if confirmar == 'n':
                        break

                    continue

                print('ERROR. Directory not exist.')

            else:
                confirmar = self.input_validation.input_string(\
                    'Deseja cancelar o diretorio? [S/N]: ',
                    ['s', 'n'],
                    0
                    )

                if confirmar == 's':
                    break


    def change_link(self, tmp_link: str = '', limpar : int = 1, atualizar_caches : int = 0) -> None:
        """
    Função: Responsavel por (re)definir o link que será usado para baixar sua midia.
        """
        if tmp_link:
            self.link = tmp_link
            return

        while True:
            if limpar:
                self.clear()

            if self.link:
                print(f' O link atual é: {self.link}')


            tmp_link = input('Novo link: ')

            if tmp_link:
                if self.input_validation.val_link(tmp_link):
                    confirmar = self.input_validation.input_string(\
                        'Deseja confirmar o novo link? [S/N]: ',
                        ['s', 'n'], 1)

                    if confirmar == 's':
                        self.link = tmp_link
                        if atualizar_caches:
                            self.__atualizar_caches()
                        break

                    if confirmar == 'n':
                        break


            else:
                confirmar = self.input_validation.input_string(\
                    'Deseja cancelar o link de download? [S/N]: ',
                    ['s', 'n'], 0)

                if confirmar == 's':
                    break


    def read_file(self, file_addres : str = '') -> list:
        """
    Função: Responsavel por ler um arquivo TXT ou CSV para coletar links de downloads do YouTube.
 retornando uma lista com os links.
        """
        while True:
            try:
                if not file_addres:
                    file_addres = input('Endereco do arquivo: ')

                    if not file_addres:
                        confirmar = self.input_validation.input_string(\
                            'Deseja cancelar o link de download? [S/N]: ',
                            ['s', 'n'], 0)

                        if confirmar == 's':
                            break

                        continue

                else:
                    try:
                        with open(file_addres, 'r', encoding='utf-8') as rarq:
                            rarq.close()

                    except FileNotFoundError as erro:
                        print(erro)
                        continue

                linhas = []
                with open(file_addres, 'r', encoding='utf-8') as rarq:
                    if file_addres[file_addres.rfind('.'):] == 'csv':
                        arq_reader = csv.reader(rarq)

                    else:
                        arq_reader = rarq.readlines()

                    for linha in arq_reader:
                        if linha:
                            if self.input_validation.val_link(linha):
                                linha = linha.replace('\n', '')

                                linhas.append(linha)

                self.link = linhas
                return True

            except GeneratorExit as erro:
                print(f'Error: {erro}')
                