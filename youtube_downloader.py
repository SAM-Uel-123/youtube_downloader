#pylint: disable=missing-module-docstring
#pylint: disable=missing-class-docstring
#pylint: disable=missing-function-docstring
#pylint: disable=import-error

import csv
from os.path import isdir
from os import system
from pytube import YouTube, Playlist
from pytube.cli import on_progress
from pytube.helpers import safe_filename
from function_validation import InputValidation


class YouTubeDownloader:
    def __init__(self, link, directory):
        self.clear = lambda: system('clear')
        self.titulo= ''
        self.directory = directory
        self.link = link
        self.input_validation = InputValidation()
        if link:
            self.__atualizar_caches()


    def __atualizar_caches(self):
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


    def download(self, only_audio = 0):
        log= 0
        if type(self.link).__name__ == 'list' or Validation.val_link(self.link):
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


    def __video_download(self, link, directory= './'):
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


    def __audio_download(self, link, directory= './'):
        log= 0
        if InputValidation.val_link(link):
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


    def __playlist_download(self, link, directory= './', only_audio= 0 ):
        log= 0
        if Validation.val_link(link):
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


    def change_directory(self, limpar = 1):
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


    def change_link(self, limpar = 1, atualizar_caches= 0):
        while True:
            if limpar:
                self.clear()

            if self.link:
                print(f' O link atual é: {self.link}')

            tmp_link = input('Novo link: ')
            if tmp_link:
                if Validation.val_link(tmp_link):
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


    def read_file(self):
        while True:
            try:
                file_addres = input('Endereco do arquivo: ')
                if not file_addres:
                    confirmar = self.input_validation.input_string(\
                        'Deseja cancelar o link de download? [S/N]: ',
                        ['s', 'n'], 0)

                    if confirmar == 's':
                        break

                with open(file_addres, 'r', encoding='utf-8') as rarq:
                    rarq.close()

                linhas = []
                with open(file_addres, 'r', encoding='utf-8') as rarq:
                    if file_addres[file_addres.rfind('.'):] == 'csv':
                        arq_reader = csv.reader(rarq)

                    else:
                        arq_reader = rarq.readlines()

                    for linha in arq_reader:
                        if linha:
                            if Validation.val_link(linha):
                                if '\n' in linha:
                                    linha = linha.replace('\n', '')

                                linhas.append(linha)

                self.link = linhas

            except GeneratorExit as erro:
                print(f'Error: {erro}')
