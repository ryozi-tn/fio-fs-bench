'''
bench_fio.shで取ったfio.logの内容を雑に表にする

python3 parse-fio.py

| 00000000 |     1 | 231.0 MiB/s |  461 |  54.7 MiB/s |   109 |
| 00000000 |     4 | 768.0 MiB/s | 1536 |  94.7 MiB/s |   189 |
| 00000000 |     8 | 827.0 MiB/s | 1654 | 130.0 MiB/s |   260 |
| 00000000 |    16 | 828.0 MiB/s | 1656 | 170.0 MiB/s |   340 |
| 00001571 |     1 | 247.0 MiB/s |  493 |  53.0 MiB/s |   106 |
...

'''
import glob
import re

FIO_IOPS_PATTERN = re.compile(r'^  (read|write): IOPS=(\d+), BW=([\d\.]+)(\w+)/s')

def find_value(s):
    index = s.find("=")
    if index == -1:
        return s
    return s[index+1:]

def get_value(v,  *keys, default=''):
    for k in keys:
        if isinstance(v, dict) and k in v:
            v = v[k]
        else:
            return default
    return v

def deepupdate(d, n):
  for k, v in n.items():
    if isinstance(v, dict) and k in d:
      deepupdate(d[k], v)
    else:
      d[k] = v

data = {}

for file in glob.glob("./logs/**/fio.log", recursive=True):
    sp_file = file.split('/')
    uniq = sp_file[2]
    iodepth = find_value(sp_file[3])
    rw = find_value(sp_file[4])
    name = uniq[-8:]
    print(f"file={file}, iodepth={iodepth}")
    with open(file) as fp:
        for line in fp:
            m = FIO_IOPS_PATTERN.match(line)
            if m:
                deepupdate(data, {
                    name :{
                        iodepth: {
                            m[1]: {
                                "IOPS": float(m[2]),
                                "BW": float(m[3]),
                                "BW_Unit": m[4]
                            }
                        }
                    }
                })

for (name, v) in sorted(data.items(), key=lambda v: v[0]):
    for (iodepth, v) in sorted(v.items(), key=lambda v: int(v[0])):
        print(f'| {name:8s} | {iodepth:>5s} | { get_value(v, "read","BW", default=0):>5.1f} {get_value(v, "read","BW_Unit")}/s | { get_value(v, "read", "IOPS", default=0):>4.0f} | { get_value(v, "write","BW", default=0):>5.1f} {get_value(v, "write","BW_Unit")}/s |  { get_value(v, "write", "IOPS", default=0):>4.0f} |')