from AudioPrograms.AudioTools import ecualizar
import os
import shutil


def wav_cutter(path):
    for sala in os.listdir(path):
        for song in os.listdir(path+'{}/'.format(sala)):
            with open(path+'{}/'.format(sala)+song, 'rb') as f:
                data = bytearray(f.read())

            os.remove(path+'{}/'.format(sala)+song)

            new = min(8000000, int.from_bytes(data[4:8], 'little'))
            data[4:8] = new.to_bytes(4, 'little')
            data[40:44] = (new-36).to_bytes(4, 'little')

            with open(path+'{}/'.format(sala)+song, 'wb') as f2:
                f2.write(data[:new+8])


def wav_editor(path, freq, n):
    salas = os.listdir(path)
    for sala in salas:
        if 'Freq' not in sala:
            x = sala+' - (Freq {},Filtrado {})'.format(freq, n)
            for song in os.listdir(path+'{}/'.format(sala)):
                path_eq = path+'{}/'.format(sala)+song
                new_file = ecualizar(path_eq, freq, n)

                destino = path+'{}/'.format(x)+song

                if not os.path.exists(path+'/{}'.format(x)):
                    os.makedirs(path+'{}'.format(x))

                with open(destino, 'wb') as f:
                    f.write(new_file)
        elif ' - (Freq {},Filtrado {})'.format(freq, n) not in sala:
            shutil.rmtree(path+'{}'.format(sala))
