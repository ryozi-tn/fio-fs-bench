
書き出したファイルに対してfioでベンチマークを行う

### 前準備

fio, atopをインストール

```sh
# epel有効化
dnf install epel-release
# RHEL
dnf install fio atop
```

ファイルシステムの初期化

```sh
sudo umount /mnt
sudo mkfs -t ext4 /dev/md127 
```

/mntへマウント

```sh
sudo mount /dev/md127 /mnt
```

settings.shを修正

ベンチマーク用のダミーファイルを作る

```sh
sudo bash make-dummy-file.sh
```

filefrag等を使いベンチマークに使う対象ダミーファイルを選定

```sh
filefrag -v /mnt/dummy_file.00000000
filefrag -v /mnt/dummy_file.00001000
filefrag -v /mnt/dummy_file.00002000
filefrag -v /mnt/dummy_file.00003000
```

ダミーファイルに対してベンチマーク実行（断片化）

```sh
sudo bash bench_fio.sh /mnt/dummy_file.00003000
```

