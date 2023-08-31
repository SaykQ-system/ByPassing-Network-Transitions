import subprocess
import time
import os

def create_reverse_ssh_tunnel(local_host, local_port, remote_host, remote_port, ssh_host, ssh_port, ssh_username, ssh_password):
    while True:
        try:
            # Plink.exe komutunu oluşturma
            plink_command = [
                "plink.exe",
                "-ssh",
                f"{ssh_username}@{ssh_host}",
                "-P",
                str(ssh_port),
                "-pw",
                ssh_password,
                "-R",
                f"{remote_port}:{local_host}:{local_port}",
                "-N",  # Arka planda çalıştırma
            ]

            # Plink.exe komutunu başlatma
            process = subprocess.Popen(plink_command, stdin=subprocess.PIPE, cwd=os.getcwd())  # Çalışma dizinini güncelledik

            print(f"Bağlantı yönlendiriliyor: {remote_host}:{remote_port} -> {local_host}:{local_port}")

            # Plink.exe'nin "Return" tuşuna basmasını sağlama
            process.communicate(input=b"\n")

            # Oturum sürekli açık kalsın diye ana programı uyutuyoruz
            process.wait()

        except subprocess.CalledProcessError as e:
            print(f"Hata (Bağlantı koptu!):", e)

        # Oturum koparsa yeniden bağlanmak için 5 saniye bekleyelim
        time.sleep(5)

if __name__ == "__main__":
    # Yerel uygulamanın çalıştığı adres ve port
    local_host = "127.0.0.1"  # Yerel makine IP'si veya "localhost"
    local_port = 3389

    # Uzak sunucu ve port (yönlendirilecek hedef)
    remote_host = "127.0.0.1"
    remote_port = 3390  # Uzak sunucuda açılacak port

    # SSH sunucu bilgileri
    ssh_host = ""
    ssh_port = 22
    ssh_username = ""
    ssh_password = ""

    create_reverse_ssh_tunnel(local_host, local_port, remote_host, remote_port, ssh_host, ssh_port, ssh_username, ssh_password)