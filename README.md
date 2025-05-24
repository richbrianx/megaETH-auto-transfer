# megaETH-auto-transfer

Skrip ini digunakan untuk mentransfer token (seperti MegaETH, cUSD, tkETH, tkUSDC, tkWBTC) dari beberapa wallet ke wallet penerima yang ditentukan. Skrip ini menggunakan Web3.py untuk berinteraksi dengan blockchain MegaETH.

## Peringatan

**Skrip ini hanya untuk tujuan edukasi.** Harap jaga dengan baik **private key** Anda, dan gunakan skrip ini dengan bijak. Jangan pernah membagikan private key Anda kepada siapa pun atau menaruhnya di tempat yang tidak aman.

**DYOR (Do Your Own Research)** sebelum menggunakan skrip ini dalam situasi apapun yang melibatkan uang atau aset berharga. Keamanan dan risiko penggunaan berada sepenuhnya di tangan Anda.

## Prasyarat

- Python 3.x
- Web3.py

## Instalasi

1. Install dependensi yang diperlukan:

    ```
    pip install -r requirements.txt
    ```

2. Edit file `pk.txt` dengan private key Anda (jangan upload file ini ke GitHub atau tempat umum lainnya).

3. Jalankan skrip:

    ```
    python main.py
    ```

4. Masukkan alamat dompet penerima saat diminta.

## Catatan

- Jangan pernah meng-commit private key Anda ke repository ini atau tempat umum lainnya. Pastikan `pk.txt` Anda diabaikan oleh Git dengan menambahkannya ke `.gitignore`.
- Skrip ini dapat berinteraksi dengan token yang disebutkan di dalam kontrak (MegaETH, cUSD, tkETH, tkUSDC, tkWBTC). Pastikan Anda telah melakukan riset yang cukup mengenai token-token ini sebelum menggunakannya.

## Kontribusi

Jika Anda ingin berkontribusi pada skrip ini, pastikan Anda mengikuti pedoman pengembangan yang baik, dan ingat bahwa tujuan utama skrip ini adalah untuk edukasi.
