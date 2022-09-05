from function_validation import *
from os.path import isdir

class YouTubeDownloader:
    import csv
    from pytube import YouTube, Playlist
    from pytube.cli import on_progress
    from pytube.helpers import safe_filename
    from os import system



    def __init__(self, link, directory):
        import csv
        from pytube import YouTube, Playlist
        
        from os import system
        self.clear = lambda: self.system('clear')
        self.titulo= ''
        self.directory = directory
        self.link = link
        if link:
            self.__atualizar_caches__()
          

    def safe_titulo(self, titulo):
        caracteres_invalidos= [':', ';', '.', '*', '/', '\\', '|']
        
        for caractere in caracteres_invalidos:
            if caractere in titulo:
                titulo = titulo.replace(caractere, '')

        return titulo


    def __atualizar_caches__(self):
        obj_YouTube= None
        titulo= ''
        link = self.link
        if type( link ).__name__ == 'str':
            if 'playlist' in link:
                self.titulo= []
                obj_YouTube = self.Playlist(link).videos
                for video in obj_YouTube:
                    titulo= video.title
                    titulo = self.safe_titulo(titulo)
                    self.titulo.append(titulo)
                    
            else:
                obj_YouTube = self.YouTube(link)
                titulo = obj_YouTube.title
                titulo= self.safe_titulo(titulo)

                self.titulo= titulo

        elif type( link ).__name__ == 'list':
            self.titulo = []
            for vid in link:
                obj_YouTube = self.YouTube(vid)
                titulo = obj_YouTube.title
                titulo = self.safe_titulo(titulo)
                self.titulo.append(titulo)  


    def download(self, only_audio = 0):
        log= 0
        if type(self.link).__name__ == 'list' or validation.valLink(self.link):
            print('==' * 30, flush= True)
            if 'playlist' in self.link:
                log= self.__playlist_download__(self.link, self.directory, only_audio)

            elif type(self.link).__name__ == 'list':
                tmp_link= self.link
                for vid in tmp_link:
                    self.link = vid
                    log= self.download(only_audio)
                    if log:
                        break

            else:
                if only_audio:
                    log= self.__audio_download__(self.link, self.directory)

                else:
                    log= self.__video_download__(self.link, self.directory)

            print('==' * 30)

        else:
            print('link invalido.')
            log= 1

        return log

    def __video_download__(self, link, directory= './'):
        log= 0
        if validation.valLink(link):
            try:
                from pytube.cli import on_progress
                obj_YouTube = self.YouTube(link, on_progress_callback= on_progress)
                titulo= obj_YouTube.title
                titulo = self.safe_titulo(titulo)
                print('--' * 30)
                print(f'Baixando o video: {titulo}')
                YouTube_streams = obj_YouTube.streams.get_highest_resolution()
                YouTube_streams.download(filename=titulo, output_path = directory, skip_existing = True)
                
                print()
                print('Download Comcluido com sucesso.')
                print('--' * 30)

            except Exception as erro:
                print(erro)
                log= 1

        else:
            print('ERROR, Link invalido.')    
            log= 1

        return log


    def __audio_download__(self, link, directory= './'):
        log= 0
        if validation.valLink(link):
            try:
                from pytube.cli import on_progress
                obj_YouTube = self.YouTube(link, on_progress_callback = on_progress)
                titulo = self.safe_titulo(obj_YouTube.title)
                titulo += '.mp3'
                print('--' * 30)
                print(f'Baixando o audio: {titulo}')
                YouTube_streams = obj_YouTube.streams.get_audio_only()
                YouTube_streams.download(filename= titulo, output_path= directory, skip_existing= True)
                print()
                print('Download Concluido com sucesso.')
                print('--' * 30)

            except Exception as erro:
                log= 1

        else:
            print('ERROR, link invalido')
            log= 1
        
        return log

    def __playlist_download__(self, link, directory= './', only_audio= 0 ):
        log= 0
        if validation.valLink(link):
            obj_Playlist = self.Playlist( link )
            print(f'Baixando a playlist: {obj_Playlist.title}')
            if only_audio == 0:
                for index, video in enumerate(obj_Playlist.video_urls):
                    index += 1
                    print(f' {index if len(str(index)) > 1 else f"0{index}"} -> ', end='')
                    log= self.__video_download__( link= video, directory= directory )
                    if log:
                        break
                    
            else:
                for index, video in enumerate( obj_Playlist.video_urls ):
                    index += 1
                    print(f' {index if len(str(index)) > 1 else f"0{index}"} -> ', end='')
                    log= self.__audio_download__( link= video, directory= directory )
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
                    confirmar = input_validation.inputValString('Deseja confirmar o novo diretorio? [S/N]', opcs=['s', 'n'], lower=1)
                    if confirmar == 's':
                        self.directory = tmp_directory
                        break
                    
                    elif confirmar == 'n':
                        break

                else:
                    print('ERROR. Directory not exist.')
            
            else:
                confirmar = input_validation.inputValString('Deseja cancelar o diretorio? [S/N]: ', opcs=['s', 'n'], lower=0)
                if confirmar == 's':
                    break



    def change_link(self, limpar = 1, atualizar_caches= 0):
        from os import system
        while True:
            if limpar:
                self.clear()

            if self.link:
                print(f' O link atual é: {self.link}')

            tmp_link = input('Novo link: ')
            if tmp_link:
                if validation.valLink(tmp_link):
                    confirmar = input_validation.inputValString(' Deseja confirmar o novo link? [S/N]: ', opcs=['s', 'n'], lower=1)
                    if confirmar == 's':
                        self.link = tmp_link
                        self.__atualizar_caches__(self.link)
                        break

                    elif confirmar == 'n':
                        break

            else:
                confirmar = input_validation.inputValString('Deseja cancelar o link de download? [S/N]: ', opcs=['s', 'n'], lower=0)
                if confirmar == 's':
                    break

    def read_file(self):
        while True:
            try:
                file_addres = input('Endereco do arquivo: ')
                if not file_addres:
                    confirmar = input_validation.inputValString('Deseja cancelar o link de download? [S/N]: ', opcs=['s', 'n'], lower=0)
                    if confirmar == 's':
                        break

                with open(file_addres, 'r') as rarq:
                    rarq.close()

                linhas = []
                with open(file_addres, 'r') as rarq:
                    if file_addres[file_addres.rfind('.'):] == 'csv':
                        arqReader = self.csv.reader(rarq)

                    else:
                        arqReader = rarq.readlines()

                    for linha in arqReader:
                        if linha:
                            if validation.valLink(linha):
                                if '\n' in linha:
                                    linha = linha.replace('\n', '')

                                linhas.append(linha)

                self.link = linhas

            except:
                print('Error.')



    